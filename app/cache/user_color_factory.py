from app.twitch.emote import Emote

class UserColorFactory:
    _users = {}

    def random_color():
        import random
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 0xFF), random.randint(0, 0xFF), random.randint(0, 0xFF))

    def get_color(user_id):
        if user_id not in UserColorFactory._users:
            UserColorFactory._users[user_id] = UserColorFactory.random_color()
        return UserColorFactory._users[user_id]