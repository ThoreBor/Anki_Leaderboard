import json
import requests
from aqt.utils import showWarning

def postRequest(url, data, statusCode):
	url = f"http://127.0.0.1:8000/api/v2/{url}"
	#url = f"https://ankileaderboard.pythonanywhere.com/api/v2/{url}"
	try:
		response = requests.post(url, data=data, timeout=15)
		
		if response.status_code == statusCode:
			return response
		else:
			showWarning(str(response.text))
			return False	
	except Exception as e:
		showWarning(f"Timeout error [{url}] - No internet connection, or server response took too long. \n\n {str(e)}", title="Leaderboard Error")
		return False

def getRequest(url):
	url = f"http://127.0.0.1:8000/api/v2/{url}"
	#url = f"https://ankileaderboard.pythonanywhere.com/api/v2/{url}"
	try:
		response = requests.get(url, timeout=15)
		
		if response.status_code == 200:
			return response
		else:
			showWarning(str(response.text))
			return False	
	except Exception as e:
		showWarning(f"Timeout error [{url}] - No internet connection, or server response took too long. \n\n {str(e)}", title="Leaderboard Error")
		return False