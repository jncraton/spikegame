import asyncio
import importlib.resources
import pygame

SCREEN_SIZE = (640, 480)


async def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    running = True

    ball_position = pygame.Vector2((100, 100))
    ball_speed = 0.25

    ball_image_path = importlib.resources.files("spikegame").joinpath("assets/box.png")
    ball_image = pygame.image.load(ball_image_path)

    ball_rect = ball_image.get_rect()
    ball_radius_x = ball_rect.width // 2
    ball_radius_y = ball_rect.height // 2

    font = pygame.Font(size=32)

    last_ticks = pygame.time.get_ticks()
    dt = 0.0

    while running:
        events = pygame.event.get()

        if any(event.type == pygame.QUIT for event in events):
            running = False

        screen.fill(pygame.Color("black"))

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_a]:
            move.x = -1
        if keys[pygame.K_d]:
            move.x = 1
        if keys[pygame.K_w]:
            move.y = -1
        if keys[pygame.K_s]:
            move.y = 1

        if move.length() > 0:
            move = move.normalize()

        ball_position += move * ball_speed * dt

        ball_position.x = max(
            ball_radius_x, min(SCREEN_SIZE[0] - ball_radius_x, ball_position.x)
        )
        ball_position.y = max(
            ball_radius_y, min(SCREEN_SIZE[1] - ball_radius_y, ball_position.y)
        )

        # Draw the ball, text, and flip the framebuffer
        ball_rect.center = ball_position
        screen.blit(ball_image, ball_rect)
        screen.blit(font.render("Benji was here", True, pygame.Color("white")), (100, 100))
        pygame.display.flip()

        # Replacement for framerate-less pygame.Clock.tick
        ticks = pygame.time.get_ticks()
        dt = ticks - last_ticks
        last_ticks = ticks

        # Yield each frame, pyodide doesn't work properly with a value of 0 so we use a small delay
        await asyncio.sleep(1.0 / 120.0)


if __name__ == "__main__":
    asyncio.run(main())
