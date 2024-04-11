import sqlite3
from telebot import types

#add word and it's translation to list.db
def click_add(bot, message):
    user_input = message.text.strip().lower()

    # Function to handle the next step after prompting for translation
    def handle_translation_step(message):
        translation = message.text.strip()

        if translation:
            word = user_input
            word = word.strip()

            conn = sqlite3.connect('database/list.db')
            c = conn.cursor()

            chat_id = message.chat.id
            username = message.from_user.username

            c.execute('INSERT INTO users (chat_id, word, translate, watchlist, username) VALUES (?, ?, ?, ?, ?)',
                      (chat_id, word, translation, 0, username))
            conn.commit()
            bot.send_message(message.chat.id, text='Successfully added✅')

            c.close()
            conn.close()
        else:
            bot.send_message(message.chat.id, text="Invalid input. Please provide the translation for the word.")

    if user_input:
        # Prompt the user to enter the translation directly
        bot.send_message(message.chat.id, text="Please enter the translation for the word:")
        bot.register_next_step_handler(message, handle_translation_step)
    else:
        bot.send_message(message.chat.id, text="Invalid input format. Please provide the word you want to add.")

        
        
    #clear all user's items in db
def click_clear(bot, message):
    
    answer = message.text.strip().lower()
    
    if answer == 'y':
        conn = sqlite3.connect('database/list.db')
        c = conn.cursor()
            
        chat_id = message.chat.id

        if c.execute('DELETE FROM users WHERE chat_id = ?', (chat_id,)).rowcount > 0:
            conn.commit()
            bot.send_message(message.chat.id, text='Successfully cleared✅')
        else:
            bot.send_message(message.chat.id, text='Your dictionary is empty😑')
                    
        conn.commit()
                
        c.close()
        conn.close()
    else:
        bot.send_message(message.chat.id, text='DALBAYOB KRIVORUKIY, PO KNOPKACH POPADAY' )
        bot.delete_message(message.chat.id, message.message_id) 
        bot.delete_message(message.chat.id, message.message_id -1) 
        
        
    #remove word and it's translation in db
def click_remove(bot, message):
    
    word = message.text.strip().lower()
    
    conn = sqlite3.connect('database/list.db')
    c = conn.cursor()
    
    chat_id = message.chat.id
    
    print(chat_id)
    
    c.execute('SELECT * FROM users WHERE chat_id = ? AND (word = ? OR translate = ?)', (chat_id, word, word))
    temp = c.fetchall()
    
    if len(temp) > 0:
        c.execute('DELETE FROM users WHERE chat_id = ? AND (word = ? OR translate = ?)', (chat_id, word, word))
        bot.send_message(message.chat.id, text='Successfully removed✅')
    else:
        bot.send_message(message.chat.id, text="Your dictionary is empty or this word is not in your dictionary❗️")
        
    conn.commit()
    c.close()
    conn.close()  


    #print user's words and translations
def click_show(bot, message):
    
    conn = sqlite3.connect('database/list.db')
    c = conn.cursor()
    
    chat_id = message.chat.id
    
    c.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id, ))
    users = c.fetchall()
    
    j = 1
    if len(users) > 0:
        items = ''
        for i in users:
            items += f'{j}. {i[2]} - {i[3]}\n'
            j+=1 
            
        bot.send_message(message.chat.id, text='<b><u>Your dictionary:</u></b>\n\n'+ items, parse_mode='html')        
    else:
        bot.send_message(message.chat.id, text='Your dictionary is empty😑')    
    
    conn.commit()
    
    c.close()
    conn.close()
    

    #find word or translation in db
def click_find(bot, message):
    
    word = message.text.strip().lower()
    
    chat_id = message.chat.id
            
    if len(word) >= 1:
        conn = sqlite3.connect('database/list.db')
        c = conn.cursor()
    
        c.execute('SELECT * FROM users WHERE chat_id = ? AND (translate = ? OR word = ?)', (chat_id, word, word))
        users = c.fetchall()
        
        if len(users) <= 0:
            bot.send_message(message.chat.id, text="This word is not in your dictionary")
        else:
            items = ''
            for i in users:
                items += f'{i[2]} - {i[3]}\n'
                
            bot.send_message(message.chat.id, text=items)       
            
        conn.commit()
    
        c.close()
        conn.close()
        
    else:
        bot.send_message(message.chat.id, text="Invalid input. Please provide both the word and it's translation separated by a hyphen (-).")
        
        #add word to favourite
def click_add_favourite(bot, message):
    chat_id = message.chat.id

    # Function to handle the next step after prompting for translation
    def handle_translation_step(message, word):
        translation = message.text.strip()

        if translation:
            conn = sqlite3.connect('database/list.db')
            c = conn.cursor()

            c.execute('INSERT INTO users (chat_id, word, translate, watchlist) VALUES (?, ?, ?, ?)', (chat_id, word, translation, 1))
            conn.commit()
            bot.send_message(message.chat.id, text=f'The word "{word}" and its translation have been added to your dictionary and favorites✅')

            c.close()
            conn.close()
        else:
            bot.send_message(message.chat.id, text="Invalid input. Please provide the translation for the word.")

    user_input = message.text.strip().lower()

    if len(user_input) >= 1:
        word = user_input.strip().lower()

        if word:
            conn = sqlite3.connect('database/list.db')
            c = conn.cursor()

            c.execute('SELECT * FROM users WHERE chat_id = ? AND (word = ? OR translate = ?)', (chat_id, word, word))
            existing_entry = c.fetchone()

            if existing_entry:
                watchlist = existing_entry[4]

                if watchlist == 0:
                    c.execute('UPDATE users SET watchlist = 1 WHERE chat_id = ? AND (word = ? OR translate = ?)', (chat_id, word, word))
                    conn.commit()
                    bot.send_message(message.chat.id, text=f'The word "{word}" has been added to your favorites✅')
                else:
                    bot.send_message(message.chat.id, text=f'The word "{word}" is already in your dictionary.')
            else:
                # Prompt the user to enter the translation directly
                bot.send_message(message.chat.id, text=f"The word '{word}' isn't in your dictionary. Please enter its translation:")
                bot.register_next_step_handler(message, lambda msg: handle_translation_step(msg, word))

            c.close()
            conn.close()
        else:
            bot.send_message(message.chat.id, text="Invalid input. Please provide the word you want to add.")
    else:
        bot.send_message(message.chat.id, text="Invalid input format. Please provide the word you want to add.")


    #clear all items from favourite
def click_clear_favourite(bot, message):
    
    answer = message.text.strip().lower()
    chat_id = message.chat.id
    count = 0
    
    if answer == 'y':
        conn = sqlite3.connect('database/list.db')
        c = conn.cursor()

        c.execute('UPDATE users SET watchlist = 0 WHERE chat_id = ?', (chat_id,))
        conn.commit()

        count = c.rowcount
        c.close()
        conn.close()

        if count > 0:
            bot.send_message(message.chat.id, text="Your watchlist has been cleared successfully✅")
        else:
            bot.send_message(message.chat.id, text="Your watchlist is already empty.")
    else:
        bot.send_message(message.chat.id, text='DALBAYOB KRIVORUKIY, PO KNOPKACH POPADAY')
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)



    #remove word from favourite
def click_remove_favourite(bot, message):
    
    user_input = message.text.strip().lower()
    chat_id = message.chat.id
    
    if len(user_input) >= 1:
        word = user_input.strip() 
        
        if word:
            conn = sqlite3.connect('database/list.db')
            c = conn.cursor()

            c.execute('SELECT * FROM users WHERE chat_id = ? AND (word = ? OR translate = ?)', (chat_id, word, word))
            existing_entry = c.fetchone()

            if existing_entry:
                watchlist = existing_entry[4]
                
                if watchlist == 1:
                    c.execute('UPDATE users SET watchlist = 0 WHERE chat_id = ? AND (word = ? OR translate = ?)', (chat_id ,word, word))
                    conn.commit()
                    bot.send_message(message.chat.id, text=f'The word "{word}" has been removed from your favorites❌')
                else:
                    bot.send_message(message.chat.id, text=f"The word '{word}' isn't in your favorites.")
            else:
                bot.send_message(message.chat.id, text=f"The word '{word}' isn't in the list.")

            c.close()
            conn.close()
        else:
            bot.send_message(message.chat.id, text="Invalid input. Please provide the word you wanna remove.")
    else:
        bot.send_message(message.chat.id, text="Invalid input format. Please provide the word you wanna remove.")

    #print all elements in watchlist
def click_show_favourite(bot, message):
    
    conn = sqlite3.connect('database/list.db')
    c = conn.cursor()
    
    chat_id = message.chat.id
    
    c.execute('SELECT * FROM users WHERE chat_id = ? AND watchlist = 1', (chat_id,))
    favourites = c.fetchall()
    
    if favourites:
        items = ''
        for entry in favourites:
            items += f'{entry[2]} - {entry[3]}\n\n'
        bot.send_message(message.chat.id, text="<b><u>The words you're learning now:</u></b>\n\n" + items, parse_mode='html')
    else:
        bot.send_message(message.chat.id, text='Your favorites list is empty')

    conn.commit()
    c.close()
    conn.close()
