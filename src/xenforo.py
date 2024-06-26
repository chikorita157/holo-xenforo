from logging import debug, info, warning, error, exception
import requests

# Initialization

_config = None

def init_xenforo(config):
	global _config
	_config = config

# Thing doing

def submit_text_post(forum, title, body):
	try:  			
		info("Submitting post to {}".format(forum))
		newHeaders = {'Content-type': 'application/x-www-form-urlencoded', 'XF-Api-Key': _config.xenforo_api_key}
		response = requests.post(_config.xenforo_url + '/api/threads/',
 		data={'node_id': forum, 'title': title, 'message' : body},
 		headers=newHeaders)
		print("Status code: ", response.status_code)
		if response.status_code == 200:
			responsedata = response.json()
			thread = responsedata['thread']
			posturl = _config.xenforo_url + '/threads/' + str(thread['thread_id'])
			if _config.misskey_instance_url is not None:
				if _config.misskey_api_key is not None:
					share_thread_url_to_misskey(title, posturl)
			return posturl
		else:
			print("Response: ", response.json())
			exception("Failed to create thread")
			return None
	except:
		exception("Failed to create threead")
		return None

def edit_text_post(threadid, body):
	try:
		info(f"Editing post {threadid}")
		thread = get_text_post(threadid)
		post_id = thread['thread']['first_post_id']
		print("Editing post: ", post_id)
		newHeaders = {'Content-type': 'application/x-www-form-urlencoded', 'XF-Api-Key': _config.xenforo_api_key}
		response = requests.post(_config.xenforo_url + '/api/posts/' + str(post_id) + '/',
 		data={'message' : body, 'silent' : True, 'clear_edit' : True},
 		headers=newHeaders)
		print("Status code: ", response.status_code)
		if response.status_code == 200:
			responsedata = response.json()
			return _config.xenforo_url + '/threads/' + str(threadid)
   
		elif response.status_code == 404:
			print("Does not exist")
			return None
		else:
			print("Response: ", response.json())
			exception("Failed to edit the first post of the thread")
			return None
	except requests.exceptions.HTTPError as err:
		print(err.request.url)
		print(err)
		print(err.response.text)
		#exception("Failed to edit the first post of the thread")
		return None

def get_text_post(threadid):
	try:
		newHeaders = {'Content-type': 'application/x-www-form-urlencoded', 'XF-Api-Key': _config.xenforo_api_key}
		response = requests.get(_config.xenforo_url + '/api/threads/' + str(threadid) + '/',
 		headers=newHeaders)
		print("Status code: ", response.status_code)
		if response.status_code == 200:
			return response.json()
		elif response.status_code == 404:
			print("Does not exist")
			return None
		else:
			print("Response: ", response.json())
			exception("Failed to retrieve thread informationt")
			return None
	except:
		exception("Failed to retrieve thead inforrmation")
		return None

def share_thread_url_to_misskey(title, url):
	try:
		info("Sharing link on Misskey for {}".format(title))
		newHeaders = {'Content-type': 'application/json', 'Authorization': _config.misskey_api_key}
		response = requests.post(_config.misskey_instance_url + '/api/notes/create',
 	json={'visibility': 'home', 'text':'New Anime Discussion Thread is now available: ' + title + '\n' + url + '\n\nNote: Anyone can participate on Sakurajima Forums. Users who are on Sakurajima Mastodon server can sign in/create an account using the Mastodon button. Other users can use any other social logins or create an account using an email.', 'i': _config.misskey_api_key},
 		headers=newHeaders)
		print("Status code: ", response.status_code)
		if response.status_code == 200:
			responsedata = response.json()
			print("Response: ", response.json())
			return None;
		else:
			print("Response: ", response.json())
			exception("Failed to create thread")
			return None
	except:
		return None

# Utilities

def get_shortlink_from_id(threadid):
	return _config.xenforo_url + '/threads/' + str(threadid)
