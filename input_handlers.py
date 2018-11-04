import tcod

def handle_keys(key):
    key_char = chr(key.c)
    
    # Movement Keys
    if key.vk == tcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'q':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'z':
        return {'move': (-1 ,1)}
    elif key_char == 'c':
        return {'move': (1, 1)}
    
    # Alt+Enter: toogle full screen
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    # Exit the game
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    # No key was pressed
    return {}