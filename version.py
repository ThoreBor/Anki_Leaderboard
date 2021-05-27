version = "v1.7.0"

about_text = f"""
<h2>Leaderboard {version}</h2>
This add-on ranks all of its users by the number of cards reviewed today, time spend studying today, 
current streak, reviews in the past 31 days, and retention. You can also compete against friends, join groups, 
and join a country leaderboard. You'll only see users, that synced on the same day as you.<br><br>
In the league tab, you see everyone that synced at least once during the current season. There are four leagues
(Alpha, Beta, Gamma, and Delta). A season lasts two weeks. You don't have to sync every day.
The XP formula is:<br><b>XP = days studied percentage x ((6 x time) + (2 x reviews x retention))</b>.<br>
You have to study at least 5 minutes per day, otherwise those days won't be count as "studied"
(<i><a href="https://github.com/ThoreBor/Anki_Leaderboard/issues/122">See this issue for more info<a/></i>).
At the end of each season, the top 20% will be promoted, and the last 20% will be relegated.<br><br>
The code for the add-on is available on <a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub.</a> 
It is licensed under the <a href="https://github.com/ThoreBor/Anki_Leaderboard/blob/master/LICENSE">MIT License.</a> 
If you like this add-on, rate and review it on <a href="https://ankiweb.net/shared/info/41708974">AnkiWeb.</a><br><br>
You can also check the leaderboard (past 24 hours) on this <a href="https://ankileaderboard.pythonanywhere.com/">website</a>.<br>
<div>Crown icon made by <a href="https://www.flaticon.com/de/autoren/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Person icon made by <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Confetti gif from <a href="https://giphy.com/stickers/giphycam-rainbow-WNJATm9pwnjpjI1i0g">Giphy</a></div><br>
Contact: leaderboard_support@protonmail.com, <a href="https://www.reddit.com/user/Ttime5">Reddit</a> or 
<a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub</a>.
<br><br>
<b>© Thore Tyborski 2021<br>
With contributions from <a href="https://github.com/khonkhortisan">khonkhortisan</a>, <a href="https://github.com/zjosua">zjosua</a>, 
<a href="https://www.reddit.com/user/SmallFluffyIPA/">SmallFluffyIPA</a> and <a href="https://github.com/AtilioA">Atílio Antônio Dadalto</a>.<br>
Also thank you to everyone who reported bugs and suggested new features!</b>
<h3>Change Log:</h3>
- added option to join multiple groups <b>(you have to rejoin the group you previously joined)</b><br>
- added option to report users<br>
- added config shortcut<br>
- removed E-Mail from group request<br>
- fixed stats bug (rescheduled cards were counted as reviews)<br>
- fixed days studied bug<br>
- minimum study time for leagues is now 5 minutes<br>
- adjusted dark mode colors<br>
- UI changes<br>
- various under the hood changes (add-on and server-side)<br><br>
<b>You can check out the full change log on <a href="https://github.com/ThoreBor/Anki_Leaderboard/blob/master/changelog.md">GitHub</a>.</b>
"""