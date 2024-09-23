from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime

# declarative base class
class Base(DeclarativeBase):
    pass


# an example mapping using the base
class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    date_published: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None)
    # genre: Mapped[]


def main() -> None:
    # Create an SQLite database
    engine = create_engine("sqlite:///books.db", echo=True)

    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Example of adding a new book to the database
    with Session(engine) as session:
        new_book = Book(title="1984", author="George Orwell", date_published=datetime.datetime(1984,1,1))
        session.add(new_book)
        session.commit()

if __name__ == "__main__":
    main()