import json


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
