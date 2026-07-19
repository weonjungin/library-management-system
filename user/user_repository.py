class User:
    def __init__(self, user_id, password, name, phone, email):
        self._user_id = user_id
        self._password = password
        self._name = name
        self._phone = phone
        self._email = email

    @property
    def user_id(self): 
        return self._user_id  
    
    def update(self, **kwargs):
        self._name = kwargs.get("name", self._name)
        self._phone = kwargs.get("phone", self._phone)
        self._email = kwargs.get("email", self._email)
    
    def change_password(self, current_password, new_password):
        if current_password == self._password:
            self._password = new_password
            return True
        else : 
            return False

    def to_dict(self):
        return {
            "user_id" : self._user_id,
            "name" : self._name,
            "phone" : self._phone,
            "email" : self._email
        }
    
class Student(User):
    def __init__(self, user_id, password, name, phone, email, major, preferred_genre):
        super().__init__(user_id, password, name, phone, email)
        self.__major = major
        self.__preferred_genre = preferred_genre

    @property
    def major(self):
        return self.__major
    
    @property
    def preferred_genre(self):
        return self.__preferred_genre

    def update(self, **kwargs):
        if "major" in kwargs:
            self.__major = kwargs["major"]
        if "preferred_genre" in kwargs:
            self.__preferred_genre = kwargs["preferred_genre"]
        super().update(**kwargs)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "major": self.__major,
            "preferred_genre": self.__preferred_genre
        })
        return data
    
class Librarian(User):
    def __init__(self, user_id, password, name, phone, email):
        super().__init__(user_id, password, name, phone, email)
        # level, 권한 관리 기능은 생략됨 (요구사항 반영)

class UserRepository:
    def __init__(self):
        self._userList = []  

    def register_user(self, user):
        if self.check_id(user.user_id):
            return False
        self._userList.append(user)
        return True

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if user:
            self._userList.remove(user)
            return True
        return False

    def check_id(self, user_id):
        return any(user.user_id == user_id for user in self._userList)

    def get_user(self, user_id):
        return next((user for user in self._userList if user.user_id == user_id), None)

    def get_all_users(self):
        return self._userList[:]

user_repository = UserRepository()