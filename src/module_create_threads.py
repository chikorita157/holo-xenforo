from logging import debug, info, warning, error
from datetime import date, timedelta

import services
from data.models import Stream, Episode
import xenforo
import wordpress

from module_find_episodes import _create_xenforo_post, _edit_xenforo_post, _create_wordpress_post, _edit_wordpress_post

def main(config, db, show_name, episode):
	int_episode = Episode(int(episode), None, None, None)
	xenforo.init_xenforo(config)
	wordpress.init_wordpress(config)
	show = db.get_show_by_name(show_name)
	if not show:
		raise IOError(f"Show {show_name} does not exist!")
	stream = Stream.from_show(show)

	post_url = _create_xenforo_post(config, db, show, stream, int_episode, submit=not config.debug)
	info("  Xenforo Post URL: {}".format(post_url))
 
	wp_post_url = _create_wordpress_post(config, db, show, stream, int_episode, submit=not config.debug)
	info("  WordPress Post URL: {}".format(post_url))
	if post_url is not None:
		post_url = post_url.replace("http:", "https:")
		wp_post_url = post_url.replace("http:", "https:")
		db.add_episode(show, int_episode.number, post_url)
		if show.delayed:
			db.set_show_delayed(show, False)
		for editing_episode in db.get_episodes(show):
			_edit_xenforo_post(config, db, show, stream, editing_episode, editing_episode.link, submit=not config.debug)
			_edit_wordpress_post(config, db, show, stream, editing_episode, editing_episode.wp_post_link, submit=not config.debug)
		return True
	else:
		error("  Episode not submitted")
	return False
