version = "v1.6.3.1"

about_text = f"""
<h2>Anki Leaderboard {version}</h2>
This add-on ranks all of its users by the number of cards reviewed today, time spend studying today, 
current streak, reviews in the past 31 days, and retention. You can also compete against friends, join a group, 
and join a country leaderboard. You'll only see users, that synced on the same day as you.<br><br>
In the league tab, you see everyone that synced at least once during the current season. There are four leagues
(Alpha, Beta, Gamma, and Delta). A season lasts two weeks. You don't have to sync every day.
<b>Starting from season 6,</b> the XP formula is:<br><code>XP = days studied percentage x ((6 x time) + (2 x reviews x retention))</code>
<i><a href="https://github.com/ThoreBor/Anki_Leaderboard/issues/122">See this issue for more info<a/></i><br>
At the end of each season, the top 20% will be promoted, and the last 20% will be relegated.<br><br>
The code for the add-on is available on <a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub.</a> 
It is licensed under the <a href="https://github.com/ThoreBor/Anki_Leaderboard/blob/master/LICENSE">MIT License.</a> 
If you like this add-on, rate and review it on <a href="https://ankiweb.net/shared/info/41708974">Anki Web.</a><br><br>
You can also check the leaderboard (past 24 hours) on this <a href="https://ankileaderboard.pythonanywhere.com/">website</a>.<br>
<div>Crown icon made by <a href="https://www.flaticon.com/de/autoren/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Person icon made by <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Confetti gif from <a href="https://giphy.com/stickers/giphycam-rainbow-WNJATm9pwnjpjI1i0g">Giphy</a></div>
<br>
<b>© Thore Tyborski 2020<br><br>
With contributions from <a href="https://github.com/khonkhortisan">khonkhortisan</a>, <a href="https://github.com/zjosua">zjosua</a>, 
<a href="https://www.reddit.com/user/SmallFluffyIPA/">SmallFluffyIPA</a> and <a href="https://github.com/AtilioA">Atílio Antônio Dadalto</a>.<br><br>
Also thank you to everyone who reported bugs and suggested new features!</b><br><br>
Contact: leaderboard_support@protonmail.com, <a href="https://www.reddit.com/user/Ttime5">Reddit</a> or 
<a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub</a>.
<h3>Change Log:</h3>
<b>{version}:</b><br>
- streak hotfix<br>
- increased window width<br>
<b>v1.6.3:</b><br>
- fixed odd number bug on home screen leaderboard<br>
- reduced home screen leaderboard server requests (improves performance)<br>
- home screen leaderboard users are clickable (for more info about user)<br>
- top three users of each league will get a medal that can be shown next to the username (optional) and will appear in the profile (starting from season 4)<br>
- season results are now being saved for each user and appear in their profile (starting from season 4)<br>
- "🥇", "🥈", "🥉" and "|" aren't allowed in usernames anymore<br>
- minor ui changes<br>
- improve the efficiency of statistical calculations (improves performance)<br>
- added "days studied" (in the current season) to league tab (a day counts when the user studied for at least 10 minutes)<br>
- users with 0 XP will be relegated in addition to the last 20%<br>
- notifications (server downtime, updates etc.) will only be shown once<br>
- new XP formula: <code>XP = days studied percentage x ((6 x time) + (2 x reviews x retention))</code> <b>starting from season 6<b>
"""