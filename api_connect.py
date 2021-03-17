import json
import requests
from aqt.utils import tooltip, showWarning

def connectToAPI(url, jsn, data, response, function):
	url = f"https://ankileaderboard.pythonanywhere.com/{url}"
	try:
		if jsn:
			x = requests.post(url, data=data).json()
		else:
			x = requests.post(url, data=data)
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