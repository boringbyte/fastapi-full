import uuid

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

from src.books.schemas import BookResponseModel, BookCreateModel, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", 'user'])


@book_router.get("/", response_model=list[BookResponseModel], dependencies=[Depends(role_checker)])
async def get_all_books(session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session=session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponseModel,
                  dependencies=[Depends(role_checker)])
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session),
                        user_details=Depends(access_token_bearer)) -> dict:
    """
        {
        "id": 11,
        "title": "Shadows of the Forgotten",
        "author": "Lena Morrell",
        "publisher": "Eclipse Press",
        "published_date": "2022-11-12",
        "page_count": 412,
        "language": "en"
      }
    """
    new_book = await book_service.create_book(book_data=book_data, session=session)
    return new_book


@book_router.get("/{book_uid}", response_model=BookResponseModel, dependencies=[Depends(role_checker)])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session),
                   user_details=Depends(access_token_bearer)) -> dict:
    book = await book_service.get_book(book_uid, session=session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find the book with id: {book_uid}")


@book_router.put("/{book_uid}", response_model=BookResponseModel, dependencies=[Depends(role_checker)])
async def update_book(book_uid: str, book_update_data: BookUpdateModel,
                      session: AsyncSession = Depends(get_session),
                      user_details=Depends(access_token_bearer)) -> dict:
    """
    {
		"title": "Shadows of the Forgotten",
		"author": "Lena Morrell",
		"publisher": "Eclipse Press",
		"page_count": 412,
		"language": "en"
    }
    """
    updated_book = await book_service.update_book(book_uid, book_update_data, session=session)
    if updated_book:
        return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Could not find the book with id: {book_uid}")


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_checker)])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session),
                      user_details=Depends(access_token_bearer)):
    deleted_book = await book_service.delete_book(book_uid, session=session)
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find the book with id: {book_uid}")
