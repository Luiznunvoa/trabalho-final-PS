SCREEN_W, SCREEN_H = 1400, 900
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DGRAY = (100, 100, 100)
LGRAY = (220, 220, 220)
GOLD = (255, 215, 0)
BG = (22, 22, 38)
PANEL_BG = (30, 30, 50)
PANEL_BD = (55, 55, 85)
CARD_BG = (245, 240, 230)

PLAYER_COLORS = [(220, 60, 60), (60, 130, 230), (50, 190, 70), (230, 190, 40)]
PLAYER_NAMES = ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"]

REGION_COLORS = [
    (190, 55, 55), (50, 130, 190), (60, 160, 70),
    (200, 175, 45), (155, 85, 180), (195, 120, 50),
]

REGION_NAMES = [
    "Montanhas Rubras", "Lago Azul", "Floresta Verde",
    "Planicies Douradas", "Pantano Purpura", "Deserto Laranja",
]

REGION_SHORT = ["Mont.", "Lago", "Flor.", "Plan.", "Pant.", "Des."]

REGION_SCORES = [
    [8, 4, 2], [10, 6, 3], [6, 3, 1],
    [8, 4, 2], [12, 6, 3], [10, 5, 2],
]

BAND_BONUS = {1: 0, 2: 1, 3: 3, 4: 6, 5: 10, 6: 15}

ALL_TRIBES = ["Centauro", "Halfling", "Esqueleto", "Elfo", "Gigante", "Mago", "Troll", "Orc"]

TRIBE_COLORS = {
    "Centauro": (160, 82, 45), "Halfling": (34, 139, 34),
    "Esqueleto": (180, 180, 195), "Elfo": (65, 105, 225),
    "Gigante": (139, 69, 19), "Mago": (128, 0, 128),
    "Troll": (85, 107, 47), "Orc": (178, 34, 34),
}

TRIBE_SYMBOLS = {
    "Centauro": "C", "Halfling": "H", "Esqueleto": "S", "Elfo": "E",
    "Gigante": "G", "Mago": "M", "Troll": "T", "Orc": "O",
}

TRIBE_DESC = {
    "Centauro": "Compra 1 carta extra ao jogar banda",
    "Halfling": "+1 ponto por carta na banda",
    "Esqueleto": "Guarda cartas jogadas p/ proxima Era",
    "Elfo": "Mantem 1 carta ao descartar",
    "Gigante": "+3 pontos bonus por banda",
    "Mago": "Compra carta do topo ao jogar banda",
    "Troll": "+1 controle extra na regiao",
    "Orc": "Compra 1 carta do mercado ao jogar banda",
}

NUM_DRAGONS = 3

TOP_H = 72
MAP_Y = 80
MAP_H = 300
MKT_Y = 390
MKT_H = 110
ACT_Y = 510
HAND_Y = 550
HAND_H = 145
MSG_Y = SCREEN_H - 36