import pygame, os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60
THICKNESS = 15
PADDLE_LENGTH = 100
PADDLE_SPEED = 5

class Position():
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
        self.paddleLeftPos = Position(5, (WINDOW_HEIGHT - PADDLE_LENGTH) / 2)
        self.playerDirection = 0
        self.paddleRightPos = Position(WINDOW_WIDTH - THICKNESS - 5, (WINDOW_HEIGHT - PADDLE_LENGTH) / 2)
        self.computerDirection = 0


    def _processInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.playerDirection -= PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    self.playerDirection += PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.playerDirection += PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    self.playerDirection -= PADDLE_SPEED

            if event.type == pygame.QUIT:
                self.isRunning = False

    def _updateGame(self):
        self.paddleLeftPos.y += self.playerDirection

        # Stop paddles when colliding with walls
        if self.paddleLeftPos.y < THICKNESS:
            self.paddleLeftPos.y = THICKNESS
        if self.paddleLeftPos.y + PADDLE_LENGTH > WINDOW_HEIGHT - THICKNESS:
            self.paddleLeftPos.y = WINDOW_HEIGHT - THICKNESS - PADDLE_LENGTH
        if self.paddleRightPos.y < THICKNESS:
            self.paddleRightPos.y = THICKNESS
        if self.paddleRightPos.y + PADDLE_LENGTH > WINDOW_HEIGHT - THICKNESS:
            self.paddleRightPos.y = WINDOW_HEIGHT - THICKNESS - PADDLE_LENGTH


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
