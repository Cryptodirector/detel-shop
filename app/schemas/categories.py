from fastapi import Form
from pydantic import BaseModel


class CategoriesSchemas(BaseModel):
    title: str = Form()


class CategoriesDTO(BaseModel):
    id: int | None = None
    title: str | None = None
