from aiogram import Bot
import app.database.requests as req
import asyncio
import requests

CRYPTOPAY_TOKEN = "251800:AALOUYSmX2KNjpV92qkNQYx95Il7qqJHvi5"

async def create_invoice(amount, user_id):
    headers = {"Crypto-Pay-API-Token": CRYPTOPAY_TOKEN}
    data = {"asset": "USDT", "amount": float(amount), 'allow_anonymous': False}
    r = requests.get("https://pay.crypt.bot/api/createInvoice", data=data, headers=headers).json()
    invoice = {
        "url": r['result']['bot_invoice_url'],
        "invoice_id": r['result']['invoice_id'],
    }
    return invoice


async def check_payment(bot: Bot, user_id, invoice_id, amount):
    headers = {"Crypto-Pay-API-Token": CRYPTOPAY_TOKEN}
    finded = False
    while not finded:
        response = requests.get(f'https://pay.crypt.bot/api/getInvoices', headers=headers)
        invoices = response.json().get('result', [])
        for invoice in invoices['items']:
            if(invoice['status'] == 'paid' and invoice['invoice_id'] == invoice_id):
                await req.add_balance(user_id, amount)
                await bot.send_message(user_id, f'На ваш баланс зачислено <b>{amount}$</b>!')
                finded = True
        await asyncio.sleep(6)  