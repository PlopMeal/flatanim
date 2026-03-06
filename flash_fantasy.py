import math
import sys
import pygame

WIDTH, HEIGHT = 960, 540
FPS = 60
DURATION_SECONDS = 30

# Colors
SKY_TOP = (40, 22, 62)
SKY_BOTTOM = (93, 61, 121)
GROUND = (54, 77, 48)
HOUSE = (221, 198, 158)
ROOF = (120, 56, 40)
DOOR = (102, 66, 40)
WHITE = (245, 245, 245)
BLACK = (10, 10, 10)
BLAIR_SHIRT = (62, 121, 205)
BLAIR_PANTS = (31, 45, 88)
BABY_WRAP = (172, 204, 149)
ALIEN_SKIN = (128, 244, 196)
ALIEN_GLOW = (146, 255, 227)
TEXT = (250, 236, 190)


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



def draw_house(screen):
    base = pygame.Rect(110, 180, 350, 260)
    pygame.draw.rect(screen, HOUSE, base, border_radius=8)
    roof = [(90, 190), (285, 80), (480, 190)]
    pygame.draw.polygon(screen, ROOF, roof)
    pygame.draw.rect(screen, DOOR, (255, 300, 70, 140), border_radius=4)
    pygame.draw.rect(screen, WHITE, (150, 240, 72, 58), border_radius=6)
    pygame.draw.rect(screen, WHITE, (350, 240, 72, 58), border_radius=6)
    pygame.draw.circle(screen, (245, 214, 91), (315, 370), 4)



def draw_ground(screen):
    pygame.draw.rect(screen, GROUND, (0, 430, WIDTH, HEIGHT - 430))
    for i in range(28):
        x = i * 40 + (i % 3) * 3
        pygame.draw.line(screen, (70, 108, 56), (x, 430), (x + 12, 450), 2)



def draw_blair(screen, x, y, shock=0.0, run_t=0.0):
    wobble = math.sin(run_t * 18) * 4 if run_t > 0 else 0

    # legs
    pygame.draw.line(screen, BLAIR_PANTS, (x - 10, y + 48), (x - 14 + wobble, y + 90), 7)
    pygame.draw.line(screen, BLAIR_PANTS, (x + 10, y + 48), (x + 18 - wobble, y + 90), 7)

    # torso
    pygame.draw.ellipse(screen, BLAIR_SHIRT, (x - 24, y - 8, 48, 64))

    # arms
    arm_raise = int(shock * 24)
    pygame.draw.line(screen, (230, 188, 148), (x - 22, y + 8), (x - 46, y - 8 - arm_raise), 6)
    pygame.draw.line(screen, (230, 188, 148), (x + 22, y + 8), (x + 46, y - 8 - arm_raise), 6)

    # head
    pygame.draw.circle(screen, (233, 196, 154), (x, y - 34), 20)
    eye_spread = 7 + int(shock * 3)
    eye_r = 2 + int(shock * 2)
    pygame.draw.circle(screen, BLACK, (x - eye_spread, y - 38), eye_r)
    pygame.draw.circle(screen, BLACK, (x + eye_spread, y - 38), eye_r)
    mouth_h = 3 + int(shock * 8)
    pygame.draw.ellipse(screen, BLACK, (x - 7, y - 28, 14, mouth_h))



def draw_bundle(screen, x, y, reveal_t=0.0):
    """A mysterious wrapped shape that opens to reveal an alien cub (non-explicit)."""
    shred = max(0.0, min(1.0, reveal_t))

    # wrap (tears away over time)
    if shred < 1:
        wrap_w = int(88 * (1 - 0.65 * shred))
        wrap_h = int(56 * (1 - 0.45 * shred))
        pygame.draw.ellipse(screen, BABY_WRAP, (x - wrap_w // 2, y - wrap_h // 2, wrap_w, wrap_h))
        if shred > 0.35:
            for i in range(4):
                dx = i * 16 - 24
                pygame.draw.polygon(
                    screen,
                    (144, 177, 120),
                    [(x + dx, y - 10), (x + dx + 8, y - 32), (x + dx + 14, y - 6)],
                )

    # alien body
    glow = int(110 + 120 * math.sin(pygame.time.get_ticks() * 0.008) ** 2)
    pygame.draw.circle(screen, (ALIEN_GLOW[0], min(255, ALIEN_GLOW[1]), ALIEN_GLOW[2]), (x, y), int(22 + shred * 10), 2)
    pygame.draw.ellipse(screen, ALIEN_SKIN, (x - 28, y - 22, 56, 46))
    pygame.draw.circle(screen, ALIEN_SKIN, (x, y - 30), 18)

    # eyes
    pygame.draw.circle(screen, BLACK, (x - 7, y - 34), 3)
    pygame.draw.circle(screen, BLACK, (x + 7, y - 34), 3)

    # animated appendage flipping up (stylized and non-explicit)
    flip = max(0.0, min(1.0, (reveal_t - 0.55) / 0.45))
    angle = lerp(-0.4, -1.5, flip)
    length = 30 + int(flip * 18)
    x2 = x + int(math.cos(angle) * length)
    y2 = y + int(math.sin(angle) * length)
    pygame.draw.line(screen, (96, 220, 170), (x + 6, y + 5), (x2, y2), 7)

    # sparks for shocking effect
    if reveal_t > 0.6:
        for i in range(7):
            th = i * (math.pi * 2 / 7) + pygame.time.get_ticks() * 0.01
            sx = x + int(math.cos(th) * (36 + i * 2))
            sy = y + int(math.sin(th) * (20 + i * 2))
            pygame.draw.line(screen, (200, 255, 244), (x, y), (sx, sy), 2)



def draw_caption(screen, font, text, y, alpha=255):
    surf = font.render(text, True, TEXT)
    surf.set_alpha(alpha)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    outline = font.render(text, True, BLACK)
    outline.set_alpha(alpha)
    for ox, oy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        screen.blit(outline, outline.get_rect(center=(WIDTH // 2 + ox, y + oy)))
    screen.blit(surf, rect)



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fantasy Flash-Style Scene")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 42, bold=True)
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
        draw_house(screen)
        draw_ground(screen)

        # Timeline sections
        # 0-8s intro: Blair babysitting inside/near house
        # 8-18s discovery and shock
        # 18-26s frantic run
        # 26-30s ending FIN
        if t < 8:
            bx = 315 + int(math.sin(t * 1.8) * 10)
            by = 328 + int(math.sin(t * 5.0) * 2)
            draw_blair(screen, bx, by)
            draw_bundle(screen, 380, 340, reveal_t=0.05)
            draw_caption(screen, text_font, "Blair babysits on a quiet fantasy night...", 50)

        elif t < 18:
            p = (t - 8) / 10.0
            shock = max(0.0, min(1.0, (p - 0.35) / 0.45))
            bx = 330 + int(math.sin(t * 10) * shock * 2)
            draw_blair(screen, bx, 328, shock=shock)
            draw_bundle(screen, 465, 336, reveal_t=p)
            if p < 0.45:
                draw_caption(screen, text_font, "He finds a strange hanging alien cub...", 50)
            else:
                draw_caption(screen, text_font, "The wrapping shreds. A sudden flip startles him!", 50)

        elif t < 26:
            p = (t - 18) / 8.0
            bx = int(340 + p * 730)
            by = 332 + int(abs(math.sin(t * 13)) * 8)
            draw_blair(screen, bx, by, shock=1.0, run_t=t)
            draw_bundle(screen, 520, 338, reveal_t=1.0)
            draw_caption(screen, text_font, "Blair panics and sprints out of the house!", 50)

        else:
            fade = min(1.0, (t - 26) / 2.5)
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(int(220 * fade))
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            draw_caption(screen, title_font, "FIN", HEIGHT // 2, alpha=int(255 * fade))

        # progress bar
        pygame.draw.rect(screen, (28, 28, 42), (20, 500, WIDTH - 40, 18), border_radius=8)
        pygame.draw.rect(
            screen,
            (238, 212, 124),
            (20, 500, int((WIDTH - 40) * (t / DURATION_SECONDS)), 18),
            border_radius=8,
        )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
