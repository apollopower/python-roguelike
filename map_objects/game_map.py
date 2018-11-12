import tcod
from random import randint

from components.fighter import Fighter
from components.ai import BasicMonster

from entity import Entity

from render_functions import RenderOrder

from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    def make_map(self):
        # Create two rooms for demonstration purposes
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)

        self.create_h_tunnel(25, 40, 23)
    
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
                player, entities, max_monsters_per_room, max_items_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width & height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Random position without going out of bounds of map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Using Rect class to instantiate rooms
            new_room = Rect(x, y, w, h)

            # Check other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # Room is valid, create it

                # "Paint" room to map's tiles
                self.create_room(new_room)

                # Set coordinate of new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # This is the first room being created, so place player here
                    player.x = new_x
                    player.y = new_y
                else:
                    # For all rooms after the first:
                    # Connect to previous room with a tunnel

                    # Center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Random selection for tunner route (50/50 chance)
                    if (randint(0,1) == 1):
                        # First move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # First vertical, then horizontal
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                
                # Place any rendered enemies
                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                # Finished with room, append it to room list and increment count
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
    

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        # Get a random number of items
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    # Creates an Orc

                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    # Creates a Troll

                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                
                entities.append(monster)
        
        for i in range(number_of_items):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
        
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item = Entity(x, y, '!', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM)

                entities.append(item)
    
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        
        return False