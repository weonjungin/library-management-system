class SampleDataGenerator:

    @staticmethod
    def generate_book_data(book_controller):
        sample_books = [
            ("파이썬 프로그래밍", "홍길동", "한빛미디어", "2021", "SCI", "978-89-1234-0001"),
            ("자료구조와 알고리즘", "이몽룡", "생능출판사", "2020", "SCI", "978-89-1234-0002"),
            ("인간 본성의 심리학", "정도전", "심리출판", "2018", "HUM", "978-89-1234-0003"),
            ("세계 명작 단편선", "이서현", "문학동네", "2015", "LIT", "978-89-1234-0004"),
            ("미술로 보는 세계사", "김연아", "예술과지식", "2019", "ART", "978-89-1234-0005"),
            ("현대 소설 읽기", "박하늘", "창비", "2022", "FIC", "978-89-1234-0006"),
            ("기초 경제학", "최진기", "경제북스", "2017", "HUM", "978-89-1234-0007"),
            ("IT 트렌드 2024", "조영현", "한빛미디어", "2024", "SCI", "978-89-1234-0008"),
            ("클래식 음악 입문", "유재하", "예술북스", "2016", "ART", "978-89-1234-0009"),
            ("청소년을 위한 철학", "이기적", "철학출판", "2023", "HUM", "978-89-1234-0010"),
        ]

        for title, author, publisher, year, genre, isbn in sample_books:
            book_data = {
                "title": title,
                "author": author,
                "publisher": publisher,
                "published_year": year,
                "genre": genre,
                "isbn": isbn
            }
            book_controller.register_book(book_data)
            
    @staticmethod
    def generate_student_data(user_controller):
        sample_students = [
            ("s1001", "pass123", "김철수", "010-1234-5678", "kim@uni.ac.kr", "컴퓨터공학", "SCI"),
            ("s1002", "pass456", "이영희", "010-2345-6789", "lee@uni.ac.kr", "심리학", "HUM"),
            ("s1003", "pass789", "박민수", "010-3456-7890", "park@uni.ac.kr", "문예창작", "LIT"),
            ("s1004", "pass321", "최지우", "010-4567-8901", "choi@uni.ac.kr", "예술학", "ART"),
            ("s1005", "pass654", "정예린", "010-5678-9012", "jung@uni.ac.kr", "경제학", "HUM"),
            ("s1006", "pass987", "한지원", "010-6789-0123", "han@uni.ac.kr", "정보통신", "SCI"),
            ("s1007", "pass159", "오세훈", "010-7890-1234", "oh@uni.ac.kr", "경영학", "FIC"),
            ("s1008", "pass753", "배수지", "010-8901-2345", "bae@uni.ac.kr", "음악학", "ART"),
            ("s1009", "pass258", "김남준", "010-9012-3456", "nam@uni.ac.kr", "철학", "HUM"),
            ("s1010", "pass147", "장원영", "010-0123-4567", "jang@uni.ac.kr", "문헌정보", "SCI"),
        ]

        for user_id, password, name, phone, email, major, preferred_genre in sample_students:
            student_data = {
                "user_id": user_id,
                "password": password,
                "name": name,
                "phone": phone,
                "email": email,
                "major": major,
                "preferred_genre": preferred_genre
            }
            result = user_controller.register_user("student", student_data)
