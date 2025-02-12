# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "bonhomme",  # TODO: bonhomme
        "tail": "bonhomme",  # TODO: bonhomme
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_body = game_state["you"]["body"]  # Full body of the snake
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    food = game_state['board']['food']
    turn_number = game_state['turn']
    
    print(f"Turn {turn_number}: Head Position: {my_head}, Board: {board_width}x{board_height}")
    
    # Ensure snake doesn't grow too large but survives at least 300 turns
    max_length = 7
    if len(my_body) >= max_length and turn_number < 300:
        food = []  # Ignore food to prevent further growth
    
    # Strengthened out-of-bounds prevention (treating as solid walls)
    if my_head["x"] <= 1:
        is_move_safe["left"] = False
    if my_head["x"] >= board_width - 2:
        is_move_safe["right"] = False
    if my_head["y"] <= 1:
        is_move_safe["down"] = False
    if my_head["y"] >= board_height - 2:
        is_move_safe["up"] = False
    
    # Stronger self-collision prevention by checking next move positions
    future_positions = set((segment["x"], segment["y"]) for segment in my_body)
    
    if (my_head["x"] - 1, my_head["y"]) in future_positions:
        is_move_safe["left"] = False
    if (my_head["x"] + 1, my_head["y"]) in future_positions:
        is_move_safe["right"] = False
    if (my_head["x"], my_head["y"] - 1) in future_positions:
        is_move_safe["down"] = False
    if (my_head["x"], my_head["y"] + 1) in future_positions:
        is_move_safe["up"] = False
    
    # Avoid other snakes
    for snake in game_state['board']['snakes']:
        for segment in snake['body']:
            if (segment["x"], segment["y"]) in future_positions:
                if segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"]:
                    is_move_safe["left"] = False
                if segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"]:
                    is_move_safe["right"] = False
                if segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1:
                    is_move_safe["down"] = False
                if segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1:
                    is_move_safe["up"] = False
    
    print(f"Safe Moves after collision check: {is_move_safe}")
    
    # Remove unsafe moves
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
    
    if not safe_moves:
        print(f"MOVE {turn_number}: No safe moves detected! Defaulting to 'down'")
        return {"move": "down"}
    
    # Move towards the closest food in the current direction if past 300 turns
    if food and turn_number >= 300:
        closest_food = min(food, key=lambda f: abs(f["x"] - my_head["x"]) + abs(f["y"] - my_head["y"]))
        current_direction = safe_moves[0] if safe_moves else "down"
        
        if current_direction == "left" and closest_food["x"] < my_head["x"]:
            return {"move": "left"}
        if current_direction == "right" and closest_food["x"] > my_head["x"]:
            return {"move": "right"}
        if current_direction == "down" and closest_food["y"] < my_head["y"]:
            return {"move": "down"}
        if current_direction == "up" and closest_food["y"] > my_head["y"]:
            return {"move": "up"}
    
    # Choose a random safe move if no clear food path in current direction
    next_move = random.choice(safe_moves)
    print(f"MOVE {turn_number}: {next_move}")
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
