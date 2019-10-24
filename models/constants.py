
# константы статов
STRENGTH = 'strength'
AGILITY = 'agility'
CONSTITUTION = 'constitution'
INTELLIGENCE = 'intelligence'
CHARISMA = 'charisma'
WIZDOM = 'wizdom'

STATS = (
    STRENGTH,
    AGILITY,
    CONSTITUTION,
    INTELLIGENCE,
    CHARISMA,
    WIZDOM
)
BASE_STAT = 8

BASE_START_POINTS = 20

STAT_UPDATE_ORDER = [0, 10, 12, 14, 16]
STAT_UPDATE_COST = {
    0: 1,
    10: 2,
    12: 3,
    14: 4,
    16: 5
}
