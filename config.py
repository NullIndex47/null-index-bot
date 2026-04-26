# config.py

PROJECT_NAME = "NULL INDEX"

# Pesos de dificultad
LEVELS = [
    {"name": "NOISE", "weight": 30},
    {"name": "EASY", "weight": 20},
    {"name": "MEDIUM", "weight": 20},
    {"name": "HARD", "weight": 15},
    {"name": "DEEP", "weight": 10},
    {"name": "VOID", "weight": 5},
]

# Cada cuánto saldrá el siguiente post
INTERVALS_HOURS = [
    {"hours": 4, "weight": 20},
    {"hours": 6, "weight": 35},
    {"hours": 24, "weight": 45},
]

# Tamaños visibles del bloque hexadecimal según nivel
# Recuerda: 1 byte = 2 caracteres hex visibles
HEX_SIZES = {
    "NOISE": [600, 900, 1200, 1800],
    "EASY": [500, 700, 900],
    "MEDIUM": [900, 1300, 1800],
    "HARD": [1500, 2200, 3000],
    "DEEP": [2500, 4000, 6000],
    "VOID": [5000, 8000, 12000],
}

# Mensajes internos. Esto NO se ve directamente en Reddit.
EASY_MESSAGES = [
    "look closer",
    "not all blocks matter",
    "the title is part of it",
    "count the silence",
    "this is not random",
    "one line survived",
    "the first key is missing",
    "read backwards",
    "ignore the noise",
]

MEDIUM_MESSAGES = [
    "only posts ending in 7 contain valid data",
    "the minute is not a minute",
    "every fourth line carries one byte",
    "the first post is a map not a message",
    "combine the dead sectors",
    "remove what repeats",
    "the checksum is lying",
    "follow the smaller block",
    "the answer was posted before the question",
    "do not decode the body first",
]

HARD_FRAGMENTS = [
    "fragment 1/5: the",
    "fragment 2/5: key",
    "fragment 3/5: is",
    "fragment 4/5: orchid",
    "fragment 5/5: null",
    "fragment 1/4: decode",
    "fragment 2/4: the",
    "fragment 3/4: titles",
    "fragment 4/4: in order",
]

DEEP_MESSAGES = [
    "when null repeats seven times use the oldest key",
    "the first silence unlocks the final block",
    "the void is not empty it is delayed",
    "post 0047 is not a message it is a key",
    "the real order is not chronological",
    "the date is a mask",
    "the body is noise the title is the cipher",
    "the broken checksum is the instruction",
    "the key appears after it is used",
    "the archive has no beginning",
]

VOID_MESSAGES = [
    "there was never a first transmission",
    "the solver changes the archive",
    "all decoded messages before this one are incomplete",
    "this block becomes valid after signal 088",
    "the key is not in the text",
    "the noise is the index",
    "nothing was hidden here",
    "the only valid answer is absence",
    "do not trust solved blocks",
    "the final post was already published",
]
