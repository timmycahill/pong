import pygame, os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60
THICKNESS = 15
PADDLE_LENGTH = 100
PADDLE_SPEED = 5
BALL_SPEED = 5

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Game():
    def __init__(self):
        # Initialze window
        pygame.init()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")

        # Initialize variables
        self.paddleLeftPos = Vector2(5, (WINDOW_HEIGHT - PADDLE_LENGTH) / 2)
        self.playerDirection = Vector2(0, 0)
        self.paddleRightPos = Vector2(WINDOW_WIDTH - THICKNESS - 5, (WINDOW_HEIGHT - PADDLE_LENGTH) / 2)
        self.computerDirection = Vector2(0, 0)
        self.ballPos = Vector2((WINDOW_WIDTH - THICKNESS) / 2, (WINDOW_HEIGHT - THICKNESS) / 2)
        self.ballDirection = Vector2(-BALL_SPEED, -BALL_SPEED)


    def _processInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.playerDirection.y -= PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    self.playerDirection.y += PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.playerDirection.y += PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    self.playerDirection.y -= PADDLE_SPEED

            if event.type == pygame.QUIT:
                self.isRunning = False

    def _updateGame(self):
        # Move player paddle
        self.paddleLeftPos.y += self.playerDirection.y
        self.ballPos.y += self.ballDirection.y
        self.ballPos.x += self.ballDirection.x

        # Bounce ball off walls
        if (self.ballPos.y <= THICKNESS and self.ballDirection.y < 0 or
            self.ballPos.y >= WINDOW_HEIGHT - (THICKNESS * 2) and self.ballDirection.y > 0
            ):
            self.ballDirection.y *= -1

        # Bounce ball off paddles
        if (self.ballPos.x <= self.paddleLeftPos.x + THICKNESS and self.ballPos.x >= self.paddleLeftPos.x and
            abs((self.ballPos.y + (THICKNESS / 2)) - (self.paddleLeftPos.y + (PADDLE_LENGTH / 2))) < PADDLE_LENGTH / 2 and
            self.ballDirection.x < 0
            or
            self.ballPos.x >= self.paddleRightPos.x - THICKNESS and self.ballPos.x <= self.paddleRightPos.x and
            abs((self.ballPos.y + (THICKNESS / 2)) - (self.paddleRightPos.y + (PADDLE_LENGTH / 2))) < PADDLE_LENGTH / 2 and
            self.ballDirection.x > 0
            ):
            self.ballDirection.x *= -1



    def _generateOutputs(self):
        # Clear screen
        self.WINDOW.fill("black")

        # Draw walls
        topWall = pygame.Rect(0, 0, WINDOW_WIDTH, THICKNESS)
        self.WINDOW.fill("white", rect=topWall)
        bottomWall = pygame.Rect(0, WINDOW_HEIGHT - THICKNESS, WINDOW_WIDTH, THICKNESS)
        self.WINDOW.fill("white", rect=bottomWall)

        # Draw paddles
        leftPaddle = pygame.Rect(self.paddleLeftPos.x, self.paddleLeftPos.y, THICKNESS, PADDLE_LENGTH)
        self.WINDOW.fill("white", rect=leftPaddle)
        rightPaddle = pygame.Rect(self.paddleRightPos.x, self.paddleRightPos.y, THICKNESS, PADDLE_LENGTH)
        self.WINDOW.fill("white", rect=rightPaddle)

        # Draw ball
        ball = pygame.Rect(self.ballPos.x, self.ballPos.y, THICKNESS, THICKNESS)
        self.WINDOW.fill("white", rect=ball)

        # Update screen
        pygame.display.flip()

    def run(self):
        # Game loop
        clock = pygame.time.Clock()
        self.isRunning = True
        while self.isRunning:
            clock.tick(FPS)
            self._processInputs()
            self._updateGame()
            self._generateOutputs()


        # Uninitialize everything and close application
        pygame.quit()
