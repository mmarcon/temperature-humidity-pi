from __future__ import annotations
import Adafruit_DHT
from typing import Union
import threading
from typing import Callable
import time
import logging

class DHT(threading.Thread):
    def __init__(self, notify: Callable[[dict]], delay=10.0, retry_delay=2.0) -> DHT:
        threading.Thread.__init__(self)
        self.dht_device = Adafruit_DHT.DHT11
        self.dht_pin = 4
        self.notify = notify
        self.delay = delay
        self.retry_delay = retry_delay
        self.__stopped = False
        self.logger = logging.getLogger('DHT')

    def poll(self) -> Union[dict, None]:
        self.logger.info('Polling sensor')
        try:
            humidity, temperature = Adafruit_DHT.read(self.dht_device, self.dht_pin)
            self.logger.info('Temperature=%d, Humidity=%d', temperature, humidity)
            return {
                'temperature': temperature,
                'humidity': humidity
            }
        except RuntimeError:
            self.logger.info('Nothing came back, will try again shortly')
            return None
        except Exception as error:
            self.logger.exception('Something is unexpectedly broken, exiting')
            self.dht_device.exit()
            raise error

    def stop(self):
        self.__stopped = True
    
    def run(self):
        self.logger.debug('Thread started')
        while not self.__stopped:
            sensor_data = self.poll()
            if not sensor_data:
                time.sleep(self.retry_delay)
                continue
            self.notify(sensor_data)
            time.sleep(self.delay)