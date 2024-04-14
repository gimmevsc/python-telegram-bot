from telebot import types

def start(bot, message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Add word')
    btn2 = types.KeyboardButton('Remove word')
    btn3 = types.KeyboardButton('🔎 Find word')
    btn4 = types.KeyboardButton('📑 Show all words')
    btn5 = types.KeyboardButton('❌Clear dictionary')
    btn6 = types.KeyboardButton('Homepage')
    btn8 = types.KeyboardButton('Add to ☆')
    btn9 = types.KeyboardButton('Show ☆')
    btn10 = types.KeyboardButton('Remove fr ☆')
    btn11 = types.KeyboardButton('Help')
    btn12 = types.KeyboardButton('Clear ☆')
    murkup.row(btn1, btn2)
    murkup.row(btn3, btn8, btn5)
    murkup.row(btn10, btn12, btn9)
    murkup.row(btn4, btn6, btn11)
    
    bot.send_message(message.chat.id, '<b><u>📖DICTIONARY📖</u></b> \n'
                                    "\n<b>Hi, it's Dictionary</b>\n"
                                    "<b>\n📝INSTRUCTION📝:</b>\n"
                                    "\n ➡️<b>To add a new word to the dictionary, click the 'ADD WORD' button or type the <em>'/add'</em> command and enter the new word and translation in the following form: 'word - translation'</b>\n"
                                    " ➡️<b>To delete a word from the dictionary, click the 'REMOVE WORD word' button or enter the <em>'/remove'</em> command and type the word or its translation as you want to delete it</b>\n"
                                    " ➡️<b>Press 'FIND WORD' or type <em>'/find'</em> and enter the word or its translation to get it in the dictionary</b>\n"
                                    " ➡️<b>Press 'SHOW ALL WORDS' or type <em>'/show'</em> to get a list of all words in the dictionary</b>\n"
                                    " ➡️<b>Press ‘CLEAR DICTIONARY' or type <em>’/clear'</em> to delete all words from the dictionary</b>\n"
                                    " ➡️<b>By analogy, you can perform the same actions and commands on your favorites list</b>", reply_markup=murkup, parse_mode='html')



def home(bot, message):
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('➕ Add word', callback_data='add')
    btn2 = types.InlineKeyboardButton('➖ Remove word', callback_data='remove')
    btn3 = types.InlineKeyboardButton('🔎 Find word', callback_data='find')
    btn4 = types.InlineKeyboardButton('📑 Show all words', callback_data='show')
    btn5 = types.InlineKeyboardButton('❌Clear dictionary', callback_data='clear')
    btn6 = types.InlineKeyboardButton('📌 Pin', callback_data='pin')
    btn7 = types.InlineKeyboardButton('Close', callback_data='close')
    btn8 = types.InlineKeyboardButton('Help', callback_data='help')
    btn9 = types.InlineKeyboardButton('Add to ☆ ', callback_data='add_favourite')
    btn10 = types.InlineKeyboardButton('Show ☆', callback_data='show_favourite')
    btn11 = types.InlineKeyboardButton('Remove ☆', callback_data='remove_favourite')
    btn12 = types.InlineKeyboardButton('Clear ☆', callback_data='clear_favourite')
    murkup.row(btn1,btn2)
    murkup.row(btn3, btn4)
    murkup.row(btn10, btn11, btn9)
    murkup.row(btn12, btn5)
    murkup.row(btn6, btn8, btn7)
    bot.send_photo(message.chat.id, photo=open('img/home_photo.png', 'rb'), reply_markup=murkup)

def helpp(bot, message):
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('GitHub', url='https://github.com/gimmevsc')
    btn2 = types.InlineKeyboardButton('Developer', url='tg://resolve?domain=godgivenby')
    murkup.row(btn1,btn2)
    bot.send_message(message.chat.id, text='Bot information', reply_markup=murkup)