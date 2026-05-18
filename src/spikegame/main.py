import asyncio
import importlib.resources
import pygame

SCREEN_SIZE = (640, 480)


async def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    running = True

    ball_colour = pygame.Color("blue")
    ball_direction = pygame.Vector2(1, 1)
    ball_position = pygame.Vector2((100, 100))
    ball_radius = 40
    ball_speed = 0.25

    font = pygame.Font(size=32)

    last_ticks = pygame.time.get_ticks()
    dt = 0.0

    while running:
        events = pygame.event.get()

        if any(event.type == pygame.QUIT for event in events):
            running = False

        screen.fill(pygame.Color("black"))

        # Move ball position in the current direction according to ball_speed
        # and time since last frame
        ball_position += ball_direction * 0.25 * dt

        # Bounce the ball if it hits the left or right sides
        if ball_position.x - ball_radius < 0:
            ball_direction.x = 1
            bounced = True
        elif ball_position.x + ball_radius > SCREEN_SIZE[0]:
            ball_direction.x = -1
            bounced = True

        # Bounce the ball if it hits the top or bottom sides
        if ball_position.y - ball_radius < 0:
            ball_direction.y = 1
            bounced = True
        elif ball_position.y + ball_radius > SCREEN_SIZE[1]:
            ball_direction.y = -1
            bounced = True

        # Draw the ball, text, and flip the framebuffer
        pygame.draw.circle(screen, ball_colour, ball_position, ball_radius)
        screen.blit(font.render("Hello world", True, pygame.Color("white")), (100, 100))
        pygame.display.flip()

        # Replacement for framerate-less pygame.Clock.tick
        ticks = pygame.time.get_ticks()
        dt = ticks - last_ticks
        last_ticks = ticks

        # Yield each frame, pyodide doesn't work properly with a value of 0 so we use a small delay
        await asyncio.sleep(1.0 / 120.0)


if __name__ == "__main__":
    asyncio.run(main())
