#!/usr/bin/env python
import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7049056882:AAGwFBH9Yrv9Ruy81IrdQQmyMeGWJd-0dBw')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hello')
    
    conn = sqlite3.connect('database/list.db')
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, chat_id blob, word blob, username blob)')
    conn.commit()
    
    cur.close()
    conn.close()
    
    #button under photo
@bot.message_handler(commands=['home'])
def home(message):
    # lol = bot.send_photo(message.chat.id, photo=open('/Users/bohdanprokopchuk/Desktop/dictionary_bot/home_photo.png', 'rb'))
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('➕ Add word', callback_data='add')
    btn2 = types.InlineKeyboardButton('➖ Remove word', callback_data='remove')
    btn3 = types.InlineKeyboardButton('🔎 Find word', callback_data='find')
    btn4 = types.InlineKeyboardButton('📑 Show all words', callback_data='show')
    btn5 = types.InlineKeyboardButton('❌ Clear dictionary', callback_data='clear')
    btn6 = types.InlineKeyboardButton('📌 Pin', callback_data='pin')
    btn7 = types.InlineKeyboardButton('Close', callback_data='close')
    murkup.row(btn1,btn2)
    murkup.row(btn3)
    murkup.row(btn4, btn5)
    murkup.row(btn6, btn7)
    bot.send_photo(message.chat.id, photo=open('/Users/bohdanprokopchuk/Desktop/dictionary_bot/home_photo.png', 'rb'), reply_markup=murkup)



    #add word to list
def click_add(message):
    
    word = message.text.lower()

    
    if len(word) >= 1: 
    
        conn = sqlite3.connect('list.db')
        c = conn.cursor()
        
        bot.send_message(message.chat.id, text=word)

        chat_id = message.chat.id
        print('chatid:', chat_id)
        chat_id = str(chat_id)
        username = message.from_user.username
        print('username:', username)
        c.execute('INSERT INTO users (chat_id, word, username) VALUES ("%s", "%s", "%s")' % (chat_id, word, username))
        
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        for i in users:
            print(f'{i[1]} = {i[2]}')
        conn.commit()
        c.close()
        conn.close()
        
        bot.send_message(message.chat.id, text='Successfully added✅')
    else:
        
        bot.send_message(message.chat.id, text='The word is already in the dictionary❌')
    # if word == 'NOT IN DATABASE':
    #     bot.send_message(message.chat.id, text='Successfully added✅')
    # else:
    #     bot.send_message(message.chat.id, text='The word is already in the dictionary❌')
        
        
    #remove word from list
def click_remove(message):
    if message.text == '':
        bot.send_message(message.chat.id, text='Successfully removed✅')
    else:
        bot.send_message(message.chat.id, text="This word isn't in the dictionary❗️")

    #show all elements in list
def click_show(message):
    
    conn = sqlite3.connect('list.db')
    c = conn.cursor()
    
    chat_id = message.chat.id
    chat_id = chat_id
    print(f'chatid:' , chat_id)
    
    c.execute('SELECT * FROM users WHERE chat_id=("%s")' % (chat_id))
    users = c.fetchall()
    
    if len(users) > 0:
        items = ''
        for i in users:
            items += i[2]
            print(i[2])
            print(len(i[2]))
            items +='\n'
            
        bot.send_message(message.chat.id, text=items)        
    else:
        bot.send_message(message.chat.id, text='Your dictionary is empty😑')    
    
    conn.commit()
    
    c.close()
    conn.close()
    
    #button click
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'add':
        bot.register_next_step_handler(callback.message, click_add)
        bot.register_next_step_handler(callback.message, click_add2)
    if callback.data == 'remove':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'find':
        pass
    if callback.data == 'show':
        click_show(callback.message)
    if callback.data == 'clear':
        pass
    if callback.data == 'pin':
        bot.pin_chat_message(callback.message.chat.id, callback.message.message_id, disable_notification=True)
    if callback.data == 'close':
        bot.delete_message(callback.message.chat.id, callback.message.message_id) 
        
    #messages or actions after commads
@bot.message_handler(commands=['add'])
def start(message):
    pass


@bot.message_handler(commands=['remove'])
def start(message):
    pass
    
@bot.message_handler(commands=['show'])
def start(message):
    bot.send_message(message.chat.id, 'hello')
    
@bot.message_handler(commands=['clear'])
def start(message):
    bot.send_message(message.chat.id, 'hello')

    #list of commands
@bot.message_handler(commands=['help'])
def hepl(message):
    bot.send_message(message.chat.id, '<b><u>📖DICTIONARY📖</u></b> \n'
                                    '\n <em>/home: Open the main menu</em>\n'
                                    '<em>/add: Add a specific word to the dictionary</em>\n'
                                    '<em>/remove: Delete a specific word from the dictionary</em>\n'
                                    '<em>/find: Find a specific word in the dictionary</em>\n'
                                    '<em>/show: Show all words in the dictionary</em>\n'
                                    '<em>/clear: Delete all words from the dictionary</em>\n' ,parse_mode='html')
    
bot.infinity_polling()