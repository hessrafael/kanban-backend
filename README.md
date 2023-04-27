# API Kanban

Este projeto python (v.3.10.6) é para um sistema de Kanban para gestão de tarefas (cards)

---
## Como executar alternativamente sem o Docker (ambiente de desenvolvimento)

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenpython -m venv .v.pypa.io/en/latest/).

Para criar o ambiente virtual execute o seguinte comando:

```
python -m venv .v.pypa.io/en/latest
```
Navegue até o diretório com o seguinte comando:

```
cd .\.v.pypa.io\en\latest\Scripts  
```
E ative o ambiente rodando:

```
.\activate
```

o comando a seguir instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`. Navegue até o diretório raiz e execute:

```
(env)$ pip install -r requirements.txt
```

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.