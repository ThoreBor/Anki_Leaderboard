from aqt import mw

def write_config(name, value):
	config = mw.addonManager.getConfig(__name__)

	config_content = {"username": config["username"], "friends": config["friends"], "newday": config["newday"], 
	"subject": config["subject"], "group_pwd": config["group_pwd"], "country": config["country"], "scroll": config["scroll"], 
	"refresh": config["refresh"], "tab": config["tab"], "token": config["token"], "achievement": config["achievement"], 
	"sortby": config["sortby"], "hidden_users": config["hidden_users"], "homescreen": config["homescreen"],
	"autosync": config["autosync"], "maxUsers": config["maxUsers"], "focus_on_user": config["focus_on_user"], "import_error": config["import_error"],
	"show_medals": config["show_medals"], "notification_id": config["notification_id"],
	"homescreen_data": config["homescreen_data"], "medal_users": config["medal_users"]}
	config_content[name] = value
	mw.addonManager.writeConfig(__name__, config_content)