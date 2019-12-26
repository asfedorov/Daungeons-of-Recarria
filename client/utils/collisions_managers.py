import cocos.collision_model as cm

# PLAYER_WALL_COLLISION_MANAGER = None
# PLAYER_WATER_COLLISION_MANAGER = None
# PLAYER_DEATH_COLLISION_MANAGER = None

col_managers = (
    'PLAYER_WALL_COLLISION_MANAGER',
    'PLAYER_WATER_COLLISION_MANAGER',
    'PLAYER_DEATH_COLLISION_MANAGER'
)


def initialize(width, height, size):
    for manager_name in col_managers:
        if globals().get(manager_name):
            globals()[manager_name].clear()
        print(globals()[manager_name])
        globals()[manager_name] = cm.CollisionManagerGrid(
            0,
            width * size * 1.5,
            0,
            height * size * 1.5,
            size * 1.5,
            size * 1.5
        )
        print(globals()[manager_name])
