from utils.logger import log_warning, log_info, log_error
from backend.repositories.user_repository import UserRepository
from backend.mappers.user_mapper import UserMapper
from backend.models.user import User

class UserService:
    def __init__(self, user_repository: UserRepository, user_mapper: UserMapper):
        self.user_mapper = user_mapper
        self.user_repository = user_repository

    def get_or_save_user_to_db(self, user: User) -> User:
        if not user or not hasattr(user, 'sub') or not user.sub:
            log_warning("Cannot save user: Invalid user object or missing sub")
            return None
            
        try:
            db_user = self.get_user_by_sub(user.sub)
            if db_user is None:
                log_info(f"User {user.sub} not found, adding to database")
                db_user = self.user_repository.add_user(user)
                if db_user:
                    log_info(f"User {user.sub} saved to database")
                    return db_user
                else:
                    log_warning(f"Failed to save user {user.sub} to database")
                    return None
            else:
                log_info(f"User {user.sub} already exists in database")
                return db_user
        except Exception as e:
            log_error("Error saving user to database: %s", str(e))
            return None

    def get_user_by_sub(self, sub: str):
        if not sub:
            log_warning("Cannot get user: Missing sub")
            return None
            
        try:
            user = self.user_repository.get_user_by_sub(sub)
            if user is None:
                log_warning(f"No user found with sub: {sub}")
                return None
            return user
        except Exception as e:
            log_error("Error getting user by sub: %s", str(e))
            return None
