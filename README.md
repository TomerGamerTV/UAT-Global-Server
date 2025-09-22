I push everytime i make ANY changes so I would suggest not pulling unless the repo hasn't been updated in 6+ hours. Its very unstable when im working on it

Hello bray I'll be detaching this fork for now since im 99% sure ur not coming back

# ⚠️🚨 !!ATTENTION!! 🚨⚠️  
### THE [ORIGINAL CREATOR](https://github.com/BrayAlter/UAT-Global-Server) IS MISSING IN ACTION 

unfortunately I too will no longer have time to work on this so hopefully he returns soon

⏰ On **September 30th 2025 onwards** I will no longer have time to work on this.  
I will do what I can to iron out everything before then.  
But when a new scenario shows up (Make a new track, grand live ect ect), I need **YOUR** help to make a **fork** to deal with that.  

I will be relying on you guys to automate the future senarios. 🙏

If not I guess ill be stuck playing URA lmao

(When i'm gone yall can run scrape.py and move the updated file to UAT-Global-Server\resource\umamusume\data to get updates for new cards/characters)

## 📄 **License & Credits**

This project is a **Global Server adaptation** of the original China Server version by [@shiokaze](https://github.com/shiokaze/UmamusumeAutoTrainer).

### **Original Project**
- **Original Author**: [@shiokaze](https://github.com/shiokaze/UmamusumeAutoTrainer)
- **Original Repository**: [UmamusumeAutoTrainer](https://github.com/shiokaze/UmamusumeAutoTrainer) (China Server)

-This is now a detached fork of [UmamusumeAutoTrainer](https://github.com/BrayAlter/UAT-Global-Server)


---
## 🚀 **Features**

### **Core Automation**
- ✅ **Automatic Training**: Complete training scenarios for ALL Uma Musume  
  - This includes the handling of:  
    - **Custom races** 
    - **Skill acquisition**
    - **Claw machine**
    - **Running styles** 
    - **Alarm clock usage** 
    - **Building fiendship early, focus on rainbows later** 
    - **Optimal event choices (Knows when to build friendship/recover energy and mood)**
      - If you want a specify a event choice instead of having the bot pick what it thinks is the best option; open up "UAT-Global-Server\resource\umamusume\data\event_data.json" and change the desired event stat gains to a very big number so it wins everytime
      - Sometimes it fails to detect the event even with fuzzy search and defaults to the first choice. When that happens you will have to rename the event to match whats being detected 
    - **Skipping bad turns with wit training**


- ✅ **Completely hands off**: Recover tp, Starting runs, finding the right guest card
  - Everything is 100% automated you can just afk for **DAYS** until legacy umas are full
  - Handles everything from disconnections to the game crashing. The show will go on as long as there isn't a new update. (it handles that too now lol)
  - Supports background play via emulators.
  - If Auto tp recovery is set to false it will wait until you have enough tp to start the career run


- ✅ **Saving of presets**: Save training parameters for easy access in future runs 

### 🎥 **Demo Run**
- I'd say its about 80% as competent as a actual player. This makes the bot not just a fan/parent farmer but it's more than capable of producing ACES
[Demo run with a f2p deck](https://youtu.be/J07n4wvLSCw)

## 🚨 **Safety**
- Question: Is this safe?
- Answer: Safer than the steam release (All of your processes are transparent lmao), I have done what I can to humanize the inputs. **BUT** if they decide to put in the effort they **WILL** find you. It is near impossible to simulate perfect human behavior with code so use at your own risk. I take no responsibility.  **HIDING BEHIND A EMULATOR DOES NOT MAKE YOU UNDETECTABLE**

- Answer 2: As long as there are people cheating on the steam release we are chilling (if ykyk)
  - https://en.wikipedia.org/wiki/Sentinel_species
  
running this 24/7 looks sus as hell so I would suggest turning it off for a few hours every day. 
(im just gonna risk it and run it 24/7 ill let you guys know if i get banned)

## 📦 **Installation & Setup**

#### **Clone Repository**
```bash
git clone https://github.com/oofmatoes/UAT-Global-Server
cd UAT-Global-Server
```

### **Emulator Setup**
- **Only tested on bluestacks pie64**
- **Resolution**: 720 × 1280 (Portrait mode)
- **DPI**: 180
- **Graphics**: Standard (not Simple)
- **ADB**: Must be enabled in emulator settings

### **Launch**
Ensure python 3.10 is installed

Recommended Python version: 3.10.9 
```bash
pip install -r requirements.txt

python main.py
```

---


**Success indicator:**
```
🚀 UAT running on http://127.0.0.1:8071
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
2. **Training Setup**: **Manually select** Uma Musume, Legacy, and Support Cards in-game before starting
3. **Support Cards**: Avoid friend cards (no specific outing strategy)

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Fan Goals Fail**
- **Failed to the next goal races because lack of Fans**: Configure the race selection first in the UAT website to avoid lack of Fans

#### **ADB Device Detection**
- **No devices found**: Ensure emulator is running and ADB is enabled and open the umamusume app
- **ADB server issues**: The app automatically restarts ADB server if needed
- **Device not detected**: Check emulator's ADB settings

#### **PowerShell Script Issues**
- **Script crashes**: Open console first to see error messages
- **Execution policy**: Reference: [PowerShell Execution Policy](https://www.jianshu.com/p/4eaad2163567)

#### **Connection Problems**
- **ADB connection fails**: Close accelerators, kill adb.exe, restart emulator
- **Recognition errors**: Manual operation to next turn, reset task in WebUI

#### **Web Interface Issues**
- **Module loading fails**: Ensure proper file permissions and paths

## ⚠️ **Known issues/Wont fix**
- I have made the bot quite slow to improve reliability
  - The focus of this bot is to be ran unsupervised for long periods of time (days/weeks) hence speed is not my concern reliability is.
  - All of my testing is done on "Loop until canceled" and "Auto recover tp" There might be bugs in single run mode
- Bot seems to get stuck sometimes
  - There are failsafes in place. It should break out of it within 5 mintues. if not then yeah I'll fix it.
- The event detection reads the text wrong sometimes
  - Go fund paddleocr
- Detection of supports sometimes fails
  - Just restart both bluestacks and the bot. If it works from the start then it should not break halfway (it either breaks 100% of the time since launch or its fine and will never break) so its not really a issue. I also have no idea whats causing this.
- Sometimes it fails to detect the hint (!)
  - Its animated, so either I kill performance and template match like 20 screenshots or we just take the L when it fails the detect like 5% of the time
  - Could also check the general area for red pixels but it led to a bunch of false positives from my testing

## 🤝 **Contributing**

wait for bray to come back and contribute to the orginal. Or make your own detached fork. I wont be here anymore in 2 weeks.

DO NOT FORK THIS AND MAKE A PULL REQUEST I WONT BE HERE TO MERGE IT

If you ask and pinky promise you won't just nuke everything I can just give you collaborator permissions.