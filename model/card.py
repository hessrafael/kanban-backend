from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from model import Base
import uuid

class Card(Base):
    __tablename__ = 'card'

    pk_card = Column(String(36), primary_key =True)
    name = Column(String(140))
    created_at = Column(DateTime)
    #campo para implementação futura de soft delete
    is_active = Column(Boolean, default=True)
    column = Column(String(36), ForeignKey("column.pk_column"), nullable=False )
    

    def __init__(self, name:str, column:str):        
        self.pk_card = uuid.uuid4().__str__()
        self.name = name
        self.column = column
        self.created_at = datetime.now()
