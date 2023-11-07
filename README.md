# ecomm_of_love
Repositório do PI2 para criar um ecommerce website rodando em JS + Python  
<!-- 
Exemplificação das operações Back-Front-Infra
![automated like clockwork](./images/Aplicação%20Básica%20-%20E-commerce.drawio.png) -->

# Estrutura da APP

| Ambiente  | Fonte  | Precisa  |   |   |
|---|---|---|---|---|
| Teste  | Sqlite | - |   |   |
| Develop | develop-ecomm-db.cvzwreo61y01.us-east-1.rds.amazonaws.com:3306/ecomm | .env ou infisical(TODO) |   |   |
|  Prod | - | - | - | - |


# Como iniciar a API 

> 1. Baixe uma versão do Python maior our igual 3.8 ou maior 

> 2. Adicione o Poetry como um pacote no seu python (no terminal digite) 

        pip install poetry

> 3. Agora inicie, na pasta do ecomm_of_love,o pacote com poetry (no terminal digite) 

        poetry install

> 4. Acesse a branch que desenvolvemos a primeira rota  no terminal digite ou no vscode ou outra IDE

        git checkout feature/products

> 5. Inicialize o interpretador Venv criado pelo Poetry 

* Pela [IDE](https://code.visualstudio.com/docs/python/environments)
* Terminal -> source .venv/bin/activate

> 6. Executar API 

* Pela [IDE](https://code.visualstudio.com/docs/python/environments)
* Terminal -> $ `python3 main.py` 

# Como realizar migrações/modificações no db

> Migrações de banco de dados: 

* Usamos Alembic, um pacote python focado em migrar. [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)


1. Utilizando a biblioteca Alembic, podemos iniciar revisões auto geradas (obs: isso funciona para grande maioria das operações, mas não todas. Conferir na doc da [biblioteca](https://alembic.sqlalchemy.org/en/latest/autogenerate.html))

2. Executar uma revisão de modelo no terminal/prompt e na pasta em que se encontra o **alembic.ini** 

```shell
alembic revision --autogenerate -m '[Texto sobre migração]'
```
Gerará um código de migração (ela não foi feita ainda) para o banco de dados

3. Para subir/aplicar as alterações 

```shell
alembic upgrade head
```

4. Para retornar/recuperar o que foi modificado (retornar tudo)

```shell
alembic downgrade base 
```

4. 1 para retornar à algo especifico (revision id é gerada no alembic revision e armazenada na pasta versions)

```shell
alembic downgrade [REVISION_ID] 
```


# TODO

1. Configurar infisical para gerenciar secrets
2. Adicionar sistema de [Checkout PRO](https://www.mercadopago.com.br/developers/pt/docs/checkout-pro/landing) + [GIT](https://github.com/mercadopago/sdk-python)
3. Configurar user_context para Front
4. Desenvolver Tela de usuários + login