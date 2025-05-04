import logging

from aiogram import Bot, dispatcher , types
from dotenv import load_dotenv
import os

load_dotenv() 
API_TOKEN=os.getenv("TOKEN")
print(API_TOKEN)