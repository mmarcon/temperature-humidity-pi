from __future__ import annotations
import os
from pi import DHT
import logging
import signal
import sys

logging.basicConfig(level=logging.DEBUG)

def main():
    logger = logging.getLogger('main')
    # Get device_id from environment
    device_id = os.environ['DEVICE_ID']

    dht = DHT(lambda sensor_data: logger.info(sensor_data))
    dht.start()

    # Terminate things gracefully
    def ctrl_c_handler(sig, frame):
        logger.info('Ctrl-C detected')
        dht.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    signal.pause()

main()