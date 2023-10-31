from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from settings import Config

# remove connect_args if using any other db than sqlite
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": Config.SQLALCHEMY_TRACK_MODIFICATIONS}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()

# Base.metadata.create_all(bind=engine)

# PRAGMA foreign_keys = ON;
# from sqlalchemy import create_engine, event

# def _fk_pragma_on_connect(dbapi_con, con_record):
#     dbapi_con.execute('pragma foreign_keys=ON')

# engine = create_engine("sqlite:///your_database.db")
# event.listen(engine, 'connect', _fk_pragma_on_connect)
