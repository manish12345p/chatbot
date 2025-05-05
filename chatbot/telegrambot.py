import logging
import asyncio
from aiogram import Bot, Dispatcher , types
from dotenv import load_dotenv
import os
from aiogram.filters import Command
from openai import RateLimitError
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
import openai
import sys

class Reference:
    """
    store previous things
    """
    def __init__(self) -> None:
        self.response=""

load_dotenv()
openai.api_key= os.getenv("OpenAI_API_key")

reference =Reference()
TOKEN= os.getenv("TOKEN")

#model name
MODEL_NAME= "gpt-4.1-mini"

#initialise bot
bot= Bot(token=TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp= Dispatcher(storage=MemoryStorage())

def clear_past():
    """
    clear previous
    """
    reference.response=""

@dp.message(Command(commands=["start"]))
async def welcome(message: types.Message):
    await message.reply(f"Hello, {message.from_user.full_name}!\nHow may i assist you.")

@dp.message(Command(commands=["clear"]))
async def clear(message: types.Message):
    clear_past()
    await message.reply("I've deletetd the previous conversation and text")

@dp.message(Command(commands=["help"]))
async def helper(message: types.Message):
    help_command=f"""
Hi there {message.from_user.full_name},
I am a chatbot created  by Manish
/start - start the conversation
/clear - to cear the past conversation
/help  - to get this help menu
I hpoe this help :)
    """
    await message.reply(help_command)


@dp.message()
async def chatgpt(message: types.Message):
    #print(f">>> USER: \n\t{message.text}")
    try:
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "assistant", "content": reference.response},
                {"role": "user", "content": message.text}
            ]
        )
        reference.response = response.choices[0].message.content
        #print(f">>> chatpromax: \n\t{reference.response}")
        await bot.send_message(chat_id=message.chat.id, text=reference.response)

    except RateLimitError:
        await bot.send_message(chat_id=message.chat.id, text="❗ Your OpenAI API quota has been exceeded. Please check your billing or try again later.")

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())