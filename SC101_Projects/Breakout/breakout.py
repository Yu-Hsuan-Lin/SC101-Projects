"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics_extension import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    global NUM_LIVES
    graphics = BreakoutGraphics()
    # Add animation loop here!
    # count = 0
    # count_top = 0
    # print(graphics.cc)
    # This 'while True' is to make second revived click start the game.
    while True:
        pause(FRAME_RATE)
        if graphics.cc == 1:
            while True:
                graphics.ball.move(graphics.get_dx(), graphics.get_dy())
                graphics.remove_brick()
                # print(graphics.get_dy())
                pause(FRAME_RATE)
                # if out of window, change direction
                if graphics.ball.x <= 0 or graphics.ball.x >= graphics.window.width - graphics.ball.width:
                    graphics.change_dx_direction()
                elif graphics.ball.y <= 0:
                    graphics.change_dy_direction()
                    # if graphics.win():
                    #     graphics.reset_ball()
                    # count_top += 1
                    # count += 1
                    # print(graphics.window.height, graphics.ball.y+graphics.ball.width, 'time?', count, graphics.get_dy())
                # print(graphics.cc)
                # if died
                elif graphics.ball.y + graphics.ball.height >= graphics.window.height:
                    NUM_LIVES -= 1
                    if NUM_LIVES > 0:
                        graphics.reset_ball()
                        # reset to make the second revived click starts the game
                        graphics.cc = 0
                        break
                    else:
                        graphics.reset_ball()
                        return None
                # win then stop the game
                if graphics.remove_count == 0:
                    graphics.reset_ball()
                    return None






if __name__ == '__main__':
    main()
