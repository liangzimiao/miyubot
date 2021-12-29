import json
from utils.service import Service
from utils.rule import is_in_service


class Text:
    text: str = ""


class Perception:
    inputText: Text

    def __init__(self):
        self.inputText = Text()


class UserInfo:
    apiKey: str = ""
    userId: str = ""


class Request:
    reqType: int = 0
    perception: Perception
    userInfo: UserInfo

    def __init__(self):
        self.perception = Perception()
        self.userInfo = UserInfo()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class AiChat(Service):
    def __init__(self):
        Service.__init__(self, "aichat", __doc__, rule=is_in_service("aichat"))
