import json
import requests
from aqt.utils import showWarning

def postRequest(endpoint, data, statusCode, warning=True):
	#url = f"http://127.0.0.1:8000/api/v2/{endpoint}"
	url = f"https://ankileaderboard.pythonanywhere.com/api/v2/{endpoint}"
	try:
		response = requests.post(url, data=data, timeout=15)
		
		if response.status_code == statusCode:
			return response
		else:
			if warning:
				showWarning(str(response.text))
				return False
			else:
				return response
	except Exception as e:
		errormsg = f"Timeout error [{url}] - No internet connection, or server response took too long. \n\n{str(e)}"
		if warning:
			showWarning(errormsg, title="Leaderboard Error")
			return False
		else:
			return errormsg


def getRequest(endpoint):
	#url = f"http://127.0.0.1:8000/api/v2/{endpoint}"
	url = f"https://ankileaderboard.pythonanywhere.com/api/v2/{endpoint}"
	try:
		response = requests.get(url, timeout=15)
		
		if response.status_code == 200:
			return response
		else:
			showWarning(str(response.text))
			return False	
	except Exception as e:
		showWarning(f"Timeout error [{url}] - No internet connection, or server response took too long. \n\n{str(e)}", title="Leaderboard Error")
		return False