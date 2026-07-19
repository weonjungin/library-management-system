# library-management-system

캡슐화, 단일 책임 원칙, 다형성, 추상화 등 객체지향 설계 원칙을 적용해 만든 콘솔 기반 도서관 도서 대출·추천 시스템입니다.

## 개요

도서관을 모델로, 학생·사서 사용자가 도서 검색·대출·반납·추천 기능을 이용할 수 있는 시스템을 설계·구현했습니다. UI–Controller–Repository 계층으로 역할을 분리해 각 클래스가 하나의 책임만 지도록 설계했습니다.

## 주요 기능

- **도서관리**: 도서 등록/수정/폐기, BookID·제목·저자·장르 기반 검색
- **사용자관리**: 학생/사서 계정 등록·수정·삭제, 비밀번호 변경
- **대출관리**: 도서 대출(최대 3권, 기본 2주)·반납, 연체 확인
- **도서추천**: 학생의 선호 장르 기반 대출 가능 도서 추천 (최신 출판순 최대 3권)

## 아키텍처

```
MenuUI (UI 계층)
  ↓
BookController / UserController / BookLoanController (제어 계층)
  ↓
BookRepository / UserRepository / BookLoanRepository (저장소 계층)
```

- **UI 계층**: 사용자 입력을 받고 결과를 출력. 로직은 Controller에 위임
- **Controller 계층**: 기능 흐름을 제어하며 UI와 Repository 사이를 중재
- **Repository 계층**: 데이터 저장·검색·수정 담당

## 적용한 객체지향 개념

- **캡슐화**: User, Book, BookLoan 등 도메인 객체는 내부 데이터를 직접 노출하지 않고 정의된 메서드로만 접근
- **단일 책임 원칙**: Controller/Repository/UI 각각 하나의 책임만 담당하도록 계층 분리
- **다형성**: 사용자 등록 시 입력 유형에 따라 Student 또는 Librarian 객체 생성, 공통 부모 클래스 User 상속
- **추상화**: MenuUI는 입력·출력만 처리하고 실제 로직은 Controller에 위임

## 실행 방법

```
python main.py
```

## 프로젝트 구조

```
library-management-system/
├── main.py                        # 진입점
├── menu_ui.py                     # UI 계층
├── sample_data_generator.py       # 샘플 데이터 생성
├── book/
│   ├── book_controller.py
│   └── book_repository.py
├── book_loan/
│   ├── book_loan_controller.py
│   └── book_loan_repository.py
└── user/
    ├── user_controller.py
    └── user_repository.py
```

## 알려진 한계 및 향후 개선 방향

- 로그인 후 사용자 인증이 세션으로 유지되지 않아, 기능마다 사용자 ID를 재입력하는 구조 (추후 세션 기반 인증 도입 예정)
- 모든 데이터가 메모리에만 저장되어 프로그램 종료 시 소실 (JSON/SQLite 기반 영구 저장으로 확장 가능)
- 도서 추천은 현재 선호 장르 기반 단순 필터링 방식 (대출 이력·평점 기반 알고리즘으로 고도화 가능)

## 개발 환경

- Python 3.12+
