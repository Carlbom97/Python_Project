from fastapi import FastAPI
from db import call_db, print_db, update_db
from pydantic import BaseModel

class Game(BaseModel):
    id: int = None
    Home_Team: str
    Home_Team_id: int
    Away_Team: str
    Away_Team_id: int
    Home_Coach: str
    Away_Coach: str
    Home_Goals: int
    Away_Goals: int

class Player(BaseModel):
    id: int = None
    Name: str
    Team: str

class Name(BaseModel):
    Name: str




app = FastAPI()

@app.get("/")
def root():
    return "Standard Root"

@app.post("/add_game")
def add_game(game: Game):
    query = """
    INSERT INTO Games (Home_Team, Home_Team_id, Away_Team, Away_Team_id, Home_Coach, Away_Coach, Home_Goals, Away_Goals)
    VALUES (?,?,?,?,?,?,?,?)
    """
    call_db(query, game.Home_Team, game.Home_Team_id, game.Away_Team, game.Away_Team_id, game.Home_Coach, game.Away_Coach, game.Home_Goals, game.Away_Goals)
    return "Add a new game"

@app.post("/add_player")
def add_player(player: Player):
    query = """
    INSERT INTO Players (Name, Team)
    VALUES (?,?)
    """
    call_db(query, player.Name, player.Team)
    return "Add a new player"

@app.get("/get_results/{id}")
def get_results(id: int):
    
    query = "SELECT Home_Team, Away_Team, Home_Goals, Away_Goals FROM Games WHERE Home_Team_id = ?"
    data1 = call_db(query, id)
    query = "SELECT Home_Team, Away_Team, Home_Goals, Away_Goals FROM Games WHERE Away_team_id = ?"
    data2 = call_db(query, id)

    return data1, data2

@app.get("/get_players/{id}")
def get_players(id: int):

    query = "SELECT Team_Name FROM teams WHERE id = ?"
    data = call_db(query, id)
    team = data[0][0]
    query = f"SELECT Name FROM players WHERE team = '{team}'"
    data = call_db(query)
    return data

@app.put("/update_coach/{id}")
def update_coach(id: int, new_name: Name):
    query = """UPDATE teams SET Coach = ? WHERE id = ?"""
    call_db(query, new_name.Name ,id)
    return {"message": "Success"}


@app.put("/update_player/{id}")
def update_player(id: int, new_name: Name):
    query = """UPDATE players SET Team = ? WHERE id = ?"""
    call_db(query, new_name.Name ,id)
    return {"message": "Success"}

@app.delete("/delete_player/{id}")
def delete_player(id: int):
    delete_query = "DELETE FROM players WHERE id = ?"
    call_db(delete_query, id)
    return True