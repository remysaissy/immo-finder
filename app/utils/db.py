import time
from _datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import settings

engine = create_engine(settings.core.DATABASE_URL)
Base = declarative_base()

class Offer(Base):
    """
    A table to store data on listings from the various providers.
    """

    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    datasource_name = Column(String)
    datasource_id = Column(String)

    @staticmethod
    def is_new_offer(o, datasource_name):
        """ Check if a an offer is already in the database. """
        results = session.query(Offer).filter_by(datasource_id=o.id, datasource_name=datasource_name).first()
        return results is None

    @staticmethod
    def persist_offer(o, datasource_name):
        """ Write an offer in the db. """
        created = o.created_at
        if created is None:
            created = datetime.fromtimestamp(time.time())
        db_offer = Offer(
            created=created,
            datasource_name=datasource_name,
            datasource_id=o.id
        )
        session.add(db_offer)
        session.commit()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
