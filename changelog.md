# Change Log
## v2.1.0
- fixed rest Password error message
- fixed homescreen group bug
- added PyQt6 support
- added option to change username
- added privacy policy

## v2.0.0
- use email address and password to authenticate users
- minor UI changes
- minor performance improvements
- fixed some bugs

## v1.7.0
- added option to join multiple groups (__you have to rejoin the group you previously joined__)
- added option to report and suspend users
- added config shortcut
- added option to delete account and/or create a backup of the configurations before deleting the add-on (this option will be available in Anki >2.1.44)
- removed E-Mail from group request
- fixed review stats bug (rescheduled cards were counted as reviews)
- fixed days studied bug
- minimum study time for leagues is now 5 minutes
- adjusted dark mode colors
- UI changes
- various under the hood changes (add-on and server-side)

## v1.6.3.1
- streak hotfix
- increased window width

## v1.6.3
- fixed odd number bug on home screen leaderboard
- reduced home screen leaderboard server requests (improves performance)
- home screen leaderboard users are clickable (for more info about user)
- top three users of each league will get a medal that can be shown next to the username (optional) and will appear in the profile (starting from season 4)
- season results are being saved now for each user and appear in their profile (starting from season 4)
- "🥇", "🥈", "🥉" and "|" aren't allowed in usernames anymore
- minor UI changes
- improve the efficiency of statistical calculations (improves performance)
- added "days studied" (in the current season) to the league tab (a day counts when the user studied for at least 10 minutes)
- users with 0 XP will be relegated in addition to the last 20%
- notifications (server downtime, updates, etc.) will only be shown once
- new XP formula: `XP = days studied percentage x ((6 x time) + (2 x reviews x retention))` __starting from season 6__

## v1.6.2
- join group bug fix

## v1.6.1
- added # column to home screen leaderboard
- leagues also work on the home screen leaderboard now
- added option to focus on user on home screen leaderboard
- config UI changes
- added password-protected groups (Users that requested a new group in v1.6.0 are automatically admins. Groups can only be
	changed in v1.6.1 and future versions. Older versions won't be supported anymore)
- fixed various bugs

## v1.6.0
- added leagues
- added option to request groups from config
- added option to show the leaderboard on the home screen
- added auto-sync option after finishing reviews
- added option to set a status message
- added option to click on a user to add them as a friend/hide them, show status message & other info
- added some tooltips
- config UI changes
- fixed dark mode bug and adjusted colors
- better timeout error handling
- more info in about tab
- display HTML in notification properly

## v1.5.4
- store verification token in config.json
- fixed delete account bug
- added "sort by..." to config

## v1.5.3:
- fixed verification issue
- sync version number
- added ENEM/Vestibular to groups

## v1.5.2:
- stats bug fix
- sync token fix

## v1.5.1:
- store and sync SHA1 token to verify users
- added timeout for post/get requests + error message
- added UCFCOM and Concursos to groups

## v1.5:
- changed "N/A" to an empty string in retention stats
- fixed dark mode highlight bug
- adjustments for new API (older versions of this add-on won't be supported for much longer)
- added error messages when syncing fails
- threading timer stops when the leaderboard is closed
- added option to sync without opening the leaderboard (Shift+S)
- added MCAT to groups
- added option to choose default leaderboard

## v1.4.6:
- Added retention to stats
- Bug fixes

## v1.4.5:
- Fixed stats bug
- Added notification for maintenance, downtime, etc.
- Fixed typo

## v1.4.4.1:
- Patches for v.1.4.4
- Automatic refresh opt-in option (only for Anki 2.1.24)

## v1.4.4:
- When left open, the leaderboard automatically refreshes every two minutes (only for Anki 2.1.24+). Enable "Scroll to yourself" in the config and watch 
	yourself climb up the leaderboard in real-time while you do your reviews.
- Minor UI changes
- Friends can be exported to a text file
- Various bug fixes
- Added a few error messages
- Added change log to about tab

## v1.4.3:
- various hotfixes
- friends are now sorted alphabetically in the config and can be imported from a text file

## v1.4.2:
- new config UI
- leaderboard is now resizable
- leaderboard can be left open during reviews (I'm working on automatically refreshing the leaderboard every x minutes)
- added option to automatically scroll to username
- changed 'Reviews past 30 days' to 'Reviews past 31 days' and fixed a calculation bug
- username is now highlighted on all leaderboards
- friends are now highlighted on all leaderboards, but the friends' leaderboard
- first three places are now highlighted on all leaderboards
- max length for new usernames is now 15 characters
- added Medical School Anki as a group/subject
- config UI also opens when you go to Tools>Add-on>Config

## v1.4.1:
- small fixes for v.1.4
- added dropdown list for countries
- I can only officially support Anki 2.1.22, but it should also run on 2.1.23 and even 2.1.24 thanks to zjosua

## v1.4:
- UI changes
- added country leaderboard
- added subject leaderboard (you can choose between languages, medicine, and law for now. I can add more later)
- added reviews in the last 30 days to stats
- fixed some more stats issues
- reduced server requests
- other bug fixes

## v1.3.1 (hotfix):
- fixed calculation bug of stats between midnight and start of the new day

## v1.3:
- the beginning of the new day is now completely customizable (this affects how the streak is calculated and which users are shown on the leaderboard)
- friends are now blue on the global leaderboard
- added error message if you're not connected to the internet

## v1.2:
- fixed calculating the streak (new day starts now at 4:00 am)
- logging in, creating an account, and deleting an account is now more user friendly
- you can now add friends and compete with them in the "Friends" Tab
- leaderboard only shows people that synced the same day as you

## v1.1
- fixed calculating reviews and time bug
- username is limited to 10 characters for now
- fixed alignment issue
- added option to delete an account
