from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

incoming_dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
traversal_path = []
reversal_path = []
visited = {}

visited[player.current_room.id] = player.current_room.get_exits()

while len(visited) < len(room_graph) - 1:
    room_id = player.current_room.id

    # print('******************************************')
    # print('ROOM_ID: ', room_id)
    # print('EXITS:  ', player.current_room.get_exits())
    # print('******************************************')

    # add to visited if room not already visited
    if room_id not in visited:
        visited[room_id] = player.current_room.get_exits()
        # shuffle exits to randomize path taken
        random.shuffle(visited[room_id])
        # remove incoming direction from exits to avoid going back
        incoming_dir = reversal_path[-1]
        visited[room_id].remove(incoming_dir)

    # if dead end reverse back a level
    while len(visited[player.current_room.id]) is 0:
        incoming_dir = reversal_path.pop()
        traversal_path.append(incoming_dir)
        player.travel(incoming_dir)

    # print('BEFORE visited: ', visited)
    # print('BEFORE reversal_path: ', reversal_path)
    # print('BEFORE traversal_path: ', traversal_path)

    next_dir = visited[player.current_room.id].pop(0)
    # print('next_dir: ', next_dir)

    # add next move to traversal and incoming direction to reversal
    traversal_path.append(next_dir)
    reversal_path.append(incoming_dirs[next_dir])

    # print('AFTER visited: ', visited)
    # print('AFTER reversal_path: ', reversal_path)
    # print('AFTER traversal_path: ', traversal_path)

    player.travel(next_dir)
    # print('-------------------END--------------------')


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
