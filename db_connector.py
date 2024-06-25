from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import json
import logging
logging.basicConfig(level=logging.INFO)

Base = declarative_base()


class DBConnector:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as file:
            config = json.load(file)
            db_config = config["database"]
            self.engine = create_engine(
                f"mariadb+mariadbconnector://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
                echo=True
            )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def execute(self, query, params=None):
        with self.get_session() as session:
            try:
                if params:
                    result = session.execute(text(query), params)
                else:
                    result = session.execute(text(query))
                session.commit()
                return result.mappings()
            except Exception as e:
                session.rollback()
                logging.error("Could not execute query: " + str(e))
                raise ValueError(str(e))
