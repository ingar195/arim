import requests
import logging
import json
import mqtt
import time
from datetime import datetime

# Logging setup
log_file = "arim.log"

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO,
    handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
    ])
logging.info("------------------------------------------------------")
logging.debug("Logger initialized")


def read_config(config_json="/home/user/arim_api/config.json"):
    """
    Reads the config file and returns token and VIN
    """
    # config_json = "config.json"
    with open(config_json) as f:
        config = json.load(f)
    logging.debug(config)
    url = config["url"]
    mqtt_host = config["mqtt_host"]
    mqtt_port = config["mqtt_port"]
    mqtt_user = config["mqtt_user"]
    mqtt_password = config["mqtt_password"]

    return url, mqtt_host, mqtt_port, mqtt_user, mqtt_password


def get_pickup_dates():
    url, mqtt_host, mqtt_port, mqtt_user, mqtt_password = read_config()

    response = requests.get(url)
    logging.debug(response.text)
    return response.json()["fetchDays"]


def send_messages(type, date):
    url, mqtt_host, mqtt_port, mqtt_user, mqtt_password = read_config()

    mqtt.run(mqtt_host, mqtt_port, mqtt_user, mqtt_password, f"arim/{type}", date)


def parse():
    for x in get_pickup_dates():
        frak = x["FraksjonId"]
        date = x["Tommedatoer"][0].split("T")[0]

        
        pattern = '%Y-%m-%d'
        epoch = int(time.mktime(time.strptime(date, pattern)))
        logging.debug(epoch)

        now = datetime.now()
        current_epoch = time.mktime(now.timetuple())

        logging.info(f"Current epoch: {current_epoch}")
        logging.info(f"Epoch: {epoch}")
        if epoch <= current_epoch:
            date = x["Tommedatoer"][1].split("T")[0]
            epoch = int(time.mktime(time.strptime(date, pattern)))
            logging.info("Changed to next pickupday")

        if frak == 1:
            logging.debug(f"waste: {date}")
            send_messages("waste/date", date)
            send_messages("waste/epoch", epoch)

        elif frak == 2:
            logging.debug(f"cardboard: {date}")
            send_messages("cardboard/date", date)
            send_messages("cardboard/epoch", epoch)
            
        elif frak == 4:
            logging.debug(f"metal: {date}")
            send_messages("metal/date", date)
            send_messages("metal/epoch", epoch)
parse()
