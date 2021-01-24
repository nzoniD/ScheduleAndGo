class CarTask:
    def __init__(self, destination, distance, arrival_time, deadline):
        """

        :rtype: object CarTask
        """
        self._destination = destination
        self._distance = distance
        self._arrival_time = arrival_time
        self._deadline = deadline

    def get_distance(self):
        return self._distance

    def __repr__(self):
        return "-> " + self._destination + " expected arrival: " + str(self._arrival_time) + " (" \
               + str(self._deadline) + ")"

    def get_arrival_time(self):
        return self._arrival_time

    def get_destination(self):
        return self._destination
