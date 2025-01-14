from fastapi import Form
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from app.models.products import Products, Categories, JobText, Payment, Contacts


class ProductsService:

    @staticmethod
    async def add_prod(
        session: AsyncSession,
        name: str,
        size: str,
        price: int,
        url_photo: str,
        id_categories: int
    ) -> None:
        await session.execute(
            insert(Products).values(
                name=name,
                size=size,
                price=price,
                url_photo=url_photo,
                id_categories=id_categories
            )
        )
        await session.commit()
        return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def update_prod(
        id_product: int,
        name: str,
        session: AsyncSession,
        size: str | None = None,
        price: int | None = None,
        url_photo: str | None = None,
        id_categories: int | None = None,

    ) -> None:
        await session.execute(
            update(Products).where(
                Products.id == id_product
            ).values(
                name=name,
                size=size,
                price=price,
                url_photo=url_photo,
                id_categories=id_categories
            )
        )

        await session.commit()
        return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def delete_prod(
            id_product: int,
            session: AsyncSession
    ) -> None:
        await session.execute(
            delete(Products).where(
                Products.id == id_product
            )
        )

        await session.commit()
        return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def all_prod(
            session: AsyncSession
    ) -> None:
        result = await session.execute(
            select(Products)
        )

        return result.scalars().all()

    @staticmethod
    async def select_prod(
            session: AsyncSession
    ):
        result = await session.execute(
            select(
                Products.id,
                Categories.title,
                Products.name,
                Products.size,
                Products.price,
                Products.url_photo
            ).join(Categories, Products.id_categories == Categories.id)
        )
        return result.mappings().all()

    @staticmethod
    async def select_prod_in_cat(
            id_cat: int,
            session: AsyncSession
    ):
        result = await session.execute(
            select(Products).where(Products.id_categories == id_cat)
        )
        return result.scalars().all()

    @staticmethod
    async def get_product(
        id_product: int,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(Products).where(Products.id == id_product)
        )
        return result.scalars().all()

    @staticmethod
    async def add_text_job(
        session: AsyncSession,
        id: int = 1,
        text: str | None = Form(None)
    ):
        subq = await session.execute(
            select(JobText).where(JobText.id == id)
        )

        if subq.scalar() is None:
            await session.execute(
                insert(JobText).values(text=text)
            )
            await session.commit()
            return RedirectResponse(url='/admin', status_code=303)

        else:
            await session.execute(
                update(JobText).where(JobText.id == id).values(text=text)
            )
            await session.commit()
            return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def add_payments(
        session: AsyncSession,
        id: int = 1,
        text: str | None = Form(None)
    ):
        subq = await session.execute(
            select(Payment).where(Payment.id == id)
        )

        if subq.scalar() is None:
            await session.execute(
                insert(Payment).values(text=text)
            )
            await session.commit()
            return RedirectResponse(url='/admin', status_code=303)

        else:
            await session.execute(
                update(Payment).where(Payment.id == id).values(text=text)
            )
            await session.commit()
            return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def add_contact(
        session: AsyncSession,
        id: int = 1,
        text: str | None = Form(None)
    ):
        subq = await session.execute(
            select(Contacts).where(Contacts.id == id)
        )
        if subq.scalar() is None:
            await session.execute(
                insert(Contacts).values(text=text)
            )
            await session.commit()
            return RedirectResponse(url='/admin', status_code=303)

        else:
            await session.execute(
                update(Contacts).where(Contacts.id == id).values(text=text)
            )
            await session.commit()
            return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def get_job_text(
        session: AsyncSession,
    ):
        result = await session.execute(
            select(JobText)
        )

        return result.scalars().all()

    @staticmethod
    async def get_payment(
            session: AsyncSession,
    ):
        result = await session.execute(
            select(Payment)
        )

        return result.scalars().all()

    @staticmethod
    async def get_contact(
            session: AsyncSession,
    ):
        result = await session.execute(
            select(Contacts)
        )

        return result.scalars().all()