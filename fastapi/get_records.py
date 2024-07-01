import json
from fastapi import APIRouter
import requests
from database import *
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class AddTask(BaseModel):
    name: str
    description: str
    

@router.post('/api/v1/addtask')
async def add_task(token: str, item: AddTask):

    session = Session()
    result = session.query(License).filter(License.war_token==token).first()
    if result != None:
        return item
    else:
        return {'error':'Ошибка токена'}
    

@router.get('/api/v1/task')
async def get_task(token: str, id_task: str):

    session = Session()
    result = session.query(License).filter(License.war_token==token).first()
    if result != None:
        task = session.query(Task).filter(Task.id==id_task).first()
        if task.owner == result.login.username or result.login.is_staff == '1' or task.executor.username == result.login.username:
            result = session.query(Task).filter(Task.id==id_task).first()
            return {"id": f"{result.id}", 
                    "name": f"{result.name}",
                    "description": f"{result.description}",
                    "owner": f"{result.owner}",
                    "priority": f"{result.priority}",
                    "date_create": f"{result.date_create}",
                    "executor": f"{result.executor.username}"
                    }
                    
        else:
            return {"result": "Отсутствует доступ к задаче"}
    else:
        return {"error": "Ошибка токена"}

@router.get('/api/v1/tasks')
async def get_tasks(token: str):

    answer = ""
    session = Session()
    result = session.query(License).filter(License.war_token==token).first()
    if result != None:
        check_is_staff = session.query(User).filter(User.id==result.login_id).first()
        if check_is_staff.is_staff == 1:
            tasks = session.query(Task).all()
            for i in tasks:
                i.executor_id = i.executor.username
            return tasks
        else:
            return {"result": "0"}
    else:
        return {"error": "Ошибка токена"}
    
@router.delete('/api/v1/deletetask')
async def delete_task(token: str, id_task: str):

    session = Session()
    license_check = session.query(License).filter(License.war_token==token).first()
    task = session.query(Task).filter(Task.id==id_task).first()

    if license_check != None:
        if license_check.login.is_staff == 1 or license_check.login.username == task.owner:
            if task is not None:
                try:
                    session.delete(task)
                    session.commit()
                    return {'result': 'Задача успешно удалена'}
                except Exception as e:
                    print(e)
                    return {'error': 'Системная ошибка'}
            else:
                return {'error': 'Задача не найдена!'}
        else:
            return {'error': 'Ошибка доступа к задаче'}
    else:
        return {"error": "Ошибка токена"}
