from datetime import datetime, timedelta

class BookLoan:
    def __init__(self, user_id, book_id):
        self.__id = f"{user_id}_{book_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.__user_id = user_id
        self.__book_id = book_id
        self.__loan_date = datetime.now()
        self.__due_date = self.__loan_date + timedelta(days=14)
        self.__return_date = None
        self.__status = "대출 중"

    
    @property
    def ID(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def book_id(self):
        return self.__book_id

    @property
    def loan_date(self):
        return self.__loan_date

    @property
    def due_date(self):
        return self.__due_date

    @property
    def return_date(self):
        return self.__return_date

    @property
    def status(self):
        return self.check_status()

    
    def borrow_book(self):
        self.__loan_date = datetime.now()
        self.__due_date = self.__loan_date + timedelta(days=14)
        self.__return_date = None
        self.__status = "대출 중"

    def return_book(self):
        self.__return_date = datetime.now()
        self.__status = "반납 완료"

    def extend_loan(self):
        self.__due_date += timedelta(days=7)

    def check_status(self):
        if self.__status == "대출 중" and datetime.now() > self.__due_date:
            return "연체"
        return self.__status

    def to_dict(self):
        return {
            "loan_id": self.ID,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date.strftime("%Y-%m-%d"),
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "return_date": self.return_date.strftime("%Y-%m-%d") if self.return_date else None,
            "status": self.status
        }


class BookLoanRepository:
    def __init__(self):
        self.book_loan_list = []

    def borrow_book(self, user_id, book_id):
        loan = BookLoan(user_id, book_id)
        self.book_loan_list.append(loan)
        return loan.ID

    def return_book(self, book_id):
        loan = self.get_active_loan_by_book(book_id)
        if loan:
            loan.return_book()
            return True
        return False

    def get_active_loan_by_book(self, book_id):
        for loan in self.book_loan_list:
            if loan.book_id == book_id and loan.status == "대출 중":
                return loan
        return None

    def get_current_loans_by_user(self, user_id):
        return [loan for loan in self.book_loan_list if loan.user_id == user_id and loan.status == "대출 중"]

    def is_user_overdue(self, user_id):
        for loan in self.book_loan_list:
            if loan.user_id == user_id and loan.status == "연체":
                return True
        return False

    def get_overdue_users(self):
        overdue_users = set()
        for loan in self.book_loan_list:
            if loan.status == "연체":
                overdue_users.add(loan.user_id)
        return list(overdue_users)
    
    def get_loaned_book_ids(self):
        return [loan.book_id for loan in self.book_loan_list if loan.status == "대출 중"]


book_loan_repository = BookLoanRepository()
