# Troubleshooting & Known Issues

## Common Issues

### Fan Goals Fail
- **Issue**: Failed to reach the next goal races because of a lack of Fans.
- **Solution**: Configure the race selection first in the UAT website to ensure you meet fan requirements.

### ADB Device Detection
- **No devices found**: Ensure the emulator is running, ADB is enabled, and the Umamusume app is open.
- **ADB server issues**: The app automatically restarts the ADB server if needed.
- **Device not detected**: Check your emulator's ADB settings.

### PowerShell Script Issues
- **Script crashes**: Open the console first to see error messages.
- **Execution policy**: You may need to change your execution policy. Reference: [PowerShell Execution Policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)

### Connection Problems
- **ADB connection fails**: Close any game accelerators/VPNs if they interfere with local connections, kill `adb.exe` in Task Manager, and restart the emulator.

---

## Known Issues / Won’t Fix

> **Note**: 100% of testing is currently done on **MuMuPlayer**, using **Loop until canceled** mode with **auto recover TP** enabled. Issues outside this configuration are lower priority.

- **Bot gets stuck**: 
  - There are failsafes in place. It should break out of the loop within 5 minutes.
  
- **Support Card Detection Fails**:
  - **Symptom**: It keeps clicking Wit training or a bad training, and logs show scores are stuck or only detecting unknown cards.
  - **Solution**: Restart both the emulator and the bot. If it works from the start, it usually won't break halfway.

- **Hint (!) Detection Fails**:
  - Sometimes it fails to detect the hint icon because it is animated. We accept this ~5% failure rate to save performance (avoiding template matching 20 screenshots).

- **Outdated Data**:
  - See [Issue #63](https://github.com/BrayAlter/UAT-Global-Server/issues/63#issuecomment-3296260518) for updates.