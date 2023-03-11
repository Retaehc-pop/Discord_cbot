from discord.ext import commands


class UserBlacklisted(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but is blacklisted.
    """

    def __init__(self, message="User is blacklisted!"):
        self.message = message
        super().__init__(self.message)


class UserNotOwner(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but is not an owner of the bot.
    """

    def __init__(self, message="User is not an owner of the bot!"):
        self.message = message
        super().__init__(self.message)

class VoiceError(commands.CheckFailure):
    """
    thrown when there is an error with voice
    """
    def __init__(self, message="VOICE Error!"):
        self.message = message
        super().__init__(self.message)


class YTDLError(commands.CheckFailure):
    """
    thrown when there is an error with youtube-dl
    """
    def __init__(self, message="YTDL Error!"):
        self.message = message
        super().__init__(self.message)
        
class ApiError(commands.CheckFailure):
    """
    thrown when there is an error with the api
    """
    def __init__(self, message="There is something wrong with the API, please try again later"):
        self.message = message
        super().__init__(self.message)
