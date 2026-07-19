from datetime import datetime

class Book:
    def __init__(self, title, author, publisher, published_year, genre, isbn):
        self.__title = title
        self.__author = author
        self.__publisher = publisher
        self.__published_year = published_year
        self.__genre = genre
        self.__isbn = isbn
        self.__book_id = None

    @property
    def book_id(self): 
        return self.__book_id

    @book_id.setter
    def book_id(self, book_id): 
        self.__book_id = book_id

    @property
    def title(self): 
        return self.__title

    @property
    def author(self): 
        return self.__author

    @property
    def publisher(self): 
        return self.__publisher
    
    @property
    def published_year(self):
        return self.__published_year


    @property
    def genre(self): 
        return self.__genre

    def update(self, **kwargs):
        self.__title = kwargs.get("title", self.__title)
        self.__author = kwargs.get("author", self.__author)
        self.__publisher = kwargs.get("publisher", self.__publisher)
        self.__published_year = kwargs.get("published_year", self.__published_year)
        self.__genre = kwargs.get("genre", self.__genre)
        self.__isbn = kwargs.get("isbn", self.__isbn)

    def to_dict(self):
        return {
            "book_id": self.__book_id,
            "title": self.__title,
            "author": self.__author,
            "publisher": self.__publisher,
            "published_year": self.__published_year,
            "genre": self.__genre,
            "isbn": self.__isbn
        }

    
class BookRepository:
    def __init__(self):
        self.__book_list = []

    def generate_book_id(self):
        today = datetime.now().strftime("%Y%m%d")
        count = sum(1 for book in self.__book_list if book.book_id[:8] == today)
        return today + str(count + 1).zfill(2)

    def insert(self, book):
        self.__book_list.append(book)

    def delete(self, book_id):
        book = self.find_by_id(book_id)
        if book:
            self.__book_list.remove(book)
            return True
        return False

    def find_by_id(self, book_id):
        return next((book for book in self.__book_list if book.book_id == book_id), None)

    def find_all(self):
        return self.__book_list

    def find_by_title(self, title):
        return [book for book in self.__book_list if book.title == title]

    def find_by_author(self, author):
        return [book for book in self.__book_list if book.author == author]

    def find_by_genre(self, genre):
        return [book for book in self.__book_list if book.genre == genre]
    
    # === 도서 추천 ===
    def get_loaned_book_ids(self):
        return [loan.book_id for loan in self.book_loan_list if loan.status == "대출 중"]

    def get_available_books(self):
        from book_loan.book_loan_repository import book_loan_repository
        loaned_ids = book_loan_repository.get_loaned_book_ids()
        return [book for book in self.__book_list if book.book_id not in loaned_ids]


    def get_top_recent_books_by_genre(self, genre, limit=3):    
        books = [book for book in self.get_available_books() if book.genre == genre]
        books.sort(key=lambda book: book.to_dict()["published_year"], reverse=True)
        return books[:limit]


book_repository = BookRepository()