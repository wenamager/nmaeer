from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
import asyncio
from app import states
from app.handlers import user_router
from app import dialogs
from app.database.models import init_models


bot = Bot('7047637117:AAExkCDwjhQKk9IVVDCgUmPEBreQ0R1VcV8', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()



async def main():
    await init_models()
    dp.include_router(user_router)
    dp.include_router(dialogs.start_dialog)
    dp.include_router(dialogs.menu_dialog)
    dp.include_router(dialogs.profile_dialog)
    dp.include_router(dialogs.pull_balance_dialog)
    dp.include_router(dialogs.help_dialog)
    dp.include_router(dialogs.instruction_dialog)
    dp.include_router(dialogs.promo_dialog)
    dp.include_router(dialogs.to_subscribe_dialog)
    dp.include_router(dialogs.show_stavka_dialog)
    dp.include_router(dialogs.home_dialog)
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())