from backend.models.user import User 
from backend.dtos.user_dto import UserDTO

class UserMapper:
    
    @staticmethod
    def map_user_model_to_dto(user_model: User, token: str) -> UserDTO:
        """Maps UserModel to UserDTO."""
        return UserDTO(id=user_model.id, sub=user_model.sub, name=user_model.name, email=user_model.email, token=token)

    @staticmethod
    def map_payload_to_user(payload: dict) -> User:
        """Maps payload to User."""
        return User(sub=payload.get("sub"), name=payload.get("name"), email=payload.get("email"))
