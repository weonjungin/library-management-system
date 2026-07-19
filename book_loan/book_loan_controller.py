from .book_loan_repository import book_loan_repository
from user.user_repository import user_repository
from book.book_repository import book_repository

class BookLoanController:
    MAX_BOOKS_PER_USER = 3                           

    def __init__(self): 
        pass  

    def borrow_book(self, user_id, book_id):
        user = user_repository.get_user(user_id)
        if not user:
            return False, "존재하지 않는 사용자입니다."

        if book_loan_repository.is_user_overdue(user_id):
            return False, "연체 중인 사용자는 대출할 수 없습니다."

        current_loans = book_loan_repository.get_current_loans_by_user(user_id)
        if len(current_loans) >= BookLoanController.MAX_BOOKS_PER_USER:
            return False, "최대 대출 권수를 초과하였습니다."

        if not book_repository.find_by_id(book_id):
            return False, "존재하지 않는 도서입니다."

        book_loan_repository.borrow_book(user_id, book_id)
        return True, "도서 대출이 완료되었습니다."

    def return_book(self, book_id):
        success = book_loan_repository.return_book(book_id)
        if success:
            return True, "도서 반납이 완료되었습니다."
        return False, "대출 중인 도서가 아닙니다."

    def extend_loan_date(self, book_id):
        # 구현 생략: 요구사항상 연장 기능은 고려하지 않음
        return False, "대출 기한 연장은 지원하지 않습니다."

    def email_overdue(self):
        overdue_users = book_loan_repository.get_overdue_users()
        for user_id in overdue_users:
            print(f"[연체 알림 메일] 사용자 {user_id}님, 연체된 도서를 반납해주세요.")
    
    def get_user_loans(self, user_id):
        return book_loan_repository.get_current_loans_by_user(user_id)

    def get_loan_by_book(self, book_id):
        return book_loan_repository.get_active_loan_by_book(book_id)

    def get_all_loans(self):
        return book_loan_repository.book_loan_list
    
book_loan_controller = BookLoanController()
