import asyncio

from aiogram import Bot, Dispatcher, filters, executor, types

from services import  Services
from settings import TOKEN, ADMIN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
services = Services('https://mw2.global/forum/')


async def process_loop(message, data):
    while True:
        new_data = services.get_data_table()

        if new_data != data:
            data = new_data

            await bot.send_message(message.from_user.id, "\n".join(data))

        await asyncio.sleep(10)
        await bot.send_message(message.from_user.id, "I'm working")


@dp.message_handler(lambda message: 'Adduser' in message.text)
async def add_user(message: types.Message):
    username, err = services.get_user_name(message.text)

    if not message.from_user.username == ADMIN or err:
        return

    whitelist, in_whitelist = services.get_check_whitelist(username)

    if not in_whitelist:
        whitelist.append(username)
        services.write_file(whitelist)

        await bot.send_message(
            message.from_user.id,
            'User has been successfully added to the whitelist.')
    else:
        await bot.send_message(
            message.from_user.id,
            'User already in the whitelist.')


@dp.message_handler(lambda message: 'Removeuser' in message.text)
async def remove_user(message: types.Message):
    username, err = services.get_user_name(message.text)

    if not message.from_user.username == ADMIN or err:
        return

    whitelist, in_whitelist = services.get_check_whitelist(username)

    if message.from_user.username == ADMIN and in_whitelist:
        whitelist.remove(username)
        services.write_file(whitelist)

        await bot.send_message(
            message.from_user.id,
            'User has been removed from the whitelist.')
    else:
        await bot.send_message(
            message.from_user.id,
            'User already is in the whitelist.')


@dp.message_handler(lambda message: 'Whitelist' in message.text)
async def user_list(message: types.Message):
    data, err = services.check_text(message.text)

    if err or len(data) > 1:
        return

    user_id = message.from_user.id
    whitelist = services.read_file()

    if message.from_user.username == ADMIN:
        await bot.send_message(user_id, "\n".join(whitelist))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    username = message.from_user.username
    whitelist, in_whitelist = services.get_check_whitelist(username)
    loop = asyncio.get_event_loop()
    data = []

    if in_whitelist or message.from_user.username == ADMIN:
        asyncio.ensure_future(process_loop(message, data))
        loop.run_forever()
    else:
        await  bot.send_message(
            message.from_user.id,
            'You have no right for it.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
