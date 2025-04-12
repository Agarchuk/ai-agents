from pydantic import BaseModel

class DatasetTopic(BaseModel):
    dataset_topic: str

    class Config:
        arbitrary_types_allowed = True
    