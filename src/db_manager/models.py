from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey, String
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
    genres = relationship("Genre", secondary="book_genre_association", back_populates="books")

# association table for many-to-many relationship
book_genre_association = Table(
    "book_genre_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("genre_id", Integer, ForeignKey("genres.id"))
)

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    books = relationship("Book", secondary=book_genre_association, back_populates="genres")

Book.genres = relationship("Genre", secondary=book_genre_association, back_populates="books")

def main() -> None:
    # Create an SQLite database
    engine = create_engine("sqlite:///books.db", echo=True)

    # delete the database
    Base.metadata.drop_all(engine)
    # Create the tables in the database
    Base.metadata.create_all(engine)


    # Example of adding a new book to the database
    with Session(engine) as session:
        genre1 = Genre(name="Dystopian")
        genre2 = Genre(name="Science Fiction")
        genre3 = Genre(name="Political Fiction")

        session.add_all([genre1, genre2, genre3])
        session.commit()
        new_book = Book(title="1984", author="George Orwell", date_published=datetime.datetime(1984,1,1), genres=[genre1, genre3])

        session.add(new_book)
        session.commit()

if __name__ == "__main__":
    main()