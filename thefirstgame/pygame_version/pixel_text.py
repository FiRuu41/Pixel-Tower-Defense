import pygame
from config import get_font

class PixelText:
    """把任意文字渲染成像素块风格"""

    def render(self, surf, text, x, y, size=24, pixel_size=3, color=(255, 255, 255),
               shadow=False, shadow_offset=(2, 2), shadow_color=(30, 30, 30),
               center_x=False, center_y=False):
        font = get_font(size, bold=shadow)
        # 先用字体渲染成普通 surface
        ts = font.render(text, True, (255, 255, 255))
        w, h = ts.get_size()

        ps = pixel_size
        # 以 ps 为步长遍历，但像素块画 ps-1（留1px间隙，更有像素感）
        block = max(1, ps - 1)
        cols = w // ps + 1
        rows = h // ps + 1
        points = []
        for ry in range(rows):
            for cx in range(cols):
                px = cx * ps + ps // 2
                py = ry * ps + ps // 2
                if 0 <= px < w and 0 <= py < h:
                    a = ts.get_at((px, py))[3]
                    if a > 100:
                        points.append((cx * ps, ry * ps))

        total_w = max((p[0] for p in points), default=0) + block
        total_h = max((p[1] for p in points), default=0) + block

        dx = x
        dy = y
        if center_x:
            dx = x - total_w // 2
        if center_y:
            dy = y - total_h // 2

        if shadow:
            for px, py in points:
                pygame.draw.rect(surf, shadow_color, (dx + px + shadow_offset[0], dy + py + shadow_offset[1], block, block))

        for px, py in points:
            pygame.draw.rect(surf, color, (dx + px, dy + py, block, block))

        return total_w, total_h
