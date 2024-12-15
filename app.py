from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from meeting_room import MeetingRoom
from schema import Player
from connection_manager import manager
from minesweeper import Minesweeper, main

app = FastAPI()

@app.get("/")
def home():
    return {"message":"welcome"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
           
            meeting_room = MeetingRoom()
            player_A:Player = {
                "name":"Player A",
                "score":0
            }
            
            player_B:Player = {
                "name":"Player B",
                "score":0
            }
            room = await meeting_room.get_room_info()
            print(room["members"])
            if room["members"]== 0:
                await meeting_room.create_meeting_room(player_A)
                message = "You have joined as Player A, waiting for Player B"
                await manager.send_message(message, websocket)
                print(room["members"])
            if room["members"] ==1:
                await meeting_room.create_meeting_room(player_B)
                message = "You have joined as Player B, game can start"
                await manager.send_message(message, websocket)
                main()


            data = await websocket.receive_text()
            await manager.send_message(f"Client {client_id}: {data}", websocket)
            
            await manager.broadcast(f"Client {client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")