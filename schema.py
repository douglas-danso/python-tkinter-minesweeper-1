from pydantic import BaseModel


class Player(BaseModel):

    name:str
    score:int

class Room(BaseModel):
    members:int = 0
    playerA:Player = None
    playerB:Player = None


