# Backend - Connectors

---

## Código Inicial: criação das conexões/sessões com o DB

---

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# remove connect_args if using any other db than sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session: Session = SessionLocal()
    try:
        yield session
        # session.commit()
    # except Exception as exc:
    #     session.rollback()
    #     raise exc
    finally:
        session.close()

Base = declarative_base()

Base.metadata.create_all(bind=engine)

# PRAGMA foreign_keys = ON;
# from sqlalchemy import create_engine, event

# def _fk_pragma_on_connect(dbapi_con, con_record):
#     dbapi_con.execute('pragma foreign_keys=ON')

# engine = create_engine("sqlite:///your_database.db")
# event.listen(engine, 'connect', _fk_pragma_on_connect)
```

## PARTE 1 - Importação das bibliotecas

---

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
```

Aqui, são importadas as classes e funções necessárias da biblioteca SQLAlchemy para criar, definir modelos e gerenciar sessões de banco de dados.

## PARTE 2 - Importação da URL do banco de dados

---

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
```

Isso define a URL do banco de dados SQLite. O banco de dados será criado no arquivo **`sql_app.db`** no diretório atual.

## PARTE 3 - Criação do motor do banco de dados

---

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
```

Aqui, um motor (engine) do SQLAlchemy é criado usando a URL do banco de dados SQLite. O parâmetro **`connect_args={"check_same_thread": False}`** é usado para evitar problemas de concorrência em aplicativos multi-threading, mas isso não é apropriado para aplicativos em produção. Esse motor é uma interface para interagir com o banco de dados.

O **`create_engine`** é uma função fundamental da biblioteca SQLAlchemy, que é uma biblioteca de mapeamento objeto-relacional (ORM) em Python. Essa função é usada para criar um objeto de "motor" (engine) de banco de dados, que é essencialmente uma interface que permite ao seu programa se comunicar com um banco de dados.

A função **`create_engine`** recebe uma URL de conexão como seu principal argumento e retorna um objeto de motor configurado para se conectar ao banco de dados especificado na URL. A URL de conexão varia de acordo com o tipo de banco de dados que você deseja acessar e contém informações como o tipo de banco de dados, o local, as credenciais de autenticação e outras configurações específicas do banco de dados. O **`create_engine`** cria um objeto de motor (**`engine`**) que pode ser usado posteriormente para executar consultas, criar tabelas, inserir dados e realizar outras operações de banco de dados usando a biblioteca SQLAlchemy.

## PARTE 4 - Criação da classe SessionLocal

---

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

A classe **`SessionLocal`** é criada usando a função **`sessionmaker`**. Essa classe será usada para criar sessões do SQLAlchemy, que são usadas para realizar operações no banco de dados. Os parâmetros **`autocommit`** e **`autoflush`** são definidos como **`False`** para que o controle sobre as transações seja mais explícito.

O **`autocommit`** é uma configuração que determina o comportamento de transações em um banco de dados quando você executa operações de leitura ou gravação. No contexto do SQLAlchemy e de muitos sistemas de gerenciamento de banco de dados (DBMS), o **`autocommit`** é um parâmetro que pode ser configurado ao criar uma sessão de banco de dados. Vou explicar os conceitos associados a ele:

1. **Modo de Autocommit**:
    - **Autocommit Ativado (`autocommit=True`)**: Neste modo, cada operação de banco de dados (como uma consulta **`SELECT`** ou uma instrução **`INSERT`**, **`UPDATE`** ou **`DELETE`**) é automaticamente confirmada (comitada) assim que é executada. Isso significa que cada operação é tratada como uma transação independente e não é necessário chamar manualmente **`commit()`** para confirmar as alterações no banco de dados.
    - **Autocommit Desativado (`autocommit=False`)**: Neste modo, as operações de banco de dados não são automaticamente confirmadas. Você deve explicitamente chamar **`commit()`** para confirmar as alterações em uma transação. Isso permite agrupar várias operações em uma única transação, que pode ser confirmada ou revertida em conjunto.
2. **Quando Usar o Autocommit**:
    - **Autocommit Ativado (`autocommit=True`)**: Isso é útil quando você está realizando principalmente operações de leitura (consultas) no banco de dados e não precisa manter controle explícito sobre transações. É mais eficiente em termos de recursos para leitura de dados.
    - **Autocommit Desativado (`autocommit=False`)**: Isso é apropriado quando você está realizando operações de gravação (inserções, atualizações, exclusões) e precisa garantir a atomicidade das operações. Em outras palavras, você deseja que todas as operações sejam confirmadas juntas como uma única transação ou revertidas em caso de erro.

No código que você compartilhou, a função **`sessionmaker`** é usada para criar uma fábrica de sessões (**`SessionLocal`**) com **`autocommit=False`**. Isso significa que, por padrão, as operações de banco de dados realizadas em sessões criadas a partir dessa fábrica não serão automaticamente confirmadas, exigindo que você chame explicitamente **`commit()`** para confirmar as alterações. Isso é comum em cenários de aplicativos onde o controle transacional é importante para garantir a consistência dos dados no banco de dados.

O **`autoflush`** é uma configuração relacionada ao comportamento de uma sessão do SQLAlchemy em relação ao envio de alterações ao banco de dados. Essa configuração pode ser ajustada ao criar uma sessão por meio da função **`sessionmaker`**. O **`autoflush`** tem dois modos principais:

1. **Autoflush Ativado (`autoflush=True`) - Comportamento Padrão**:
    - Neste modo, sempre que você realiza uma operação que modifica o estado dos objetos mapeados da sessão (como criar, atualizar ou excluir objetos), o SQLAlchemy automaticamente "despeja" (flush) essas modificações para o banco de dados antes de executar qualquer consulta. Isso garante que todas as modificações pendentes sejam aplicadas ao banco de dados antes de qualquer consulta ser executada.
    - O autoflush é útil quando você deseja garantir que as alterações sejam aplicadas ao banco de dados em tempo real, evitando assim inconsistências entre os objetos em memória e o estado do banco de dados.
2. **Autoflush Desativado (`autoflush=False`) - Comportamento Personalizado**:
    - Neste modo, o SQLAlchemy não realiza automaticamente um "flush" das modificações da sessão antes de executar uma consulta. Isso significa que as operações de gravação (como inserções, atualizações e exclusões) são mantidas em memória até que você chame explicitamente **`session.commit()`**, que então confirma todas as alterações pendentes no banco de dados.
    - O autoflush desativado pode ser útil quando você deseja um controle mais fino sobre quando as alterações devem ser confirmadas no banco de dados, permitindo que você agrupe várias operações em uma única transação ou reverta todas as alterações em caso de erro.

Em resumo, o **`autoflush`** controla se as alterações feitas em objetos mapeados em uma sessão do SQLAlchemy são automaticamente aplicadas ao banco de dados antes de executar consultas. A escolha entre ativá-lo ou desativá-lo depende dos requisitos específicos do seu aplicativo e da necessidade de controle sobre o ciclo de vida das transações e das alterações de banco de dados.

## PARTE 5 - Definição da função *get_db*

---

```python
def get_db():
    session: Session = SessionLocal()
    try:
        yield session
        # session.commit()
    # except Exception as exc:
    #     session.rollback()
    #     raise exc
    finally:
        session.close()
```

Esta função **`get_db`** é um gerador que fornece uma sessão do SQLAlchemy quando chamada. A sessão é criada usando **`SessionLocal()`** e é devolvida com **`yield`**, permitindo que seja usada em um contexto de gerenciamento de contexto (geralmente um bloco **`with`**). Após a conclusão do contexto, a sessão é fechada no bloco **`finally`**.

**`SessionLocal`** é uma fábrica de sessões. Isso significa que **`SessionLocal()`** é usado para criar instâncias individuais de sessões que podem ser usadas para interagir com o banco de dados. Portanto, **`SessionLocal`** é o tipo ou classe que representa sessões.

Nesse caso, **`session`** é uma instância específica da sessão criada a partir de **`SessionLocal`**. A variável **`session`** contém uma sessão ativa que pode ser usada para executar consultas e operações no banco de dados associado ao motor **`engine`** especificado.

Assim, **`Session`** é o tipo de sessão (ou seja, a classe que representa sessões), e **`session`** é uma instância específica dessa sessão que você pode usar em seu código para interagir com o banco de dados.

**`Session`** é uma classe importada da biblioteca SQLAlchemy. Essa classe é usada para representar uma sessão de banco de dados em SQLAlchemy. Uma sessão é uma unidade de trabalho em um banco de dados, onde você realiza operações de leitura e gravação de dados. As sessões são usadas para gerenciar transações, garantir consistência nos dados e fornecer um contexto de trabalho seguro com o banco de dados.

A classe **`Session`** é parte do sistema de ORM (Mapeamento Objeto-Relacional) do SQLAlchemy, que mapeia objetos Python para tabelas no banco de dados e vice-versa. Você usa instâncias dessa classe para realizar operações no banco de dados, como inserir, atualizar, excluir e consultar registros.

No código que você compartilhou, a classe **`Session`** não é usada diretamente, mas é parte da configuração do SQLAlchemy. A função **`sessionmaker`** é usada para criar uma fábrica de sessões, que é usada para criar instâncias de sessões sempre que você precisa trabalhar com o banco de dados.

Quando você terminar de usar a sessão, você deve chamá-la de **`session.close()`** para liberar recursos e encerrar a sessão. Quando você chama o método **`session.close()`** em uma sessão do SQLAlchemy, vários recursos importantes são liberados e a sessão é encerrada de forma apropriada. Esses recursos incluem:

1. **Conexão com o Banco de Dados**: A sessão geralmente mantém uma conexão com o banco de dados enquanto está aberta. Quando você fecha a sessão, essa conexão é fechada e devolvida ao pool de conexões (se estiver sendo usado um pool). Isso libera a conexão para ser reutilizada por outras partes do aplicativo.
2. **Transações Pendentes**: Se houver alguma transação pendente (ou seja, operações que foram realizadas na sessão, mas não foram confirmadas com um **`commit`**), essas transações serão revertidas (rollback) quando a sessão for fechada. Isso garante que as mudanças não confirmadas não sejam persistidas no banco de dados.
3. **Cache de Identidade**: O SQLAlchemy mantém um cache de identidade para objetos mapeados para linhas do banco de dados. Ao fechar a sessão, esse cache é liberado, o que significa que todas as referências aos objetos mapeados pela sessão não são mais válidas.
4. **Limpeza de Estado**: Todos os objetos em estado pendente ou gerenciado pela sessão têm seu estado liberado e não estão mais vinculados à sessão.
5. **Recursos de Memória**: A sessão pode alocar memória para armazenar objetos e informações relacionadas a consultas e transações. Fechar a sessão libera esses recursos de memória.

Em resumo, **`session.close()`** é uma operação importante para garantir que as transações sejam tratadas de forma apropriada, que as conexões com o banco de dados sejam liberadas e que os recursos de memória sejam liberados. Isso ajuda a manter a integridade do aplicativo e a garantir que não haja vazamento de recursos ao trabalhar com o SQLAlchemy.

### Sobre try e finally

1. Se uma exceção (erro) for lançada em algum lugar dentro do bloco **`try`**, o fluxo de controle é transferido para o bloco **`finally`** imediatamente após o bloco **`try`**. Isso acontece mesmo se a exceção não for tratada dentro do bloco **`try`**.
2. O bloco **`finally`** é executado, independentemente de ter ocorrido ou não uma exceção. Isso permite que você coloque código que deve ser executado de forma consistente, como a limpeza de recursos ou ações de encerramento, no bloco **`finally`**.

### Sobre o yield

A palavra-chave **`yield`** é usada em Python para criar uma função geradora. Uma função geradora é um tipo especial de função que permite pausar sua execução e "retornar" um valor temporariamente para o chamador sem sair completamente da função. A execução da função geradora pode ser retomada a partir do ponto onde foi pausada, mantendo seu estado interno. Isso é útil quando você precisa iterar sobre um grande conjunto de dados ou gerar valores sob demanda, economizando memória e melhorando o desempenho.

Funções geradoras são frequentemente usadas em combinação com loops, permitindo a iteração eficiente sobre sequências de dados que não precisam ser totalmente carregadas na memória. Além disso, elas são fundamentais em Python para a implementação de iteradores personalizados, como os usados em estruturas de dados complexas ou para processamento de grandes volumes de dados.

## PARTE 6 - Criação da base declarativa

---

```python
Base = declarative_base()
```

Uma classe base declarativa é criada. Isso é usado para definir modelos de banco de dados que serão mapeados para tabelas no banco de dados.

Uma base declarativa é um conceito relacionado à biblioteca SQLAlchemy em Python e se refere a uma maneira de definir e criar modelos de dados de forma mais simples e declarativa, em oposição a uma abordagem imperativa.

A base declarativa no SQLAlchemy é implementada por meio da classe **`declarative_base()`**. Vamos entender os conceitos envolvidos:

1. **Mapeamento Objeto-Relacional (ORM)**: SQLAlchemy é uma biblioteca ORM, o que significa que ela permite que você mapeie objetos Python para tabelas em um banco de dados relacional e vice-versa. Isso facilita a interação com bancos de dados ao tratar as tabelas como classes e as linhas como instâncias de objetos.
2. **Base Declarativa (`declarative_base()`)**: A base declarativa é uma classe especial fornecida pelo SQLAlchemy que simplifica a definição de modelos de dados. Em vez de definir tabelas manualmente usando SQL, você pode criar classes Python que herdam da **`declarative_base()`**. Cada classe representa uma tabela no banco de dados e os atributos da classe mapeiam diretamente para colunas na tabela.

### Exemplo de uso

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
```

Neste exemplo, a classe **`Pessoa`** herda de **`Base`** e define uma tabela chamada "pessoas" com colunas "id", "nome" e "idade". As colunas são representadas como atributos da classe.

**Vantagens da Base Declarativa**:

- Clareza: A definição de modelos é mais legível e semelhante ao código Python comum.
- Redução de erros: Menos oportunidades para erros de digitação, pois os nomes das colunas são definidos como atributos da classe.
- Reutilização: Classes de modelo podem ser facilmente reutilizadas em diferentes partes do código.

**Interação com o Banco de Dados**: Uma vez que você tenha definido seus modelos usando a base declarativa, você pode criar, consultar, atualizar e excluir registros no banco de dados usando essas classes de modelo. O SQLAlchemy cuida da tradução entre objetos Python e instruções SQL para você.

Em resumo, uma base declarativa no SQLAlchemy é uma abordagem que permite definir modelos de dados usando classes Python, facilitando a interação com bancos de dados relacionais de uma maneira mais orientada a objetos e declarativa. Isso torna o código mais legível e menos suscetível a erros, além de facilitar a manutenção e reutilização de modelos.

## PARTE 7 - Criação das tabelas no banco de dados

---

```python
Base.metadata.create_all(bind=engine)
```

Finalmente, o código cria todas as tabelas no banco de dados especificado no motor. Isso é feito usando o método **`create_all`** da metainformação da base declarativa (**`Base.metadata`**) e associando-o ao motor criado anteriormente.

A linha de código **`Base.metadata.create_all(bind=engine)`** no SQLAlchemy é usada para criar as tabelas no banco de dados de acordo com as definições de classe que você criou usando a base declarativa (**`Base`**). Vou explicar essa linha de código em detalhes:

1. **`Base`**: No código que você compartilhou, **`Base`** é uma instância da classe base declarativa que você definiu anteriormente usando **`Base = declarative_base()`**. Essa classe serve como base para todas as classes de modelo que você cria para representar tabelas no banco de dados.
2. **`metadata`**: **`Base.metadata`** é um objeto especial no SQLAlchemy que armazena metadados sobre as tabelas e colunas definidas nas classes de modelo. Ele é usado para rastrear e gerenciar as definições das tabelas.
3. **`create_all()`**: **`create_all()`** é um método do objeto **`metadata`** que é usado para criar todas as tabelas associadas às classes de modelo definidas em **`Base`**. Quando você chama este método, o SQLAlchemy gera automaticamente as instruções SQL necessárias para criar as tabelas no banco de dados.
4. **`bind=engine`**: O parâmetro **`bind`** é usado para especificar o motor de banco de dados ao qual você deseja associar (vincular) as tabelas que estão sendo criadas. Neste caso, você está vinculando as tabelas ao motor **`engine`** que você definiu anteriormente usando **`engine = create_engine(SQLALCHEMY_DATABASE_URL)`**.

Quando você executa **`Base.metadata.create_all(bind=engine)`**, o SQLAlchemy gera e executa as instruções SQL necessárias para criar todas as tabelas definidas em suas classes de modelo no banco de dados associado ao motor **`engine`**. Isso cria as estruturas de tabela no banco de dados de acordo com as definições de colunas e tabelas que você especificou em suas classes de modelo.

Essa operação é geralmente executada uma vez durante a configuração inicial do seu aplicativo para criar as tabelas no banco de dados. Após a criação das tabelas, você pode usar as classes de modelo para realizar operações de leitura, gravação e consulta de dados no banco de dados de maneira orientada a objetos.

# Backend - Models

# Backend - Schemas

