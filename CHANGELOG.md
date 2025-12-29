# Changelog

## 29/12/2025
- Changed image in the panel.
- Renamed 2 support cards from chinese to english.
- Fixed website being blank.
- Fixed merge issues.
- Rewrote the whole readme, split some stuff into different files.
- Better update checking. 

## 28/12/2025
- Removed spyware that existed the original repo.
- Disconnected this fork from the original repo.
- Fixed a skill name.

## 27/12/2025
- Fixed VRAM issue.
- Event list updated.
- Added cache to improve speed.
- Added `twinturbo.png`.

## 25/12/2025
- **Showtime mode**: Fixed UI stuck issue.
- **Navigation**: Always find and click `next.png` as a last resort.
- **GPU**: Made GPU support public (due to speed issues causing stuck states).
- **Logic**: Decision-making now restarts if OCR/template match isn't used for 10 seconds.

## 23/12/2025
- Fixed date phrasing failure causing a loop.
- **Update Required**: Please update `requirements.txt`.

## 21/12/2025
- Logging in from another device now causes the current task to pause.
- Forced brightness check every time the infirmary is pressed.

## 19/12/2025
- Exposed event weight to WebUI for user configuration.

## 16/12/2025
- Event list updated.

## 14/12/2025
- **Training**: Having 2+ rainbow trainings now applies a 7.5% multiplier for every additional rainbow above 1.
- Fixed spirit explosions and special training not respecting user inputs.

## 13/12/2025
- Minimum score before conserving energy (Summer) and minimum score before forcing Wit training are now customizable.

## 12/12/2025
- Fixed recreation breaking training (forcing Wit) when Pal outing is configured with no Pal notification.

## 11/12/2025
- Miscellaneous bug fixes.

## 9/12/2025
- **Outings**: Fixed outing not having priority over rest.
- **Pal Cards**: Pal Cards are fully supported.
- Fixed infinite loop issue from previous day.
- Custom scoring for Finale dates.
- Pal outing overrides rest if conditions met and max energy threshold < 90.
- Added option to override "insufficient fans" forced races.
- Blacklisted event name `''` to prevent misclicks.

## 8/12/2025
- Updated event list.
- Added custom card names.
- Added custom thresholds for Pal event chains.

## 5/12/2025
- Added override for event "Training" to click the 5th choice if 5 choices are detected.
- **Training**: Tweaks to energy management efficiency.

## 30/11/2025
- Added -10% score penalty to the highest stat in senior year to balance stats (Experimental).

## 29/11/2025
- Fixed getting stuck at Aoharu tutorial event.
- Updated event list.
- Added Select/Deselect all skills blacklist/priority.
- Dropped repetitive clicks recovery reset threshold from 5 to 2.

## 28/11/2025
- Fixed bot potentially getting stuck after ending a career.
- Fixed bot restarting unnecessary when detecting an event.
- **Skills**: Will now purchase the highest skill hint level of each priority before moving to next priority.

## 22/11/2025
- Added drag and drop for skills between priorities and blacklist.

## 16/11/2025
- Crash fixes.
- Patched up Team Trials execution mode.

## 15/11/2025
- Updated support card names.
- Aoharu (Unity Cup) team name selection fixed.

## 14/11/2025
- Updated skill list.
- Fixed getting stuck in support card selection.
- Stat cap score calc hard cap implemented.
- Default target attributes changed.

## 12/11/2025
- "Use last selected parents" option added in WebUI.
- Support for Team Trials quick mode.

## 10/11/2025 (Game Updated)
- Fixed bot breaking due to game update.
- Enemy team selection for races 1-4 (Aoharu).
- Fixed "Auto select team" taking too long.

## 10/10/2025
- **Aoharu Implementation (Beta)**:
  - Able to reach the end (assuming Team Zenith is beaten).
  - Customizable special training parameters.
  - Customizable spirit explosion parameters.
  - Logic to ignore Wit spirit explosions when energy is high.
- Customizable "Stuck" handling.

## 26/10/2025
- Easier event choice customization.

## 25/10/2025
- Fixes for buying skills.
- Prep for Aoharu Hai.

## 20/10/2025
- "Stuck clicking something" failsafe part 2.

## 19/10/2025
- UI changes.
- Fuzzy matching for buying skills.

## 18/10/2025
- Customizable energy limit.
- Option to adjust score based on training failure rate.

## 29/9/2025
- Soft reset after every task to help with memory issues.

## 28/9/2025
- **Team Trials**: Execution mode added (Experimental).
- Fix for card selection breaking.