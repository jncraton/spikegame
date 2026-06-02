import asyncio
import importlib.resources
import pygame
import os

SCREEN_SIZE = (640, 480)


def get_asset_path(relpath):
    if os.path.exists(relpath):
        return relpath
    else:
        importlib.resources.files("spikegame").joinpath(relpath)


async def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    running = True

    ball_position = pygame.Vector2((100, 100))
    ball_speed = 0.251
    gravity = 0.003
    block_size = 64

    blocks = [
        pygame.Vector2((32+64*4, 32+64*4)),
        pygame.Vector2((32+64*6, 32+64*2)),
    ]
    for x in range(32, 640, 64):
        blocks.append(pygame.Vector2((x, 448)))

    ball_image_path = get_asset_path("assets/box.png")
    ball_image = pygame.image.load(ball_image_path)

    ball_rect = ball_image.get_rect()
    ball_radius_x = ball_rect.width // 2
    ball_radius_y = ball_rect.height // 2

    font = pygame.Font(size=32)

    last_ticks = pygame.time.get_ticks()
    dt = 0.0

    vel = pygame.Vector2(0, 0.3)

    while running:
        events = pygame.event.get()

        if any(event.type == pygame.QUIT for event in events):
            running = False

        screen.fill(pygame.Color("black"))

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vel.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vel.y = 2
        if move.length() > 0:
            move = move.normalize()

        vel.y = vel.y + gravity * dt

        ball_position += (move + vel) * ball_speed * dt

        for block in blocks:
            if (
                block.x - block_size < ball_position.x < block.x + block_size
                and block.y - block_size < ball_position.y < block.y + block_size
            ):
                # undo move
                ball_position.y -= (move.y + vel.y) * ball_speed * dt

        ball_position.x = max(
            ball_radius_x, min(SCREEN_SIZE[0] - ball_radius_x, ball_position.x)
        )
        ball_position.y = max(
            ball_radius_y, min(SCREEN_SIZE[1] - ball_radius_y, ball_position.y)
        )

        # Draw the ball, text, and flip the framebuffer
        ball_rect.center = ball_position
        screen.blit(ball_image, ball_rect)

        for block in blocks:
            block_rect = ball_image.get_rect()

            block_rect.center = block
            screen.blit(ball_image, block_rect)

        screen.blit(font.render(f"{vel.y}", True, pygame.Color("white")), (100, 100))
        pygame.display.flip()

        # Replacement for framerate-less pygame.Clock.tick
        ticks = pygame.time.get_ticks()
        dt = ticks - last_ticks
        last_ticks = ticks

        # Yield each frame, pyodide doesn't work properly with a value of 0 so we use a small delay
        await asyncio.sleep(1.0 / 120.0)

    exit(1)


if __name__ == "__main__":
    asyncio.run(main())
