import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup,URLInputFile
from aiogram.filters import Command
import asyncio

# TOKEN = '5421069203:AAFfrwK4v58x-7N4cmhcGa9i6_wLoYUnz8M'
TOKEN = '5421069203:AAFfrwK4v58x-7N4cmhcGa9i6_wLoYUnz8M'

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()



def generate_keyboard(keyboard_type: str):
    if keyboard_type == "subject":
        # Generate keyboard for selecting 9th or 10th grade
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="9th Grade", callback_data="subject_9th"),
                    InlineKeyboardButton(text="10th Grade", callback_data="subject_10th")
                ]
            ]
        )
    
    elif keyboard_type == "chapter":
        chapters = [str(i) for i in range(1, 15)]  # Chapters 1 to 14
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[ 
             # List of rows (each row is a list of buttons)
            [InlineKeyboardButton(text=f"Chapter :{chapters[i]}:", callback_data=f"chapter_{chapters[i]}")
             for i in range(j, min(j + 3, len(chapters)))]  # Create a row of 3 buttons
            for j in range(0, len(chapters), 3)  # Iterate over the chapters in steps of 3,

        ]
    )
    keyboard.inline_keyboard.insert( 0,[InlineKeyboardButton(text="All Chapters", callback_data="chapter_all")])
    
    return keyboard

def genrate_rkm(options:list):
    if len(options)%2==1:
         options.append("")
    btn = [[KeyboardButton(text=f"{str(options[i]).capitalize()}"),
            KeyboardButton(text=f"{str(options[i+1]).capitalize()}")
            ]
            for i in range(0, len(options),2)]
    return ReplyKeyboardMarkup(keyboard=btn,resize_keyboard=True,input_field_placeholder="Select Category:-")


user_state={}

@dp.message(Command('start'))
async def startbot(msg:types.Message):
    await msg.answer("Select Subject:", reply_markup=genrate_rkm(['Notes','Book','Solution','MarkWise Question','Testpapers']))
    
# Command handler for /notes
@dp.message(Command('notes'))
async def cmd_notes(message: types.Message):
         user_state[message.from_user.id] = {}
         await chapterHandler(message,'notes')

    # await message.answer("Select your grade:", reply_markup=generate_keyboard(keyboard_type='subject'))
    # await message.delete()
# Command handler for /book
@dp.message(Command('book'))
async def cmd_book(message: types.Message):
    user_state[message.from_user.id] = {}
    await chapterHandler(message,'book')

@dp.message(Command('solution'))
async def cmd_solution(message: types.Message):
        user_state[message.from_user.id] = {}
        await chapterHandler(message,'solution')

    # await message.answer("Select your solution type:", reply_markup=generate_keyboard("subject"))

@dp.message(Command('markwise'))
async def cmd_markwise(message: types.Message):
        user_state[message.from_user.id] = {}
        await chapterHandler(message,'markwise')

    # await message.answer("Select your MarkWise questions:", reply_markup=generate_keyboard("subject"))

async def chapterHandler(msg: types.message,category:str):
    user_state[msg.from_user.id]['category']= category.lower()
    print(user_state.items())
    await msg.answer(f"Select your {category.capitalize()}:", reply_markup=generate_keyboard("subject"))


@dp.message(lambda msg: msg.text in ['Notes','Book','Solution','MarkWise Question','Testpapers'])
async def category_handler(msg: types.Message):
    user_state[msg.from_user.id] = {}
    await chapterHandler(msg,msg.text)


# Callback query handler for selecting the grade (9th or 10th)
@dp.callback_query(lambda c: c.data.startswith('subject_'))
async def process_subject_selection(callback_query: types.CallbackQuery):
    subject_code = callback_query.data.split("_")[1]
    user_state[callback_query.from_user.id]['class'] = subject_code
    # await bot.answer_callback_query(callback_query.id)
    await asyncio.sleep(0.5)
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=f"Now, select a chapter for {subject_code} Grade:"
    )
    print(user_state.items())

    # After selecting the subject (9th or 10th), show the chapters
    await bot.edit_message_reply_markup(
        chat_id= callback_query.from_user.id,
        message_id= callback_query.message.message_id,
        reply_markup=generate_keyboard('chapter'),
    )
    # await bot.send_message(callback_query.from_user.id, f"Now, select a chapter for {subject_code} Grade:",)

pdfurl = "https://cloud.appwrite.io/v1/storage/buckets/672e4699000c9ac7f3f0/files/67332ba60012c79b8e71/view?project=672e34dc001691a52a72"

# Callback query handler for selecting a chapter (1-14)
@dp.callback_query(lambda c: c.data.startswith('chapter_'))
async def process_chapter_selection(callback_query: types.CallbackQuery):
    chapter_no = callback_query.data.split("_")[1]
    user_state[callback_query.from_user.id]['chapter']=chapter_no
    await bot.answer_callback_query(callback_query.id)
    pdf = URLInputFile(
         pdfurl,filename="Ch -1 Chemical reaction and equation.pdf",
    )
    img = URLInputFile(
         pdfurl,filename="Ch -1 Chemical reaction and equation.png",
    )
    # Send the selected chapter number to the user
    print(user_state.items())
    await bot.send_message(callback_query.from_user.id, f"You selected Chapter {chapter_no}")
    await bot.send_document(thumbnail=img, document=pdf,chat_id=callback_query.from_user.id)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Bot is started')
    asyncio.run(main())
    # executor.start_polling(dp, skip_updates=True)


