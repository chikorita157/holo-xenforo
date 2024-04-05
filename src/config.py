import configparser
from logging import warning

class WhitespaceFriendlyConfigParser(configparser.ConfigParser):
	def get(self, section, option, *args, **kwargs):
		val = super().get(section, option, *args, **kwargs)
		return val.strip('"')

class Config:
	def __init__(self):
		self.debug = False
		self.module = None
		self.database = None
		self.useragent = None
		self.ratelimit = 1.0
		self.forum = None
		self.xenforo_url = None
		self.xenforo_api_key = None
		
		self.services = dict()
		
		self.new_show_types = list()
		self.record_scores = False
		
		self.discovery_primary_source = None
		self.discovery_secondary_sources = list()
		self.discovery_stream_sources = list()
		
		self.post_title = None
		self.post_title_with_en = None
		self.post_title_postfix_final = None
		self.post_body = None
		self.batch_thread_post_title = None
		self.batch_thread_post_title_with_en = None
		self.batch_thread_post_body = None
		self.post_formats = dict()
		
		self.wordpress_url = None
		self.wordpress_username = None
		self.wordpress_app_password = None
		self.wordpress_post_body = None
		self.wordpress_batch_thread_post_body = None
		self.wordpress_post_formats = dict()
		
		self.misskey_api_key = None
		self.misskey_instance_url = None
	
def from_file(file_path):
	if file_path.find(".") < 0:
		file_path += ".ini"
	
	parsed = WhitespaceFriendlyConfigParser()
	success = parsed.read(file_path, encoding='utf-8')
	if len(success) == 0:
		print("Failed to load config file")
		return None
	
	config = Config()
	
	if "data" in parsed:
		sec = parsed["data"]
		config.database = sec.get("database", None)
	
	if "connection" in parsed:
		sec = parsed["connection"]
		config.useragent = sec.get("useragent", None)
		config.ratelimit = sec.getfloat("ratelimit", 1.0)
	
	if "xenforo" in parsed:
		sec = parsed["xenforo"]
		config.forum = sec.get("forum", None)
		config.xenforo_url = sec.get("xenforo_url", None)
		config.xenforo_api_key = sec.get("xenforo_api_key", None)
	
	if "options" in parsed:
		sec = parsed["options"]
		config.debug = sec.getboolean("debug", False)
		from data.models import str_to_showtype
		config.new_show_types.extend(map(lambda s: str_to_showtype(s.strip()), sec.get("new_show_types", "").split(" ")))
		config.record_scores = sec.getboolean("record_scores", False)
	
	if "options.discovery" in parsed:
		sec = parsed["options.discovery"]
		config.discovery_primary_source = sec.get("primary_source", None)
		config.discovery_secondary_sources = sec.get("secondary_sources", "").split(" ")
		config.discovery_stream_sources = sec.get("stream_sources", "").split(" ")
	
	if "post" in parsed:
		sec = parsed["post"]
		config.post_title = sec.get("title", None)
		config.post_title_with_en = sec.get("title_with_en", None)
		config.post_title_postfix_final = sec.get("title_postfix_final", None)
		config.post_body = sec.get("body", None)
		config.batch_thread_post_title = sec.get("batch_thread_title", None)
		config.batch_thread_post_title_with_en = sec.get("batch_thread_title_with_en", None)
		config.batch_thread_post_body = sec.get("batch_thread_body", None)
		for key in sec:
			if key.startswith("format_") and len(key) > 7:
				config.post_formats[key[7:]] = sec[key]
				
	if "wordpress" in parsed:
		sec = parsed["wordpress"]
		config.wordpress_url = sec.get("wordpress_url", None)
		config.wordpress_username = sec.get("wordpress_username", None)
		config.wordpress_app_password = sec.get("wordpress_app_password", None)
		config.wordpress_body = sec.get("wordpress_body", None)
		config.wordpress_batch_thread_post_body = sec.get("wordpress_batch_thread_body", None)
		for key in sec:
			if key.startswith("wordpress_format_") and len(key) > 17:
				config.wordpress_post_formats[key[17:]] = sec[key]
	
	
	# Services
	for key in parsed:
		if key.startswith("service."):
			service = key[8:]
			config.services[service] = parsed[key]
	
	# Misskey
	if "misskey" in parsed:
		sec = parsed["misskey"]
		config.misskey_api_key = sec.get("misskey_api_key", None)
		config.misskey_instance_url = sec.get("misskey_instance_url", None)
	return config
def validate(config):
	def is_bad_str(s):
		return s is None or len(s) == 0
	
	if is_bad_str(config.database):
		return "database missing"
	if is_bad_str(config.useragent):
		return "useragent missing"
	if config.ratelimit < 0:
		warning("Rate limit can't be negative, defaulting to 1.0")
		config.ratelimit = 1.0
	if config.forum == 0:
		return "invalid forum id or missing"
	if is_bad_str(config.xenforo_url):
		return "missing xenforo url"
	if is_bad_str(config.xenforo_url):
		return "missing xenforo api key"
	if is_bad_str(config.post_title):
		return "post title missing"
	if is_bad_str(config.post_body):
		return "post title missing"
	return False
