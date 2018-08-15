from threading import local


class Storage(local):
    def __init__(self):
        self.user_id = None

    def set_user_id(self, user_id: int):
        self.user_id = int(user_id)

    def get_user_id(self) -> int:
        return self.user_id

    def reset_user_id(self):
        self.user_id = None


storage = Storage()
