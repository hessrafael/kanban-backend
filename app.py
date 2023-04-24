from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
#from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Board, Card, Columns
import schemas

from flask_cors import CORS


info = Info(title="API Kanban", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo as tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
board_tag = Tag(name="Board", description="Adição e visualização de quadros à base")
column_tag = Tag(name="Coluna", description="Adição de Colunas a um Board")
card_tag = Tag(name="Card", description="Adição remoção e alteração de Cards na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/add_board',tags=[board_tag],
         responses={"200": schemas.BoardViewSchema, "409": schemas.ErrorSchema, "400": schemas.ErrorSchema})
def add_board(form: schemas.BoardSchema):
    """Adiciona um novo Board à base de dados    
    """
    #instancia o Board a ser adicionado
    board = Board(
     name= form.name     
    )

    try:
        #adiciona o Board no banco de dados
        session = Session()
        session.add(board)
        session.commit()

        #consulta a PK do board adicionado para linkar às colunas
        board = session.query(Board).order_by(Board.created_at.desc()).first()
        pk_board = board.pk_board
        
        #realiza a adição das colunas na ordem informada
        cols_names= form.columns
        if len(cols_names) > 0:
            for col_name in cols_names:
                col = Columns(name=col_name,board=pk_board)
                session.add(col)
                #commit dentro do for para que as colunas sejam adicionadas na ordem especificada
                session.commit()         
        
        return  schemas.show_board(board), 200
    
    except IntegrityError as e:
        error_msg = "item de mesmo (nome, board) já salvo na base :/"
        return {"message": error_msg}, 409
    
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400

@app.get('/board',tags=[board_tag],
         responses={"200": schemas.BoardViewSchema, "404": schemas.ErrorSchema})
def get_board(query: schemas.BoardConsultaSchema):
    """Consulta um Board específico no banco de dados    
    """
    #recupera o nome do board para realizar a consulta
    board_name = query.name
    session = Session()
    board = session.query(Board).filter(Board.name == board_name).first()
    if not board:
        error_msg = "Item não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        return schemas.show_board(board), 200
    
@app.get('/all_boards',tags=[board_tag],
         responses={"200": schemas.BoardListViewSchema,"404": schemas.ErrorSchema})
def get_all_boards():
    """Retorna uma lista com todos os Boards presentes no banco de dados    
    """
    try:
        #consulta todos os boards presentes no banco de dados e retorna
        session = Session()
        boards = session.query(Board).filter(Board.is_active == 1).all()        
        return schemas.show_all_boards(boards),200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta :/"
        return {"message": error_msg}, 400


@app.post('/add_cols',tags=[column_tag],
          responses={"200": schemas.ColumnsViewSchema,"409": schemas.ErrorSchema, "400": schemas.ErrorSchema})
def add_cols(form: schemas.ColumnsSchema):
    """Adiciona uma nova coluna no banco de dados, linkando a um Board
    """
    #identifica o nome da nova coluna e a qual Board ela pertence
    cols_names = form.columns_name
    board_id = form.board_id    
    
    try:
        #inicia conexão ao banco
        session = Session()
        columns=[]
        #para cada nome de coluna, cria uma entidade Columns linkada ao Board
        if len(cols_names) > 0:
            for col_name in cols_names:
                col = Columns(name=col_name,board=board_id)
                session.add(col)
                columns.append(col)
            #envia as Columns para o banco de dados
            session.commit()
        #retorna as Columns criadas
        return schemas.show_multipe_columns(columns), 200
    
    except IntegrityError as e:
        error_msg = "item de mesmo (nome, board) já salvo na base :/"
        return {"message": error_msg}, 409
    
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400

# @app.get('/column',tags=[column_tag],
#          responses={"200": schemas.ColumnsViewSchema, "404": schemas.ErrorSchema})
# def get_column(query: schemas.ColumnsConsultaSchema):
#     """Consulta a informação de uma Coluna no Banco de Dados
#     """
#     #identifica a coluna a ser consultada
#     column_id = query.column_id
#     session = Session()
#     #recupera a coluna no banco de dados
#     column = session.query(Columns).filter(Columns.pk_column == column_id).first()
#     if not column:
#         error_msg = "Item não encontrado na base :/"
#         return {"message": error_msg}, 404
#     else:
#         return schemas.show_column(column), 200

@app.post('/add_card', tags=[card_tag],
         responses={"200": schemas.CardViewSchema, "409": schemas.ErrorSchema, "400": schemas.ErrorSchema})
def add_card(form: schemas.CardSchema):
    """Adiciona um card no banco de dados, linkando a uma coluna e a um Board
    """
    #especifica em qual Board e em qual Coluna deve adicionar o Card
    board_id = form.board_id
    col_name = form.col_name
    card_desc = form.name

    try:
        #inicia a conexão com o banco de dados
        session = Session()
        #recupera a coluna com base no Board e no Nome
        column = session.query(Columns).filter(Columns.board == board_id, Columns.name == col_name).first()
        
        #cria o card linkado à coluna  
        card = Card(name=card_desc,column=column.pk_column)
        
        #adiciona o card no banco
        session.add(card)
        session.commit()
        return schemas.show_card(card=card), 200
    
    except IntegrityError as e:
        error_msg = "item de mesmo id já salvo na base :/"
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400
    
# @app.get('/card',tags=[card_tag],
#          responses={"200": schemas.CardViewSchema, "404": schemas.ErrorSchema})
# def get_card(query: schemas.CardConsultaSchema):
#     """Consulta a um Card no banco de dados
#     """
#     #identifica o Card a ser consultado no banco
#     card_id = query.card_id
#     session = Session()
#     #consulta o Card no banco com base no id
#     card = session.query(Card).filter(Card.pk_card == card_id).first()
#     if not card:
#         error_msg = "Item não encontrado na base :/"
#         return {"message": error_msg}, 404
#     else:
#         return schemas.show_card(card), 200

@app.patch('/move_card', tags=[card_tag],
           responses={"200": schemas.CardViewSchema, "400": schemas.ErrorSchema})
def move_card(form: schemas.CardMoveSchema):
    """Move um Card no banco de dados para uma Coluna de destino
    """
    #identifica o Card e a Coluna de destino
    card_id = form.card_id
    dest_col = form.dest_col

    try:
        #inicia a conexão com o banco
        session = Session()
        #recupera o card no banco
        card = session.query(Card).filter(Card.pk_card == card_id).first()
        #recupera a coluna destino no banco
        column = session.query(Columns).filter(Columns.pk_column == dest_col).first()
        #altera a coluna do Card para a nova coluna        
        card.column = column.pk_column
        session.commit()
        return schemas.show_card(card), 200
    
    except Exception as e:
        error_msg = "Não foi possível mover o item :/"
        return {"message": error_msg}, 400

@app.delete('/del_card', tags=[card_tag],
           responses={"200": schemas.CardDelSchema, "400": schemas.ErrorSchema})    
def del_card(query: schemas.CardConsultaSchema):
    """Deleta um Card a partir do id informado e retorna uma mensagem de confirmação da remoção.
    """
    card_id = query.card_id  
    #criando conexão com a base
    session = Session()
    #fazendo a remoção
    count = session.query(Card).filter(Card.pk_card == card_id).delete()
    session.commit()

    if count:
        #retorna a representação da mensagem de confirmação
        return {"message": "Produto removido", "id": card_id}
    else:
        #se o produto não foi encontrado
        error_msg = "Card não encontrado na base :/"        
        return {"message": error_msg}, 404

