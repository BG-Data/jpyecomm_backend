# Python Ecommerce Backend
Repositório de Projeto Integrador II da UNIVESP criado para sustentar o servidor de backend que servirá como base para um Ecommerce junto React (outro repositório)  
<!-- 
Exemplificação das operações Back-Front-Infra
![automated like clockwork](./images/Aplicação%20Básica%20-%20E-commerce.drawio.png) -->

## Motivação
1. Criar uma aplicação de Ecommerce que opera utilizando Python;
2. Desenvolver habilidades de desenvolvimento Backend utilizando Fastapi, sqlalchemy, integrações com mercado pago e outrem;
3. Servir como base de prática para estruturações mais agnósticas (polimorficas) e aplicação de conceito de design orientado por domínio 
4. Aprender a desenvolver código aberto e boas práticas com a comunidade [Guia](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)


# TODOs

## Backend
1. Criar tabela para registro de requisiçõe s(logger)
2. Adicionar sistema de [Checkout PRO](https://www.mercadopago.com.br/developers/pt/docs/checkout-pro/landing) + [GIT](https://github.com/mercadopago/sdk-python)
3. Criar auth via google api
4. Criar serviço para usuários adicionarem fotos pessoais 
5. Criar sistema de permissões básico (Admin, Vendedor, Comprador)
6. Adicionar estrutura para recuperação de senha via envio de e-mail com token 
7. Adicionar MFA em login 
8. Criar tutorial a-z do backend
9. Configurar CORS adequadamente 

## Devops
1. Garantir que arquivos no bucket estejam protegidos
2. Desenvolver Deploy de Ambiente em Kubernets
3. 

## Frontend
1. Not here my friend haha


# Estrutura da APP

| Ambiente  | Fonte  | Precisa  |   |   |
|---|---|---|---|---|
| Teste  | Sqlite | - |   |   |
| Develop | - | .env ou infisical |   |   |
|  Prod | - | - | - | - |

<!-- Make the tree with tre -d -I __pycache__ >> tree.txt -->

## A árvore:

* **Ubuntu** 
```shell
sudo apt-get install tree 
```
* **Execute** no terminal
 ```shell
tree -d -I __pycache__ >> tree.txt
 ```
```shell
.
├── images # Arquivo e imagens do readme
└── src # Pasta fonte da aplicação
    ├── api # APIs desenvolvidas
    ├── app # Camada de domínio e serviços
    │   └── checkout # Módulo de checkout 
    ├── common # Pacotes comuns desenvolvidos e amplamente utilizados pela aplicação
    ├── migrations # Opera atividades de alteração do banco de dados
    │   └── versions
    ├── base # Inicializador das dependências da Main.
    ├── structure # Abstração do banco de dados, esquemas, conectores, etc
    └── utils # Utilitários da aplicação (Usados mas não tão frequentemente)
```


# Como iniciar a API 

1. Baixe uma versão do Python maior our igual 3.8 ou maior 

2. Adicione o Poetry como um pacote no seu python (no **terminal** digite) 

```shell
pip install poetry
```

3. Agora inicie, na pasta do ecomm_of_love,o pacote com poetry (no **terminal** digite) 

```shell
poetry install
```

4. Acesse a branch que desenvolvemos a primeira rota  no **terminal** digite ou no vscode ou outra IDE

```shell
git checkout develop
```

5. Inicialize o interpretador Venv criado pelo Poetry 

* Pela [IDE](https://code.visualstudio.com/docs/python/environments)
* Terminal -> Ubuntu/Windows:
```shell
source .venv/bin/activate
```

6. Executar API 

* Pela [IDE](https://code.visualstudio.com/docs/python/environments)
* Terminal -> Ubuntu/Windows:
 ```shell
 python3 main.py
 ``` 

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
