class UserTask:

    def __init__(self, destination, deadline):
        self._destination = destination
        self._deadline = deadline

    def get_destination(self):
        return self._destination

    def get_deadline(self):
        return self._deadline
