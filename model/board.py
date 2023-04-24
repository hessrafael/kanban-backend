from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from model import Base
import uuid

class Board(Base):
    __tablename__ = 'board'

    pk_board = Column(String(36), primary_key =True)
    name = Column(String(255))
    created_at = Column(DateTime)
    #campo para implementação futura de soft delete
    is_active = Column(Boolean, default=True)
    columns = relationship("Columns")
    
    def __init__(self, name:str):
        self.pk_board = uuid.uuid4().__str__()
        self.name = name
        self.created_at = datetime.now()

           

        