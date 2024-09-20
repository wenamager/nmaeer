from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram.types import Message, User
import app.database.requests as requests

async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {
        'username': event_from_user.username,
        'id': event_from_user.id,
        'balance': await requests.check_balance(event_from_user.id),
        'subscribe': await requests.check_subscribe(event_from_user.id),
        'stavka_1': 'Минск - Питер',
        }

