# Importerar de paket jag vill använda samt funktioner från andra filer
import requests
from db import call_db, print_db, get_value
from api import Game, Player, Name

# Skapar en funktion för ett enkelt kunna använda url till api
def url(route: str):
    return f"http://127.0.0.1:8000{route}"

# Skapar en funktion som printar ut menyn med de val som användaren har
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

# Skapar en funktion som kommer lägga till en match i databasen 
def add_game():
    # Printar ut för användaren vilka lag som finns i databasen 
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    #Sparar även detta som en vaiabel
    data = print_db(print_teams)

    # Skapar en tom lista för att spara alla inputs som är gilitga
    valid_input = []

    # Ger listan data genom att gå igenom data som sparar alla ids i listan
    for row in data:
        valid_input.append(row[0])

    # Skapar en while loop för att när ett ogiltigt val av hemma lag ges så börjar den om
    while True:
        Home_Team_id = input("ID of the Home Team: ")
        if Home_Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    # Samma med valet utav bortalag
    while True:
        Away_Team_id = input("ID of the Away Team: ")
        if Away_Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    # utifrån valen utav lag genom att välja id så hämtas nu infomration om lagen
    Home_Team = get_value(f"SELECT Team_Name FROM Teams WHERE id ={Home_Team_id}")
    Away_Team = get_value(f"SELECT Team_Name FROM Teams WHERE id ={Away_Team_id}")
    Home_Coach = get_value(f"SELECT Coach FROM Teams WHERE id = {Home_Team_id}")
    Away_Coach = get_value(f"SELECT Coach FROM Teams WHERE id = {Away_Team_id}")

    # Skapar en while loop för att användaren ska lägga in antal mål för lagen, är det inte en siffra så börjar loopen om
    while True:
        Home_Goals = input("Home team goals: ")
        if not str.isdigit(Home_Goals):
            print("Goals must be a number!")
            continue
        else:
            break
    while True:
        Away_Goals = input("Home team goals: ")
        if not str.isdigit(Away_Goals):
            print("Goals must be a number!")
            continue
        else:
            break

    # Skapar en ny vaiabel för klassen Game som jag hämtat från API och sparar datan i den
    new_game = Game(Home_Team=Home_Team, Home_Team_id=int(Home_Team_id), Away_Team=Away_Team, Away_Team_id=int(Away_Team_id), Home_Coach=Home_Coach, Away_Coach=Away_Coach, Home_Goals=int(Home_Goals), Away_Goals=int(Away_Goals))
    # Anropar API klassen för att genomföra POST requesten och informationen om den nya macthen läggs till i databasen.
    res = requests.post(url("/add_game"), json=new_game.dict())
    print(res)

# Skapar en funktion som kommer lägga till en spelare i databasen.
def add_player():
    # Användaren får skriva in namnet på spelaren sen printas de tillgängliga lagen ut 
    Player_Name = input("Type the players name: ")
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    data = print_db(print_teams)

    # Samma som förra funktionen där de giltiga inputsen sparas
    valid_input = []

    for row in data:
        valid_input.append(row[0])

    # While loop som startar om ifall användaren gen en ogiltig input om vilket lag spelaren tillhör
    while True:
        Team_id = input("Type the team id: ")
        if Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    # Hämtar lagnamnet från databasen utifån det id som angavs
    Team = get_value(f"SELECT Team_Name FROM Teams WHERE id = {Team_id}")
    # Skapar en variabel från klassen Players som finns skapan i API och lägger in de värden som ska läggas till i databasen
    new_player = Player(Name=Player_Name, Team=Team)
    # Anropar API klassen för att göra en POST request och spelaren kommer att läggas till i databasen
    res = requests.post(url("/add_player"), json=new_player.dict())
    print(res)

# Skapar en funktion som kommer hämta alla resultat från ett lag som användaren väljer
def get_results():
    # Printar ut de lagen som finns i databasen så att användaren vet
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    data = print_db(print_teams)

    # Samma som tidigare funktioner
    valid_input = []

    for row in data:
        valid_input.append(row[0])

    while True:
        Team_id = input("Please enter the teams id: ")
        if Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    
    # Anropar API klassen för att göra en GET request för att få datan för de matcherna som laget spelat
    res = requests.get(url(f"/get_results/{Team_id}"))

    for row in res.json():
        print(row)
    
# Skapar en funktion som kommer att hämta alla spelare från ett lag som användaren väljer
def get_players():
    # Printar ut alla tillgängliga lag
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    data = print_db(print_teams)

    # Samma funktion som tidigare funktioner
    valid_input = []

    for row in data:
        valid_input.append(row[0])

    while True:
        Team_id = input("Please enter the teams id: ")
        if Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break

    # Anropar API klassen för att göra en GET requet för att få alla spelare från det valda laget
    res = requests.get(url(f"/get_players/{Team_id}"))
    
    for row in res.json():
        print(row)
    
# Skapar en funktion för att uppdatera tränare hos ett lag
def update_coach():
    #Printar ut lagen som är tillgängliga
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    data = print_db(print_teams)

    # Samma funktion som tidigare funktioner
    valid_input = []

    for row in data:
        valid_input.append(row[0])

    while True:
        Team_id = input("Please enter the team id: ")
        if Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    # Ber användaren ange namnet för den nya tränaren
    name = input("Please enter the name of the new coach: ")
    # Sparar data i Name klassen
    new_name = Name(Name=name)
    # Anropar API och gör en PUT request som kommer att byta ut namnet för tränaren i laget som angavs
    res = requests.put(url(f"/update_coach/{Team_id}"), json=new_name.dict())
    print(res)

# Skapar en funktion som kommer att uppdatera lagen som en spelare spelar för
def update_player():
    # Printar ut de tillgängliga lagen
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    data = print_db(print_teams)

    # Samma funktion som tidigare funktioner
    valid_input = []

    for row in data:
        valid_input.append(row[0])

    while True:
        Team_id = input("Please enter the id of the team the player plays for: ")
        if Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    
    # Skapar en query för att hämta lagets namn som id tillhör
    query = f"""SELECT Team_Name FROM teams WHERE id = ?"""
    team_name = get_value(query, Team_id)
    # Printar ut de spalare som tillhör det valda laget
    print_players = """SELECT id, name FROM players WHERE team = ?"""
    data2 = print_db(print_players, team_name)

    # Skapar en till valid input med de id som tillhör spelarna i det valda laget
    valid_input2 = []

    for row in data2:
        valid_input2.append(row[0])

    while True:
        Player_id = input("Please enter the id of the player: ")
        if Player_id not in str(valid_input2):
            print("Please enter a valid input! Valid inputs:", valid_input2)
            continue
        else:
            break
    # Printar ut lagen igen för att användare ska kunna välja det nya laget som spelaren kommer tillhöra
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    print_db(print_teams)

    while True:
        new_team_id = input("Please enter the id of the new team: ")
        if new_team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    
    name = get_value(query, new_team_id)
    new_name = Name(Name=name)
    # Anropar API och gör en PUT request som kommer uppdatera laget för spelaren i databasen
    res = requests.put(url(f"/update_player/{Player_id}"), json=new_name.dict())
    print(res)

    

# Skapar en funktion för att deleta spelare från databasen
def delete_player():
    print_teams = """
        SELECT id, Team_Name from teams;
    """
    data = print_db(print_teams)

    valid_input = []
    for row in data:
        valid_input.append(row[0])

    while True:
        Team_id = input("Please enter the id of the team the player plays for: ")
        if Team_id not in str(valid_input):
            print("Please enter a valid input! Valid inputs:", valid_input)
            continue
        else:
            break
    
    # printar ut spelarna från de valda lagen
    query = f"""SELECT Team_Name FROM teams WHERE id = ?"""
    team_name = get_value(query, Team_id)
    print_players = """SELECT id, name FROM players WHERE team = ?"""
    data2 = print_db(print_players, team_name)

    valid_input2 = []

    for row in data2:
        valid_input2.append(row[0])

    while True:
        Player_id = input("Please enter the id of the player: ")
        if Player_id not in str(valid_input2):
            print("Please enter a valid input! Valid inputs:", valid_input2)
            continue
        else:
            break
    # Anropar API klassen för att göra en DELETE request så att spelaren tas bort från databasen
    res = requests.delete(url(f"/delete_player/{Player_id}"))
    print(res)
    
# Skapar en main funktion som kommer att vara den som körs och de funktioner som tidigare skapats anropas i den
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