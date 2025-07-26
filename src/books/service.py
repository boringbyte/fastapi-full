from datetime import datetime
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel
from src.books.models import BookTable


class BookService:

    async def get_all_books(self, session: AsyncSession):
        stmt = select(BookTable).order_by(desc(BookTable.created_at))
        result = await session.exec(stmt)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        stmt = select(BookTable).where(BookTable.uid == book_uid)
        result = await session.exec(stmt)
        book = result.first()
        return book if book else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = BookTable(**book_data_dict)
        new_book.published_date = datetime.strptime(book_data_dict["published_date"], "%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update:
            book_update_dict = update_data.model_dump()
            for k, v in book_update_dict.items():
                setattr(book_to_update, k, v)
            await session.commit()
            return book_to_update
        return

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
        else:
            return
