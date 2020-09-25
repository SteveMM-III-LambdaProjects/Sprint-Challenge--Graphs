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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

"""
Objective:
    Traverse the maze, visiting every room in less than 2000 steps (less than 960 for stretch)

Each room has a max of 4 exits (N,S,E,W)
Exits can be retreived with room.get_exits()
Each room has an ID

Current room from player.current_room
Travel with player.travel( "direction" )

---
Keep track of reverse path for backtracking
Backtrack from deadends, checking rooms for other exits

Room not visited:
    add to path & visited
Dead end:
    backtrack
Visited:
    new direction
    update reverse
    remove direction from room
    add to path
"""

def travel():
    path    = []
    reverse = []
    visited = {}

    prev = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

    #starting room and exits
    visited[ player.current_room.id ] = player.current_room.get_exits()

    # loop through all rooms
    while len( visited ) < len( room_graph ):
        
        # unvisited
        if player.current_room.id not in visited:
            exits = player.current_room.get_exits()
            # remove came from direction
            exits.remove( prev[ path[ -1 ] ] )
            # add to visited
            visited[ player.current_room.id ] = exits
        
        # dead end
        if len( visited[ player.current_room.id ] ) == 0:
            # get last prev
            prev_dir = reverse.pop()
            # add to path
            path.append( prev_dir )
            # move to prev room
            player.travel( prev_dir )
        
        # visited
        else:
            # get current number of exits
            num_exits = len( visited[ player.current_room.id ] )
            exit_ndx  = ( random.randint( 0, num_exits -1 ) if num_exits > 0 else 0 )
            direction = visited[ player.current_room.id ][ exit_ndx ]
            # remove from options
            visited[ player.current_room.id ].pop( exit_ndx )
            # move to next room
            player.travel( direction )
            # add to path
            path.append( direction )
            # add opposite to prev
            reverse.append( prev[ direction ] )
    
    return path

traversal_path = travel()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
"""
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""
