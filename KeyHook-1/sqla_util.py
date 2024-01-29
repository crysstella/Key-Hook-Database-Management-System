from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

db_url = "postgresql+psycopg2://postgres:J4r3dr3y100!@localhost:5432/postgres"
engine = create_engine(db_url, pool_size=5, pool_recycle=3600, echo=True)
Base = declarative_base(metadata=MetaData(schema="semester_proj"))
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
metadata = Base.metadata
