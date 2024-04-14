
#!/usr/bin/env python
import telebot
from util.clicks import click_add, click_clear, click_remove, click_show, click_find, click_add_favourite, click_remove_favourite, click_show_favourite, click_clear_favourite, create_database, callback_message
from util.commands import start, home, helpp
from util.gdrive_db import download_database, start_replacing
from threading import Thread


bot = telebot.TeleBot('YOUR_BOT_TOKEN')


#Call the function to download the database file from GOogle Drive
# download_database()

#Create a background thread to run the start_replacing function (replace list.db on Google Drive every 20 minutes (1200))
# replacing_thread = Thread(target=start_replacing)
# replacing_thread.start()

    #Create database in folder database if not exists
create_database()

    #Keyboard buttons and start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    start(bot, message)

    #Homepage
@bot.message_handler(commands=['home'])
def handle_home(message):
    home(bot, message)


    #keyboard buttons
@bot.message_handler(func=lambda message: message.text == 'Add word')
def add_word(message):
    bot.register_next_step_handler(message, lambda message: click_add(bot, message))

@bot.message_handler(func=lambda message: message.text == 'Remove word')
def remove_word(message):
    bot.register_next_step_handler(message, lambda message: click_remove(bot, message))
    
@bot.message_handler(func=lambda message: message.text == '🔎 Find word')
def find_word(message):
    bot.register_next_step_handler(message, lambda message: click_find(bot, message))

@bot.message_handler(func=lambda message: message.text == '📑 Show all words')
def show_words(message):
    click_show(bot, message)

@bot.message_handler(func=lambda message: message.text == 'Add to ☆')
def add_favourite(message):
    bot.register_next_step_handler(message, lambda message: click_add_favourite(bot, message))

@bot.message_handler(func=lambda message: message.text == 'Show ☆')
def show_favourite(message):
    click_show_favourite(bot, message)
    
@bot.message_handler(func=lambda message: message.text == 'Clear ☆')
def clear_favourite(message):
    bot.send_message(message.chat.id, text='Are you sure you want to delete all words from favourite❓ Type y / n' )
    bot.register_next_step_handler(message, lambda message: click_clear_favourite(bot, message))
    
@bot.message_handler(func=lambda message: message.text == 'Remove fr ☆')
def remove_favourite(message):
    bot.register_next_step_handler(message, lambda message: click_remove_favourite(bot, message))

@bot.message_handler(func=lambda message: message.text == 'Homepage')
def hadle_home(message):
    home(bot, message)
    
@bot.message_handler(func=lambda message: message.text == '❌Clear dictionary')
def clear_dictionary(message):
    bot.send_message(message.chat.id, text='Are you sure you want to delete all words from the dictionary❓ Type y / n' )
    bot.register_next_step_handler(message, lambda message: click_clear(bot, message))
    
@bot.message_handler(func=lambda message: message.text == 'Help')
def handle_start(message):
    start(bot, message)
    
    
    #Homepage buttons / buttons under image (img/home_photo.png)
@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    callback_message(bot, callback)
    
    
    #messages or actions after commads
@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, text="Enter the word you'd like to add")
    bot.register_next_step_handler(message, lambda message: click_add(bot, message))
    
@bot.message_handler(commands=['remove'])
def remove(message):
    bot.send_message(message.chat.id, text="Enter the word you want to delete")
    bot.register_next_step_handler(message, lambda message: click_remove(bot, message))
    
@bot.message_handler(commands=['find'])
def remove(message):  
    bot.send_message(message.chat.id, text="Enter the word you want to find")
    bot.register_next_step_handler(message, lambda message: click_find(bot, message))
    
@bot.message_handler(commands=['show'])
def show(message):
    click_show(bot, message)

@bot.message_handler(commands=['clear'])
def clear(message):
    bot.send_message(message.chat.id, text='Are you sure you want to delete all words from the dictionary❓ Type y / n' )
    bot.register_next_step_handler(message, lambda message: click_clear(bot, message))
    

@bot.message_handler(commands=['add_favourite'])
def add(message):
    bot.send_message(message.chat.id, text="Enter the word you'd like to add")
    bot.register_next_step_handler(message, lambda message: click_add_favourite(bot, message))
    
@bot.message_handler(commands=['remove_favourite'])
def remove(message):
    bot.send_message(message.chat.id, text="Enter the word you want to delete")
    bot.register_next_step_handler(message, lambda message: click_remove_favourite(bot, message))
    
@bot.message_handler(commands=['show_favourite'])
def show(message):
    click_show_favourite(bot, message)

@bot.message_handler(commands=['clear'])
def clear(message):
    bot.send_message(message.chat.id, text='Are you sure you want to delete all words from the dictionary❓ Type y / n' )
    bot.register_next_step_handler(message, lambda message: click_clear(bot, message))

    #start/help command/button
@bot.message_handler(commands=['help'])
def handle_start(message):
    start(bot, message)

@bot.message_handler(commands=['about'])
def handle_help(message):
    helpp(bot, message)
    
bot.infinity_polling()