![Holo, of course.](holo.png)

# Holo
Anime episode discussion post bot for [Sakurajima Xenforo Forums](https://forums.sakurajima.moe/) and WordPress. Monitors online stream services for newly published episodes and creates a new thread for each for a specified forum via Xenforo and WordPress API. This is a fork of the original Holo to work on Xenforo and WordPress via its API.

To use Holo with Xenforo only, use the xenforo branch

Season configurations (show names and associated service URLs for each anime season) can be found in `season_configs`. Each can be loaded using the `edit` module.

## Requirements
* Python 3.5+
* `requests`
* `feedparser`
* `beautifulsoup4`
* `unidecode`
* `pyyaml`

## Design notes
* Partitioned into multiple self-contained runnable modules
* Runs once and exits to play nice with schedulers
* Source sites (Crunchyroll, Funimation, Nyaa) are self-contained with a common interface
* Adds support to share the newly created discussion link to Misskey/Sharkey (ActivityPub software compatible with other Fediverse software like Mastodon)

### Modules

Name|Run freq|Command
:--|:-:|:--
Find new episodes|high|python holo.py
Update shows|med|python holo.py -m update
Find new show|low (or manual)|python holo.py -m find
Edit shows|manual|python holo.py -m edit [show-config]
Setup database|once|python holo.py -m setup

## Quick setup for development on an XenForo forums

1. Update config file with your desired useragent, URL to your XenForo forums, and the API key generated from the Admin control panel.See the [XenForo Documentation](https://xenforo.com/docs/dev/rest-api/) on how to enable the API and generate an API key. For WordPress, add the URL to your WordPress site, the username, and App Password
```
[connection]
useragent = useragent_to_use

[xenforo]
forum=
xenforo_url=
xenforo_api_key=

[wordpress]
wordpress_url =
wordpress_username =
wordpress_app_password =
```

2. Set up the database by running `python src/holo.py -m setup`
3. Load the desired season config files by running `python src/holo.py -m edit season_configs/[season]_[year].yaml`
4. Update the show information by running `python src/holo.py -m update`
5. The bot is now ready to post threads with `python src/holo.py`
