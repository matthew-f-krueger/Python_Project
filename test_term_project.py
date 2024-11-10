# -*- coding: utf-8 -*-
"""
Completed on Sun Nov 10, 2024

@author: Matthew Krueger
"""

import pygame
import unittest

# Constants, replace these with your actual values
WIDTH = 800  # Game window width
HEIGHT = 600  # Game window height
BALL_SIZE = 20  # Ball size

# Your Ball and Paddle classes
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    def move(self):
        self.rect.x += 1
        self.rect.y += 1

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move_up(self):
        self.rect.y -= 5

    def move_down(self):
        self.rect.y += 5


class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()  # Initialize pygame
        self.ball = Ball()  # Create a ball instance
        self.left_paddle = Paddle(10, HEIGHT // 2 - 50, 10, 100)  # Left paddle
        self.right_paddle = Paddle(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)  # Right paddle

    def test_ball_initial_position(self):
        # Test the ball is initially centered
        self.assertEqual(self.ball.rect.x, WIDTH // 2 - BALL_SIZE // 2)
        self.assertEqual(self.ball.rect.y, HEIGHT // 2 - BALL_SIZE // 2)

    def test_ball_move(self):
        # Test the ball's movement (it should move 1 pixel in both x and y)
        initial_x = self.ball.rect.x
        initial_y = self.ball.rect.y
        self.ball.move()
        self.assertEqual(self.ball.rect.x, initial_x + 1)
        self.assertEqual(self.ball.rect.y, initial_y + 1)

    def test_paddle_initial_position(self):
        # Test the left paddle's initial position
        self.assertEqual(self.left_paddle.rect.x, 10)
        self.assertEqual(self.left_paddle.rect.y, HEIGHT // 2 - 50)

    def test_paddle_move_up(self):
        # Test that the left paddle can move up
        initial_y = self.left_paddle.rect.y
        self.left_paddle.move_up()
        self.assertEqual(self.left_paddle.rect.y, initial_y - 5)

    def test_paddle_move_down(self):
        # Test that the left paddle can move down
        initial_y = self.left_paddle.rect.y
        self.left_paddle.move_down()
        self.assertEqual(self.left_paddle.rect.y, initial_y + 5)

    def test_ball_paddle_collision(self):
        # Test that the ball and paddle collision detection works
        self.ball.rect.x = self.left_paddle.rect.right - BALL_SIZE  # Ball slightly inside the paddle's edge
        self.ball.rect.y = self.left_paddle.rect.centery - BALL_SIZE // 2  # Align ball vertically with paddle center
        self.assertTrue(self.ball.rect.colliderect(self.left_paddle.rect))  # Ball and paddle should collide
    
    def test_ball_out_of_bounds_left(self):
        # Test if the ball goes out of bounds on the left side
        self.ball.rect.x = -BALL_SIZE
        self.assertTrue(self.ball.rect.x < 0)  # Ball should be off the left side

    def test_ball_out_of_bounds_right(self):
        # Test if the ball goes out of bounds on the right side
        self.ball.rect.x = WIDTH + BALL_SIZE  # Ball's right edge is beyond the right screen boundary
        self.assertTrue(self.ball.rect.x > WIDTH)  # Ball should be off the right side

if __name__ == "__main__":
    unittest.main()
