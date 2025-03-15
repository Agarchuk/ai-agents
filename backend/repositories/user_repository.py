from backend.models.user import User
from utils.logger import log_info
from backend.clients.postgres_client import PostgresClient

class UserRepository:
    def __init__(self):
        self.session = PostgresClient.get_instance().Session()

    def add_user(self, user: User):
        """Add user to database."""
        self.session.add(user)
        self.session.commit()
        log_info(f"User added to database: {user.id}")
        return user

    def get_user_by_sub(self, sub: str):
        """Get user by sub."""
        return self.session.query(User).filter_by(sub=sub).first()
