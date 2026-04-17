import math
import os
import json
import pygame
from config import *
from entities import Enemy, Tower, Projectile, Particle
from audio import audio
from pixel_text import PixelText

pygame.init()

class Game:
    def __init__(self):
        self.scale = 1.5
        self.canvas_h = SCREEN_H
        self.ui_y = int(SCREEN_H * self.scale)
        win_w = int(SCREEN_W * self.scale)
        win_h = self.ui_y + 240
        self.screen = pygame.display.set_mode((win_w, win_h))
        pygame.display.set_caption('像素塔防')
        self.clock = pygame.time.Clock()
        self.font = get_font(18, True)
        self.small_font = get_font(14)
        self.big_font = get_font(48, True)
        self.tiny_font = get_font(12)
        self.pixel_text = PixelText()
        self.menu_particles = []

        self.running = True
        self.show_settings = False
        self.difficulty = 'normal'
        self.volume = 0.35
        audio.init()
        audio.set_volume(self.volume)

        self.save_path = os.path.join(os.path.dirname(__file__), 'save.json')
        self.app_state = 'menu'
        self.menu_items = []
        self.hover_menu = -1
        self.hover_level = -1
        self.has_save = False

        self.reset_game()
        self.load_save()
        self.refresh_menu_items()

    def reset_game(self):
        self.lives = 25
        self.money = 180
        self.wave = 1
        self.level = 1
        self.game_over = False
        self.victory = False
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.particles = []
        self.wave_in_progress = False
        self.spawn_timer = 0
        self.enemies_to_spawn = 0
        self.spawn_interval = 50
        self.selected_tower_type = 'basic'
        self.selected_tower_index = -1
        self.level_decorations = {}
        self.generate_level_decorations()
        self.update_ui()

    def load_save(self):
        if not os.path.exists(self.save_path):
            self.has_save = False
            return
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.has_save = data.get('has_save', False)
            if self.has_save:
                self.level = data.get('level', 1)
                self.wave = data.get('wave', 1)
                self.money = data.get('money', 180)
                self.lives = data.get('lives', 25)
                self.difficulty = data.get('difficulty', 'normal')
                self.volume = data.get('volume', 0.35)
                audio.set_volume(self.volume)
                self.max_level_unlocked = data.get('max_level_unlocked', 1)
            else:
                self.max_level_unlocked = 1
        except Exception:
            self.has_save = False
            self.max_level_unlocked = 1

    def save_game(self):
        data = {
            'has_save': True,
            'level': self.level,
            'wave': self.wave,
            'money': self.money,
            'lives': self.lives,
            'difficulty': self.difficulty,
            'volume': self.volume,
            'max_level_unlocked': max(getattr(self, 'max_level_unlocked', 1), self.level),
        }
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def refresh_menu_items(self):
        first = '继续游戏' if self.has_save else '开始游戏'
        self.menu_items = [first, '关卡选择', '设置']

    def start_new_game(self):
        self.reset_game()
        self.save_game()
        self.app_state = 'playing'

    def continue_game(self):
        # 已经通过 load_save 恢复了进度
        self.app_state = 'playing'

    def start_level(self, level):
        self.reset_game()
        self.level = level
        self.save_game()
        self.app_state = 'playing'

    def reset_current_level(self):
        cur = self.level
        self.reset_game()
        self.level = cur
        self.save_game()

    def update_ui(self):
        pass

    def get_path(self):
        return LEVEL_PATHS[(self.level - 1) % len(LEVEL_PATHS)]

    def is_path(self, tx, ty):
        return (tx, ty) in self.get_path()

    def can_build(self, tx, ty):
        if self.is_path(tx, ty):
            return False
        dec = self.level_decorations.get(self.level, {})
        if (tx, ty) in dec.get('rivers', set()):
            return False
        if (tx, ty) in dec.get('trees', set()):
            return False
        if (tx, ty) in dec.get('flowers', set()):
            return False
        return True

    def generate_level_decorations(self):
        import random
        self.level_decorations = {}
        random.seed(42 + self.level)
        for lv in range(1, MAX_LEVELS + 1):
            path_set = set(LEVEL_PATHS[lv - 1])
            rivers = set()
            trees = set()
            flowers = set()

            # helper：在指定中心附近生成一个小水塘（2~4格）
            def add_pond(cx, cy):
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        tx, ty = cx + dx, cy + dy
                        if 0 <= tx < COLS and 0 <= ty < ROWS and (tx, ty) not in path_set:
                            # 去掉四角，让水塘更圆
                            if abs(dx) == 1 and abs(dy) == 1 and random.random() < 0.35:
                                continue
                            rivers.add((tx, ty))

            # 每关只放 1~3 个小水塘，避免长条河
            if lv == 1:
                add_pond(5, 3)
                add_pond(16, 10)
            elif lv == 2:
                add_pond(3, 6)
                add_pond(16, 5)
            elif lv == 3:
                add_pond(8, 7)
                add_pond(12, 2)
            elif lv == 4:
                add_pond(10, 7)
                add_pond(5, 11)
            elif lv == 5:
                add_pond(3, 10)
                add_pond(16, 2)
            elif lv == 6:
                add_pond(10, 10)
                add_pond(4, 2)
            elif lv == 7:
                add_pond(7, 10)
                add_pond(12, 3)
            elif lv == 8:
                add_pond(9, 7)
                add_pond(3, 2)
            elif lv == 9:
                add_pond(5, 5)
                add_pond(15, 10)
            elif lv == 10:
                add_pond(6, 4)
                add_pond(14, 11)
                add_pond(10, 8)

            # 在剩余草地上随机放花和树
            occupied = path_set | rivers
            grass = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in occupied]
            random.shuffle(grass)
            # 树：每关8-14棵，占用地大
            tree_count = random.randint(8, 14)
            for i in range(min(tree_count, len(grass))):
                trees.add(grass[i])
            # 花：每关15-25朵
            flower_candidates = [g for g in grass[tree_count:] if g not in trees]
            flower_count = random.randint(15, 25)
            for i in range(min(flower_count, len(flower_candidates))):
                flowers.add(flower_candidates[i])

            self.level_decorations[lv] = {
                'rivers': rivers,
                'trees': trees,
                'flowers': flowers,
            }

    def get_tower_at_tile(self, tx, ty):
        for i, t in enumerate(self.towers):
            tcx = t.cx // TILE
            tcy = t.cy // TILE
            if tcx == tx and tcy == ty:
                return i
        return -1

    def create_particles(self, x, y, color, count, size=None):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, size))

    def start_next_wave(self):
        if self.wave_in_progress or self.game_over or self.victory:
            return
        self.wave_in_progress = True
        self.enemies_to_spawn = 5 + self.wave * 2 + self.level
        self.spawn_timer = 0
        self.spawn_interval = max(16, 50 - self.wave * 1.1 - self.level * 0.7)
        audio.sfx_wave_start()

    def end_wave(self):
        self.wave_in_progress = False
        self.wave += 1
        self.money += 35
        if self.wave > MAX_WAVES:
            self.level += 1
            if self.level > MAX_LEVELS:
                self.victory = True
                self.wave_in_progress = False
                self.save_game()
                audio.sfx_victory()
                return
            self.wave = 1
            self.money += 200
            self.towers.clear()
            self.selected_tower_index = -1
            audio.sfx_level_up()
        self.save_game()

    def spawn_logic(self):
        if not self.wave_in_progress:
            return
        if self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                is_boss = (self.wave % 5 == 0) and (self.enemies_to_spawn == 1)
                self.enemies.append(Enemy(self.wave, self.level, self.difficulty, is_boss))
                self.enemies_to_spawn -= 1
        elif len(self.enemies) == 0:
            self.end_wave()

    def update(self):
        if self.game_over or self.victory:
            return
        self.spawn_logic()
        for e in self.enemies:
            e.update(self)
        self.enemies = [e for e in self.enemies if not e.dead and not e.reached]
        for t in self.towers:
            t.update(self)
        for p in self.projectiles:
            p.update(self)
        self.projectiles = [p for p in self.projectiles if not p.dead]
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]
        if self.lives <= 0 and not self.game_over:
            self.game_over = True
            self.wave_in_progress = False
            self.save_game()
            audio.sfx_game_over()

    def draw_map(self, surf):
        # 草地底色带轻微纹理
        surf.fill((28, 56, 42))
        for x in range(COLS):
            for y in range(ROWS):
                px, py = tile_to_px((x, y))
                noise = ((x * 3 + y * 7) % 5) * 2
                col = (28 + noise, 56 + noise, 42 + noise)
                pygame.draw.rect(surf, col, (px, py, TILE, TILE))

        dec = self.level_decorations.get(self.level, {})
        # 河流
        river_set = dec.get('rivers', set())
        for (tx, ty) in river_set:
            cx, cy = tile_to_px((tx, ty))
            cx += TILE // 2
            cy += TILE // 2
            self._draw_water_tile(surf, cx, cy, river_set, tx, ty)
        # 花
        for (tx, ty) in dec.get('flowers', set()):
            cx, cy = tile_to_px((tx, ty))
            cx += TILE // 2
            cy += TILE // 2
            variety = (tx * 3 + ty * 7) % 4
            self._draw_flower(surf, cx, cy, variety)
        # 树
        for (tx, ty) in dec.get('trees', set()):
            cx, cy = tile_to_px((tx, ty))
            cx += TILE // 2
            cy += TILE // 2
            self._draw_tree(surf, cx, cy)

        path = self.get_path()
        for t in path:
            p = tile_to_px(t)
            pygame.draw.rect(surf, (42, 82, 152), (p[0], p[1], TILE, TILE))
            pygame.draw.rect(surf, (54, 106, 181), (p[0] + 2, p[1] + 2, TILE - 4, TILE - 4))
        s = tile_to_px(path[0])
        pygame.draw.rect(surf, (0, 255, 0), (s[0] + 4, s[1] + 4, TILE - 8, TILE - 8))
        e = tile_to_px(path[-1])
        pygame.draw.rect(surf, (255, 0, 0), (e[0] + 4, e[1] + 4, TILE - 8, TILE - 8))

    def _draw_tree(self, surf, cx, cy):
        # 树干
        pygame.draw.rect(surf, (101, 67, 33), (cx - 3, cy - 2, 6, 10))
        # 树叶三层
        pygame.draw.rect(surf, (34, 85, 51), (cx - 10, cy - 10, 20, 10))
        pygame.draw.rect(surf, (46, 125, 50), (cx - 8, cy - 16, 16, 8))
        pygame.draw.rect(surf, (58, 160, 60), (cx - 5, cy - 20, 10, 6))

    def _draw_flower(self, surf, cx, cy, variety=0):
        # 更精致、更多样的小花，每个占一个 tile
        stem = (60, 140, 60)
        if variety == 0:
            # 四瓣小白花 + 黄叶心
            for dx, dy in [(-4, -4), (4, -4), (-4, 4), (4, 4)]:
                pygame.draw.rect(surf, (255, 255, 255), (cx + dx - 2, cy + dy - 2, 4, 4))
            pygame.draw.rect(surf, (255, 215, 0), (cx - 2, cy - 2, 4, 4))
        elif variety == 1:
            # 粉红花苞（郁金香风格），带两小叶
            pygame.draw.rect(surf, stem, (cx - 1, cy + 2, 2, 6))
            pygame.draw.rect(surf, (120, 200, 120), (cx - 4, cy + 4, 3, 3))
            pygame.draw.rect(surf, (120, 200, 120), (cx + 1, cy + 4, 3, 3))
            pygame.draw.rect(surf, (255, 105, 180), (cx - 4, cy - 8, 8, 10))
            pygame.draw.rect(surf, (255, 130, 200), (cx - 2, cy - 6, 4, 6))
        elif variety == 2:
            # 橙黄圆形花，多层花瓣
            petals = [
                (-5, -2), (3, -2), (-5, 2), (3, 2),
                (-2, -5), (-2, 3), (2, -5), (2, 3)
            ]
            for dx, dy in petals:
                pygame.draw.rect(surf, (255, 160, 60), (cx + dx, cy + dy, 3, 3))
            pygame.draw.rect(surf, (139, 69, 19), (cx - 2, cy - 2, 4, 4))
        else:
            # 蓝紫小花，十字放射
            for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5)]:
                pygame.draw.rect(surf, (147, 112, 219), (cx + dx - 2, cy + dy - 2, 4, 4))
            pygame.draw.rect(surf, (255, 255, 224), (cx - 2, cy - 2, 4, 4))

    def _draw_water_tile(self, surf, cx, cy, river_set, tx, ty):
        # 水底色：比草地深的蓝绿色
        base = (35, 85, 120)
        pygame.draw.rect(surf, base, (cx - TILE//2, cy - TILE//2, TILE, TILE))
        # 水体主体：圆角感
        pygame.draw.rect(surf, (45, 105, 145), (cx - TILE//2 + 2, cy - TILE//2 + 2, TILE - 4, TILE - 4))
        # 相邻连接：如果旁边也有水，画出连通感
        neighbors = [(1,0),(-1,0),(0,1),(0,-1)]
        for dx, dy in neighbors:
            if (tx+dx, ty+dy) in river_set:
                # 向邻居方向延伸颜色
                nx = cx + dx * TILE // 2
                ny = cy + dy * TILE // 2
                pygame.draw.rect(surf, (45, 105, 145), (nx - TILE//2 + 2, ny - TILE//2 + 2, TILE - 4, TILE - 4))
        # 高光波纹（1~2条随机位置）
        seed = (tx * 7 + ty * 13) % 4
        if seed % 2 == 0:
            pygame.draw.rect(surf, (90, 150, 190), (cx - 4 + seed, cy - 2, 6, 2))
        if seed > 1:
            pygame.draw.rect(surf, (90, 150, 190), (cx - 2, cy + 2 - seed, 4, 2))

    def draw_selected_ui(self, surf):
        if self.selected_tower_index < 0:
            return
        t = self.towers[self.selected_tower_index]
        if not t:
            return
        pygame.draw.circle(surf, (255, 255, 255), (int(t.cx), int(t.cy)), t.range, 2)
        sx = t.cx - 22
        sy = t.cy - 22
        pygame.draw.rect(surf, (233, 69, 96), (sx, sy, 16, 16))
        for ox, oy in [(2,2),(4,4),(6,6),(8,8),(10,10),(12,12),(12,2),(10,4),(8,6),(4,8),(2,10)]:
            pygame.draw.rect(surf, (255, 255, 255), (sx + ox, sy + oy, 2, 2))
        ux = t.cx + 6
        uy = t.cy - 22
        pygame.draw.rect(surf, (255, 215, 0), (ux, uy, 16, 16))
        ax, ay = ux + 8, uy + 4
        pts = [(ax, ay), (ax - 4, ay + 6), (ax + 4, ay + 6)]
        pygame.draw.polygon(surf, (34, 34, 34), pts)
        up_price = get_upgrade_price(t)
        # 注：升级价格文字也画在canvas上会被缩放，所以只在选中时画一个小的
        txt = self.tiny_font.render(f'{up_price}$', True, (255, 215, 0))
        surf.blit(txt, (ux - 2, uy - 14))

    def draw_ui_bar(self, surf):
        diff = DIFFICULTY[self.difficulty]
        max_t = diff['max_towers']
        max_txt = '--' if max_t >= 900 else str(max_t)

        # 左上角齿轮图标
        self._draw_pixel_gear(surf, 28, 28)

        # 右上角状态栏（物理坐标）
        x_base = surf.get_width() - 200
        y_base = 16
        row_h = 42

        # 生命
        self._draw_pixel_heart(surf, x_base + 18, y_base + 18, (233, 69, 96))
        txt = self.font.render(f'{self.lives}', True, (255, 255, 255))
        surf.blit(txt, (x_base + 44, y_base + 6))

        # 金币
        self._draw_pixel_coin(surf, x_base + 18, y_base + row_h + 18, (255, 215, 0))
        txt = self.font.render(f'{self.money}', True, (255, 255, 255))
        surf.blit(txt, (x_base + 44, y_base + row_h + 6))

        # 塔位
        self._draw_pixel_tower_icon(surf, x_base + 18, y_base + row_h * 2 + 18, (0, 191, 255))
        txt = self.font.render(f'{len(self.towers)}/{max_txt}', True, (255, 255, 255))
        surf.blit(txt, (x_base + 44, y_base + row_h * 2 + 6))

        # 波次/关卡
        wave_txt = self.small_font.render(f'Wave {self.wave}/{MAX_WAVES}  Lv.{self.level}', True, (224, 224, 224))
        surf.blit(wave_txt, (x_base, y_base + row_h * 3 + 6))

        # 底部控制栏
        btn_y = self.ui_y + 10
        self._draw_button(surf, '开始下一波', 20, btn_y, 110, 32, (233, 69, 96), enabled=not self.wave_in_progress and not self.game_over and not self.victory)

        # 底部当前金币（放在按钮旁边，不用抬头看右上角）
        coin_x = 140
        coin_y = btn_y + 4
        self._draw_pixel_coin(surf, coin_x + 12, coin_y + 12, (255, 215, 0))
        gold_txt = self.font.render(str(self.money), True, (255, 255, 255))
        surf.blit(gold_txt, (coin_x + 32, coin_y + 2))

        # 塔卡片
        card_y = btn_y + 46
        cards = ['basic', 'sniper', 'slow', 'splash']
        for i, ctype in enumerate(cards):
            selected = (self.selected_tower_type == ctype)
            can_afford = self.money >= TOWER_DEFS[ctype]['price']
            self._draw_tower_card(surf, ctype, 20 + i * 120, card_y, selected, can_afford)

        # 提示
        hint = self.small_font.render('点击草地建造 · 点击塔升级/拆除 · 河流/花/树不可建塔', True, (170, 170, 170))
        surf.blit(hint, (20, card_y + 80))

    def _draw_pixel_heart(self, surf, cx, cy, color):
        pattern = [
            "  XX XX  ",
            " XXXXXXX ",
            "XXXXXXXXX",
            "XXXXXXXXX",
            " XXXXXXX ",
            "  XXXXX  ",
            "   XXX   ",
            "    X    ",
        ]
        for row, line in enumerate(pattern):
            for col, ch in enumerate(line):
                if ch == 'X':
                    pygame.draw.rect(surf, color, (cx + col * 4 - 18, cy + row * 4 - 16, 4, 4))

    def _draw_pixel_coin(self, surf, cx, cy, color):
        # 外圈金色圆
        for y in range(-10, 11):
            for x in range(-10, 11):
                if x*x + y*y <= 100:
                    pygame.draw.rect(surf, color, (cx + x, cy + y, 1, 1))
        # 内圈稍深
        for y in range(-7, 8):
            for x in range(-7, 8):
                if x*x + y*y <= 50:
                    pygame.draw.rect(surf, (255, 237, 100), (cx + x, cy + y, 1, 1))
        # 中间竖条
        pygame.draw.rect(surf, (180, 140, 0), (cx - 1, cy - 7, 3, 14))

    def _draw_pixel_tower_icon(self, surf, cx, cy, color):
        # 基座
        pygame.draw.rect(surf, (60, 60, 60), (cx - 9, cy + 3, 18, 8))
        # 塔身
        pygame.draw.rect(surf, color, (cx - 6, cy - 5, 12, 10))
        # 塔顶
        pygame.draw.rect(surf, (200, 200, 200), (cx - 4, cy - 10, 8, 5))
        # 炮管
        pygame.draw.rect(surf, (40, 40, 40), (cx + 3, cy - 8, 8, 3))

    def _draw_pixel_gear(self, surf, cx, cy):
        color = (220, 220, 220)
        # 外轮廓圆（描边）
        pygame.draw.circle(surf, color, (cx, cy), 22, 5)
        # 8 个齿（矩形突起）
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            r = 22
            # 齿中心
            tx = cx + math.cos(rad) * r
            ty = cy + math.sin(rad) * r
            # 计算矩形方向
            ux = math.cos(rad)
            uy = math.sin(rad)
            vx = -uy
            vy = ux
            def pt(u, v):
                return (tx + ux * u + vx * v, ty + uy * u + vy * v)
            pts = [
                pt(7, 4), pt(7, -4), pt(-2, -4), pt(-2, 4)
            ]
            pygame.draw.polygon(surf, color, pts)
        # 再画一次内圆环，覆盖齿伸入圆环内部的多余部分
        pygame.draw.circle(surf, (30, 58, 47), (cx, cy), 16, 0)
        pygame.draw.circle(surf, color, (cx, cy), 16, 5)
        # 中心孔
        pygame.draw.circle(surf, (30, 58, 47), (cx, cy), 6, 0)
        pygame.draw.circle(surf, (80, 80, 80), (cx, cy), 6, 2)

    def _draw_button(self, surf, text, x, y, w, h, color, enabled=True):
        c = color if enabled else (85, 85, 85)
        pygame.draw.rect(surf, c, (x, y, w, h))
        pygame.draw.rect(surf, (233, 69, 96) if enabled else (85, 85, 85), (x, y, w, h), 2)
        txt = self.small_font.render(text, True, (255, 255, 255))
        rect = txt.get_rect(center=(x + w // 2, y + h // 2))
        surf.blit(txt, rect)

    def _draw_tower_card(self, surf, ttype, x, y, selected, can_afford=True):
        w, h = 110, 70
        color = (26, 74, 122) if selected else (15, 52, 96)
        border = (255, 215, 0) if selected else (54, 106, 181)
        pygame.draw.rect(surf, color, (x, y, w, h))
        pygame.draw.rect(surf, border, (x, y, w, h), 2)
        d = TOWER_DEFS[ttype]
        lines = [d['name'], f'{d["price"]}金币']
        for idx, line in enumerate(lines):
            if idx == 1 and not can_afford:
                txt_color = (255, 80, 80)
            else:
                txt_color = (255, 215, 0) if idx == 1 else (224, 224, 224)
            txt = self.small_font.render(line, True, txt_color)
            surf.blit(txt, (x + 8, y + 6 + idx * 16))
        desc = {'basic':'攻速快，伤害中等','sniper':'超远射程，高伤害','slow':'减速敌人，低伤害','splash':'范围爆炸，群攻利器'}[ttype]
        txt = self.tiny_font.render(desc, True, (170, 170, 170))
        surf.blit(txt, (x + 8, y + 44))
        if not can_afford:
            s = pygame.Surface((w, h))
            s.set_alpha(100)
            s.fill((20, 20, 20))
            surf.blit(s, (x, y))

    def draw_settings(self, surf):
        if not self.show_settings:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surf.blit(overlay, (0, 0))

        mw, mh = 400, 360
        mx = (self.screen.get_width() - mw) // 2
        my = (self.screen.get_height() - mh) // 2
        pygame.draw.rect(surf, (22, 33, 62), (mx, my, mw, mh))
        pygame.draw.rect(surf, (15, 52, 96), (mx, my, mw, mh), 3)

        title = self.big_font.render('设置', True, (233, 69, 96))
        surf.blit(title, (mx + 20, my + 15))

        # volume slider
        lbl = self.small_font.render('音乐音量', True, (170, 170, 170))
        surf.blit(lbl, (mx + 20, my + 70))
        pygame.draw.rect(surf, (100, 100, 100), (mx + 20, my + 95, 260, 10))
        fill_w = int(self.volume * 260)
        pygame.draw.rect(surf, (233, 69, 96), (mx + 20, my + 95, fill_w, 10))
        pygame.draw.circle(surf, (233, 69, 96), (mx + 20 + fill_w, my + 100), 8)
        val_txt = self.small_font.render(f'{int(self.volume * 100)}%', True, (255, 215, 0))
        surf.blit(val_txt, (mx + 290, my + 90))

        # difficulty buttons
        lbl = self.small_font.render('游戏难度', True, (170, 170, 170))
        surf.blit(lbl, (mx + 20, my + 130))
        diffs = ['easy', 'normal', 'hard']
        for idx, dkey in enumerate(diffs):
            sel = (self.difficulty == dkey)
            bx = mx + 20 + idx * 120
            by = my + 155
            col = (233, 69, 96) if sel else (15, 52, 96)
            pygame.draw.rect(surf, col, (bx, by, 100, 34))
            pygame.draw.rect(surf, (54, 106, 181), (bx, by, 100, 34), 2)
            txt = self.small_font.render(DIFFICULTY[dkey]['label'], True, (255, 255, 255))
            rect = txt.get_rect(center=(bx + 50, by + 17))
            surf.blit(txt, rect)

        desc = DIFFICULTY[self.difficulty]['desc']
        txt = self.tiny_font.render(desc, True, (136, 192, 208))
        surf.blit(txt, (mx + 20, my + 200))

        # back to menu button
        self._draw_button(surf, '回到主菜单', mx + 20, my + 230, 360, 38, (233, 69, 96))
        # reset level button
        self._draw_button(surf, '重置本关', mx + 20, my + 272, 360, 38, (233, 69, 96))
        # close button
        self._draw_button(surf, '关闭', mx + 20, my + 314, 360, 38, (54, 106, 181))

    def draw_menu(self):
        self.screen.fill((26, 26, 46))
        cx = self.screen.get_width() // 2

        # 立体像素标题
        title_y = 55
        self.pixel_text.render(self.screen, '像素塔防', cx, title_y, size=130, pixel_size=3,
                               color=(255, 215, 0), shadow=True,
                               shadow_offset=(5, 5), shadow_color=(180, 100, 0),
                               center_x=True)

        # 菜单项：固定高度区域，彻底避免 rect 重叠
        start_y = 265
        item_h = 56
        gap = 62
        mx, my = pygame.mouse.get_pos()
        rects = []
        for i, item in enumerate(self.menu_items):
            y = start_y + i * gap
            tmp_s = pygame.Surface((1, 1))
            tw, th = self.pixel_text.render(tmp_s, item, 0, 0, size=48, pixel_size=3, color=(255, 255, 255))
            # 固定高度的点击区，确保不重叠
            rect = pygame.Rect(cx - tw // 2 - 16, y + (item_h - th) // 2 - 4, tw + 32, item_h)
            rects.append((y, tw, th, rect))

        self.hover_menu = -1
        for i, (_, _, _, rect) in enumerate(rects):
            if rect.collidepoint(mx, my):
                self.hover_menu = i
                break  # 只取第一个

        for i, (y, tw, th, rect) in enumerate(rects):
            is_hover = (i == self.hover_menu)
            if is_hover:
                pygame.draw.rect(self.screen, (255, 215, 0), rect, 3)
                color = (255, 215, 0)
            else:
                color = (224, 224, 224)
            self.pixel_text.render(self.screen, self.menu_items[i], cx, y, size=48, pixel_size=3, color=color, center_x=True)

        # 底部小提示
        hint = '自动保存进度 · 随时可继续挑战'
        self.pixel_text.render(self.screen, hint, cx, self.screen.get_height() - 40,
                               size=16, pixel_size=3, color=(170, 170, 170), center_x=True)

        # 底部装饰：飘动的像素粒子
        for p in self.menu_particles:
            pygame.draw.rect(self.screen, p['color'], (int(p['x']), int(p['y']), p['size'], p['size']))

        self.draw_settings(self.screen)
        pygame.display.flip()

    def _draw_lock_icon(self, surf, cx, cy, color):
        # 画一个 20x24 左右的像素锁
        ps = 3
        # 锁体 (下方矩形 6x4 像素块)
        body_w = 6 * ps
        body_h = 4 * ps
        bx = cx - body_w // 2
        by = cy
        pygame.draw.rect(surf, color, (bx, by, body_w, body_h))
        # 锁钩 (上方U形)
        # 左右两根竖线
        pygame.draw.rect(surf, color, (bx + ps, by - 3 * ps, ps, 3 * ps))
        pygame.draw.rect(surf, color, (bx + body_w - 2 * ps, by - 3 * ps, ps, 3 * ps))
        # 顶部横线
        pygame.draw.rect(surf, color, (bx + ps, by - 3 * ps, body_w - 2 * ps, ps))
        # 锁孔
        pygame.draw.rect(surf, (26, 26, 46), (cx - ps // 2, by + ps, ps, ps * 2))

    def draw_level_select(self):
        self.screen.fill((26, 26, 46))
        cx = self.screen.get_width() // 2

        self.pixel_text.render(self.screen, '关卡选择', cx, 60, size=64, pixel_size=3,
                               color=(255, 215, 0), shadow=True,
                               shadow_offset=(4, 4), shadow_color=(180, 100, 0),
                               center_x=True)

        self.hover_level = -1
        cols = 5
        card_w = 100
        card_h = 70
        gap_x = 30
        gap_y = 30
        start_x = cx - (cols * card_w + (cols - 1) * gap_x) // 2
        start_y = 180

        mx, my = pygame.mouse.get_pos()
        for lv in range(1, MAX_LEVELS + 1):
            col = (lv - 1) % cols
            row = (lv - 1) // cols
            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)
            unlocked = lv <= getattr(self, 'max_level_unlocked', 1)
            rect = pygame.Rect(x, y, card_w, card_h)
            hovered = unlocked and rect.collidepoint(mx, my)
            if hovered:
                self.hover_level = lv
                border_color = (255, 215, 0)
                bg_color = (26, 74, 122)
            else:
                border_color = (54, 106, 181) if unlocked else (60, 60, 60)
                bg_color = (15, 52, 96) if unlocked else (40, 40, 40)

            pygame.draw.rect(self.screen, bg_color, rect)
            pygame.draw.rect(self.screen, border_color, rect, 3)

            cx_card = x + card_w // 2
            cy_card = y + card_h // 2
            if unlocked:
                # 数字用普通字体，清晰不错位
                num_font = get_font(40, bold=True)
                txt = num_font.render(str(lv), True, (255, 255, 255))
                rect = txt.get_rect(center=(cx_card, cy_card))
                self.screen.blit(txt, rect)
            else:
                # 画一个像素小锁
                self._draw_lock_icon(self.screen, cx_card, cy_card, (100, 100, 100))

        # 返回按钮
        back_rect = pygame.Rect(20, self.screen.get_height() - 60, 80, 36)
        back_hovered = back_rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, (233, 69, 96) if back_hovered else (15, 52, 96), back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255) if back_hovered else (54, 106, 181), back_rect, 2)
        back_font = get_font(20, bold=True)
        back_txt = back_font.render('返回', True, (255, 255, 255))
        self.screen.blit(back_txt, back_txt.get_rect(center=back_rect.center))

        self.draw_settings(self.screen)
        pygame.display.flip()

    def draw(self):
        if self.app_state == 'menu':
            self.draw_menu()
            return
        if self.app_state == 'level_select':
            self.draw_level_select()
            return

        canvas = pygame.Surface((SCREEN_W, SCREEN_H))
        self.draw_map(canvas)
        for t in self.towers:
            t.draw(canvas)
        for e in self.enemies:
            e.draw(canvas)
        for p in self.projectiles:
            p.draw(canvas)
        for p in self.particles:
            p.draw(canvas)
        self.draw_selected_ui(canvas)

        self.screen.fill((26, 26, 46))
        scaled = pygame.transform.scale(canvas, (int(SCREEN_W * self.scale), self.ui_y))
        self.screen.blit(scaled, (0, 0))
        self.draw_ui_bar(self.screen)
        self.draw_settings(self.screen)

        if self.game_over:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            txt1 = self.big_font.render('GAME OVER', True, (233, 69, 96))
            txt2 = self.small_font.render(f'关卡 {self.level} - 波次 {self.wave}', True, (255, 255, 255))
            txt3 = self.small_font.render('点击 "重置游戏" 再战江湖', True, (255, 255, 255))
            self.screen.blit(txt1, txt1.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 30)))
            self.screen.blit(txt2, txt2.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 20)))
            self.screen.blit(txt3, txt3.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50)))
        elif self.victory:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            txt1 = self.big_font.render('VICTORY!', True, (255, 215, 0))
            txt2 = self.small_font.render('恭喜通关全部10个关卡！', True, (255, 255, 255))
            txt3 = self.small_font.render('像素塔防大师！', True, (255, 255, 255))
            self.screen.blit(txt1, txt1.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 30)))
            self.screen.blit(txt2, txt2.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 20)))
            self.screen.blit(txt3, txt3.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50)))

        pygame.display.flip()

    def handle_click(self, pos):
        audio.init()
        mx, my = pos
        if self.show_settings:
            self.handle_settings_click(mx, my)
            return

        if self.app_state == 'menu':
            self.handle_menu_click(mx, my)
            return
        if self.app_state == 'level_select':
            self.handle_level_select_click(mx, my)
            return

        # 左上角齿轮设置图标
        if 0 <= mx <= 56 and 0 <= my <= 56:
            self.show_settings = True
            return

        # UI bar clicks (物理坐标)
        if my >= self.ui_y:
            self.handle_ui_click(mx, my)
            return

        if self.game_over or self.victory:
            return

        # 游戏区域点击，转回逻辑坐标
        lx = int(mx / self.scale)
        ly = int(my / self.scale)
        tx = lx // TILE
        ty = ly // TILE

        if self.selected_tower_index >= 0:
            t = self.towers[self.selected_tower_index]
            if t:
                sx, sy = t.cx - 22, t.cy - 22
                if sx <= lx <= sx + 16 and sy <= ly <= sy + 16:
                    refund = TOWER_DEFS[t.type]['price'] // 2
                    self.money += refund
                    self.towers.pop(self.selected_tower_index)
                    self.selected_tower_index = -1
                    self.create_particles(t.cx, t.cy, (170, 170, 170), 8)
                    audio.sfx_sell()
                    return
                ux, uy = t.cx + 6, t.cy - 22
                if ux <= lx <= ux + 16 and uy <= ly <= uy + 16:
                    price = get_upgrade_price(t)
                    if self.money >= price:
                        self.money -= price
                        upgrade_tower(t)
                        self.create_particles(t.cx, t.cy, (255, 215, 0), 10, 4)
                        audio.sfx_upgrade()
                    return

        tower_idx = self.get_tower_at_tile(tx, ty)
        if tower_idx >= 0:
            self.selected_tower_index = tower_idx
            return

        self.selected_tower_index = -1
        if not self.can_build(tx, ty):
            return

        diff = DIFFICULTY[self.difficulty]
        if diff['max_towers'] < 900 and len(self.towers) >= diff['max_towers']:
            return

        ttype = self.selected_tower_type
        price = TOWER_DEFS[ttype]['price']
        if self.money >= price:
            self.money -= price
            self.towers.append(Tower(tx * TILE + TILE // 2, ty * TILE + TILE // 2, ttype))
            audio.sfx_build()
            self.create_particles(tx * TILE + TILE // 2, ty * TILE + TILE // 2, (233, 69, 96), 8)

    def handle_ui_click(self, mx, my):
        y_base = self.ui_y + 10
        # start wave button
        if y_base <= my <= y_base + 32:
            # 坐标要和 draw_ui_bar 里 _draw_button 的保持一致
            if 20 <= mx <= 130:
                self.start_next_wave()
                return

        # tower cards
        card_y = y_base + 46
        if card_y <= my <= card_y + 70:
            for i in range(4):
                x = 20 + i * 120
                if x <= mx <= x + 110:
                    types = ['basic', 'sniper', 'slow', 'splash']
                    self.selected_tower_type = types[i]
                    self.selected_tower_index = -1
                    return

    def handle_settings_click(self, mx, my):
        mw, mh = 400, 320
        sx = (self.screen.get_width() - mw) // 2
        sy = (self.screen.get_height() - mh) // 2
        if sx + 20 <= mx <= sx + 380 and sy + 230 <= my <= sy + 268:
            self.app_state = 'menu'
            self.show_settings = False
            return
        if sx + 20 <= mx <= sx + 380 and sy + 272 <= my <= sy + 310:
            self.reset_current_level()
            self.show_settings = False
            return
        if sx + 20 <= mx <= sx + 380 and sy + 314 <= my <= sy + 352:
            self.show_settings = False
            return
        if sy + 95 <= my <= sy + 105 and sx + 20 <= mx <= sx + 280:
            rel = (mx - (sx + 20)) / 260
            self.volume = max(0, min(1, rel))
            audio.set_volume(self.volume)
            return
        diffs = ['easy', 'normal', 'hard']
        for idx, dkey in enumerate(diffs):
            bx = sx + 20 + idx * 120
            by = sy + 155
            if bx <= mx <= bx + 100 and by <= my <= by + 34:
                self.difficulty = dkey
                return

    def handle_menu_click(self, mx, my):
        cx = self.screen.get_width() // 2
        start_y = 265
        item_h = 56
        gap = 62
        for i, item in enumerate(self.menu_items):
            y = start_y + i * gap
            tmp_s = pygame.Surface((1, 1))
            tw, th = self.pixel_text.render(tmp_s, item, 0, 0, size=48, pixel_size=3, color=(255, 255, 255))
            rect = pygame.Rect(cx - tw // 2 - 16, y + (item_h - th) // 2 - 4, tw + 32, item_h)
            if rect.collidepoint(mx, my):
                if i == 0:
                    if self.has_save:
                        self.continue_game()
                    else:
                        self.start_new_game()
                elif i == 1:
                    self.app_state = 'level_select'
                elif i == 2:
                    self.show_settings = True
                return

    def handle_level_select_click(self, mx, my):
        # 返回按钮
        back_rect = pygame.Rect(20, self.screen.get_height() - 60, 80, 36)
        if back_rect.collidepoint(mx, my):
            self.app_state = 'menu'
            return
        cols = 5
        card_w = 100
        card_h = 70
        gap_x = 30
        gap_y = 30
        cx = self.screen.get_width() // 2
        start_x = cx - (cols * card_w + (cols - 1) * gap_x) // 2
        start_y = 180
        for lv in range(1, MAX_LEVELS + 1):
            col = (lv - 1) % cols
            row = (lv - 1) // cols
            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)
            unlocked = lv <= getattr(self, 'max_level_unlocked', 1)
            rect = pygame.Rect(x, y, card_w, card_h)
            if unlocked and rect.collidepoint(mx, my):
                self.start_level(lv)
                return

    def run(self):
        import random
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
            if self.app_state == 'playing':
                self.update()
            elif self.app_state == 'menu':
                import random
                # 更新底部飘动粒子
                for p in self.menu_particles:
                    p['x'] += p['vx']
                    p['y'] += p['vy']
                    p['life'] -= 1
                self.menu_particles = [p for p in self.menu_particles if p['life'] > 0]
                # 补充新粒子
                while len(self.menu_particles) < 40:
                    w = self.screen.get_width()
                    h = self.screen.get_height()
                    self.menu_particles.append({
                        'x': random.randint(0, w),
                        'y': random.randint(h - 120, h - 20),
                        'vx': random.uniform(-0.3, 0.3),
                        'vy': random.uniform(-0.8, -0.2),
                        'life': random.randint(60, 180),
                        'size': random.randint(2, 5),
                        'color': random.choice([
                            (54, 106, 181), (233, 69, 96), (255, 215, 0), (0, 255, 255)
                        ])
                    })
            self.draw()
            self.clock.tick(FPS)

        audio.stop_bgm()
        pygame.quit()
