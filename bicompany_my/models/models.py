from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .meta import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    author_id = Column(ForeignKey("authors.id"), nullable=False)
    author = relationship("Author")
