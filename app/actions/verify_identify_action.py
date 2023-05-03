from fastapi import HTTPException, Request
from app.models.data_identification_model import DataIdentificationModel
from app.repositories import UserDataRepository, DefaultDataRepository


_user_repo = UserDataRepository()
_default_repo = DefaultDataRepository()


class VerifyIdentityAction(object):
    def extract_identifier(self, identifier_header) -> DataIdentificationModel:
        """
        Extracts the identifier from the header and returns it as a DataIdentificationModel
        :param identifier_header: The identifier header
        :return: The identifier as a DataIdentificationModel
        """
        identifier = identifier_header.split(' ')
        if len(identifier) != 3:
            raise HTTPException(status_code=422, detail=f"Invalid identifier: {identifier_header}")
        return DataIdentificationModel(application=identifier[0], release=identifier[1], name=identifier[2])

    def extract_client(self, client_header) -> str:
        """
        Extracts the client from the header and returns it as a string
        :param client_header: The client header
        :return: The client as a string
        """
        if client_header is None:
            raise HTTPException(status_code=422, detail="Missing client identifier")
        return client_header

    async def find_client_data_by_header(self, request: Request, db):
        """
        Finds the data for the client and identifier in the request
        :param request: The request
        :param db: The database
        :return: The data for the client and identifier in the request
        """
        client = self.extract_client(request.headers.get('client'))
        identifier = self.extract_identifier(request.headers.get('identifier'))
        db_filter = identifier.create_filter()
        db_filter['client'] = client
        return await _user_repo.get_one(db_filter, db)

    async def find_default_data_by_header(self, request: Request, db):
        """
        Finds the default data for the identifier in the request
        :param request: The request
        :param db: The database
        :return: The default data for the identifier in the request
        """
        identifier = self.extract_identifier(request.headers.get('identifier'))
        db_filter = identifier.create_filter()
        return await _default_repo.get_one(db_filter, db)

    async def exist_default_data_by_header(self, request: Request, db):
        """
        Checks if the default data for the identifier in the request exists
        :param request: The request
        :param db: The database
        :return: True if the default data exists, False otherwise
        """
        identifier = self.extract_identifier(request.headers.get('identifier'))
        db_filter = identifier.create_filter()
        return await _default_repo.exists(db_filter, db)

    async def exist_default_data(self, identifier: DataIdentificationModel, db):
        """
        Checks if the default data for the identifier in the request exists
        :param identifier: The identifier
        :return: True if the default data exists, False otherwise
        """
        db_filter = identifier.create_filter()
        return await _default_repo.exists(db_filter, db)

    async def exist_user_data(self, identifier: DataIdentificationModel, db):
        """
        Checks if the user data for the identifier in the request exists
        :param identifier: The identifier
        :return: True if the default data exists, False otherwise
        """
        db_filter = identifier.create_filter()
        res = await _user_repo.exists(db_filter, db)
        return res
