from telebot import TeleBot
from telebot.types import Message


def anti_spam(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != 'OK':
            return
    bot.send_message(
        message.chat.id,
        """This is demo spam command.
If you send this command more than once within 2 seconds, 
bot will warn you.
This is made by using middlewares."""
)