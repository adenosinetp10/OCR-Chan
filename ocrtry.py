#This is an experimental OCR bot for telegram using the python-telegram-bot Wrapper and an Open Source API for OCR found on the Internet
#Importing every shit that gonna be used..
from telegram.ext import CommandHandler,Updater,MessageHandler,Filters
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import telegram
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException
from traceback import print_exc
import os
import json
#Getting API AUTH KEY FOR OCR API CloudMersive(Costs a lot of money ;(  )
CLOUDMERSIVE_API_KEY =os.environ.get("CLOUDMERSIVE_API_KEY","")

#Defining /start command 
def start(update,context):
    fname = update.message.from_user.first_name
    update.message.reply_text("Hi %s, if you are stuck or don't know what to do,\nTry doing /help to look out for all available commands."%(fname))

#Defining /help command 
def help(update,context):
    update.message.reply_text("Upload a photo which has clear and distinguishable english words.\nThen after confirmation of the image, OCR-chan will automatically\nsend you your text from the picture\n/start   -   Start OCR-chan!\n/help    -   Look for help!\n/userinfo    -   See your Info\n/about   -   About OCR-chan\n/chatid    -   Display the Chat ID")

#Defining /chatid command 
def chatid(update,context):
    chatid = update.message.chat_id
    update.message.reply_text("<b>Chat ID :</b> "'<pre>'+str(chatid)+'</pre>',parse_mode='HTML')

#Defining ECHO command incase the person starts to have a convo with the bot like a TRUE SIMP
def nanikore(update,context):
    nanikore = update.message.text
    nani = "%s ??? \nNani Kore ? "%(nanikore)
    update.message.reply_text(nani)
    update.message.reply_text("😕")

 #Defining /userinfo command for giving USERS their Telegram account's INFO   
def userinfo(update, context):
    fname = update.message.from_user.first_name
    lname = update.message.from_user.last_name
    uniqid = update.message.from_user.id
    usrname = update.message.from_user.username
    langcode = update.message.from_user.language_code
    dt = update.message.date
    update.message.reply_text('<b>Unique ID/Chat ID :</b> ''<pre>'+str(uniqid)+'</pre>'
                                '\n<b>First Name :</b> ''<pre>'+str(fname)+'</pre>'
                                '\n<b>Last Name :</b> ''<pre>'+str(lname)+'</pre>'
                                '\n<b>User Name :</b>' '<pre>@</pre>''<pre>'+str(usrname)+'</pre>'
                                '\n<b>Language Code :</b> ''<pre>'+str(langcode)+'</pre>'
                                '\n<b>Date & Time :</b> ''<pre>'+str(dt)+'</pre>',parse_mode='HTML')

#Defining /about command to give USERS some info about me, but GUYS donate me I'm a student and I'm broke AF    
def about(update, context):
    keyboard = [[InlineKeyboardButton('GitHub',url ="https://github.com/adenosinetp10"),InlineKeyboardButton('Paypal',url='https://paypal.me/adenosinetp10')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('<b>Developer :</b> @iLEWDloli\n'
                               'Coded in Telegram using <b>python-telegram-bot</b> Wrapper\n'
                               'Hosted with ❤ in Heroku(Free account)\n'
                               'Wanna buy me a CUP of COFFEE?\nDonate!',reply_markup = reply_markup,parse_mode='HTML')
    

#Defining MessangleHandler that will do this function when a Image is Sent, THIS IS THE MAIN FUCNTION FOR THE OCR THINGY!!
def receive(update,context):
    filename = "photo.jpg"
    fileid = update.message.photo[-1].file_id
    received = context.bot.get_file(fileid)
    received.download(filename)
    update.message.reply_text("Image received!\n🥰\n")
    api_instance =cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY
    try:
        api_response = api_instance.image_ocr_post(filename)
        sucs_percent = api_response.mean_confidence_level
        result = api_response.text_result
        update.message.reply_text("<b>Success Percentage :</b> "+str(sucs_percent*100)+"<b>%\nThe text from the Image :</b> \n"'<pre>'+str(result)+'</pre>', parse_mode = 'HTML')
    except Exception as e:
        print_exc
        update.message.reply_text("Gomen! Error Occured.\n<b>Error Details :</b> "+str(e),parse_mode='HTML')

#AS USUAL THE MAIN FUNCTION MEHHHHHH
def main():
    bot_token=os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('chatid',chatid))
    dp.add_handler(CommandHandler('userinfo',userinfo))
    dp.add_handler(CommandHandler('about',about))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, nanikore))
    dp.add_handler(MessageHandler(Filters.photo, receive))
    updater.start_polling()
    updater.idle()




if __name__ == "__main__":
    main()
