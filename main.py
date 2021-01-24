import json
import threading

from scheduler import Scheduler
from timeDaemon import TimeDaemon

with open("license.json") as license_file:
    data = json.load(license_file)


t = TimeDaemon(5)
threading.Thread(target=t.run, args=()).start()
s = Scheduler(key=data['key'], current_position="Terni Italia", time_daemon=t, polling_sec=5)
while True:
    de = input("Destination: ")
    dl = input("Deadline: ")
    r = s.schedule_new_task(destination=de, deadline=dl, actions="")
    print(r["status"])
    print(r["message"])
