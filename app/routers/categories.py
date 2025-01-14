from typing import Annotated
from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.database import get_async_session
from app.routers.backend.categories import get_cat, get_prod, check_category, check_products, get_all_prod
from app.security.auth import protected_page
from app.service.caregories import CategoriesService
from app.service.products import ProductsService
router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse, response_model=None)
async def index(
    request: Request,
    categories: Annotated[dict, Depends(get_cat)],
    products: Annotated[dict, Depends(get_all_prod)]
):

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "categories": categories,
            "products": products
        }
    )


@router.get("/category/{id_cat}", response_class=HTMLResponse, response_model=None)
async def index(
    request: Request,
    categories: Annotated[dict, Depends(get_cat)],
    products: Annotated[dict, Depends(get_prod)]
):

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "categories": categories,
            "products": products
        }
    )


@router.get("/auth", response_class=HTMLResponse, response_model=None)
async def auth(
    request: Request,
):

    return templates.TemplateResponse(
        request=request, name="auth.html"
    )


@router.get("/admin", response_class=HTMLResponse, response_model=None)
async def auth(
    request: Request,
    categories: Annotated[dict, Depends(check_category)],
    products: Annotated[dict, Depends(check_products)],
    protected=Depends(protected_page),

):
    if protected:
        return templates.TemplateResponse(
            request=request,
            name="admin.html",
            context={
                'categories': categories,
                'products': products,
            }
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post("/category/add", response_model=None)
async def add_category(
    title: str = Form(),
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page)
):
    if protected:
        return await CategoriesService.add_cat(
            title=title,
            session=session
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post("/product/add", response_model=None)
async def add_product(
    name: str = Form(),
    size: str = Form(),
    price: int = Form(),
    url_photo: str = Form(),
    id_categories: int = Form(),
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page)
):
    if protected:
        return await ProductsService.add_prod(
            name=name,
            size=size,
            price=price,
            url_photo=url_photo,
            id_categories=id_categories,
            session=session
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.get('/product/{id_product}')
async def check_product(
    request: Request,
    id_product: int,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),
):
    if protected:
        product = await ProductsService.get_product(id_product=id_product, session=session)
        categories = await CategoriesService.select_cat(session=session)
        return templates.TemplateResponse(
            request=request,
            name="product.html",
            context={
                'categories': categories,
                'prod': product,  # Заворачиваем в список, так как в шаблоне используете цикл
            }
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post('/product/{id_product}/update')
async def update_product(
    id_product: int,
    name: str = Form(),
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),
    size: str | None = Form(None),  # Опциональный параметр
    price: int | None = Form(None),  # Опциональный параметр
    url_photo: str | None = Form(None),  # Опциональный параметр
    id_categories: int | None = Form(None),  # Опциональный параметр
):
    if protected:
        return await ProductsService.update_prod(
            id_product=id_product,
            name=name,
            size=size,
            price=price,
            url_photo=url_photo,
            session=session,
            id_categories=id_categories
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post('/product/{id_product}/delete')
async def delete_product(
    id_product: int,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),

):
    if protected:
        return await ProductsService.delete_prod(
            id_product=id_product,
            session=session,

        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.get('/category/check/{id_category}')
async def get_category(
    request: Request,
    id_category: int,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),

):
    if protected:
        category = await CategoriesService.check_category(
            session=session,
            id_category=id_category
        )
        return templates.TemplateResponse(
            request=request,
            name="categories.html",
            context={
                'categories': category,

            }
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post('/category/check/{id_category}/update')
async def update_category(
    id_category: int,
    title: str = Form(),
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),

):
    if protected:
        return await CategoriesService.update_cat(
            title=title,
            id_categories=id_category,
            session=session,
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post('/category/{id_category}/delete')
async def delete_category(
    id_category: int,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),

):
    if protected:
        return await CategoriesService.delete_cat(
            id_categories=id_category,
            session=session,
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@router.post('/job_text/update')
async def update_job_text(
    text: str | None = Form(None),
    id: int = 1,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),
):

    if protected:
        return await ProductsService.add_text_job(
            session=session,
            id=id,
            text=text
        )


@router.post('/payment/update')
async def update_payment(
    text: str | None = Form(None),
    id: int = 1,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),
):

    if protected:
        return await ProductsService.add_payments(
            session=session,
            id=id,
            text=text
        )


@router.post('/contact/update')
async def update_contact(
    text: str | None = Form(None),
    id: int = 1,
    session: AsyncSession = Depends(get_async_session),
    protected=Depends(protected_page),
):

    if protected:
        return await ProductsService.add_contact(
            session=session,
            id=id,
            text=text
        )


@router.get("/job_text", response_class=HTMLResponse, response_model=None)
async def job_text(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    get_job = await ProductsService.get_job_text(
        session=session
    )
    return templates.TemplateResponse(
        "job_text.html",
        {
            "request": request,
            "jobs": get_job
        }
    )


@router.get("/payments", response_class=HTMLResponse, response_model=None)
async def payment(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    payments = await ProductsService.get_payment(
        session=session
    )
    return templates.TemplateResponse(
        "payments.html",
        {
            "request": request,
            "payments": payments
        }
    )


@router.get("/contact", response_class=HTMLResponse, response_model=None)
async def contact(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    contacts = await ProductsService.get_contact(
        session=session
    )
    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "contacts": contacts
        }
    )