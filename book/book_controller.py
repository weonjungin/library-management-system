from .book_repository import Book   
from .book_repository import book_repository    
from book_loan.book_loan_repository import book_loan_repository

class BookController:
    def __init__(self): pass    

    # === Register, Modify, Dispose === (사서 사용자)
    def register_book(self, book_data: dict):  
        book = Book(    
            book_data["title"],
            book_data["author"],
            book_data["publisher"],
            book_data["published_year"],
            book_data["genre"],
            book_data["isbn"]
        )

        book_id = book_repository.generate_book_id()     
        book.book_id = book_id                          

        book_repository.insert(book)                    
        return book_id

    def modify_book(self, book_id, **kwargs):   
        book = book_repository.find_by_id(book_id)  
        if book:
            book.update(**kwargs)
            return True
        return False

    def dispose_book(self, book_id):    
        return book_repository.delete(book_id)

    # === Check ===
    def is_book_registered(self, book_id):  
        if book_repository.find_by_id(book_id):
            return True
        else :
            return False

    # === Get/Search Book ===   
    def get_book(self, book_id):    
        book = book_repository.find_by_id(book_id)
        if book:
            return book.to_dict()
        else:
            return None

    def get_all_books(self):    
        books = book_repository.find_all()
        return [book.to_dict() for book in books]

    def search_books(self, **kwargs):   
        if "title" in kwargs:
            books = book_repository.find_by_title(kwargs["title"])
        elif "author" in kwargs:
            books = book_repository.find_by_author(kwargs["author"])
        elif "genre" in kwargs:
            books = book_repository.find_by_genre(kwargs["genre"])
        else:
            books = []

        return [book.to_dict() for book in books]
    
    # === 도서 추천 ===
    def recommend(self, user):
        if not user.preferred_genre:
            return "선호 장르를 먼저 등록해주세요."

        books = book_repository.get_top_recent_books_by_genre(user.preferred_genre)
        if not books:
            return "추천할 도서가 없습니다."

        return [{
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "year": book.published_year,
            "genre": book.genre
        } for book in books]



book_controller = BookController()  # 공용 인스턴스를 통해 사용.
