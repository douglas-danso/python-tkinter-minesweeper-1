from beanie import Document

import schema


class Room(Document, schema.Room):
    class Settings:
        name = 'room'