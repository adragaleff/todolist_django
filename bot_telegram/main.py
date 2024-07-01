import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Command, CommandObject
import simplemysql
import settings
import requests
import json
from func import check_user
from bs4 import BeautifulSoup

bot = Bot(token=settings.token)
db = simplemysql.Pymysql(host=settings.host,user=settings.user, password=settings.password,db=settings.db,port=3306)


dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    result = db.request(f"SELECT * FROM `users` WHERE user_id = '{message.from_user.id}'", 'result')
    if result != 0:
        await message.answer(f"Для просмотра команд используйте /help")
    else:
        insert_sql = db.request(f"INSERT INTO `users` (user_id, token, war_token) VALUES ('{message.from_user.id}', '0', '0')")
        await message.answer(f"Пользователь зарегестрирован.\nДля просмотра команд используйте /help")

@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    result = db.request(f"SELECT * FROM `users` WHERE user_id = '{message.from_user.id}'", 'fetchone')
    token = result['token']
    war_token = result['war_token']
    if war_token == '0':
        await message.answer(f"Используйте активацию командой /active <токен с сайта>")
    else:
        await message.answer(f'Типо команды...')

@dp.message(Command("active"))
async def cmd_start(message: types.Message):
    result = db.request(f"SELECT * FROM `users` WHERE user_id = '{message.from_user.id}'", 'fetchone')
    token = result['token']
    war_token = result['war_token']
    if war_token == '0':
        token = message.text.replace("/active ", "")
        request = requests.post(f"http://213.159.215.37:7999/api/v1/validate_token/?token={str(token)}")
        result = json.loads(request.text)
        print(result['war_token'])
        result = result['war_token']
        if result == 'Ошибка токена!':
            await message.reply(f"Ошибка токена!")
        else:
            result = result.replace("Ваш рабочий токен: ", "")
            insert_sql = db.request(f"UPDATE `users` SET war_token = '{result}' WHERE user_id = '{message.from_user.id}'", 'result')
            await message.reply(f"Токен подтвержден!")
    else:
        await message.answer(f'Ваш профиль уже активирован.')

@dp.message(Command("tasks"))
async def show_tasks(message: types.Message):
    result = await check_user(message.from_user.id)
    if result == True:
        answer = ""
        list_answer = []
        token = db.request(f"SELECT * FROM `users` WHERE user_id = '{message.from_user.id}'", 'fetchone')
        token = token['war_token']
        request = requests.get(f"http://213.159.215.37:7999/api/v1/tasks?token={token}")
        request = json.loads(request.text)
        for i in request:
            name = i['name']
            id = i['id']
            priority = i['priority']
            date_of_staging = i['date_of_staging']
            owner = i['owner']
            date_create = i['date_create']
            executor_name = i['executor']['username']
            executor_first_name = i['executor']['first_name']
            executor_last_name = i['executor']['last_name']
            executor_is_staff = i['executor']['is_staff']
            if executor_first_name == "" or executor_last_name == "":
                answer += f"ID задачи: {id}\nНазвание задачи: {name}\nПриоритет: {priority}\nДата исполнения: {date_of_staging}\nДата создания задачи: {date_create}\nСоздатель задачи: {owner}\nИсполнитель: {executor_name}\n\n\n"
            else:
                answer += f"ID задачи: {id}\nНазвание задачи: {name}\nПриоритет: {priority}\nДата исполнения: {date_of_staging}\nДата создания задачи: {date_create}\nСоздатель задачи: {owner}\nИсполнитель: {executor_name} ({executor_first_name} {executor_last_name})\n\n\n"
        
        await message.reply(answer)
    else:
        await message.reply(f"Аккаунт не активирован.")
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())