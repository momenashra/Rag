from .BaseDataModel import BaseDataModel
from .db_shemas import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId


class AssetModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_clint=db_client)
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_ASSET_NAME.value
        ]  # TAKE COLLECTION

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        # Check if the collection already exists
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            # Create the collection
            self.collection = self.collection = self.db_client[
                DataBaseEnum.COLLECTION_ASSET_NAME.value
            ]
            # Create indexes for the collection
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(
            asset.model_dump(by_alias=True, exclude_unset=True)
        )
        # Check if the insertion was successful
        Asset.id = result.inserted_id
        return Asset  # Return the created project with the assigned _id

    async def get_asset(self, asset_project_id: str, asset_name: str):
        asset_record = await self.collection.find_one(
            {
                "asset_project_id": (
                    ObjectId(asset_project_id)
                    if isinstance(asset_project_id, str)
                    else asset_project_id
                ),
                "asset_name": asset_name,
            }
        )
        if asset_record:
            return Asset(**asset_record)
        return None

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        cursor = await self.collection.find(
            {
                "asset_project_id": (
                    ObjectId(asset_project_id)
                    if isinstance(asset_project_id, str)
                    else asset_project_id
                ),
                "asset_type": asset_type,
            }
        ).to_list(length=None)
        return [Asset(**record) for record in cursor]
