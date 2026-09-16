# Escape Room Text Game - OOP Project

class Item:
    def __init__(self, name, description):
        self.name = name.lower()
        self.description = description


class KeyItem(Item):
    pass


class ClueItem(Item):
    pass


class Puzzle:
    def __init__(self, question, answer, hint, reward=None):
        self.question = question
        self.answer = answer.lower()
        self.hint = hint
        self.reward = reward
        self.solved = False

    def solve(self, user_answer):
        if self.solved:
            print("This puzzle is already solved.")
            return None

        if user_answer.lower() == self.answer:
            self.solved = True
            print("Correct! Puzzle solved.")
            return self.reward

        print("Wrong answer! Try again.")
        return None


class Room:
    def __init__(self, name, description, puzzle=None):
        self.name = name
        self.description = description
        self.items = []
        self.connections = {}
        self.puzzle = puzzle

    def connect(self, direction, room):
        self.connections[direction.lower()] = room


class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None
        self.score = 0

    def has_item(self, item_name):
        return any(item.name == item_name.lower() for item in self.inventory)

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:", ", ".join(item.name.title() for item in self.inventory))


class GameEngine:
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.game_running = True
        self.create_game()

    def create_game(self):
        # Puzzles
        library_puzzle = Puzzle(
            "I follow you everywhere, but disappear in darkness. What am I?",
            "shadow",
            "Think about light."
        )

        kitchen_puzzle = Puzzle(
            "What number comes after 41?",
            "42",
            "It is the next number."
        )

        basement_puzzle = Puzzle(
            "What has hands but cannot clap?",
            "clock",
            "It tells time."
        )

        # Rooms
        entrance = Room("Entrance Hall", "A dusty hall with a broken chandelier.")
        library = Room("Library", "Old books cover every wall.", library_puzzle)
        kitchen = Room("Kitchen", "A cold kitchen with an old locked cabinet.", kitchen_puzzle)
        basement = Room("Basement", "A dark basement. Strange noises surround you.", basement_puzzle)
        secret_room = Room("Secret Room", "A hidden room containing the exit door.")
        exit_room = Room("Exit Door", "A huge wooden door leading outside.")

        # Connections
        entrance.connect("library", library)
        entrance.connect("kitchen", kitchen)
        library.connect("entrance", entrance)
        kitchen.connect("entrance", entrance)
        kitchen.connect("basement", basement)
        basement.connect("kitchen", kitchen)
        basement.connect("secret room", secret_room)
        secret_room.connect("basement", basement)
        secret_room.connect("exit", exit_room)

        # Items
        entrance.items.append(KeyItem("rusty key", "An old key for the basement door."))
        library.items.append(ClueItem("map", "A map showing hidden rooms in the mansion."))

        self.rooms = {
            "entrance": entrance,
            "library": library,
            "kitchen": kitchen,
            "basement": basement,
            "secret room": secret_room,
            "exit": exit_room
        }

    def look(self):
        room = self.player.current_room
        print(f"\n--- {room.name} ---")
        print(room.description)

        if room.items:
            print("Items here:", ", ".join(item.name.title() for item in room.items))

        print("You can move to:", ", ".join(room.connections.keys()).title())

        if room.puzzle and not room.puzzle.solved:
            print("There is a puzzle here. Type 'solve' to attempt it.")

    def move(self, destination):
        destination = destination.lower()
        current = self.player.current_room

        if destination not in current.connections:
            print("You cannot go there from this room.")
            return

        # Basement needs flashlight and rusty key
        if destination == "basement":
            if not self.player.has_item("rusty key"):
                print("The basement door needs a Rusty Key.")
                return
            if not self.player.has_item("flashlight"):
                print("It is too dark. You need a Flashlight.")
                return

        # Secret room requires basement puzzle
        if destination == "secret room":
            basement = self.rooms["basement"]
            if not basement.puzzle.solved:
                print("A hidden door is locked. Solve the Basement puzzle first.")
                return

        # Exit requires secret key
        if destination == "exit":
            if not self.player.has_item("secret key"):
                print("The exit door needs the Secret Key.")
                return

            print("\n🎉 Congratulations! You escaped the Haunted Mansion!")
            print(f"Final Score: {self.player.score}")
            self.game_running = False
            return

        self.player.current_room = current.connections[destination]
        self.look()

    def take_item(self, item_name):
        room = self.player.current_room

        for item in room.items:
            if item.name == item_name.lower():
                self.player.inventory.append(item)
                room.items.remove(item)
                print(f"You picked up: {item.name.title()}")
                return

        print("That item is not in this room.")

    def solve_puzzle(self):
        room = self.player.current_room

        if not room.puzzle:
            print("There is no puzzle in this room.")
            return

        if room.puzzle.solved:
            print("Puzzle already solved.")
            return

        print("\nPuzzle:", room.puzzle.question)
        answer = input("Your answer: ")
        reward = room.puzzle.solve(answer)

        if reward is not None:
            self.player.inventory.append(reward)
            self.player.score += 10
            print(f"You received: {reward.name.title()}")

    def show_hint(self):
        puzzle = self.player.current_room.puzzle
        if puzzle and not puzzle.solved:
            print("Hint:", puzzle.hint)
        else:
            print("No hint is needed here.")

    def show_help(self):
        print("""
Commands:
look                - View current room
move <room>         - Move to another room
take <item>         - Pick up an item
inventory           - View collected items
solve               - Solve current room puzzle
hint                - Get puzzle hint
help                - Show commands
quit                - Exit game
""")

    def start(self):
        name = input("Enter your name: ")
        self.player = Player(name)
        self.player.current_room = self.rooms["entrance"]

        # Puzzle rewards added after player starts
        self.rooms["library"].puzzle.reward = ClueItem(
            "code note", "A note containing a mysterious code."
        )
        self.rooms["kitchen"].puzzle.reward = Item(
            "flashlight", "It helps you see in dark places."
        )
        self.rooms["basement"].puzzle.reward = KeyItem(
            "secret key", "This key opens the final exit door."
        )

        print(f"\nWelcome {name}! Escape the Haunted Mansion.")
        self.show_help()
        self.look()

        while self.game_running:
            command = input("\n> ").strip().lower()

            if command == "look":
                self.look()

            elif command.startswith("move "):
                self.move(command[5:])

            elif command.startswith("take "):
                self.take_item(command[5:])

            elif command == "inventory":
                self.player.show_inventory()

            elif command == "solve":
                self.solve_puzzle()

            elif command == "hint":
                self.show_hint()

            elif command == "help":
                self.show_help()

            elif command == "quit":
                print("Game closed. Bye!")
                self.game_running = False

            else:
                print("Invalid command. Type 'help'.")


if __name__ == "__main__":
    game = GameEngine()
    game.start()