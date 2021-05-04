"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.
TIME = 0


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # to create win situation
        self.remove_count = brick_rows * brick_cols
        self.brick_number = brick_rows * brick_cols

        # check click to start but not restart
        self.cc = TIME

        # check if the four vertex of the ball has touched anything
        self.not_touch_anything = True

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # create score board
        self.scores = GLabel('Scores: 0')
        self.scores.font = '-20'
        self.window.add(self.scores, x=10, y=30)
        self.score = 0

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle_x = (window_width - paddle_width) / 2
        self.paddle_y = self.window.height - paddle_offset
        self.window.add(self.paddle, self.paddle_x, self.paddle_y)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball_x = (window_width - self.ball.width) / 2
        self.ball_y = (window_height - self.ball.height) / 2
        self.window.add(self.ball, self.ball_x, self.ball_y)

        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx

        # Initialize our mouse listeners
        onmouseclicked(self.click_check)
        onmousemoved(self.paddle_reset_position)

        # Draw bricks
        for i in range(brick_rows):
            if i == 0:
                brick_y = brick_offset
            else:
                brick_y += brick_height + brick_spacing
            for j in range(brick_cols):
                if j == 0:
                    brick_x = 0
                else:
                    brick_x += brick_width + brick_spacing
                brick = GRect(brick_width, brick_height)
                color_list = ['red', 'orange', 'yellow', 'green', 'blue']
                per_row = brick_rows // len(color_list)
                if per_row < 1:
                    per_row = 1
                brick.color = color_list[i//per_row]
                brick.filled = True
                brick.fill_color = color_list[i//per_row]
                self.window.add(brick, brick_x, brick_y)

    # getter
    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    # change direction
    def change_dx_direction(self):
        self.__dx = -self.__dx
        return self.__dx

    def change_dy_direction(self):
        self.__dy = -self.__dy
        return self.__dy

    def paddle_reset_position(self, mouse):
        """
        if mouse is outside the window, the paddle will be at the edge.
        """
        if (0 + self.paddle.width / 2) <= mouse.x <= (self.window.width - self.paddle.width / 2):
            self.paddle_x = mouse.x - self.paddle.width / 2
            self.window.add(self.paddle, self.paddle_x, self.paddle_y)

    def click_check(self, mouse):
        """
        The first click (or revived click) starts the game, and the others no impact. onmouseclicked(self.click_check)
        """
        self.cc += 1
        return self.cc

    def remove_brick(self):
        for ball_x_ in range(int(self.ball.x), int(self.ball.x + self.ball.width + 1), self.ball.width):
            for ball_y_ in range(int(self.ball.y), int(self.ball.y + self.ball.height + 1), self.ball.height):
                if self.not_touch_anything:
                    maybe_brick = self.window.get_object_at(ball_x_, ball_y_)  # ball's four vertex
                    if maybe_brick is not None and maybe_brick is not self.paddle and maybe_brick is not self.scores:  # brick
                        # print('maybe_brick: ', maybe_brick.x, maybe_brick.y)
                        # print(self.check_is_none)
                        # print('in', self.__dy)
                        self.change_dy_direction()
                        # print('change', self.__dy)
                        self.not_touch_anything = False
                        self.window.remove(maybe_brick)
                        # check if win
                        self.remove_count -= 1
                        # count score
                        self.score += 1
                        self.scores.text = 'Scores: ' + str(self.score)
                        self.more_difficult()
                        # print('remove: ', maybe_brick.x, maybe_brick.y, 'ball: ', ball_x_, ball_y_)
                        # if maybe_brick.x == 0:
                        #     print('self.ball.x/', self.ball.x,'self.ball.x + self.ball.width+1/',self.ball.x + self.ball.width+1)
                        #     print('BALL.X: ', self.ball.x, 'ball_x: ', ball_x_, 'ball: ', self.ball.y, 'ball_y+height: ',
                        #       ball_y_+self.ball.height,
                        #       'paddle_x: ', self.paddle.x, 'paddle_x_tail: ', self.paddle.x+self.paddle.width,
                        #       'paddle_y: ', self.paddle.y, 'paddle_y+height', self.paddle.y+self.paddle.height)
                        # print(self.not_touch_anything)
                    elif maybe_brick is not None and maybe_brick is not self.scores and maybe_brick is not self.__dy > 0:  # paddle
                        self.change_dy_direction()
                        self.not_touch_anything = False
        # reset for the next ball_move
        self.not_touch_anything = True

    def more_difficult(self):
        # print(self.score, self.brick_number)
        level_one = int(self.brick_number/5)
        level_two = int(self.brick_number/3)
        level_three = int(self.brick_number/2)
        level_four = int(self.brick_number*0.8)
        if self.score == level_four:
            self.__dy = self.__dy* 2
            # print('level_four')
        elif self.score == level_three:
            # print('level_three: ', level_three, 'score: ', self.score, self.__dy)
            self.__dy = self.__dy * 1.5
        elif self.score == level_two:
            self.__dy = self.__dy * 1.25
            # print('level_two')
        elif self.score == level_one:
            self.__dy = self.__dy * 1.2
            # print(self.brick_number, 'level_one: ', level_one, 'score: ', self.score, self.__dy)
        # print('self.__dy', self.__dy)

    def reset_ball(self):
        self.window.add(self.ball, self.ball_x, self.ball_y)
        # self.paddle.x = self.paddle_x
        # self.paddle.y = self.paddle_y
        # self.window.add(self.paddle, self.paddle_x, self.paddle_y)

    # def win(self):
    #     check_loop = 0
    #     all_brick_height = self.brick_offset + self.brick_rows*self.brick_height + self.brick_spacing*(self.brick_rows-1)
    #     for i in range(0, self.window.width):
    #         for j in range(0, all_brick_height):
    #             maybe_no_brick = self.window.get_object_at(i, j)
    #             # if there is brick
    #             if maybe_no_brick is not None and maybe_no_brick is not self.paddle and maybe_no_brick is not self.ball:
    #                 check_loop = 1
    #     if check_loop == 0:
    #         return True
    #     check_loop = 0







