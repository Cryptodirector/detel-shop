from pydantic import BaseModel
from app.schemas.categories import CategoriesDTO


class CatDto(BaseModel):
    title: str


class ProductSchemas(BaseModel):
    name: str
    size: str
    price: int
    url_photo: str
    id_categories: int


class ProductDTO(BaseModel):
    id: int
    name: str
    size: str
    price: int
    url_photo: str | None = None
    id_categories: "CatDto" = None

