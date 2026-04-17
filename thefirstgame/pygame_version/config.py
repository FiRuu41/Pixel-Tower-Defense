import math
import os
import pygame

pygame.font.init()

TILE = 32
COLS = 20
ROWS = 15
SCREEN_W = 640
SCREEN_H = 480
FPS = 60

MAX_WAVES = 20
MAX_LEVELS = 10
UI_H = 160

LEVEL_PATHS = [
    [(0,2),(1,2),(2,2),(3,2),(4,2),(4,3),(4,4),(4,5),(5,5),(6,5),(7,5),(8,5),(8,6),(8,7),(8,8),(8,9),(9,9),(10,9),(11,9),(12,9),(12,10),(12,11),(12,12),(13,12),(14,12),(15,12),(16,12),(17,12),(18,12),(19,12)],
    [(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(13,7),(13,6),(13,5),(13,4),(13,3),(14,3),(15,3),(16,3),(17,3),(18,3),(19,3)],
    [(10,0),(10,1),(10,2),(10,3),(10,4),(9,4),(8,4),(7,4),(6,4),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,10),(7,10),(8,10),(9,10),(10,10),(11,10),(12,10),(13,10),(14,10),(15,10),(15,11),(15,12),(15,13),(15,14)],
    [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(18,1),(18,2),(18,3),(18,4),(18,5),(18,6),(18,7),(18,8),(18,9),(18,10),(18,11),(18,12),(18,13),(17,13),(16,13),(15,13),(14,13),(13,13),(12,13),(11,13),(10,13),(9,13),(8,13),(7,13),(6,13),(5,13),(4,13),(3,13),(2,13),(1,13),(1,12),(1,11),(1,10),(1,9),(1,8),(1,7),(1,6),(1,5),(1,4),(1,3),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(15,2),(16,2),(16,3),(16,4),(16,5),(16,6),(16,7),(16,8),(16,9),(16,10),(15,10),(14,10),(13,10),(12,10),(12,9),(12,8),(12,7),(12,6),(12,5),(12,4),(12,3),(13,3),(14,3),(14,4),(14,5),(14,6),(14,7),(14,8),(13,8)],
    [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(5,6),(5,5),(5,4),(5,3),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12),(11,12),(12,12),(13,12),(14,12),(15,12),(15,11),(15,10),(15,9),(15,8),(15,7),(16,7),(17,7),(18,7),(19,7)],
    [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(8,4),(8,3),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(15,2),(16,2),(16,3),(16,4),(16,5),(16,6),(16,7),(16,8),(15,8),(14,8),(13,8),(12,8),(11,8),(10,8),(9,8),(8,8),(7,8),(6,8),(5,8),(4,8),(4,9),(4,10),(4,11),(4,12),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13),(17,13),(18,13),(19,13)],
    [(0,2),(1,2),(2,2),(3,2),(4,2),(4,3),(4,4),(4,5),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(9,5),(9,4),(9,3),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(14,3),(14,4),(14,5),(14,6),(15,6),(16,6),(17,6),(18,6),(19,6)],
    [(0,13),(1,13),(2,13),(3,13),(4,13),(5,13),(5,12),(5,11),(5,10),(5,9),(5,8),(5,7),(5,6),(5,5),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10),(13,10),(14,10),(15,10),(16,10),(17,10),(18,10),(18,9),(18,8),(18,7),(18,6),(18,5),(18,4),(18,3),(18,2),(19,2)],
    [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(7,6),(7,5),(7,4),(7,3),(7,2),(7,1),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(13,1),(13,2),(13,3),(13,4),(13,5),(13,6),(13,7),(13,8),(13,9),(13,10),(13,11),(13,12),(13,13),(13,14),(14,14),(15,14),(16,14),(17,14),(18,14),(19,14)],
    [(0,1),(1,1),(2,1),(3,1),(3,2),(3,3),(3,4),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(8,4),(8,3),(8,2),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),(15,8),(15,9),(15,10),(14,10),(13,10),(12,10),(11,10),(10,10),(9,10),(8,10),(7,10),(6,10),(5,10),(5,11),(5,12),(5,13),(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13),(17,13),(18,13),(19,13)]
]

TOWER_DEFS = {
    'basic':  {'name':'机枪塔', 'price':50,  'range':110, 'damage':5,  'cooldown':35, 'color':(233, 69, 96),  'projectile_speed':6},
    'sniper': {'name':'狙击塔', 'price':80,  'range':190, 'damage':24, 'cooldown':110,'color':(0, 191, 255),  'projectile_speed':10},
    'slow':   {'name':'冰霜塔', 'price':70,  'range':95,  'damage':2,  'cooldown':28, 'color':(0, 255, 255),  'projectile_speed':5},
    'splash': {'name':'爆破塔', 'price':120, 'range':105, 'damage':8,  'cooldown':55, 'color':(255, 140, 0),  'projectile_speed':5.5},
}

DIFFICULTY = {
    'easy':   {'hp_mul':0.75, 'speed_mul':0.85, 'max_towers':999, 'label':'简单', 'desc':'简单难度：敌人血量-25%，速度-15%，塔位无限制'},
    'normal': {'hp_mul':1.0,  'speed_mul':1.0,  'max_towers':22,  'label':'普通', 'desc':'普通难度：标准敌人，最多建造22座塔'},
    'hard':   {'hp_mul':1.45, 'speed_mul':1.25, 'max_towers':14,  'label':'困难', 'desc':'困难难度：敌人血量+45%，速度+25%，最多建造14座塔'},
}

_CJK_FONT_PATH = None

def _find_cjk_font():
    global _CJK_FONT_PATH
    if _CJK_FONT_PATH is not None:
        return _CJK_FONT_PATH
    candidates = [
        'simhei', 'simsun', 'nsimsun',
        'microsoftyahei', 'microsoftyaheiui',
        'msgothic', 'meiryo', 'malgun',
        'wenquanyimicrohei', 'wenquanyizenhei',
        'dengxian', 'fangsong', 'kaiti',
    ]
    for name in candidates:
        path = pygame.font.match_font(name)
        if path and os.path.isfile(path):
            _CJK_FONT_PATH = path
            return path
    windows_font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/msyhl.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simsunb.ttf",
        "C:/Windows/Fonts/Deng.ttf",
        "C:/Windows/Fonts/Dengb.ttf",
    ]
    for path in windows_font_paths:
        if os.path.isfile(path):
            _CJK_FONT_PATH = path
            return path
    try:
        all_fonts = pygame.font.get_fonts()
        keywords = ['simhei', 'simsun', 'msyh', 'microsoftyahei', 'dengxian', 'wenquanyi', 'notosanscjk']
        for font_name in all_fonts:
            lower = font_name.lower()
            if any(k in lower for k in keywords):
                path = pygame.font.match_font(font_name)
                if path and os.path.isfile(path):
                    _CJK_FONT_PATH = path
                    return path
    except Exception:
        pass
    _CJK_FONT_PATH = ''
    return ''

_FONT_CACHE = {}

def get_font(size, bold=False):
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    path = _find_cjk_font()
    if path:
        try:
            font = pygame.font.Font(path, size)
            if bold:
                font.set_bold(True)
            _FONT_CACHE[key] = font
            return font
        except Exception:
            pass
    font = pygame.font.SysFont('arial', size, bold=bold)
    _FONT_CACHE[key] = font
    return font

def tile_to_px(t):
    return (t[0]*TILE, t[1]*TILE)

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def get_upgrade_price(tower):
    base = TOWER_DEFS[tower.type]['price']
    return int(base * 0.55 * tower.level)

def upgrade_tower(tower):
    tower.level += 1
    tower.damage = int(tower.damage * 1.28)
    tower.range = int(tower.range * 1.1)
    tower.max_cooldown = max(8, int(tower.max_cooldown * 0.93))
