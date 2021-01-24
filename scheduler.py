import datetime
import itertools
import threading
import time
from threading import Lock

import googlemaps

from carTask import CarTask
from userTask import UserTask


class Scheduler:
    def __init__(self, key, current_position, time_daemon, polling_sec):
        self._client = googlemaps.Client(key=key)
        self._current_user_tasks = []
        self._car_tasks_lock = Lock()
        self._current_car_tasks = []
        self._current_position = current_position
        self._time_daemon = time_daemon
        self._polling_sec = polling_sec
        threading.Thread(target=self._emulate_current_position).start()

    def _emulate_current_position(self):
        while True:
            self._car_tasks_lock.acquire()
            for car_task in self._current_car_tasks:
                if car_task.get_arrival_time() < self._time_daemon.get_current_time():
                    del self._current_car_tasks[0]
                    self._current_position = car_task.get_destination()
                    print("Reached " + self._current_position + " (" +
                          str(car_task.get_arrival_time()) + ")")
                else:
                    break
            self._car_tasks_lock.release()
            time.sleep(self._polling_sec)

    @staticmethod
    def get_overall_distance_from_car_tasks_schedule(car_tasks_schedule):
        total_distance = 0
        for car_task in car_tasks_schedule:
            total_distance += car_task.get_distance()
        return total_distance

    def compute_schedule(self, candidate_user_tasks_schedule):
        waypoints = None
        if len(candidate_user_tasks_schedule) > 1:
            waypoints = []
            for w in candidate_user_tasks_schedule[:-1]:
                waypoints.append(w.get_destination())
        directions_result = self._client.directions(origin=self._current_position,
                                                    destination=candidate_user_tasks_schedule[
                                                        -1].get_destination(),
                                                    waypoints=waypoints)
        pos = -1
        predicted_time = self._time_daemon.get_current_time()
        candidate_car_tasks_schedule = []
        for leg in directions_result[0]['legs']:
            pos = pos + 1
            predicted_time = predicted_time + datetime.timedelta(seconds=leg['duration']['value'])
            predicted_time = predicted_time.replace(microsecond=0)
            if predicted_time > candidate_user_tasks_schedule[pos].get_deadline():
                return {"status": "ERR", "message": "Scheduling not feasible!"}
            candidate_car_tasks_schedule.append(CarTask(
                destination=candidate_user_tasks_schedule[pos].get_destination(), distance=leg[
                    'distance']['value'], arrival_time=predicted_time, deadline=
                candidate_user_tasks_schedule[pos].get_deadline()))
        return {"status": "OK", "candidate_schedule": candidate_car_tasks_schedule}

    def schedule_new_task(self, destination, deadline):
        """
        :type destination: str
        :type deadline: str with the format '%H:%M %d/%m/%y'
        """
        print("Scheduling a new task...")
        datetime_deadline = datetime.datetime.strptime(deadline, '%H:%M %d/%m/%y')
        if datetime_deadline < self._time_daemon.get_current_time():
            return {"status": "ERR", "message": "This is a car not a time machine!"}
        new_task = UserTask(destination=destination, deadline=datetime_deadline)
        tmp_user_tasks_list = self._current_user_tasks.copy()
        tmp_user_tasks_list.append(new_task)
        task_permutations = list(itertools.permutations(tmp_user_tasks_list))
        candidates_car_tasks_schedule_list = list()
        for candidate_user_tasks_schedule in task_permutations:
            scheduling_result = self.compute_schedule(candidate_user_tasks_schedule)
            if scheduling_result["status"] == "OK":
                candidates_car_tasks_schedule_list.append(scheduling_result["candidate_schedule"])
        if not candidates_car_tasks_schedule_list:
            return {"status": "ERR", "message": "Due to the current scheduling is not possible to "
                                                "add this task"}

        best_car_tasks_schedule = candidates_car_tasks_schedule_list[0]
        min_distance = self.get_overall_distance_from_car_tasks_schedule(
            candidates_car_tasks_schedule_list[0])
        for candidate_car_tasks_schedule in candidates_car_tasks_schedule_list[1:]:
            if min_distance > self.get_overall_distance_from_car_tasks_schedule(
                    candidate_car_tasks_schedule):
                min_distance = self.get_overall_distance_from_car_tasks_schedule(
                    candidate_car_tasks_schedule)
                best_car_tasks_schedule = candidate_car_tasks_schedule
        self._car_tasks_lock.acquire()
        self._current_car_tasks = best_car_tasks_schedule.copy()
        self._car_tasks_lock.release()
        self._current_user_tasks = tmp_user_tasks_list.copy()
        scheduling_message = ""
        for car_task in self._current_car_tasks:
            scheduling_message += str(car_task) + "\n"
        return {"status": "OK", "message": "New Scheduling computed: \n" + scheduling_message}
