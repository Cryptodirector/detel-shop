from app.database import Base

from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship
)

from sqlalchemy import ForeignKey


class Categories(Base):

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[list["Products"]] = relationship(
        "Products",
        back_populates="category",
        cascade="all, delete-orphan"  # Каскадное удаление и удаление сирот
    )


class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    url_photo: Mapped[str] = mapped_column(nullable=True)
    id_categories: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=True
    )

    category: Mapped["Categories"] = relationship(
        "Categories",
        back_populates="products"
    )


class JobText(Base):
    __tablename__ = 'job_text'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=True)


class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=True)


class Contacts(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=True)