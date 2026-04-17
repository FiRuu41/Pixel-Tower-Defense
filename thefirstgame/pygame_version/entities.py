import random
import math
import pygame
from config import *
from audio import audio

class Particle:
    def __init__(self, x, y, color, size=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)
        self.life = 20 + random.random() * 10
        self.color = color
        self.size = size if size is not None else random.uniform(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (int(self.x), int(self.y), int(self.size), int(self.size)))

class Enemy:
    def __init__(self, wave, level, difficulty, is_boss=False):
        self.path_index = 0
        path = LEVEL_PATHS[(level - 1) % len(LEVEL_PATHS)]
        start = tile_to_px(path[0])
        self.x = start[0] + TILE / 2
        self.y = start[1] + TILE / 2

        diff = DIFFICULTY[difficulty]
        base_hp = 10 + wave * 4 + (level - 1) * 12
        base_speed = 1.0 + wave * 0.05 + (level - 1) * 0.12

        if is_boss:
            base_hp *= 7
            base_speed *= 0.5

        self.base_speed = base_speed * diff['speed_mul']
        self.speed = self.base_speed
        self.hp_max = int(base_hp * diff['hp_mul'])
        self.hp = self.hp_max
        self.reward = (5 + wave // 2 + (level - 1)) * (10 if is_boss else 1)
        self.dead = False
        self.reached = False
        self.slow_timer = 0
        self.is_boss = is_boss

        hues = [0, 30, 120, 180, 240, 280, 60, 300]
        hue = hues[((level - 1) * 3 + (wave - 1)) % len(hues)]
        self.color_body = pygame.Color(0, 0, 0)
        self.color_body.hsva = (hue, 70 if not is_boss else 80, 50 if not is_boss else 45, 100)
        self.color_dark = pygame.Color(0, 0, 0)
        self.color_dark.hsva = (hue, 80 if not is_boss else 90, 30, 100)

    def apply_slow(self, frames=100):
        self.slow_timer = max(self.slow_timer, frames)

    def update(self, game):
        if self.dead or self.reached:
            return
        if self.slow_timer > 0:
            self.speed = self.base_speed * 0.5
            self.slow_timer -= 1
        else:
            self.speed = self.base_speed

        path = LEVEL_PATHS[(game.level - 1) % len(LEVEL_PATHS)]
        if self.path_index + 1 >= len(path):
            self.reached = True
            game.lives -= 1
            game.update_ui()
            return

        target = tile_to_px(path[self.path_index + 1])
        tx = target[0] + TILE / 2
        ty = target[1] + TILE / 2
        dx = tx - self.x
        dy = ty - self.y
        d = math.hypot(dx, dy)
        if d <= self.speed:
            self.x = tx
            self.y = ty
            self.path_index += 1
        else:
            self.x += (dx / d) * self.speed
            self.y += (dy / d) * self.speed

    def draw(self, surf):
        if self.dead:
            return
        if self.slow_timer > 0:
            pygame.draw.rect(surf, (0, 255, 255, 60), (int(self.x) - 10, int(self.y) - 10, 20, 20))

        if self.is_boss:
            pygame.draw.rect(surf, self.color_body, (int(self.x) - 12, int(self.y) - 12, 24, 22))
            pygame.draw.rect(surf, self.color_dark, (int(self.x) - 12, int(self.y) + 4, 24, 6))
            pygame.draw.rect(surf, (255, 255, 255), (int(self.x) - 5, int(self.y) - 6, 3, 3))
            pygame.draw.rect(surf, (255, 255, 255), (int(self.x) + 2, int(self.y) - 6, 3, 3))
            # crown
            pygame.draw.rect(surf, (255, 215, 0), (int(self.x) - 8, int(self.y) - 16, 16, 4))
            pygame.draw.rect(surf, (255, 215, 0), (int(self.x) - 6, int(self.y) - 18, 4, 2))
            pygame.draw.rect(surf, (255, 215, 0), (int(self.x) + 2, int(self.y) - 18, 4, 2))
            # boss hp bar
            hp_pct = self.hp / self.hp_max
            pygame.draw.rect(surf, (51, 51, 51), (int(self.x) - 14, int(self.y) - 20, 28, 3))
            pygame.draw.rect(surf, (255, 0, 255), (int(self.x) - 14, int(self.y) - 20, int(28 * hp_pct), 3))
        else:
            pygame.draw.rect(surf, self.color_body, (int(self.x) - 8, int(self.y) - 8, 16, 14))
            pygame.draw.rect(surf, self.color_dark, (int(self.x) - 8, int(self.y) + 2, 16, 4))
            pygame.draw.rect(surf, (255, 255, 255), (int(self.x) - 4, int(self.y) - 4, 2, 2))
            pygame.draw.rect(surf, (255, 255, 255), (int(self.x) + 2, int(self.y) - 4, 2, 2))
            hp_pct = self.hp / self.hp_max
            col = (0, 255, 0) if hp_pct > 0.5 else (255, 255, 0) if hp_pct > 0.25 else (255, 0, 0)
            pygame.draw.rect(surf, (51, 51, 51), (int(self.x) - 10, int(self.y) - 12, 20, 3))
            pygame.draw.rect(surf, col, (int(self.x) - 10, int(self.y) - 12, int(20 * hp_pct), 3))

    def take_damage(self, amount, game):
        self.hp -= amount
        if self.hp <= 0 and not self.dead:
            self.dead = True
            game.money += self.reward
            game.update_ui()
            game.create_particles(self.x, self.y, self.color_body, 16 if self.is_boss else 6, 5 if self.is_boss else None)

class Projectile:
    def __init__(self, x, y, target, damage, ptype, speed):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.type = ptype
        self.speed = speed
        self.dead = False

    def update(self, game):
        if self.dead:
            return
        if self.target.dead or self.target.reached:
            self.dead = True
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        d = math.hypot(dx, dy)
        if d <= self.speed:
            self.hit(self.target, game)
            self.dead = True
        else:
            self.x += (dx / d) * self.speed
            self.y += (dy / d) * self.speed

    def hit(self, enemy, game):
        if self.type == 'splash':
            audio.sfx_explode()
            game.create_particles(enemy.x, enemy.y, (255, 140, 0), 10, 4)
            radius = 48
            for e in game.enemies:
                if e.dead or e.reached:
                    continue
                if dist((enemy.x, enemy.y), (e.x, e.y)) <= radius:
                    e.take_damage(int(self.damage * 0.6), game)
        elif self.type == 'slow':
            enemy.apply_slow(100)
            enemy.take_damage(self.damage, game)
            game.create_particles(enemy.x, enemy.y, (0, 255, 255), 4)
        else:
            enemy.take_damage(self.damage, game)
            game.create_particles(enemy.x, enemy.y, (255, 238, 170), 3)
            if self.type == 'sniper':
                game.create_particles(enemy.x, enemy.y, (0, 191, 255), 4)

    def draw(self, surf):
        colors = {
            'basic': (255, 238, 170),
            'sniper': (0, 191, 255),
            'slow': (170, 255, 255),
            'splash': (255, 170, 0),
        }
        r = 3 if self.type == 'sniper' else 2
        pygame.draw.circle(surf, colors.get(self.type, (255, 255, 255)), (int(self.x), int(self.y)), r)

class Tower:
    def __init__(self, cx, cy, ttype):
        self.cx = cx
        self.cy = cy
        d = TOWER_DEFS[ttype]
        self.type = ttype
        self.range = d['range']
        self.damage = d['damage']
        self.max_cooldown = d['cooldown']
        self.cooldown = 0
        self.color = d['color']
        self.angle = 0
        self.level = 1

    def update(self, game):
        if self.cooldown > 0:
            self.cooldown -= 1
        target = None
        if self.type == 'sniper':
            # 狙击塔：优先攻击范围内剩余血量最高的敌人
            best_hp = -1
            for e in game.enemies:
                if e.dead or e.reached:
                    continue
                d = dist((self.cx, self.cy), (e.x, e.y))
                if d <= self.range and e.hp > best_hp:
                    best_hp = e.hp
                    target = e
        else:
            best_d = float('inf')
            for e in game.enemies:
                if e.dead or e.reached:
                    continue
                d = dist((self.cx, self.cy), (e.x, e.y))
                if d <= self.range and d < best_d:
                    best_d = d
                    target = e
        if target:
            desired = math.atan2(target.y - self.cy, target.x - self.cx)
            # 平滑转向：每帧最多转 12 度
            diff = desired - self.angle
            while diff > math.pi:
                diff -= 2 * math.pi
            while diff < -math.pi:
                diff += 2 * math.pi
            max_turn = math.radians(12)
            if diff > max_turn:
                diff = max_turn
            elif diff < -max_turn:
                diff = -max_turn
            self.angle += diff
            # 只有炮管大致对准目标时才开火（误差 < 8 度），避免“背射”
            if self.cooldown <= 0 and abs(diff) < math.radians(8):
                self.shoot(target, game)
                self.cooldown = self.max_cooldown

    def shoot(self, target, game):
        d = TOWER_DEFS[self.type]
        # 炮弹从炮管口射出，而不是塔中心，视觉更一致
        barrel_len = 14
        px = self.cx + math.cos(self.angle) * barrel_len
        py = self.cy + math.sin(self.angle) * barrel_len
        game.projectiles.append(Projectile(px, py, target, self.damage, self.type, d['projectile_speed']))
        audio.sfx_shoot(self.type)

    def draw(self, surf):
        pygame.draw.rect(surf, (85, 85, 85), (self.cx - 12, self.cy - 12, 24, 24))
        pygame.draw.rect(surf, (119, 119, 119), (self.cx - 10, self.cy - 10, 20, 20))

        # rotated barrel: 以 surface 中心为轴心，让炮管从中心向外延伸
        if self.type == 'basic':
            bw, bh = 36, 12
            barrel = pygame.Surface((bw, bh), pygame.SRCALPHA)
            mid = bw // 2
            pygame.draw.rect(barrel, self.color, (mid, 2, 16, 8))
            pygame.draw.rect(barrel, (176, 42, 64), (mid + 6, 0, 8, 12))
        elif self.type == 'sniper':
            bw, bh = 44, 14
            barrel = pygame.Surface((bw, bh), pygame.SRCALPHA)
            mid = bw // 2
            pygame.draw.rect(barrel, self.color, (mid, 4, 22, 6))
            pygame.draw.rect(barrel, (0, 119, 170), (mid + 14, 0, 10, 14))
        elif self.type == 'slow':
            bw, bh = 32, 12
            barrel = pygame.Surface((bw, bh), pygame.SRCALPHA)
            mid = bw // 2
            pygame.draw.rect(barrel, self.color, (mid, 2, 12, 8))
            pygame.draw.circle(barrel, (0, 204, 204), (mid + 12, 6), 5)
        elif self.type == 'splash':
            bw, bh = 36, 14
            barrel = pygame.Surface((bw, bh), pygame.SRCALPHA)
            mid = bw // 2
            pygame.draw.rect(barrel, self.color, (mid, 2, 14, 10))
            pygame.draw.rect(barrel, (204, 85, 0), (mid + 10, 0, 8, 14))
        else:
            bw, bh = 36, 12
            barrel = pygame.Surface((bw, bh), pygame.SRCALPHA)

        rotated = pygame.transform.rotate(barrel, -math.degrees(self.angle))
        rect = rotated.get_rect(center=(self.cx, self.cy))
        surf.blit(rotated, rect)

        pygame.draw.rect(surf, (255, 255, 255), (self.cx - 3, self.cy - 3, 6, 6))
        if self.level > 1:
            from config import get_font
            font = get_font(10, bold=True)
            txt = font.render(f'+{self.level - 1}', True, (255, 215, 0))
            surf.blit(txt, (self.cx + 6, self.cy - 10))
