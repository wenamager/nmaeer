from aiogram import Bot, Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from app import states
from app.database import requests

user_router = Router()

@user_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager, bot: Bot):
    user = await requests.check_user(message.from_user.id)
    if not user:
        await requests.create_user(message.from_user.id)
    await dialog_manager.start(state=states.StartSG.start, mode=StartMode.RESET_STACK)

