import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from .meta import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    initials = Column(String(255), unique=True, nullable=False)
    role = Column(String(255), nullable=False)

    password_hash = Column(Text)

    def set_password(self, password):
        password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.password_hash = password_hash.decode('utf8')

    def check_password(self, password):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(password.encode('utf8'), expected_hash)
        return False
