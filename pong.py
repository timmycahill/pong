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
        # Initialize variables
        self.paddleLeftPos = Vector2(5, (WINDOW_HEIGHT - PADDLE_LENGTH) / 2)
        self.playerDirection = Vector2(0, 0)
        self.paddleRightPos = Vector2(WINDOW_WIDTH - THICKNESS - 5, (WINDOW_HEIGHT - PADDLE_LENGTH) / 2)
        self.computerDirection = Vector2(0, 0)
        self.ballPos = Vector2((WINDOW_WIDTH - THICKNESS) / 2, (WINDOW_HEIGHT - THICKNESS) / 2)
        self.ballDirection = Vector2(-BALL_SPEED, -BALL_SPEED)
        self.player1Score = 0
        self.player2Score = 0
        self.gameOver = False


    def _resetBall(self):
        self.ballPos.x = (WINDOW_WIDTH - THICKNESS) / 2
        self.ballPos.y = (WINDOW_HEIGHT - THICKNESS) / 2
        self.ballDirection.x = -BALL_SPEED
        self.ballDirection.y = -BALL_SPEED

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
        if self.gameOver:
            pass
        else:
            # Update computer paddle direction
            if self.paddleRightPos.y + (PADDLE_LENGTH / 2) < self.ballPos.y + (THICKNESS / 2):
                self.computerDirection.y = PADDLE_SPEED
            elif self.paddleRightPos.y + (PADDLE_LENGTH / 2) > self.ballPos.y + (THICKNESS / 2):
                self.computerDirection.y = -PADDLE_SPEED

            # Move paddles and ball
            self.paddleLeftPos.y += self.playerDirection.y
            self.paddleRightPos.y += self.computerDirection.y
            self.ballPos.y += self.ballDirection.y
            self.ballPos.x += self.ballDirection.x

            # Bounce ball off walls
            if (self.ballPos.y <= THICKNESS and self.ballDirection.y < 0 or
                self.ballPos.y >= WINDOW_HEIGHT - (THICKNESS * 2) and self.ballDirection.y > 0
                ):
                self.ballDirection.y *= -1

            # Bounce ball off paddles
            lowerPaddle = False
            paddleCollision = False
            if (self.ballPos.x <= self.paddleLeftPos.x + THICKNESS and self.ballPos.x >= self.paddleLeftPos.x and
                abs((self.ballPos.y + (THICKNESS / 2)) - (self.paddleLeftPos.y + (PADDLE_LENGTH / 2))) < PADDLE_LENGTH / 2 and
                self.ballDirection.x < 0
                ):
                # Set collision to true and determine if the lower paddle was hit
                paddleCollision = True
                lowerPaddle = self.ballPos.y + (THICKNESS / 2) > self.paddleLeftPos.y + (PADDLE_LENGTH / 2)
            elif (self.ballPos.x >= self.paddleRightPos.x - THICKNESS and self.ballPos.x <= self.paddleRightPos.x and
                abs((self.ballPos.y + (THICKNESS / 2)) - (self.paddleRightPos.y + (PADDLE_LENGTH / 2))) < PADDLE_LENGTH / 2 and
                self.ballDirection.x > 0
                ):
                # Set collision to true and determine if the lower paddle was hit
                paddleCollision = True
                lowerPaddle = self.ballPos.y + (THICKNESS / 2) > self.paddleRightPos.y + (PADDLE_LENGTH / 2)

            if paddleCollision:
                # Change ball direction
                self.ballDirection.x *= -1

                # Modify ball y speed
                if lowerPaddle:
                    self.ballDirection.y += 1
                else:
                    self.ballDirection.y -= 1

            # Stop paddles when colliding with walls
            if self.paddleLeftPos.y < THICKNESS:
                self.paddleLeftPos.y = THICKNESS
            if self.paddleLeftPos.y + PADDLE_LENGTH > WINDOW_HEIGHT - THICKNESS:
                self.paddleLeftPos.y = WINDOW_HEIGHT - THICKNESS - PADDLE_LENGTH
            if self.paddleRightPos.y < THICKNESS:
                self.paddleRightPos.y = THICKNESS
            if self.paddleRightPos.y + PADDLE_LENGTH > WINDOW_HEIGHT - THICKNESS:
                self.paddleRightPos.y = WINDOW_HEIGHT - THICKNESS - PADDLE_LENGTH

            # Reset ball on score
            if self.ballPos.x < 0:
                self.player2Score += 1
                self._resetBall()
            elif self.ballPos.x > WINDOW_WIDTH - THICKNESS:
                self.player1Score += 1
                self._resetBall()

            # Check for winner
            if self.player1Score >= 11 or self.player2Score >= 11:
                self.gameOver = True


    def _generateOutputs(self):
        # Clear screen
        self.WINDOW.fill("black")

        # Draw in scores
        p1Score = self.font.render(str(self.player1Score), True, "white")
        p2Score = self.font.render(str(self.player2Score), True, "white")
        self.WINDOW.blit(p1Score, (WINDOW_WIDTH / 4 - p1Score.get_rect().width / 2, WINDOW_HEIGHT / 20))
        self.WINDOW.blit(p2Score, (WINDOW_WIDTH / 4 * 3 - p1Score.get_rect().width / 2, WINDOW_HEIGHT / 20))

        # Draw environment
        topWall = pygame.Rect(0, 0, WINDOW_WIDTH, THICKNESS)
        self.WINDOW.fill("white", rect=topWall)
        bottomWall = pygame.Rect(0, WINDOW_HEIGHT - THICKNESS, WINDOW_WIDTH, THICKNESS)
        self.WINDOW.fill("white", rect=bottomWall)
        midfield = pygame.Rect(WINDOW_WIDTH / 2 - 1, 0, 2, WINDOW_HEIGHT)
        self.WINDOW.fill("white", rect=midfield)

        # Display winner
        if self.gameOver:
            winner = "Player 1" if self.player1Score >= 11 else "Player 2"
            winnerFont = pygame.font.SysFont("Keyboard", 80)
            winnerMessage = winnerFont.render("{} Wins".format(winner), True, "white", "black")
            self.WINDOW.blit(winnerMessage, ((WINDOW_WIDTH - winnerMessage.get_rect().width) / 2, (WINDOW_HEIGHT - winnerMessage.get_rect().height) / 2))
        else:
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
        # Initialze window
        pygame.init()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.font = pygame.font.SysFont("Keyboard", 150)

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
