import json
import threading

from scheduler import Scheduler
from timeDaemon import TimeDaemon

with open("license.json") as license_file:
    data = json.load(license_file)


t = TimeDaemon(5)
threading.Thread(target=t.run, args=()).start()
s = Scheduler(key=data['key'], current_position="Terni Italia", time_daemon=t, polling_sec=5)
'''
r = s.schedule_new_task(destination="Pisa Italia", deadline="23:00 24/01/21")
print(r["status"])
print(r["message"])
r = s.schedule_new_task(destination="Lucca Italia", deadline="18:00 24/01/21")
print(r["status"])
print(r["message"])
'''
r = s.schedule_new_task(destination="Rieti Italia", deadline="19:00 24/01/21")
print(r["status"])
print(r["message"])
