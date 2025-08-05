# 🏇 Umamusume Auto Trainer (Global Server Edition)

**Uma Musume Pretty Derby Global Server Automatic Training Tool**

> **From China Server automation to Global Server excellence** - A complete transformation with enhanced features, improved UI, and robust automation capabilities.

## 🌟 **What's New in Global Server Edition**

### 🎯 **Major Improvements**
- **🌍 Global Server Migration**: 70% translation and asset updates for Global Server compatibility
- **🎨 Enhanced Web Interface**: Advanced race filtering, skill choice system, and improved user experience
- **🤖 Robust Bot System**: Dual detection (image + OCR) for reliable race fail handling
- **⚡ Performance Optimization**: JSON-based data loading for faster operation
- **🔧 Technical Upgrades**: Modern build system with automated releases

### 🆕 **New Features**
- **Advanced Race Filtering**: Filter by race type, distance, terrain, and event character
- **Skill Choice System**: Intelligent skill selection interface in web application
- **Event Choice Picker**: Smart event selection for optimal training
- **70% English Translation**: Major UI and system text translated to English
- **Automated Releases**: GitHub Actions for seamless executable distribution

### 🔄 **Current Limitations**
- **Uma Musume Selection**: Must be done manually in-game (not yet automated)
- **Support Card Selection**: Manual selection in-game required
- **Character Filter**: Race character filtering is implemented, but card name translation needed for full functionality

## 🚀 **Features**

### **Core Automation**
- ✅ **Automatic Training**: Complete training scenarios for all Uma Musume
- ✅ **Customizable Targets**: Training attributes, racing tactics, additional races
- ✅ **Skill Learning**: Optimized skill acquisition for 3-star factor farming
- ✅ **Inheritance Compatibility**: Improved breeding strategy support

### **Advanced Web Interface**
- 🎛️ **Race Management**: Advanced filtering and selection tools
- 📊 **Real-time Monitoring**: Live task status and progress tracking
- ⚙️ **Easy Configuration**: Intuitive settings and preset management
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎯 **Character Filter**: Filter races based on selected character (manual select on UAT web)

## 📦 **Installation & Setup**

### **Option 1: Download Release (Recommended)**
1. Go to [Releases](https://github.com/BrayAlter/UAT-Global-Server/releases)
2. Download the latest release zip file
3. Extract and run `UmamusumeAutoTrainer.exe`

### **Option 2: Build from Source**

#### **Clone Repository**
```bash
git clone https://github.com/BrayAlter/UAT-Global-Server.git
cd UAT-Global-Server
```

#### **Install Dependencies**
1. Install Python 3.10.9: [Download Link](https://www.python.org/downloads/release/python-3109/)
2. Run `install.ps1` (Right-click → "Run with PowerShell")
3. Ensure no `venv` folder exists in current directory

### **Configuration**

Edit `config.yaml`:

```yaml
bot:
  auto:
    adb:
      device_name: "127.0.0.1:16384"  # Your emulator's ADB port
      delay: 0
    cpu_alloc: 4  # Number of allocated CPUs
```

**Common Emulator Ports:**
- **MuMu12** (Recommended): `127.0.0.1:16384`
- **LDPlayer/BlueStacks**: `emulator-5554`

### **Emulator Setup**
- **Resolution**: 720 × 1280 (Portrait mode)
- **DPI**: 180
- **Graphics**: Standard (not Simple)

### **Launch**
```bash
# Run the application
./run.ps1
```

**Success indicator:**
```
UAT running on http://127.0.0.1:8071
```

Access the web interface at `http://127.0.0.1:8071` to configure and start tasks.

![Main Web Interface](docs/1.png)

### **Race Selection Interface**
![Race Selection](docs/2.png)

### **Skill Selection Interface**
![Skill Selection](docs/3.png)

## ⚠️ **Important Notes**

### **Game Settings**
1. **Graphics**: Must be set to "Standard", not "Basic"
2. **Training Setup**: **Manually select** Uma Musume, stallion, and support cards in-game before starting
3. **Support Cards**: Avoid friend cards (no specific outing strategy)
4. **Starting Position**: Be at main menu or training interface

### **Training Strategy**
- **Attribute Balance**: Match support card types to target attributes
- **Race Selection**: Configure custom race schedules for specific requirements
- **Skill Optimization**: Use presets for optimal skill learning

## 🔧 **Troubleshooting**

### **Common Issues**

#### **PowerShell Script Issues**
- **Script crashes**: Open console first to see error messages
- **Execution policy**: Reference: [PowerShell Execution Policy](https://www.jianshu.com/p/4eaad2163567)

#### **Connection Problems**
- **ADB connection fails**: Close accelerators, kill adb.exe, restart emulator
- **Recognition errors**: Manual operation to next turn, reset task in WebUI

#### **Web Interface Issues**
- **MIME type errors**: Check for Chinese characters in user folder path
- **Module loading fails**: Ensure proper file permissions and paths

### **Error Recovery**
1. **Stuck interfaces**: Take screenshot, attach error logs
2. **Recognition failures**: Manual intervention, then restart
3. **Connection resets**: Restart both emulator and script

## 🛠️ **Technical Details**

### **System Requirements**
- **OS**: Windows 10/11
- **Python**: 3.10.9 (for source builds)
- **Emulator**: Android emulator with ADB support
- **Memory**: 4GB+ RAM recommended

### **Dependencies**
- **Computer Vision**: OpenCV for image recognition
- **Machine Learning**: PaddleOCR for text detection
- **Web Framework**: FastAPI + Vue.js
- **Automation**: UIAutomator2 for Android control

## 🎯 **Roadmap**

### **Planned Features**
- [ ] **Scheduled Tasks**: Automated execution at specific times
- [ ] **AI Training Logic**: Enhanced decision-making algorithms
- [ ] **Event Configuration**: Advanced event choice options
- [ ] **Daily Automation**: Auto-complete daily tasks (coins, support points, JJC)
- [ ] **Uma Musume Auto-Selection**: Automated character and support card selection
- [ ] **Card Name Translation**: Complete English translation for support card names

### **Recent Updates**
- ✅ **Global Server Migration**: Complete compatibility update
- ✅ **Web Interface Enhancement**: Advanced filtering and controls
- ✅ **Performance Optimization**: JSON-based data loading
- ✅ **Error Handling**: Robust fail-safe mechanisms

## 🤝 **Contributing**

We welcome contributions! If you find issues or have improvements:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Submit a pull request**

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

## 📄 **License & Credits**

This project is a **Global Server adaptation** of the original China Server version by [@shiokaze](https://github.com/shiokaze/UmamusumeAutoTrainer).

### **Original Project**
- **Original Author**: [@shiokaze](https://github.com/shiokaze/UmamusumeAutoTrainer)
- **Original Repository**: [UmamusumeAutoTrainer](https://github.com/shiokaze/UmamusumeAutoTrainer) (China Server)

### **This Project**
- **Global Server Adaptation**: [UAT-Global-Server](https://github.com/BrayAlter/UAT-Global-Server)
- **Based on**: Original China Server version
- **Enhancements**: 70% translation, improved UI, Global Server compatibility

**Please respect the original author's work while contributing improvements.**

---
