from schema import Room,Player
from crud import get_repository


class MeetingRoom:
    def __init__(self):
        self.room = get_repository("Room")
        
        
    async def create_meeting_room(self,player:Player)-> dict:
        room = await self.room.get_many()
        
        if len(room) > 2:
            return {"message": "room is full"}
        if room:
            members = len(room) 
        else:
            members = 1
        if player:
            await self.room.create(player)
            await self.room.edit_data({
                "members":members
            })
            
            return {f"message":"You joined the room.You are now {player.name}"}
       
    async def get_room_info(self,id)->dict:
        rooms = await self.room.get_many()
        for room in rooms:

            room_info = {
                "members":room.members,
                "player_A":{
                    "name":room.playerA.name,
                    "score":room.playerA.score
                },
                "player_b":{
                    "name":room.playerB.name,
                    "score":room.playerB.score
                    
                }
            }  

        return {"data":room_info}      

    async def update_score(self,score:int,player_name:str,room_id)-> dict:
        room = await self.room.get({
            id:room_id
        })
        if player_name == room.playerA.name:
            room.playerA.score = score
        elif player_name == room.playerB.name:
            room.playerB.score = score

        else:
            return {"message":f"player with  name, {player_name} not found"}

        return {"message":f"{player_name} score updated to {score}"}
    
    async def delete(self,room_id):
        
        room = room = await self.room.get({
            id:room_id
        })

        if room.playerA.score > room.playerB.score:
            return {"message":f"player with  Player A won"}
        elif room.playerA.score < room.playerB.score:
            return {"message":f"player with  Player B won"}
        else:
            {"message":"Match was a draw"}
        

