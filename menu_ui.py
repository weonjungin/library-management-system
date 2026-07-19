from book.book_controller import book_controller
from user.user_controller import user_controller
from book_loan.book_loan_controller import book_loan_controller
from sample_data_generator import SampleDataGenerator
import unicodedata
from user.user_repository import Student, Librarian

USER_STUDENT = "1"
USER_LIBRARIAN = "2"

class MenuUI:
    def __init__(self):
        self.__user_type = None  # 1:학생사용자, 2:사서사용자
        self.__student_id = None
        self.menu_option = {
            11: self.register_user,   
            12: self.modify_user,
            13: self.change_password,
            14: self.delete_account,
            15: self.search_user,

            21: self.register_book,            
            22: self.modify_book,
            23: self.dispose_book,
            24: self.search_book,
            25: self.recommend_books,
            
            31: self.borrow_book,
            32: self.return_book,
            33: self.check_loan_status,
            34: self.search_book_loan,
            35: self.search_all_loans,
            0: self.exit_program
        }
        
        SampleDataGenerator.generate_book_data(book_controller)
        SampleDataGenerator.generate_student_data(user_controller)
        
 
    # === 사용자 관리 === 
    def register_user(self):
        print("\n[사용자 등록]")

        while True:
            role = input("사용자 유형을 입력하세요 (student/librarian): ").strip().lower()
            if role in ["student", "librarian"]:
                break
            print("잘못된 입력입니다. 'student' 또는 'librarian'을 입력해주세요.")

        user_id = input("사용자 ID (학번 또는 교직원 번호): ")
        name = input("이름: ")
        email = input("이메일: ")
        phone = input("전화번호: ")
        password = input("비밀번호: ")

        user_data = {
            "role": role,
            "user_id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "password": password
        }

        if role == "student":
            user_data["major"] = input("전공: ")

            print("선호 장르를 선택하세요:")
            print("1: ART\n2: SCIENCE\n3: HISTORY\n4: LITERATURE\n5: TECHNOLOGY")
            genre_map = {
                "1": "ART",
                "2": "SCIENCE",
                "3": "HISTORY",
                "4": "LITERATURE",
                "5": "TECHNOLOGY"
            }
            while True:
                genre_input = input("선호 장르 (번호 입력): ").strip()
                preferred_genre = genre_map.get(genre_input)
                if preferred_genre:
                    user_data["preferred_genre"] = preferred_genre
                    break
                print("숫자로 입력해주세요. 1~5 사이의 번호를 입력해주세요.")

        success, msg = user_controller.register_user(role, user_data)

        if success:
            print("등록이 완료되었습니다.")
            user = user_controller.get_user(user_id)
            self.display_user_info(user.to_dict())
        else:
            print(msg)

    def modify_user(self):
        print("\n[사용자 정보 수정]")
        user_id = input("수정할 사용자 ID: ")

        user = user_controller.get_user(user_id)
        if not user:
            print("사용자를 찾을 수 없습니다.")
            return

        print("수정 가능한 항목:")
        print("1. 이름  2. 전화번호  3. 이메일", end="")

        if isinstance(user, Student):
            print("  4. 전공  5. 선호 장르")
        else:
            print()

        key_map = {
            "1": "name",
            "2": "phone",
            "3": "email",
            "4": "major",
            "5": "preferred_genre"
        }

        selected = input("수정할 항목 번호 선택: ")
        key = key_map.get(selected)

        if not key:
            print("잘못된 선택입니다.")
            return
        
        if key == "preferred_genre":
            print("선호 장르를 선택하세요:")
            print("1: ART")
            print("2: SCIENCE")
            print("3: HISTORY")
            print("4: LITERATURE")
            print("5: TECHNOLOGY")
            genre_map = {
                "1": "ART",
                "2": "SCIENCE",
                "3": "HISTORY",
                "4": "LITERATURE",
                "5": "TECHNOLOGY"
            }
            genre_input = input("선호 장르 (번호 입력): ").strip()
            new_value = genre_map.get(genre_input)
            if not new_value:
                print("잘못된 입력입니다. 기본값 'ART'로 설정합니다.")
                new_value = "ART"
        else:
            new_value = input("새로운 값을 입력하세요: ")

        success, msg = user_controller.modify_user(user_id, **{key: new_value})
        print(msg)
        if success:
            user = user_controller.get_user(user_id)
            self.display_user_info(user.to_dict())
        
    def change_password(self):
        print("\n[비밀번호 변경]")
        user_id = input("사용자 ID: ")
        current_pw = input("현재 비밀번호: ")
        new_pw = input("새 비밀번호: ")
        success, msg = user_controller.change_password(user_id, current_pw, new_pw)
        print(msg)

    def delete_account(self):
        print("\n[사용자 삭제]")
        user_id = input("삭제할 사용자 ID: ")

        user = user_controller.get_user(user_id)
        if not user:
            print("사용자를 찾을 수 없습니다.")
            return

        confirm = input(f"정말로 사용자 '{user_id}'를 삭제하시겠습니까? (y/n): ")
        if confirm.lower() == 'y':
            success, msg = user_controller.delete_user(user_id)
            print(msg)
        else:
            print("삭제를 취소했습니다.")

    def search_user(self):
        print("\n[사용자 조회]")
        user_id = input("조회할 사용자 ID: ")
        user = user_controller.get_user(user_id)
        if user:
            self.display_user_info(user.to_dict())
        else:
            print("사용자를 찾을 수 없습니다.")

    def display_user_info(self, userDataDict): 
        print("\n[사용자 정보]")
        for key, value in userDataDict.items():
            print(f"{key}: {value}")

    def display_user_list(self, userList):
        print("\n[전체 사용자 목록]")
        for user in userList:
            self.display_user_info(user)
            print("-" * 30)
        print(f"총 {len(userList)}명 등록됨.")

    # --- 도서 추천 ---
    def recommend_books(self):
        user = user_controller.get_user(self.__student_id)
        if not user:
            print("사용자 정보를 찾을 수 없습니다.")
            return
        
        result = book_controller.recommend(user)
        if isinstance(result, str):
            print(result)
        else:
            print("📚 추천 도서 목록:")
            for book in result:
                print(f"- {book['title']} ({book['year']}) / {book['author']} / {book['publisher']} / {book['genre']}")

    

    # === 도서 관리 === 
    def register_book(self):    
        book_data_dict = {
            "title": input("제목: "),
            "author": input("저자: "),
            "publisher": input("출판사: "),
            "published_year": input("출판년도: "),
            "genre": input("장르(LIT:문학, FIC:소설, HUM:인문/사회, SCI:과학 기술, ART:예술): "),
            "isbn": input("isbn: ")
        }

        book_id = book_controller.register_book(book_data_dict)
        if book_controller.is_book_registered(book_id): 
            print(f"The book 'id:{book_id}, title:{book_data_dict.get('title')}' has been registered.")
            self.display_book_info(book_controller.get_book(book_id))

    def modify_book(self):  
        key_map = {  "1": "title",
                    "2": "author",
                    "3": "publisher",
                    "4": "published_year",
                    "5": "genre",
                    "6": "isbn" }
        
        book_id = input("수정하려는 book_id를 입력하세요: ")
        if not book_controller.is_book_registered(book_id): 
            print(f"등록된 book_id({book_id}가 아닙니다. ")
            return

        key_to_update = input("어떤 항목을 수정하시겠습니까?\n1.제목, 2.저자, 3.출판사, 4.출판년도, 5.장르, 6.isbn  : ")
        key = key_map.get(key_to_update)
        value = input("값을 입력하세요:")

        if book_controller.modify_book(book_id, **{key : value}):
            print(f"Book '{book_id}' modified.")
            self.display_book_info(book_controller.get_book(book_id))
            
    def dispose_book(self): 
        book_id = input("폐기하려는 book_id를 입력하세요: ")
        if book_controller.is_book_registered(book_id) == False: 
            print(f"등록된 book_id({book_id}가 아닙니다. ")
            return
        
        if book_controller.dispose_book(book_id):
             print(f"도서 '{book_id}'가 도서 목록에서 삭제되었습니다.")

    def search_book(self):  
        searchBy = input("검색조건을 입력하세요(1.전체, 2.book_id, 3.제목, 4.저자, 5.장르):").strip()
        match searchBy:
            case "1":
                book_list = book_controller.get_all_books()
                if book_list:
                    self.display_book_list(book_list)
                else:
                    print("등록된 도서가 없습니다.")
            
            case "2":
                book_id = input("book_id 입력: ").strip()
                book = book_controller.get_book(book_id)
                if book:
                    self.display_book_info(book)
                else:
                    print(f"book_id '{book_id}'에 해당하는 도서를 찾을 수 없습니다.")
            
            case "3":
                input_data = input("제목 입력: ").strip()
                books = book_controller.search_books(title = input_data)
                if books:
                    self.display_book_list(books)
                else:
                    print("해당 제목의 도서를 찾을 수 없습니다.")
               
            case "4":
                input_data = input("저자 입력: ").strip()
                books = book_controller.search_books(author=input_data)
                if books:
                    self.display_book_list(books)
                else:
                    print("해당 저자의 도서를 찾을 수 없습니다.")
                               
            case "5":
                input_data = input("장르(LIT:문학, FIC:소설, HUM:인문/사회, SCI:과학 기술, ART:예술) 입력: ").strip()
                books = book_controller.search_books(genre = input_data)
                if books:
                    self.display_book_list(books)
                else:
                    print("해당 장르의 도서를 찾을 수 없습니다.")
            
            case _:
                print("잘못된 입력입니다.")      
        
    def display_book_info(self, book_data_dict):   
        print(f"\n       book_id: {book_data_dict.get('book_id')}")
        print(f"        Title: {book_data_dict.get('title')}")
        print(f"       Author: {book_data_dict.get('author')}")
        print(f"    Publisher: {book_data_dict.get('publisher')}")
        print(f"PublishedYear: {book_data_dict.get('publishedYear')}")
        print(f"        Genre: {book_data_dict.get('genre')}")
        print(f"         isbn: {book_data_dict.get('isbn')}")

    def display_book_list(self, book_list): 
        print("\n")
        print("".ljust(90, "#"))
        print( self.pad('book_id', 20) + 
              self.pad('Title', 30) + 
              self.pad('Author', 14) + 
              self.pad('Genre', 10) + 
              self.pad('isbn', 20) )
        print("".ljust(90, "#"))

        for book in book_list:
            print(
                self.pad(book.get('book_id', ''), 20) +
                self.pad(book.get('title', ''), 30) +
                self.pad(book.get('author', ''), 14) +
                self.pad(book.get('genre', ''), 10) +
                self.pad(book.get('isbn', ''), 20)
            )
        print(f"\n* {len(book_list)}개의 도서가 검색되었습니다. *")
    
    # === 대출 관리 === 
    def borrow_book(self):
        user_id = input("사용자 ID를 입력하세요: ")
        if not user_controller.get_user(user_id):
            print(f"존재하지 않는 사용자 ID입니다: {user_id}")
            return
        book_id = input("대출할 도서 ID를 입력하세요: ")
        if not book_controller.is_book_registered(book_id):
            print(f"존재하지 않는 도서 ID입니다: {book_id}")
            return
        success, message = book_loan_controller.borrow_book(user_id, book_id)
        print(message)

    def return_book(self):
        book_id = input("반납할 도서 ID를 입력하세요: ")
        if not book_controller.is_book_registered(book_id):
            print(f"등록되지 않은 도서입니다: {book_id}")
            return
        
        success, message = book_loan_controller.return_book(book_id)
        print(message)

    def check_loan_status(self):
        user_id = input("사용자 ID를 입력하세요: ")
        if not user_controller.get_user(user_id):
            print(f"존재하지 않는 사용자입니다: {user_id}")
            return
        
        loans = book_loan_controller.get_user_loans(user_id)
        if not loans:
            print("현재 대출 중인 도서가 없습니다.")
        else:
            print(f"[{user_id}] 사용자의 현재 대출 목록:")
            for loan in loans:
                print(loan.to_dict())

    def search_book_loan(self):
        book_id = input("도서 ID를 입력하세요: ")
        loan = book_loan_controller.get_loan_by_book(book_id)
        if loan:
            print("해당 도서는 현재 대출 중입니다:")
            print(loan.to_dict())
        else:
            print("이 도서는 현재 대출 중이 아닙니다.")
            
    def displayBookLoanInfo(self, book_data_dict):
        if not book_data_dict:
            print("해당 도서에 대한 대출 정보가 없습니다.")
        else:
            print("대출 상세 정보:")
            for key, value in book_data_dict.items():
                print(f"{key}: {value}")

    def displayBookLoanList(self, bookLoanList):
        if not bookLoanList:
            print("등록된 대출 정보가 없습니다.")
        else:
            print("전체 대출 목록:")
            for loan in bookLoanList:
                self.displayBookLoanInfo(loan.to_dict())
                print("-" * 40)

    def search_all_loans(self):
        loans = book_loan_controller.get_all_loans()
        if not loans:
            print("현재 등록된 대출 기록이 없습니다.")
        else:
            print("[전체 대출 목록]")
            for loan in loans:
                self.displayBookLoanInfo(loan.to_dict())
                print("-" * 40)


    # === 그 밖의 === 
    def exit_program(self):
        print("프로그램을 종료합니다.")
        exit(0)

    @staticmethod
    def pad(text, width):
        def display_width(text):
            return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str(text))
        
        text = str(text)
        padding = width - display_width(text)
        return text + ' ' * padding

    def display_menu(self):
        """
        메인 메뉴를 출력하는 메서드
        """
        print("\n")

        if self.__user_type == USER_LIBRARIAN: 
            print("".ljust(80, "*"))
            print("도서관 시스템 (사서사용자)".center(80," "))
            print("".ljust(80, "*"))
            print("사용자 계정 관리                 도서 정보 관리              도서 대여 관리")
            print("11. 사용자 계정 등록             21. 도서 등록              31. 대출")
            print("12. 사용자 정보 수정             22. 도서정보 수정           32. 반납")
            print("13. 사용자 비밀번호 변경          23. 도서 폐기              33. 대출 연장")
            print("14. 사용자 계정 삭제             24. 도서 조회               34. 대출상태확인")
            print("15. 사용자 정보 조회                                         35. 대출 조회")  
        elif self.__user_type == USER_STUDENT:    
            print("".ljust(50, "*"))
            print(f"도서관 시스템(학생사용자:{self.__student_id})".center(50," "))
            print("".ljust(50, "*"))            
          
            print("12. 사용자 정보 수정")
            print("13. 사용자 비밀번호 변경")
            print("14. 사용자 탈퇴")
            print("15. 사용자 정보 조회")
            
            print("24. 도서 조회 ")
            print("25. 도서 추천 ")
            
            print("31. 대출")
            print("34. 대출상태확인")
            print("35. 대출 조회")
        else:
            print(f"사용자 구분이 잘못입력되었습니다.{self.__user_type}")
        
        print("\n0. 종료")

    def handle_choice(self, choice):
        """
        사용자의 선택을 처리하는 메서드
        """
        menu_option = self.menu_option.get(choice)
        if menu_option:
            menu_option()
        else:
            print("\n-->해당 기능은 아직 구현되지 않았거나 잘못된 입력입니다. 다시 시도해주세요.\n")

    def run(self):
        self.__user_type = input("사용자를 구분해주세요. (1.학생사용자, 2.사서): ")
        if self.__user_type == USER_STUDENT:
            self.__student_id = input("학번을 입력해주세요: ")
            # TODO: 사용자관리 개발 후 등록된 학번 확인 루틴 추가 필요

        while True:
            self.display_menu()
            try:
                choice = int(input("원하는 작업의 번호를 입력하세요: "))
                self.handle_choice(choice)
            
            except ValueError:
                print("숫자로 입력해주세요. 다시 시도해주세요.")


