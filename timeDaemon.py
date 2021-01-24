import datetime
import threading
import time


class TimeDaemon:
    def __init__(self, min_every_sec):
        self._current_time = datetime.datetime.now()
        self._running = True
        self._min_every_sec = min_every_sec

    def run(self):
        while self._running:
            self._current_time = self._current_time + datetime.timedelta(
                minutes=self._min_every_sec)
            time.sleep(1)

    def get_current_time(self):
        return self._current_time

    def display_current_time(self):
        print(str(self._current_time))

    def stop_time_daemon(self):
        self._running = False
