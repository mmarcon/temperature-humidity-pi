from __future__ import annotations
import os
from pi import DHT
from data_api import MongoDBDataAPI
import logging
import signal
import sys
from dotenv import load_dotenv
import time

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

def main():
    logger = logging.getLogger('main')
    # Get device_id from environment
    device_id = os.environ['DEVICE_ID']
    cluster_name = os.environ['cluster_name']
    app_id = os.environ['app_id']
    api_key = os.environ['api_key']

    mdb = MongoDBDataAPI(app_id=app_id, api_key=api_key, cluster_name=cluster_name)
    mdb.default_db = 'temperature_humidity_pi'
    mdb.default_collection = 'sensor_data'

    dht = DHT(lambda sensor_data: mdb.insert_one({
        "created_at": {
            "$date": { "$numberLong":  str(round(time.time() * 1000)) }
        },
        "metadata": {
            "device_id": device_id
        },
        "temperature": sensor_data['temperature'],
        "humidity": sensor_data['humidity']
    }), delay=30)
    dht.start()

    # Terminate things gracefully
    def ctrl_c_handler(sig, frame):
        logger.info('Ctrl-C detected')
        dht.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    signal.pause()

main()