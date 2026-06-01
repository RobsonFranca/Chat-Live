from app.utils.colors import Color

class UserColorFactory:
    _users = {}

    def get_color(user_id):
        if user_id not in UserColorFactory._users:
            UserColorFactory._users[user_id] = Color.get_random()
        return UserColorFactory._users[user_id]