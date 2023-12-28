![Holo, of course.](holo.png)

# Holo
Anime episode discussion post bot for [Sakurajima Xenforo Forums](https://forums.sakurajima.moe/). Monitors online stream services for newly published episodes and creates a new thread for each for a specified forum via Xenforo API. This is a fork of the original Holo to work on Xenforo via its API.

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

### Modules

Name|Run freq|Command
:--|:-:|:--
Find new episodes|high|python holo.py -s [subreddit]
Update shows|med|python holo.py -m update
Find new show|low (or manual)|python holo.py -m find
Edit shows|manual|python holo.py -m edit [show-config]
Setup database|once|python holo.py -m setup

## Quick setup for development on an XenForo forums

1. Update config file with your desired useragent, URL to your XenForo forums, and the API key generated from the Admin control panel.See the [XenForo Documentation](https://xenforo.com/docs/dev/rest-api/) on how to enable the API and generate an API key
```
[connection]
useragent = useragent_to_use

[xenforo]
forum=(
xenforo_url=
xenforo_api_key=
```

2. Set up the database by running `python src/holo.py -m setup`
3. Load the desired season config files by running `python src/holo.py -m edit season_configs/[season]_[year].yaml`
4. Update the show information by running `python src/holo.py -m update`
5. The bot is now ready to post threads with `python src/holo.py`
