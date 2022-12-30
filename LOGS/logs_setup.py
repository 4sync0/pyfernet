import logging
import os

#debug config
logging.basicConfig(filename="LOGS/logs.log", level=logging.DEBUG, format=" %(levelname)s, %(filename)s , %(asctime)s, %(message)s")

#error config
logging.basicConfig(filename="LOGS/logs.log", level=logging.ERROR, format=" %(levelname)s, %(filename)s , %(asctime)s, %(message)s")