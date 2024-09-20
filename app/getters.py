from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram.types import Message, User
import app.database.requests as requests
import parser

stavki = [
    {       
        'comand_1': 'Minsk',
        'comand_2': 'Piter',
        'id': 1,
    },
    {
        'comand_1': 'Brest',
        'comand_2': 'Moskow',
        'id': 2,
    },
    {
        'comand_1': 'Kaliningrad',
        'comand_2': 'Murmansk',
        'id': 3,
    },
]


async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {
        'username': event_from_user.username,
        'id': event_from_user.id,
        'balance': await requests.check_balance(event_from_user.id),
        'subscribe': await requests.check_subscribe(event_from_user.id),
        'stavki': stavki,
        }

def stavki_getter():
    return {
        'stavki': parser.get_live_football_matches(),
        }

