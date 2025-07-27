class Player:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

def play():
    players = [
        Player(1, "Alice", 16),
        Player(2, "Bob", 17),
        Player(3, "Charlie", 19)
    ]
    print("Welcome to play the game, players are:")
    for player in players:
        print(f"Player {player.id}: {player.name},{player.age} years old")

if __name__ == "__main__":
    play()


