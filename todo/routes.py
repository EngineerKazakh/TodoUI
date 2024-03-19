from urllib.request import Request
from fastapi import Request, Depends, Form,HTTPException
from todo.main import app,templates
from sqlalchemy.orm import Session
from todo.main import app, templates
from todo.database.base import get_db
from todo.models import ToDo
from todo.config import settings
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime
from pydantic import BaseModel


@app.get('/')
def home(request:Request, db_session:Session=Depends(get_db)):
    todos=db_session.query(ToDo).all()
    return templates.TemplateResponse('todo/index.html',{
        'request':request,
        'app_name':settings.app_name,
        'todo_list':todos
    })



@app.post('/add')
def add(
    title: str = Form(...),
    finish_time_str: str = Form(...),  
    db_session: Session = Depends(get_db)
):
    # try:
    #     finish_time = datetime.strptime(finish_time_str, "%Y-%m-%d %H:%M:%S.%f")
    # except ValueError:
    #     raise HTTPException(status_code=422, detail="Invalid date format")
    finish_time = datetime.strptime(finish_time_str, "%Y-%m-%d")
    new_todo = ToDo(title=title, finish_time=finish_time)
    db_session.add(new_todo)
    db_session.commit()
    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)



# class ToDo(BaseModel):
#     title: str
#     finish_time: datetime

# @app.post('/add')
# def add(todo: ToDo):
#     new_todo = ToDo(title=todo.title, finish_time=todo.finish_time)
#     # Perform your database operations here
#     return {"message": "Task added successfully", "task": new_todo}


@app.get('/update/{todo_id}')
def update(todo_id:int, db_session:Session=Depends(get_db)):
    todo=db_session.query(ToDo).filter(ToDo.id==todo_id).first()
    todo.is_complete = not todo.is_complete
    db_session.commit()
    url=app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/delete/{todo_id}')
def delete(todo_id:int,db_session:Session=Depends(get_db)):
    todo=db_session.query(ToDo).filter_by(id=todo_id).first()
    db_session.delete(todo)
    db_session.commit()
    url=app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

