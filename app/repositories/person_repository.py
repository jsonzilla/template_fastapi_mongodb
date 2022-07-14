from app.repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository):
    def __init__(self):
        super().__init__('_person_collection')
