from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot

class StartSG(StatesGroup):
    start = State()

class MenuSG(StatesGroup):
    menu = State()


class ProfileSG(StatesGroup):
    profile = State()
    balance = State()

class BalanceSG(StatesGroup):
    pull_balance = State()

class HelpSG(StatesGroup):
    help = State()

class InstructionSG(StatesGroup):
    instruction = State()

class PromoSG(StatesGroup):
    promo = State()

class SubscribeSG(StatesGroup):
    subscribe = State()


class StavkaSG(StatesGroup):
    stavka = State()
    home = State()
    show_stavka = State()

class ShowStavkaSG(StatesGroup):
    show_stavka = State()

