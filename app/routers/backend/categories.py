from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.service.caregories import CategoriesService
from app.service.products import ProductsService
from app.schemas.categories import CategoriesSchemas

router = APIRouter()


@router.get("/", response_model=None)
async def get_all_prod(
        session: AsyncSession = Depends(get_async_session)

):
    return await ProductsService.all_prod(session=session)


@router.get("/", response_model=None)
async def get_cat(
        session: AsyncSession = Depends(get_async_session)

):
    return await CategoriesService.select_cat(session=session)


@router.get("/category/{id_cat}", response_model=None)
async def get_prod(
        id_cat: int,
        session: AsyncSession = Depends(get_async_session)

):
    return await ProductsService.select_prod_in_cat(
        id_cat=id_cat,
        session=session
    )


@router.get("/all/category", response_model=None)
async def check_category(
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoriesService.select_cat(
        session=session
    )


@router.get('/all/products')
async def check_products(
        session: AsyncSession = Depends(get_async_session)
):
    return await ProductsService.select_prod(
        session=session
    )
