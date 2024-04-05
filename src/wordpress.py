from logging import debug, info, warning, error, exception
import requests

# Initialization

_config = None

def init_wordpress(config):
    global _config
    _config = config

# Thing doing

def submit_text_post(title, body, tags):
    try:
        info("Submitting post to WordPress")
        newHeaders = {'Content-type': 'application/json'}
		data = {
			'title' : title,
			'status': 'published',
			'content': body,
		}
        response = requests.post(_config.wordpress_url + '/wp-json/wp/v2/posts',
         json = data,
         auth=(_config.wordpress_username, _config.wordpress_app_password))
        print("Status code: ", response.status_code)
        if response.status_code == 200:
            responsedata = response.json()
            posturl = _config.wordpress_url + '/?p=' + str(responsedata['id'])
            return posturl
        else:
            print("Response: ", response.json())
            exception("Failed to create blog post")
            return None
    except:
        exception("Failed to create blog post")
        return None

def edit_text_post(postid, body):
    try:
        info(f"Editing WordPress post {postid}")
        print("Editing WordPress post: ", postid)
		data = {
			'content': body,
		}
        response = requests.put(_config.wordpress_url + '/wp-json/wp/v2/posts/' + str(post_id) + '/',
         json=data,
         auth=(_config.wordpress_username, _config.wordpress_app_password))
        print("Status code: ", response.status_code)
        if response.status_code == 200:
            responsedata = response.json()
            return _config.wordpress_url + '/?p=' + str(postid)
   
        elif response.status_code == 404:
            print("Does not exist")
            return None
        else:
            print("Response: ", response.json())
            exception("Failed to edit blog post")
            return None
    except requests.exceptions.HTTPError as err:
        print(err.request.url)
        print(err)
        print(err.response.text)
        #exception("Failed to edit the first post of the thread")
        return None

# Utilities

def get_shortlink_from_id(postid):
    return _config.wordpress_url + '?p=' + str(postid)
