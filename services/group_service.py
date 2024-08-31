import aiofiles
from typing import List
import json
import constants


class GroupService:
    __service = None

    def __new__(cls):
        if cls.__service is None:
            cls.__service = super().__new__(cls)

        return cls.__service

    def __init__(self, filename: str = constants.GROUPS_FILE) -> None:
        self.filename = f"data/{filename}"

    async def load_groups(self) -> List[str]:
        try:
            async with aiofiles.open(self.filename, "r") as file:
                content = await file.read()
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    async def save_groups(self, groups: List[str]) -> None:
        async with aiofiles.open(self.filename, "w") as file:
            await file.write(json.dumps(groups))

    async def add_group(self, chat_id: str) -> None:
        groups = await self.load_groups()
        if chat_id not in groups:
            groups.append(chat_id)
            await self.save_groups(groups)

    async def remove_group(self, chat_id: str) -> None:
        groups = await self.load_groups()
        print(chat_id, groups)
        if chat_id in groups:
            groups = [group for group in groups if group != chat_id]
            await self.save_groups(groups)

    async def get_groups(self):
        return await self.load_groups()
