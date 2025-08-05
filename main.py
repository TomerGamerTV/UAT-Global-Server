import sys
import threading
import subprocess
import os
import yaml

from bot.base.manifest import register_app
from bot.engine.scheduler import scheduler
from module.umamusume.manifest import UmamusumeManifest
from uvicorn import run


def get_adb_devices():
    """Get list of connected ADB devices"""
    try:
        # Use the adb from deps directory
        adb_path = os.path.join("deps", "adb", "adb.exe")
        
        if not os.path.exists(adb_path):
            print("❌ ADB not found in deps/adb/ directory")
            return []
        
        # First try to get devices
        result = subprocess.run([adb_path, "devices"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print(f"❌ ADB error: {result.stderr}")
            return []
        
        devices = []
        lines = result.stdout.strip().split('\n')[1:]  # Skip header line
        
        for line in lines:
            if line.strip() and '\t' in line:
                device_id, status = line.split('\t')
                if status == 'device':
                    devices.append(device_id)
        
        # If no devices found, try restarting ADB server
        if not devices:
            print("🔄 No devices found, restarting ADB server...")
            subprocess.run([adb_path, "kill-server"], capture_output=True, timeout=5)
            subprocess.run([adb_path, "start-server"], capture_output=True, timeout=10)
            
            # Try again after restart
            result = subprocess.run([adb_path, "devices"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]
                for line in lines:
                    if line.strip() and '\t' in line:
                        device_id, status = line.split('\t')
                        if status == 'device':
                            devices.append(device_id)
        
        return devices
    except Exception as e:
        print(f"❌ Error getting ADB devices: {e}")
        return []


def check_umamusume_running(device_id):
    """Check if Umamusume is running on the device"""
    try:
        adb_path = os.path.join("deps", "adb", "adb.exe")
        cmd = [adb_path, "-s", device_id, "shell", "dumpsys", "activity", "activities"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            # Look for Umamusume package in running activities
            output = result.stdout.lower()
            umamusume_packages = [
                "com.cygames.umamusume",
                "jp.co.cygames.umamusume",
                "umamusume"
            ]
            return any(pkg in output for pkg in umamusume_packages)
    except:
        pass
    return False


def select_device():
    """Let user select an ADB device"""
    print("🔍 Scanning for ADB devices...")
    devices = get_adb_devices()
    
    if not devices:
        print("❌ No ADB devices found!")
        print("Please ensure:")
        print("1. Your emulator is running")
        print("2. ADB is enabled in emulator settings")
        print("3. USB debugging is enabled")
        return None
    
    print(f"\n📱 Found {len(devices)} device(s):")
    
    # Check which devices have Umamusume running
    device_info = []
    for i, device_id in enumerate(devices, 1):
        has_umamusume = check_umamusume_running(device_id)
        status = "🎮 Umamusume Running" if has_umamusume else "📱 Device Connected"
        device_info.append((device_id, has_umamusume))
        print(f"{i}. {device_id} - {status}")
    
    # Prioritize devices with Umamusume running
    umamusume_devices = [d for d, has_uma in device_info if has_uma]
    other_devices = [d for d, has_uma in device_info if not has_uma]
    
    if umamusume_devices:
        print(f"\n🎯 Recommended devices (Umamusume detected):")
        for i, device_id in enumerate(umamusume_devices, 1):
            print(f"  {i}. {device_id}")
    
    while True:
        try:
            choice = input(f"\nSelect device (1-{len(devices)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(devices):
                selected_device = devices[choice_num - 1]
                print(f"✅ Selected device: {selected_device}")
                return selected_device
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None


def update_config(device_name):
    """Update config.yaml with selected device"""
    try:
        with open("config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['bot']['auto']['adb']['device_name'] = device_name
        
        with open("config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"✅ Updated config.yaml with device: {device_name}")
        return True
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False


if __name__ == '__main__':
    if sys.version_info.minor != 10 or sys.version_info.micro != 9:
        print("\033[33m{}\033[0m".format("注意：python 版本号不正确，可能无法正常运行"))
        print("建议python版本：3.10.9 当前：" + sys.version)
    
    # Device selection
    selected_device = select_device()
    if selected_device is None:
        print("❌ No device selected. Exiting.")
        sys.exit(1)
    
    # Update config with selected device
    if not update_config(selected_device):
        print("❌ Failed to update config. Exiting.")
        sys.exit(1)
    
    # Start the bot
    register_app(UmamusumeManifest)
    scheduler_thread = threading.Thread(target=scheduler.init, args=())
    scheduler_thread.start()
    print("🚀 UAT running on http://127.0.0.1:8071")
    run("bot.server.handler:server", host="127.0.0.1", port=8071, log_level="error")

