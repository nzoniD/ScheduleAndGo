class UserTask:

    def __init__(self, destination, deadline, actions):
        self._destination = destination
        self._deadline = deadline
        self._actions = actions

    def get_destination(self):
        return self._destination

    def get_deadline(self):
        return self._deadline
