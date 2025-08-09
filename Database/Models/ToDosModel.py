from Database.database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class ToDosModel(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id =Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Cada ToDo pertence a um usuário (Many-to-One)
    owner = relationship("UsersModel", back_populates="todos")