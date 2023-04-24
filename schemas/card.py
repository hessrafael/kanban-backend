from pydantic import BaseModel
from model.card import Card
from datetime import datetime

# Definindo os Schemas de como as Cards devem ser representados

class CardSchema(BaseModel):
    """ Define como um Card a ser inserido deve ser representado
    """
    board_id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    col_name: str = "Minha coluna"
    name: str = "Aqui está a descrição do meu card"

class CardMoveSchema(BaseModel):
    """ Define como representar a mudança do card entre colunas
    """
    card_id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    dest_col: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"

class CardConsultaSchema(BaseModel):
    """Define como é feita a estrutura de consulta, com base no id do Card
    """
    card_id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    


class CardViewSchema(BaseModel):
    """Define como um card será retornado
    """
    id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    board: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    column: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    name: str = "Meu card"
    created_at: datetime

class CardListSchema(BaseModel):
    """ Define como os cards são retornados em uma lista
    """
    id: str = "fe65f8cd-28f9-4ca5-8101-69fdf4d6537d"
    name: str = "Meu card"
    created_at: datetime

class CardDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """    
    message: str
    

def show_card(card: Card):
    """ Retorna uma representação da coluna seguindo o schema definido em
        CardViewSchema.
    """
    return {
        "id": card.pk_card,
        "column": card.column,
        "name": card.name     
    }