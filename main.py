
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
    
    cur.execute('CREATE TABLE IF NOT EXISTS "users" ("id" INTEGER NOT NULL, "chat_id" blob, "word" blob, "translate" blob, watchlist INTEGER,"username" blob, PRIMARY KEY("id" AUTOINCREMENT));')
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
    global word
    word = message.text.lower()
    print("word", word)    
    
def click_add2(message):
    
    print('word2' ,word)
    
    translate = message.text.lower()
    
    print('trans', translate)

    if len(word) >= 1: 
        
        conn = sqlite3.connect('database/list.db')
        c = conn.cursor()
        
        bot.send_message(message.chat.id, text=word)

        chat_id = message.chat.id
        print('chatid:', chat_id)
        chat_id = str(chat_id)
        username = message.from_user.username
        print('username:', username)
        
        c.execute('INSERT INTO users (chat_id, word, translate, watchlist, username) VALUES ("%s", "%s", "%s", "%d", "%s")' % (chat_id, word, translate, 0, username))
        
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        for i in users:
            print(f'{i[2]} = {i[3]}')
        conn.commit()
        c.close()
        conn.close()
        
        bot.send_message(message.chat.id, text='Successfully added✅')
    else:
        bot.send_message(message.chat.id, text='The word is already in the dictionary❌')
        
    #remove word from list
def click_remove(message):
    
    word = message.text.lower()
    
    conn = sqlite3.connect('database/list.db')
    c = conn.cursor()
    
    c.execute(f'SELECT * FROM users WHERE word LIKE "{word}" OR translate LIKE "{word}"')
    temp = c.fetchall()
    
    if len(temp) > 0:
        c.execute(f'DELETE FROM users WHERE WORD = "{word}" OR TRANSLATE = "{word}"')
        bot.send_message(message.chat.id, text='Successfully removed✅')
    else:
        bot.send_message(message.chat.id, text="Your dictionary is empty or this word is not in your dictionary❗️")
        
    conn.commit()
    c.close()
    conn.close()    
    
    #show all elements in list
def click_show(message):
    
    conn = sqlite3.connect('database/list.db')
    c = conn.cursor()
    
    chat_id = message.chat.id
    chat_id = chat_id
    
    c.execute('SELECT * FROM users WHERE chat_id=("%s")' % (chat_id))
    users = c.fetchall()
    
    if len(users) > 0:
        items = ''
        for i in users:
            print(i)
            items += f'{i[2]} - {i[3]}\n' 
            
        bot.send_message(message.chat.id, text=items)        
    else:
        bot.send_message(message.chat.id, text='Your dictionary is empty😑')    
    
    conn.commit()
    
    c.close()
    conn.close()
    
    #clear all items in list
def click_clear(message):
    
    conn = sqlite3.connect('database/list.db')
    c = conn.cursor()
    
    chat_id = message.chat.id
    chat_id = chat_id

    if c.execute('DELETE FROM users WHERE chat_id=("%s")' % (chat_id)).rowcount > 0:
        conn.commit()
        bot.send_message(message.chat.id, text='Successfully cleared✅')
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
        bot.register_next_step_handler(callback.message, click_remove)
    if callback.data == 'find':
        pass
    if callback.data == 'show':
        click_show(callback.message)
    if callback.data == 'clear':
        click_clear(callback.message)
    if callback.data == 'pin':
        bot.pin_chat_message(callback.message.chat.id, callback.message.message_id, disable_notification=True)
    if callback.data == 'close':
        bot.delete_message(callback.message.chat.id, callback.message.message_id) 
        
    #messages or actions after commads
@bot.message_handler(commands=['add'])
def add(message):
    bot.register_next_step_handler(message, click_add)
    
@bot.message_handler(commands=['remove'])
def remove(message):
    bot.register_next_step_handler(message, click_remove)
    
@bot.message_handler(commands=['show'])
def show(message):
    click_show(message)
    
@bot.message_handler(commands=['clear'])
def clear(message):
    click_clear(message)

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
