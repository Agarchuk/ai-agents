from backend.models.user import User
from backend.dtos.user_dto import UserDTO

class UserMapper:
    @staticmethod
    def map_payload_to_user(payload: dict):
        """Maps payload to User."""
        return User(sub=payload.get("sub"), name=payload.get("name"), email=payload.get("email"))

    @staticmethod
    def map_user_model_to_dto(user_model: User, token: str) -> UserDTO:
        """Maps UserModel to UserDTO."""
        return UserDTO(sub=user_model.sub, name=user_model.name, email=user_model.email, token=token)
