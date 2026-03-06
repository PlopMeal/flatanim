import math
import sys
import pygame

WIDTH, HEIGHT = 960, 540
FPS = 60
DURATION_SECONDS = 30

# Colors
SKY_TOP = (95, 168, 232)
SKY_BOTTOM = (190, 227, 255)
GRASS = (84, 162, 93)
PATH = (199, 182, 153)
TREE_TRUNK = (101, 73, 46)
TREE_LEAF = (65, 138, 76)
BENCH_WOOD = (150, 98, 62)
BENCH_METAL = (77, 85, 101)
WHITE = (245, 245, 245)
BLACK = (10, 10, 10)
MAN_SHIRT = (208, 90, 79)
MAN_PANTS = (51, 67, 118)
WRAP_CLOTH = (216, 221, 173)
ALIEN_SKIN = (131, 249, 198)
ALIEN_GLOW = (146, 255, 227)
TEXT = (251, 245, 222)


def lerp(a, b, t):
    return a + (b - a) * t


def draw_gradient(screen):
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = (
            int(lerp(SKY_TOP[0], SKY_BOTTOM[0], t)),
            int(lerp(SKY_TOP[1], SKY_BOTTOM[1], t)),
            int(lerp(SKY_TOP[2], SKY_BOTTOM[2], t)),
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))


def draw_park(screen):
    pygame.draw.rect(screen, GRASS, (0, 300, WIDTH, HEIGHT - 300))
    pygame.draw.ellipse(screen, PATH, (140, 325, 720, 170))

    # trees
    for tx in [90, 200, 760, 870]:
        pygame.draw.rect(screen, TREE_TRUNK, (tx, 220, 24, 100))
        pygame.draw.circle(screen, TREE_LEAF, (tx + 12, 195), 42)
        pygame.draw.circle(screen, TREE_LEAF, (tx - 16, 208), 30)
        pygame.draw.circle(screen, TREE_LEAF, (tx + 36, 208), 30)

    # bench
    pygame.draw.rect(screen, BENCH_METAL, (360, 312, 14, 62), border_radius=4)
    pygame.draw.rect(screen, BENCH_METAL, (555, 312, 14, 62), border_radius=4)
    pygame.draw.rect(screen, BENCH_WOOD, (332, 300, 264, 14), border_radius=5)
    pygame.draw.rect(screen, BENCH_WOOD, (332, 322, 264, 14), border_radius=5)


def draw_man(screen, x, y, shock=0.0, run_t=0.0):
    stride = math.sin(run_t * 17) * 8 if run_t > 0 else 0

    pygame.draw.line(screen, MAN_PANTS, (x - 10, y + 46), (x - 12 + stride, y + 92), 8)
    pygame.draw.line(screen, MAN_PANTS, (x + 10, y + 46), (x + 14 - stride, y + 92), 8)

    pygame.draw.ellipse(screen, MAN_SHIRT, (x - 24, y - 8, 48, 64))

    arm_raise = int(shock * 27)
    pygame.draw.line(screen, (232, 193, 152), (x - 22, y + 6), (x - 48, y - 8 - arm_raise), 6)
    pygame.draw.line(screen, (232, 193, 152), (x + 22, y + 6), (x + 50, y - 9 - arm_raise), 6)

    pygame.draw.circle(screen, (235, 199, 160), (x, y - 34), 20)
    eye_size = 2 + int(shock * 3)
    spread = 7 + int(shock * 2)
    pygame.draw.circle(screen, BLACK, (x - spread, y - 38), eye_size)
    pygame.draw.circle(screen, BLACK, (x + spread, y - 38), eye_size)

    if shock > 0.15:
        pygame.draw.ellipse(screen, BLACK, (x - 8, y - 29, 16, 11))
    else:
        pygame.draw.ellipse(screen, BLACK, (x - 7, y - 28, 14, 4))


def draw_alien_cub(screen, x, y, reveal_t=0.0):
    """Stylized non-explicit reveal animation."""
    reveal_t = max(0.0, min(1.0, reveal_t))

    if reveal_t < 1:
        cloth_w = int(95 * (1 - 0.60 * reveal_t))
        cloth_h = int(58 * (1 - 0.42 * reveal_t))
        pygame.draw.ellipse(screen, WRAP_CLOTH, (x - cloth_w // 2, y - cloth_h // 2, cloth_w, cloth_h))

        if reveal_t > 0.4:
            rip = min(1.0, (reveal_t - 0.4) / 0.6)
            for i in range(5):
                dx = i * 14 - 28
                tip = y - 12 - int(18 * rip) - (i % 2) * 5
                pygame.draw.polygon(
                    screen,
                    (181, 186, 142),
                    [(x + dx, y - 2), (x + dx + 8, tip), (x + dx + 16, y + 6)],
                )

    pulse = 2 + int(4 * math.sin(pygame.time.get_ticks() * 0.01) ** 2)
    pygame.draw.circle(screen, ALIEN_GLOW, (x, y - 8), 32 + pulse, 2)
    pygame.draw.ellipse(screen, ALIEN_SKIN, (x - 30, y - 26, 60, 50))
    pygame.draw.circle(screen, ALIEN_SKIN, (x, y - 38), 19)
    pygame.draw.circle(screen, BLACK, (x - 7, y - 42), 3)
    pygame.draw.circle(screen, BLACK, (x + 7, y - 42), 3)

    # Scary appendage flips up (no explicit anatomy)
    flip = max(0.0, min(1.0, (reveal_t - 0.55) / 0.45))
    angle = lerp(-0.2, -1.45, flip)
    length = 26 + int(flip * 28)
    x2 = x + int(math.cos(angle) * length)
    y2 = y + int(math.sin(angle) * length)
    pygame.draw.line(screen, (88, 222, 170), (x + 4, y + 4), (x2, y2), 8)

    if reveal_t > 0.65:
        # shock sparks
        for i in range(8):
            th = i * (math.pi * 2 / 8) + pygame.time.get_ticks() * 0.014
            sx = x + int(math.cos(th) * (30 + i * 2))
            sy = y + int(math.sin(th) * (22 + i * 2))
            pygame.draw.line(screen, (220, 255, 246), (x, y - 8), (sx, sy), 2)


def draw_caption(screen, font, text, y, alpha=255):
    base = font.render(text, True, TEXT)
    outline = font.render(text, True, BLACK)
    base.set_alpha(alpha)
    outline.set_alpha(alpha)
    for ox, oy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        screen.blit(outline, outline.get_rect(center=(WIDTH // 2 + ox, y + oy)))
    screen.blit(base, base.get_rect(center=(WIDTH // 2, y)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flash-Style Park Fantasy Scene")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 44, bold=True)
    text_font = pygame.font.SysFont("arial", 28, bold=True)

    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        t = (pygame.time.get_ticks() - start_ticks) / 1000.0
        if t > DURATION_SECONDS:
            t = DURATION_SECONDS

        draw_gradient(screen)
        draw_park(screen)

        # 0-9s: park setup
        # 9-18s: man approaches + reveal
        # 18-26s: screaming run
        # 26-30s: FIN card
        if t < 9:
            mx = 205 + int(math.sin(t * 1.5) * 8)
            my = 338 + int(math.sin(t * 5) * 2)
            draw_man(screen, mx, my)
            draw_alien_cub(screen, 485, 352, reveal_t=0.08)
            draw_caption(screen, text_font, "A quiet fantasy park... a strange wrapped cub waits.", 52)

        elif t < 18:
            p = (t - 9) / 9.0
            shock = max(0.0, min(1.0, (p - 0.35) / 0.45))
            mx = 260 + int(p * 90) + int(math.sin(t * 12) * shock * 2)
            draw_man(screen, mx, 338, shock=shock)
            draw_alien_cub(screen, 510, 352, reveal_t=p)
            if p < 0.5:
                draw_caption(screen, text_font, "A man comes over to ask what it is...", 52)
            else:
                draw_caption(screen, text_font, "Cloth tears—an eerie appendage snaps upward!", 52)

        elif t < 26:
            p = (t - 18) / 8.0
            mx = int(360 + p * 780)
            my = 340 + int(abs(math.sin(t * 14)) * 8)
            draw_man(screen, mx, my, shock=1.0, run_t=t)
            draw_alien_cub(screen, 510, 352, reveal_t=1.0)
            draw_caption(screen, text_font, "He screams and runs out of the park!", 52)

        else:
            fade = min(1.0, (t - 26) / 2.2)
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(int(225 * fade))
            screen.blit(overlay, (0, 0))
            draw_caption(screen, title_font, "FIN", HEIGHT // 2, alpha=int(255 * fade))

        pygame.draw.rect(screen, (20, 40, 34), (20, 500, WIDTH - 40, 18), border_radius=8)
        pygame.draw.rect(
            screen,
            (252, 218, 103),
            (20, 500, int((WIDTH - 40) * (t / DURATION_SECONDS)), 18),
            border_radius=8,
        )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
