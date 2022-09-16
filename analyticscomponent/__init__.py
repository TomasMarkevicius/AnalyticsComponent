from configparser import ConfigParser
CONFIG_PATH = "analyticscomponent/config.ini"
config = ConfigParser()

config.read(CONFIG_PATH)
cfg = config["Settings"]

