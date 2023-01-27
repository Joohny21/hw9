from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.hybrid import hybrid_property

from database.db import Base


class Contacts(Base):
    __tablename__ = 'Contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column('email', String(100), nullable=False)
    cell_phone = Column('cell_phone', String(100), nullable=False)
    address = Column('address', String(100), nullable=True)

    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name
