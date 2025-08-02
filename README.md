# UmamusumeAutoTrainer (Global Server Edition)

Uma Musume Pretty Derby Global Server Automatic Training Tool

## Features

1. Supports automatic completion of training scenarios for all Uma Musume
2. Customizable training target attributes, racing tactics, additional races, skill learning for easier 3-star factor farming and improved inheritance compatibility

## Usage Instructions

### Download

##### Clone Repository

```commandline
git clone https://github.com/shiokaze/UmamusumeAutoTrainer
```
##### Install Dependencies

1. Install Python 3.10.9, [Download Link](https://www.python.org/downloads/release/python-3109/)
2. Double-click to run install.ps1. If it opens in notepad, right-click the file and select "Open with PowerShell". Ensure there's no venv folder in the current directory when starting (If you're not in mainland China or don't need to use domestic mirrors, you can modify line 32 to `pip install --upgrade -r requirements.txt`)

### 2. Configuration

Modify the config.yaml file content

```
bot:
  auto:
    adb:
      device_name: "127.0.0.1:16384" # Change to your emulator's ADB port
      delay: 0
    cpu_alloc: 4 # Number of allocated CPUs
```
Common emulator ports:\
(Recommended) MuMu12: 127.0.0.1:16384 \
LDPlayer/BlueStacks: emulator-5554

#### BlueStacks Emulator Port Changes Every Startup (Hyper-V)
Find the bluestacks.conf file in BlueStacks emulator's data directory
- International version default path: C:\ProgramData\BlueStacks_nxt\bluestacks.conf
- China version default path: C:\ProgramData\BlueStacks_nxt_cn\bluestacks.conf

```
bot:
  auto:
    adb:
      device_name: "127.0.0.1:16384" # Change to your emulator's ADB port
      delay: 0
      bluestacks_config_path: "C:\\ProgramData\\BlueStacks_nxt\\bluestacks.conf" # Path to bluestacks.conf file
      bluestacks_config_keyword: "bst.instance.Rvc64.status.adb_port" # Port key value for corresponding emulator, Rvc64 is the emulator name, may vary (like Rvc64_1, Pie64), search for adb_port in bluestacks.conf file
    cpu_alloc: 4 # Number of allocated CPUs
```

### 3. Emulator Settings

Set emulator resolution to 720 * 1280, DPI 180 (Portrait mode)
MuMu emulator cannot enable background keep-alive function

### 4. Launch

Double-click to run run.ps1

Console displays the following content indicates successful startup
```commandline
UAT running on http://127.0.0.1:8071
```

Copy to browser to access and configure tasks through WebUI and start the script

<img alt="LOGO" src="docs/1.png" width="680" height="565" />

## Important Notes

1. In-game graphics option must be set to Standard, not Simple
2. If Uma Musume training phase includes optional races or races with xxx fan count requirements (like Oguri Cap's 2 G1 races in year 3 and Urara's fan count targets), you need to use the corresponding Uma Musume preset or configure which races to participate in custom race schedule
3. Target attributes should match the proportion of support card types carried. Don't carry 3 Intelligence + 3 Speed cards while setting high Stamina and Power targets
4. Currently doesn't support selecting training Uma Musume and breeding stallion. At startup, it will use the last trained Uma Musume and stallion saved in the game. If there's no saved record, manually select first before starting
5. Friend cards are not recommended because there's no specific strategy for friend card outings, so the effect is not as good as carrying other types of support cards
6. When starting the script, you should be at the main menu or any training interface

### If Exceptions Occur

1. If emulator connection failure or connection reset errors occur, close running accelerators (like UU Accelerator) and use Task Manager to close adb.exe, then restart both the emulator and script program
2. If recognition errors cause program crashes, enter unexpected interfaces, or get stuck on certain interfaces, manually operate to the next turn and reset the task in WebUI before restarting. You can save screenshots of stuck interfaces and attach error logs to submit issues.

## Common Issues

#### 1. install.ps1 or run.ps1 crashes when running
You can open the console first and then run the PowerShell script, so you can see the error reason when it occurs.
#### 2. System prohibits running PowerShell scripts
Reference: https://www.jianshu.com/p/4eaad2163567
#### 3. Script startup error
Check if the user folder name contains Chinese characters\
Reference: https://github.com/shiokaze/UmamusumeAutoTrainer/issues/18 \
https://github.com/shiokaze/UmamusumeAutoTrainer/issues/24
#### 4. Startup successful, but WebUI won't open and browser console shows errors
If the error message is: Failed to load module script: Expected a JavaScript module script but the server responded with a MIME type of "text/plain". Strict MIME type checking is enforced for module scripts per HTML spec. \
Reference: https://github.com/shiokaze/UmamusumeAutoTrainer/issues/9
https://github.com/shiokaze/UmamusumeAutoTrainer/issues/25

### TODO

- [ ] Scheduled task execution
- [ ] Training AI logic optimization
- [ ] Event configuration options support
- [ ] Automatic completion of daily coins/support points/JJC

### Contributing

If you feel the current code has shortcomings, pull requests are welcome

