from user.user_repository import user_repository
from user.user_repository import User, Student, Librarian

class UserController:
    def __init__(self): pass

    def register_user(self, user_type : str, user_data : dict):
        user_id = user_data["user_id"]

        if user_repository.check_id(user_id):
            return False, "이미 존재하는 사용자 ID입니다."

        if user_type == "student":
            user = Student(
                user_id,
                user_data["password"],
                user_data["name"],
                user_data["phone"],
                user_data["email"],
                user_data["major"],
                user_data["preferred_genre"]
            )
        elif user_type == "librarian":
            user = Librarian(
                user_id,
                user_data["password"],
                user_data["name"],
                user_data["phone"],
                user_data["email"]
            )
        else:
            return False, "알 수 없는 사용자 유형입니다."

        user_repository.register_user(user)
        return user_id

    def modify_user(self, user_id, **kwargs):
        user = user_repository.get_user(user_id)
        if not user:
            return False, "존재하지 않는 사용자입니다."
        user.update(**kwargs)
        return True, "사용자 정보가 수정되었습니다."
    
    def change_password(self, user_id, current_password, new_password):
        user = user_repository.get_user(user_id)
        if not user:
            return False, "존재하지 않는 사용자입니다."

        if user.change_password(current_password, new_password):
            return True, "비밀번호가 성공적으로 변경되었습니다."
        else:
            return False, "현재 비밀번호가 일치하지 않습니다."

    def delete_user(self, user_id):
        result = user_repository.delete_user(user_id)
        if result:
            return True, "사용자 계정이 삭제되었습니다."
        return False, "삭제할 사용자를 찾을 수 없습니다."

    def get_user(self, user_id):
        return user_repository.get_user(user_id)

    def get_all_users(self):
        return user_repository.get_all_users()

user_controller = UserController()