from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Column
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.types import ContentType, CallbackQuery, Message
from aiogram import Bot
from app import states
from app import getters
from app import cryptopay
import asyncio
from app.database import requests
from main import bot

bot = bot

start_message = '''
👋 Привет <b>{username}</b>!

🏆 Если ты зашел в этого бота то это судьба! Мы первый и единственный сервис на рынке который дает точные прогнозы на футбольные матчи!

❓Ты любишь делать ставки но у тебя никогда не получается выиграть? Ты изо всех сил пытаешься разобраться в этой системе?

👥 Можешь больше не беспокоиться ведь наша команда из пяти человек поможет тебе выиграть и вывестись большие деньги с это чертовой букмекерской конторы!!!

🫵 От тебя потребуется только желание и немного времени! Остальное сделают наши специалисты!'''


async def start_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.MenuSG.menu)

async def to_profile(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.ProfileSG.profile)

async def to_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.MenuSG.menu)

async def to_home(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state = states.StavkaSG.home)

async def to_help(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.HelpSG.help)

async def to_promo(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.PromoSG.promo)


async def to_subscribe(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.SubscribeSG.subscribe)

async def to_instruction(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.InstructionSG.instruction)

async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()


async def add_balance_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    amount = float(text)
    invoice = await cryptopay.create_invoice(amount, message.from_user.id)
    asyncio.create_task(cryptopay.check_payment(bot, message.from_user.id, invoice['invoice_id'], amount))
    await message.answer(f"Оплатите счет: {invoice['url']}")
    await dialog_manager.start(state=states.BalanceSG.pull_balance)

    
async def check_promo_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    if text == 'promocode':
        await message.answer("Вы ввели промокод!")
    else:
        await message.answer('Такого промокода нет!.')
    await dialog_manager.start(state=states.PromoSG.promo)

async def subscribe1_handler(callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager):
    user_balance = await requests.check_balance(callback.from_user.id)
    if user_balance >= 25:
        await requests.add_subscribe(callback.from_user.id, 1)
        await requests.add_balance(callback.from_user.id, -25)
        await callback.message.answer("Вы успешно приобрели подписку!")
    else:
        await callback.message.answer("Недостаточно средств на балансе!")
    await dialog_manager.start(state=states.SubscribeSG.subscribe)

async def subscribe3_handler(callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager):
    user_balance = await requests.check_balance(callback.from_user.id)
    if user_balance >= 50:
        await requests.add_subscribe(callback.from_user.id, 3)
        await requests.add_balance(callback.from_user.id, -50)
        await callback.message.answer("Вы успешно приобрели подписку!")
    else:
        await callback.message.answer("Недостаточно средств на балансе!")
    await dialog_manager.start(state=states.SubscribeSG.subscribe)

async def subscribe5_handler(callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager):
    user_balance = await requests.check_balance(callback.from_user.id)
    if user_balance >= 100:
        await requests.add_subscribe(callback.from_user.id, 5)
        await requests.add_balance(callback.from_user.id, -100)
        await callback.message.answer("Вы успешно приобрели подписку!")
    else:
        await callback.message.answer("Недостаточно средств на балансе!")
    await dialog_manager.start(state=states.SubscribeSG.subscribe)

async def stavka_handler(callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager):
    await dialog_manager.start(states.ShowStavkaSG.show_stavka, data = {
        'comand_1': 'Команда 1'
    })

start_dialog = Dialog(
    Window(
        Format(start_message),
        Button(
            Const("Начать!"), 
            id='start_menu',
            on_click=start_menu
            ),
        state=states.StartSG.start,
    ),
    getter=getters.user_getter
)   


menu_dialog = Dialog(
    Window(
        StaticMedia(path='menu.jpg', type=ContentType.PHOTO),
        Row(
            Button(Const('👤 Профиль'), id='profile', on_click=to_profile),
            Button(Const('⚡️ Ставки'), id='bets', on_click = to_home),
        ),
        Row(
            Button(Const('🎁 Промокод'), id='promocode', on_click=to_promo),
            Button(Const('📚 Инструкция'), id='instruction', on_click=to_instruction),
        ),
        Button(Const('📨 Техническая поддержка'), id='help', on_click = to_help),
        state=states.MenuSG.menu,
    ),
)  



profile_dialog = Dialog(
    Window(
        StaticMedia(path='menu.jpg', type=ContentType.PHOTO),
        Format(text='👤 <b>{username}</b>'),
        Format(text='⭐️ ID: <b>{id}</b>'),
        Format(text='🎟 Подписка: <b>{subscribe}</b> игр'),
        Format(text='💳 Баланс: <b>{balance}$</b>'),
        Button(Const('💵 Пополнить баланс'), id='add_balance', on_click = go_next),
        Button(Const('🎟 Оформить подписку'), id='subscribe', on_click = to_subscribe),  
        Button(Const('📨 Техническая поддержка'), id='help', on_click = to_help),
        Button(Const('◀️ Назад'), id='back', on_click=to_menu),
        getter=getters.user_getter,
        state=states.ProfileSG.profile,
    ),
    Window(
        Const("Введите сумму пополения: "),
        TextInput(
            id = 'sum_input',
            on_success=add_balance_handler,
        ),
        state=states.ProfileSG.balance,
    ),
) 


pull_balance_dialog = Dialog(
    Window(
        Const(text='Вернуться: '),
        Button(Const('◀️ Назад'),id='back',on_click=to_profile,),
        TextInput(
            id = 'sum_input',
            on_success=add_balance_handler,
        ),
        state=states.BalanceSG.pull_balance,
    ),
) 


help_dialog = Dialog (
    Window(
        Const(text='Поддержка: @wenaxera'),
        Button(Const('◀️ Назад'),id='back',on_click=to_menu,),
        state=states.HelpSG.help
    ),
)


instruction_dialog = Dialog (
    Window(
        Const(text='Инструкция: <b>инструкция</b>'),
        Button(Const('◀️ Назад'),id='back',on_click=to_menu),
        state=states.InstructionSG.instruction
    ),
)

promo_dialog = Dialog (
    Window(
        Const(text='Введите промокод: '),
        Button(Const('◀️ Назад'),id='back',on_click=to_menu,),
        TextInput(
            id = 'promo_input',
            on_success=check_promo_handler,
        ),
        state=states.PromoSG.promo,
    ),
)

to_subscribe_dialog = Dialog(
    Window(
        Const(text='Выберите нужный тариф: '),
        Button(Format('25$ за одну игру'), id='subscribe_1', on_click=subscribe1_handler),
        Button(Format('50$ за три игры'), id='subscribe_3', on_click=subscribe3_handler),
        Button(Format('100$ за пять игр'), id='subscribe_5', on_click=subscribe5_handler),
        Button(Const('◀️ Назад'),id='back',on_click=to_profile),
        state = states.SubscribeSG.subscribe
    )
)



home_dialog = Dialog(
    Window(
        StaticMedia(path='bet.jpg', type=ContentType.PHOTO),
        Button(Format('{stavka_1}'), id='subscribe_5', on_click=stavka_handler),
        getter=getters.user_getter,
        state = states.StavkaSG.home
    )
)


show_stavka_dialog = Dialog(
    Window(
        Format('Команда_1: {comand_1}'),
        Format('Команда_2:'),
        state = states.ShowStavkaSG.show_stavka
    )
)