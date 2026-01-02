# UMAMUSUME AUTO TRAINER

<div align="center">
<img src="docs/agnesyap.gif" width="500" height="100" alt="Tachyon Dance">

[![Discord](https://img.shields.io/badge/Discord-join-green?logo=discord&logoColor=white)](https://discord.gg/8nwNZdxd72)
**Official Discord of this fork**


</div>

![UAT](docs/main.png)

---

## 📖 Introduction
**An automation tool for Uma Musume: Pretty Derby**

This tool allows for completely hands-off automation of Uma Musume, handling everything from training runs to recovering TP. It runs on mobile emulators (not the Steam release) allowing for background play.

## ✨ Features

- ✅ **Fully Automated**: Recovers TP, starts runs, finds guest cards, and handles training. You can AFK for days.
- ✅ **Resilient**: Handles disconnections, game crashes, and updates automatically.
- ✅ **Background Play**: Runs on Android emulators, leaving your PC free for other tasks.
- ✅ **Scenario Support**: Supports URA and Aoharu (Unity) scenarios.
- ✅ **Smart Decision Making**: Compares skill hints, plays the claw machine, manages energy efficiently, and more.
- ✅ **Customizable**: Supports every Uma and Deck type. Nearly every aspect of training is customizable via settings.

### Tutorial

[![Tutorial Video](https://img.youtube.com/vi/v1m9Plw7M3Y/0.jpg)](https://youtu.be/v1m9Plw7M3Y)
> *Note: Video may be outdated. Check the changelog for the latest features.*

---

## 🚨 Safety & Disclaimer

**Is this safe?**
Safer than the Steam release (since it uses ADB/Emulator), but **use at your own risk**.

- **Detection**: While I have humanized inputs, it is impossible to perfectly simulate a human. If the developers decide to investigate, they *can* find you. Hiding behind an emulator does not make you undetectable.
- **Recommendation**: Do not run this 24/7. It looks suspicious. Set a schedule in `main.py` (start/end times) to take breaks.
- **Responsibility**: I take no responsibility for bans. This is for educational purposes only. Do not misuse to violate TOS.

---

## 📦 Installation & Setup

### Prerequisites
- **Emulator**: MuMuPlayer (Recommended) or BlueStacks Pie64.
  - Resolution: **720 × 1280 (Portrait)**
  - DPI: **180**
  - Graphics: **Standard** (not Simple)
  - ADB: Must be enabled in emulator settings.
  - FPS: **Do NOT lower below 30!!!!!**
- **Python**: Version 3.10

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TomerGamerTV/UAT-Global-Server
   cd UAT-Global-Server
   ```

2. **Install Python 3.10** (if not already installed):
   ```bash
   winget install -e --id Python.Python.3.10
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Bot**:
   ```bash
   python main.py
   ```
   *Or simply run `start.bat`.*

### GPU Acceleration
For faster processing using an NVIDIA GPU, please refer to the **[GPU Setup Guide](docs/GPU_SETUP.md)**.

---

## ⚙️ Configuration & Tips

### Game Settings
1. **Graphics**: Must be set to `Standard`, not `Basic`.
2. **Training Setup**: Manually select Uma Musume, Legacy, and Support Cards in-game before starting the first run.
3. **Support Cards**: Avoid friend cards unless you have a specific strategy.

### Stat Caps
- **Normal Usage**: Set a large number for all caps so the bot always picks the best training option.
  ![Stat Caps](docs/statCaps.png)
- **Advanced Usage**: If you are maxing out a stat too early (e.g., 1200 Speed before Year 2 Summer), you can cap it to force the bot to train other stats.
  ![Cap Speed](docs/capSpeed.png)
  - **Soft Cap**: -10% to -30% score penalty as you approach the goal.
  - **Hard Cap**: 0 score if >95% of goal. *Warning: This forces suboptimal training. It is better to adjust your deck.*

---

## 🔧 Troubleshooting

For common issues, errors, and known bugs, please check the **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)**.

---

## 📝 Changelog

See **[CHANGELOG.md](CHANGELOG.md)** for the full history of updates.

---

## 🤝 Contributing
Anyone can contribute! Pull requests are welcome, though not guaranteed to be merged.

## 📜 Credits
- **Original Repository**: [UmamusumeAutoTrainer](https://github.com/shiokaze/UmamusumeAutoTrainer) by [Shiokaze](https://github.com/shiokaze)
- **Global Port**: [UmamusumeAutoTrainer-Global](https://github.com/BrayAlter/UAT-Global-Server) by [BrayAlter](https://github.com/BrayAlter)
- **Maintained up until 27/21/25 by [oofmytoes](https://www.youtube.com/watch?v=C-CG5w4YwOI)** (he decided to put [sloppy spyware](https://i.4cdn.org/vg/1766880133564919.png) in the program so no linking source)
- **TomerGamerTV**: Removing the spyware from his repo and creating this fork.

![uma](docs/goldship.jpeg)


