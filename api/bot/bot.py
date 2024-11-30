import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, URLInputFile, FSInputFile
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from aiogram.types import Update
import asyncio
from dotenv import load_dotenv
from api.services.appwriteservice import fetchurl

load_dotenv()
TOKEN = os.getenv('TOKEN')
# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()
base_dir = './store/'
previousclass = ''
classdata = {}
# chporg = ChapterOrganizer()

def generate_keyboard(keyboard_type: str, categorylen = 0):
    if keyboard_type == "subject":
        # Generate keyboard for selecting 9th or 10th grade
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="9th Grade 📚", callback_data="subject_9th"),
                    InlineKeyboardButton(text="10th Grade 📖", callback_data="subject_10th")
                ]
            ]
        )

    elif keyboard_type == "chapter":
        chapters = [str(i) for i in range(1, categorylen+1)]  # Chapters 1 to 14
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                # List of rows (each row is a list of buttons)
                [InlineKeyboardButton(text=f"Chapter {chapters[i]} ", callback_data=f"chapter_{chapters[i]}")
                 for i in range(j, min(j + 3, len(chapters)))]  # Create a row of 3 buttons
                for j in range(0, len(chapters), 3)  # Iterate over the chapters in steps of 3
            ]
        )
        keyboard.inline_keyboard.insert(0, [InlineKeyboardButton(text="All Chapters 📚", callback_data="all_chapter")])

        return keyboard

def genrate_rkm(options: list):
    if len(options) % 2 == 1:
        options.append("Cancel ❌")
    btn = [[KeyboardButton(text=f"{str(options[i])} "),
            KeyboardButton(text=f"{str(options[i + 1])} ")
            ]
           for i in range(0, len(options), 2)]
    return ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True, input_field_placeholder="Select Category : 👇👇👇")


user_state = {}

@dp.message(Command('start'))
async def startbot(msg: types.Message):
    await msg.answer("Welcome to *SmartBhaiya* 🤖💡! \n\nYour study buddy who's smarter than your Wi-Fi🛜! or Your crush 💖😏 hm...\nReady to level up your study game? Let's do this! 💥\nSelect the category you want to explore with SmartBhaiya (yes, I know you need it! Dont be Shy ahh😜): ❓🔍😊",parse_mode='markdown',
                      reply_markup=genrate_rkm(['Notes 📝', 'Book 📖', 'Solution 📘', 'MarksWise Question 🎯', 'Testpapers 📑']))

# @dp.message(Command('start'))
# async def startbot(msg: types.Message):
#     await msg.answer("Welcome to the StudyBot! 📚\nSelect the category you want to explore: ❓🔍😊",
#                       reply_markup=genrate_rkm(['Notes 📝', 'Book 📖', 'Solution 📘', 'MarksWise Question 🎯', 'Testpapers 📑']))

# Command handler for /notes
@dp.message(Command('notes'))
async def cmd_notes(message: types.Message):
    user_state[message.from_user.id] = {}
    await chapterHandler(message, 'notes')

# Command handler for /book
@dp.message(Command('book'))
async def cmd_book(message: types.Message):
    user_state[message.from_user.id] = {}
    await chapterHandler(message, 'book')

@dp.message(Command('solution'))
async def cmd_solution(message: types.Message):
    user_state[message.from_user.id] = {}
    await chapterHandler(message, 'solution')

@dp.message(Command('markswise'))
async def cmd_markwise(message: types.Message):
    user_state[message.from_user.id] = {}
    await chapterHandler(message, 'markswise')

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    help_text = ('''
        Welcome to *SmartBhaiya* 🤖💡! Here's how you can use this bot to get your study materials:\n
        1. **/notes**: Get the best study notes for *Science, Maths, Accountancy, Economics* (6th-12th). 📚
        2. **/book**: Access the class textbooks 📖.
        3. **/solution**: Get solutions for book exercises. 📘
        4. **/markswise**: Explore important questions based on marks distribution. 🎯
        
        *How to use this bot:*  
        - Start the bot with **/start**.  
        - Use the inline keyboard that will appear after choosing the **subject** (Science, Maths, etc.).  
        - Select options like **Notes**, **Books**, **Solutions**, and **Markswise Questions** via the buttons.  
        - Use the **/help** command at any time for guidance! 💡'''
    )
    await message.answer(help_text, parse_mode="Markdown")

async def chapterHandler(msg: types.Message, category: str):
    user_state[msg.from_user.id]['category'] = category.lower().split(' ')[0]
    # print(user_state.items())
    await msg.answer(f"Select your {category.capitalize()} 📘 for which class you want? ❓😊 👇👇👇", reply_markup=generate_keyboard("subject"))

@dp.message(lambda msg: msg.text in ['Notes 📝', 'Book 📖', 'Solution 📘', 'MarksWise Question 🎯', 'Testpapers 📑'])
async def category_handler(msg: types.Message):
    user_state[msg.from_user.id] = {}
    await chapterHandler(msg, msg.text)

# Callback query handler for selecting the grade (9th or 10th)
@dp.callback_query(lambda c: c.data.startswith('subject_'))
async def process_subject_selection(callback_query: types.CallbackQuery):
    subject_code = callback_query.data.split("_")[1]
    global previousclass
    global classdata
   
    # fbasedir = base_dir+subject_code.split('t')[0] + 'science'
    if previousclass == '':
        previousclass = subject_code
        classdata = await fetchurl(class_name=subject_code)
        print("it fetched")
        # print(previousclass)
    elif previousclass != subject_code:
        classdata = await fetchurl(class_name=subject_code)
        print("it fetced again")
        previousclass = subject_code
    

    user_state[callback_query.from_user.id]['class'] = subject_code

    await asyncio.sleep(0.5)
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=f"Now, select a chapter for {subject_code} Grade 📘:👇👇👇 "
    )

    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=generate_keyboard('chapter', categorylen = len(classdata)),
    )


# Callback query handler for selecting a chapter (1-14)
@dp.callback_query(lambda c: c.data.startswith('chapter_'))
async def process_chapter_selection(callback_query: types.CallbackQuery):
    chapter_no = callback_query.data.split("_")[1]
    user_state[callback_query.from_user.id]['chapter'] = chapter_no
    category = user_state[callback_query.from_user.id]['category']
    # classn = user_state[callback_query.from_user.id]['class']
    # print(classn)
    print(category)
    await bot.answer_callback_query(callback_query.id)
    # data = chporg.query(chapter_no=int(chapter_no), category=category.split(' ')[0])
    # data = fetchurl(class_name=classn,query =category,chpno=int(chapter_no))[0]
    # print(data)
    data = classdata[int(chapter_no)-1]
    # pdf = FSInputFile(
    #     data['filepath'], filename=f"{data['name']}.pdf",
    # )
    pdf = URLInputFile(url=data[category],filename=f"{data['name']}.pdf")
    # Send the selected chapter number to the user
    await bot.send_message(callback_query.from_user.id, f"Sending {str(category).capitalize()} of  {data['name']} 📖....")
    await bot.send_document(document=pdf, chat_id=callback_query.from_user.id)


@dp.callback_query(lambda c: c.data.startswith('all_chapter'))
async def process_all_chapters(callback_query: types.CallbackQuery):
    # classnm = user_state[callback_query.from_user.id]['class']
    categ = user_state[callback_query.from_user.id]['category']
    # datas = chporg.query(category=categ)
    # datas = classdata
    await bot.send_message(callback_query.from_user.id, f"Sending {str(categ).capitalize()} of All Chapters 📚... Please wait ⏳...")

    for data in classdata:
        pdf = URLInputFile(
            url=data[str(categ)],filename=f"{data['name']}.pdf"
        )
        await bot.send_document(document=pdf, chat_id=callback_query.from_user.id)


async def on_webhook(request):
    try:
        update = await request.json()  # Get the incoming update
        update_obj = Update(**update)  # Convert to aiogram Update object
        await dp.process_update(update_obj)  # Process the update
        return web.Response(status=200)  # Return a successful response to Telegram
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return web.Response(status=500)  
    # try:
    #     update = request.get_json()  # Get the update from the incoming request
    #     update = Update(**update)  # Convert the dictionary to the aiogram Update object
    #     await dp.process_updates([update])  # Process the update
    #     return '', 200  # Return a success status to Telegram
    # except Exception as e:
    #     logging.error(f"Error processing webhook: {e}")
    #     return '', 500 # Return a 200 status code

async def set_webhook():

    WEBHOOK_URL = 'https://smartbhaiya-telegrambot.onrender.com/webhook'  # Replace with your actual Render URL
    webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = await bot.get_webhook_info()
    if not response.url == WEBHOOK_URL:  # If webhook is not set
        await bot.set_webhook(url=WEBHOOK_URL)
        logging.info(f"Webhook set to {WEBHOOK_URL}")
    else:
        logging.info(f"Webhook is already set to: {WEBHOOK_URL}")

async def delete_webhook():
    try:
        await bot.delete_webhook()  # This removes any existing webhook.
        logging.info("Webhook deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting webhook: {e}")

async def on_startup(bot: Bot) -> None:
    # Delete any existing webhook before setting a new one
    WEBHOOK_URL = 'https://smartbhaiya-telegrambot.onrender.com/webhook'
    await delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook set successfully.")

def start_webhook_server():
    app = web.Application()
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path='/webhook')
    
    # Setup webhook handler and run the server
    web.run_app(app, host="0.0.0.0", port=8080)

async def main():
    # await dp.stop_polling(bot)
    # stop()
    # await set_webhook()
    # await delete_webhook()
    # await set_webhook()
    # await on_startup(bot)
    logging.info('Bot is started 🚀')
    await dp.start_polling(bot)

# main()
# async def stop():
#     await dp.stop_polling()
#     await dp.shutdown()
if __name__ == '__main__':
    print('Bot is started 🚀')
    main()
    asyncio.run(main())