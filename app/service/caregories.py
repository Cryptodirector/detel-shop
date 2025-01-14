from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.schemas.categories import CategoriesDTO
from app.models.products import Categories


class CategoriesService:

    @staticmethod
    async def add_cat(
        session: AsyncSession,
        title: str
    ) -> None:
        await session.execute(
            insert(Categories).values(title=title)
        )
        await session.commit()
        return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def update_cat(
        id_categories: int,
        title: str,
        session: AsyncSession
    ) -> None:
        await session.execute(
            update(Categories).where(
                Categories.id == id_categories
            ).values(title=title)
        )

        await session.commit()
        return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def delete_cat(
        id_categories: int,
        session: AsyncSession
    ) -> None:

        await session.execute(
            delete(Categories).where(
                Categories.id == id_categories
            )
        )

        await session.commit()
        return RedirectResponse(url='/admin', status_code=303)

    @staticmethod
    async def select_cat(
        session: AsyncSession
    ):
        result = await session.execute(
            select(Categories)
        )

        return [
            CategoriesDTO.model_validate(row, from_attributes=True)
            for row in result.scalars().all()
        ]

    @staticmethod
    async def check_category(
        id_category: int,
        session: AsyncSession,
    ):

        result = await session.execute(
            select(Categories).where(Categories.id == id_category)
        )

        return result.scalars().all()