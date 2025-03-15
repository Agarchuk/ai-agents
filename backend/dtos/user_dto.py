from dataclasses import dataclass, asdict

@dataclass
class UserDTO:
    """User DTO."""
    sub: str
    name: str
    email: str
    token: dict

    def to_dict(self):
        return asdict(self)
