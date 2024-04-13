
#!/usr/bin/env python
import telebot
from telebot import types
import sqlite3
from util.clicks import click_add, click_clear, click_remove, click_show, click_find, click_add_favourite, click_remove_favourite, click_show_favourite, click_clear_favourite
from keep_alive import keep_alive

keep_alive()

bot = telebot.TeleBot('7049056882:AAGwFBH9Yrv9Ruy81IrdQQmyMeGWJd-0dBw')

@bot.message_handler(commands=['start'])
def start(message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Add word')
    btn2 = types.KeyboardButton('Remove word')
    btn3 = types.KeyboardButton('🔎 Find word')
    btn4 = types.KeyboardButton('📑 Show all words')
    btn5 = types.KeyboardButton('❌Clear dictionary')
    btn6 = types.KeyboardButton('Homepage')
    btn8 = types.KeyboardButton('Add to ☆')
    btn9 = types.KeyboardButton('Show ☆')
    btn14 = types.KeyboardButton('Clear ☆')
    btn10 = types.KeyboardButton('Remove fr ☆')
    btn11 = types.KeyboardButton('Help')
    murkup.row(btn1, btn2)
    murkup.row(btn3, btn8, btn5)
    murkup.row(btn10, btn14, btn9)
    murkup.row(btn4, btn6, btn11)
    
    bot.send_message(message.chat.id, '<b><u>📖DICTIONARY📖</u></b> \n'
                                    "\n<b>Hi, it's Dictionary</b>\n"
                                    "<b>\n📝INSTRUCTION📝:</b>\n"
                                    "\n ➡️<b>To add a new word to the dictionary, click the 'ADD WORD' button or type the <em>'/add'</em> command and enter the new word and translation in the following form: 'word - translation'</b>\n"
                                    " ➡️<b>To delete a word from the dictionary, click the 'REMOVE WORD word' button or enter the <em>'/remove'</em> command and type the word or its translation as you want to delete it</b>\n"
                                    " ➡️<b>Press 'FIND WORD' or type <em>'/find'</em> and enter the word or its translation to get it in the dictionary</b>\n"
                                    " ➡️<b>Press 'SHOW ALL WORDS' or type <em>'/show'</em> to get a list of all words in the dictionary</b>\n"
                                    " d\n"
                                    
                                    '\n<em>/home: Open the main menu</em>\n'
                                    '<em>/add: Add a specific word to the dictionary</em>\n'
                                    '<em>/remove: Delete a specific word from the dictionary</em>\n'
                                    '<em>/find: Find a specific word in the dictionary</em>\n'
                                    '<em>/show: Show all words in the dictionary</em>\n'
                                    '<em>/clear: Delete all words from the dictionary</em>\n' , reply_markup=murkup, parse_mode='html')
    
    conn = sqlite3.connect('database/list.db')
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS "users" ("id" INTEGER NOT NULL, "chat_id" blob, "word" blob, "translate" blob, "watchlist" INTEGER, "username" blob, PRIMARY KEY("id" AUTOINCREMENT));')
    conn.commit()
    
    cur.close()
    conn.close()
    
    
    #buttons under photo
@bot.message_handler(commands=['home'])
def home(message):
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('➕ Add word', callback_data='add')
    btn2 = types.InlineKeyboardButton('➖ Remove word', callback_data='remove')
    btn3 = types.InlineKeyboardButton('🔎 Find word', callback_data='find')
    btn4 = types.InlineKeyboardButton('📑 Show all words', callback_data='show')
    btn5 = types.InlineKeyboardButton('❌ Clear', callback_data='clear')
    btn6 = types.InlineKeyboardButton('📌 Pin', callback_data='pin')
    btn7 = types.InlineKeyboardButton('Close', callback_data='close')
    btn8 = types.InlineKeyboardButton('Help', callback_data='help')
    btn9 = types.InlineKeyboardButton('Add to ☆ ', callback_data='add_watch')
    btn10 = types.InlineKeyboardButton('Show ☆', callback_data='show_watch')
    btn11 = types.InlineKeyboardButton('Remove ☆', callback_data='remove_watch')
    murkup.row(btn1,btn2)
    murkup.row(btn3)
    murkup.row(btn4, btn5)
    murkup.row(btn10, btn11, btn9)
    murkup.row(btn6, btn8, btn7)
    bot.send_photo(message.chat.id, photo=open('/Users/bohdanprokopchuk/Desktop/dictionary_bot/home_photo.png', 'rb'), reply_markup=murkup)


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
def home2(message):
    home(message)
    
@bot.message_handler(func=lambda message: message.text == '❌Clear dictionary')
def clear_dictionary(message):
    bot.send_message(message.chat.id, text='Are you sure you want to delete all words from the dictionary❓ Type y / n' )
    bot.register_next_step_handler(message, lambda message: click_clear(bot, message))
    
@bot.message_handler(func=lambda message: message.text == 'Help')
def start3(message):
    start(message)
    
    
    #buttons under image
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'add':
        add_word(callback.message)
    elif callback.data == 'remove':
        remove_word(callback.message)
    elif callback.data == 'find':
        find_word(callback.message)
    elif callback.data == 'show':
        show_words(callback.message)
    elif callback.data == 'show_watch':
        show_favourite(callback.message)
    elif callback.data == 'add_watch':
        add_favourite(callback.message)
    elif callback.data == 'help':
        start(callback.message)
    elif callback.data == 'remove_watch':
        remove_favourite(callback.message)
    elif callback.data == 'clear':
        clear_dictionary(callback.message)
    elif callback.data == 'pin':
        bot.pin_chat_message(callback.message.chat.id, callback.message.message_id, disable_notification=True)
    elif callback.data == 'close':
        bot.delete_message(callback.message.chat.id, callback.message.message_id) 
    
    
    #clear all dictionary y/n
@bot.callback_query_handler(func=lambda callback: callback.data == 'clear1')
def callback_message2(callback):
    click_clear(bot, callback.message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'no')
def callback_message2(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    
    #messages or actions after commads
@bot.message_handler(commands=['add'])
def add(message):
    bot.register_next_step_handler(message, lambda message: click_add(bot, message))
    
@bot.message_handler(commands=['remove'])
def remove(message):
    bot.register_next_step_handler(message, lambda message: click_remove(bot, message))
    
@bot.message_handler(commands=['find'])
def remove(message):  
    bot.register_next_step_handler(message, lambda message: click_find(bot, message))
    
@bot.message_handler(commands=['show'])
def show(message):
    click_show(bot, message)

@bot.message_handler(commands=['clear'])
def clear(message):
    bot.send_message(message.chat.id, text='Are you sure you want to delete all words from the dictionary❓ Type y / n' )
    bot.register_next_step_handler(message, lambda message: click_clear(bot, message))
    
    
    #start/help command/button
@bot.message_handler(commands=['help'])
def start2(message):
    start(message)
    
    
bot.infinity_polling()
