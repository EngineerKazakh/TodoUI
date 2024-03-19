# from todo.database import Base ,engine
from sqlalchemy import Column, String, Integer, Boolean, DateTime
import datetime
from todo.database.base import Base, engine



class ToDo(Base):
    __tablename__='todos'

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    finish_time = Column(DateTime)
    is_complete=Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)



