from pydantic import BaseModel
from typing import List
from datetime import datetime
from model.column import Columns
from schemas.card import CardListSchema

# Definindo os Schemas de como as colunas devem ser representados

class ColumnsSchema(BaseModel):
    """ Define como uma coluna a ser inserido deve ser representada
    """
    board_id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    columns_name: list[str] = "col1","col2"

class ColumnsConsultaSchema(BaseModel):
    """Define como é feita a estrutura de consulta, com base no id da Coluna
    """
    column_id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    


class ColumnsViewSchema(BaseModel):
    """Define como uma coluna será retornada, apresentando seus cards associados
    """
    id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    board: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    name: str = "Minha Coluna"
    total_cards: int = 30
    cards: List[CardListSchema]
    created_at: datetime

class ColumnsListSchema(BaseModel):
    """ Define como uma coluna será retornada em modo lista
    """
    id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    name: str = "Minha Coluna"
    total_cards: int = 30
    cards: List[CardListSchema]
    created_at: datetime

def show_column(column: Columns):
    """ Retorna uma representação da coluna seguindo o schema definido em
        ColumnsViewSchema.
    """
    cards = []
    for card in column.card:
        cards.append({
            "id": card.pk_card,
            "name": card.name
        })

    return {
        "id": column.pk_column,
        "board": column.board,
        "name": column.name,
        "total_cards": len(column.card),
        "cards": cards       
    }

def show_multipe_columns(columns: List[Columns]):
    """ Retorna uma representação de múltiplas colunas
    """
    result = []
    cards = []
    for column in columns:
        for card in column.card:
            cards.append({
            "id": card.pk_card,
            "name": card.name
        })

        result.append({
            "id": column.pk_column,
            "nome": column.name,
            "total_cards": len(column.card),
            "cards": cards              
        })

    return {
        "board": columns[0].board,
        "columns": result}