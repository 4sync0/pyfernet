import logging
import os

# debug config
logging.basicConfig(filename="LOGS/logs.log", level=logging.DEBUG, format=" %(levelname)s, %(filename)s , %(asctime)s, %(message)s")

# info config
logging.basicConfig(filename="LOGS/logs.log", level=logging.INFO, format=" %(levelname)s, %(filename)s , %(asctime)s, %(message)s")