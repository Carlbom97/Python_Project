import requests
from db import call_db, print_db, get_value
from api import Game, Player, Name
from typing import List

def url(route: str):
    return f"http://127.0.0.1:8000{route}"

def print_menu():
    print(
        """
        1. Add Game
        2. Add Player
        3. Get Results
        4. Get Players
        5. Update Coach
        6. Update Player
        7. Delete Player
        8. Exit
        """
    )

def add_game():
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    print_db(print_teams)
    Home_Team_id = int(input("ID of the Home Team: "))
    Away_Team_id = int(input("ID of the Away Team: "))
    Home_Team = get_value(f"SELECT Team_Name FROM Teams WHERE id ={Home_Team_id}")
    Away_Team = get_value(f"SELECT Team_Name FROM Teams WHERE id ={Away_Team_id}")
    Home_Coach = get_value(f"SELECT Coach FROM Teams WHERE id = {Home_Team_id}")
    Away_Coach = get_value(f"SELECT Coach FROM Teams WHERE id = {Away_Team_id}")
    Home_Goals = int(input("Home team goals: "))
    Away_Goals = int(input("Home team goals: "))

    new_game = Game(Home_Team=Home_Team, Home_Team_id=Home_Team_id, Away_Team=Away_Team, Away_Team_id=Away_Team_id, Home_Coach=Home_Coach, Away_Coach=Away_Coach, Home_Goals=Home_Goals, Away_Goals=Away_Goals)
    res = requests.post(url("/add_game"), json=new_game.dict())
    print(res)

def add_player():
    Player_Name = input("Type the players name: ")
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    print_db(print_teams)
    Team_id = input("Type the team id: ")
    Team = get_value(f"SELECT Team_Name FROM Teams WHERE id = {Team_id}")
    new_player = Player(Name=Player_Name, Team=Team)
    res = requests.post(url("/add_player"), json=new_player.dict())
    print(res)

def get_results():
    team_id = int(input("Please enter the teams id: "))
    res = requests.get(url(f"/get_results/{team_id}"))

    for row in res.json():
        print(row)
    

def get_players():
    team_id = input("Please enter the teams id: ")
    res = requests.get(url(f"/get_players/{team_id}"))
    
    for row in res.json():
        print(row)
    

def update_coach():
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    print_db(print_teams)
    team_id = int(input("Please enter the team id: "))
    name = input("Please enter the name of the new coach: ")
    new_name = Name(Name=name)
    res = requests.put(url(f"/update_coach/{team_id}"), json=new_name.dict())
    print(res)

def update_player():
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    print_db(print_teams)
    team_id = int(input("Please enter the id of the team the player plays for: "))
    query = f"""SELECT Team_Name FROM teams WHERE id = ?"""
    team_name = get_value(query, team_id)
    print_players = """SELECT id, name FROM players WHERE team = ?"""
    print_db(print_players, team_name)
    player_id = int(input("Please enter the id of the player: "))
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    print_db(print_teams)
    new_team_id = int(input("Please enter the id of the new team: "))
    name = get_value(query, new_team_id)
    new_name = Name(Name=name)
    res = requests.put(url(f"/update_player/{player_id}"), json=new_name.dict())
    print(res)

    


def delete_player():
    delete_player = input("Type the id of the player to delete: ")
    if not str.isdigit(delete_player):
        print("Id is a number!")
        return
    res = requests.delete(url(f"/delete_player/{delete_player}"))
    print(res)
    

def main():
    print_menu()
    choise = input("Choose your action: ")
    choise = choise.strip()
    if not str.isdigit(choise):
        print("Invalid input, please enter a number from the menu!")
        return

    match int(choise):
        case 1:
            add_game()
        case 2:
            add_player()
        case 3:
            get_results()
        case 4:
            get_players()
        case 5:
            update_coach()
        case 6:
            update_player()
        case 7:
            delete_player()
        case 8:
            exit()
        case _:
            print("Not a valid choise, try again.")
while __name__ == "__main__":
    main()