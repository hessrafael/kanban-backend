from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from model import Base
import uuid

class Columns(Base):
    __tablename__ = 'column'

    pk_column = Column(String(36), primary_key =True)
    name = Column(String(50))
    created_at = Column(DateTime)
    #campo para implementação futura de soft delete
    is_active = Column(Boolean, default=True)
    board = Column(String(36), ForeignKey("board.pk_board"), nullable=False )
    card = relationship("Card")

    #adicionando a restrição de que um board não pode ter colunas com nome repetidos
    __table_args__ = (UniqueConstraint('board', 'name', name='uq_board_name'),
                      )

    def __init__(self, name:str, board: str):
        self.pk_column = uuid.uuid4().__str__()    
        self.name = name
        self.board = board
        self.created_at = datetime.now()

    def get_board(self):
        return self.board
