import json
import requests
from aqt.utils import showWarning

def connectToAPI(url, jsn, data, response, function):
	#url = f"http://127.0.0.1:8000/{url}"
	url = f"https://ankileaderboard.pythonanywhere.com/{url}"
	try:
		if jsn:
			x = requests.post(url, data=data, timeout=30).json()
		else:
			x = requests.post(url, data=data, timeout=30)
		if response:	
			if x.text == response:
				return x
			else:
				showWarning(str(x.text))
				return x
		else:
			return x
	except:
		showWarning(f"Timeout error [{function}] - No internet connection, or server response took too long.", title="Leaderboard error")