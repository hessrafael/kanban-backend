from pydantic import BaseModel
from typing import List
from model.board import Board
from schemas.column import ColumnsListSchema
from datetime import datetime

# Definindo os Schemas de como os quadros devem ser representados

class BoardSchema(BaseModel):
    """ Define como um quadro a ser inserido deve ser representado
    """
    name: str = "Meu Quadro"
    columns: list[str] = "col1","col2"

class BoardConsultaSchema(BaseModel):
    """Define como é feita a estrutura de consulta, com base no nome do Board
    """
    name: str = "Meu Quadro"


class BoardViewSchema(BaseModel):
    """Define como um quadro será retornado, apresentando as suas colunas e cards associados
    """
    id: str
    name: str = "Meu Quadro"
    total_columns: int = 2
    total_cards: int = 1
    columns: List[ColumnsListSchema]
    created_at: datetime

class BoardListViewSchema(BaseModel):
    """ Define como uma lista de quadros será retornada
    """
    boards: List[BoardViewSchema]

def show_board(board: Board):
    """ Retorna uma representação do board seguindo o schema definido em
        BoardViewSchema.
    """
    columns = []
    total_cards = 0
    
    for column in board.columns:
        cards = []
        for card in column.card:
            total_cards += 1
            cards.append({
                "id": card.pk_card,
                "name": card.name,
                "created_at": card.created_at
            })
        cards = sorted(cards, key=lambda card: card["created_at"])
        columns.append({
            "id": column.pk_column,
            "name": column.name,
            "created_at": column.created_at,
            "total_cards": len(cards),
            "cards": cards
        })
        columns = sorted(columns, key=lambda column: column["created_at"])

    
    return {
        "id": board.pk_board,
        "name": board.name,
        "total_columns": len(board.columns),
        "columns": columns,
        "total_cards": total_cards,
        "created_at": board.created_at     
    }

def show_all_boards(boards: List[Board]):
    result = []
    for board in boards:
        result.append(show_board(board=board))
    return result
