import logging
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, URLInputFile, FSInputFile
from aiogram.filters import Command
import asyncio
from Organizer import ChapterOrganizer
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()
base_dir = '../store/'
# base_dir = sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'store'))
previousclass = ''
chporg = ChapterOrganizer()

def generate_keyboard(keyboard_type: str, category=None):
    
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
        categorylen = chporg.get_len(category=category)
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
    fbasedir = base_dir+subject_code.split('t')[0] + 'science'
    if previousclass == '':
        previousclass = subject_code
        # print(previousclass)
    elif previousclass != subject_code:
        chporg.run(n=16, base_dir=fbasedir)
        previousclass = subject_code
        # print(previousclass)

    category = user_state[callback_query.from_user.id]['category']

    if chporg.chpterwised == {}:
        chporg.run(n=16, base_dir=fbasedir)

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
        reply_markup=generate_keyboard('chapter', category=category),
    )


# Callback query handler for selecting a chapter (1-14)
@dp.callback_query(lambda c: c.data.startswith('chapter_'))
async def process_chapter_selection(callback_query: types.CallbackQuery):
    chapter_no = callback_query.data.split("_")[1]
    user_state[callback_query.from_user.id]['chapter'] = chapter_no
    category = user_state[callback_query.from_user.id]['category']
    # print(category)
    await bot.answer_callback_query(callback_query.id)
    data = chporg.query(chapter_no=int(chapter_no), category=category.split(' ')[0])

    pdf = FSInputFile(
        data['filepath'], filename=f"{data['name']}.pdf",
    )

    # Send the selected chapter number to the user
    await bot.send_message(callback_query.from_user.id, f"Sending {data['name']} 📖....")
    await bot.send_document(document=pdf, chat_id=callback_query.from_user.id)


@dp.callback_query(lambda c: c.data.startswith('all_chapter'))
async def process_all_chapters(callback_query: types.CallbackQuery):
    categ = user_state[callback_query.from_user.id]['category']
    datas = chporg.query(category=categ)
    await bot.send_message(callback_query.from_user.id, "Sending All Chapters 📚... Please wait ⏳...")

    for k, data in datas.items():
        pdf = FSInputFile(
            data['filepath'], filename=f"{data['name']}.pdf",
        )
        await bot.send_document(document=pdf, chat_id=callback_query.from_user.id)


async def main():
    # await dp.stop_polling(bot)
    
    await dp.start_polling(bot)

async def stop():
    await dp.stop_polling()
    await dp.shutdown()
# if __name__ == '__main__':
#     print('Bot is started 🚀')
#     main()
    # asyncio.run(main())