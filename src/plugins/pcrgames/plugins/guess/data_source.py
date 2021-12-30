import json
from utils.service import Service
from utils.rule import is_in_service


class Guess(Service):
    def __init__(self):
        Service.__init__(self, "guess", __doc__, rule=is_in_service("guess"))
