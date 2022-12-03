import time

from aiogram import Bot, Dispatcher, filters, executor, types

from services import  Services
from settings import TOKEN, ADMIN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
services = Services('https://mw2.global/forum/')


@dp.message_handler(lambda message: 'Adduser' in message.text)
async def add_user(message: types.Message):
    full_name, err = services.get_user_name(message.text)

    if not message.from_user.full_name == ADMIN or err:
        return

    whitelist, in_whitelist = services.get_check_whitelist(full_name)

    if not in_whitelist:
        whitelist.append(full_name)
        services.write_file(whitelist)

        await message.reply('User has been successfully added to the whitelist.')
    else:
        await message.reply('User already in the whitelist.')


@dp.message_handler(lambda message: 'Removeuser' in message.text)
async def remove_user(message: types.Message):
    full_name, err = services.get_user_name(message.text)

    if not message.from_user.full_name == ADMIN or err:
        return

    whitelist, in_whitelist = services.get_check_whitelist(full_name)

    if message.from_user.full_name == ADMIN and in_whitelist:
        whitelist.remove(full_name)
        services.write_file(whitelist)

        await message.reply('User has been removed from the whitelist.')
    else:
        await message.reply('User already is in the whitelist.')


@dp.message_handler(lambda message: 'Whitelist' in message.text)
async def user_list(message: types.Message):
    data, err = services.check_text(message.text)

    if err or len(data) > 1:
        return

    user_id = message.from_user.id
    whitelist = services.read_file()

    if message.from_user.full_name == ADMIN:
        await bot.send_message(user_id, "\n".join(whitelist))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_full_name = message.from_user.full_name
    whitelist, in_whitelist = services.get_check_whitelist(user_full_name)
    data = []

    if in_whitelist:
        while True:
            new_data = services.get_data_table()

            if new_data != data:
                data = new_data

                await bot.send_message(message.from_user.id, "\n".join(data))

            time.sleep(60)
    else:
        await  message.reply('You have no right for it.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
