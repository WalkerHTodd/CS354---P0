"""Grid robot simulator with Pygame visualization.

Run with the -h flag for usage information.

Author: Nathan Sprague
Version: 8/24/2022
"""
import argparse
from PIL import Image
import importlib.util
import sys
import contextlib
from util import get_neighbor


SCREEN_SIZE = (640, 480)
GRID_SIZE = 4


class Simulator:

    def __init__(self, bot, obstacles, display=True, sim_speed=33):
        self.bot = bot
        self.loc = (0, 0)
        self.obstacles = obstacles
        self.display = display
        self.sim_speed = sim_speed
        self.bumped = set()

        if self.display:
            # Suppress pygame welcome string.
            with contextlib.redirect_stdout(None):
                global pygame
                import pygame
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode(SCREEN_SIZE)
            self.draw_bg()
            pygame.display.flip()

    def loc_to_rect(self, loc):
        center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
        return (loc[0] * GRID_SIZE + center[0],
                center[1] - loc[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE)

    def draw_bg(self):
        self.screen.fill((255, 255, 255))
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, (0, 0, 255),
                             self.loc_to_rect(obs))

    def draw_bump(self, bump_loc):
        bump_rect = self.loc_to_rect(bump_loc)
        pygame.draw.rect(self.screen, (255, 0, 0),
                         bump_rect)
        pygame.display.update(bump_rect)
        self.clock.tick(self.sim_speed)

    def draw_move(self, old_loc, new_loc):
        old_rect = self.loc_to_rect(old_loc)
        new_rect = self.loc_to_rect(new_loc)
        pygame.draw.rect(self.screen, (128, 128, 128),
                         old_rect)
        pygame.draw.rect(self.screen, (0, 0, 0),
                         new_rect)
        pygame.display.update(old_rect)
        pygame.display.update(new_rect)

    def tick(self):
        if self.display:
            self.clock.tick(self.sim_speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

    def run(self, num_steps):
        for _ in range(num_steps):
            self.step()
            self.tick()

    def step(self):
        direction = self.bot.step(self.loc)
        next_loc = get_neighbor(self.loc, direction)

        if next_loc in self.obstacles:
            if self.display:
                self.draw_bump(next_loc)
            next_loc = self.loc
        else:
            if self.display:
                self.draw_move(self.loc, next_loc)
            self.loc = next_loc


def simulate(robot, num_steps, obstacles, display=False, speed=1000):
    sim = Simulator(robot, obstacles, display=display, sim_speed=speed)
    sim.run(num_steps)
    found = robot.obstacles
    imaginary = found - obstacles
    percent = (len(found) - len(imaginary)) / len(obstacles) * 100
    return found, percent, imaginary


def img_to_obstacles(img_file):
    im = Image.open(img_file)
    px = im.load()
    obstacles = set()
    for x in range(im.width):
        for y in range(im.height):
            if px[x, y] != 0:
                obstacles.add((x - im.width // 2, im.height // 2 - y))
    return obstacles


def main():
    # Process command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("robot_file", metavar="ROBOT_FILE",
                        help='Name of Python file containing Robot class.')
    parser.add_argument('obstacle_img', metavar="OBSTACLE_IMG",
                        help='Grayscale image.  Non-zero pixels are obstacles.')
    parser.add_argument('-n', '--num-steps', default=100, type=int,
                        help='Number of simulation steps to execute.')
    parser.add_argument('-d', '--display', action='store_true',
                        help="Show robot visualization")
    parser.add_argument('-s', '--speed', default=33, type=int,
                        help="Visualization speed (in hz)")

    args = parser.parse_args()

    # Load the provided file as a module
    spec = importlib.util.spec_from_file_location("module.name",
                                                  args.robot_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = mod
    spec.loader.exec_module(mod)

    robot = mod.Robot()
    obstacles = img_to_obstacles(args.obstacle_img)

    sim = Simulator(robot, obstacles, display=args.display,
                    sim_speed=args.speed)
    sim.run(args.num_steps)
    found = robot.obstacles
    imaginary = found - obstacles
    percent = (len(found) - len(imaginary)) / len(obstacles) * 100

    # print result
    out_str = "Obstacles discovered: {}/{}: {:.2f}%"
    print(out_str.format(len(found) - len(imaginary), len(obstacles), percent))
    if len(imaginary) > 0:
        print(f'Robot has "discovered" non-existent obstacles:\n{imaginary}')

    # Spin pygame until the user exits.
    if args.display:
        while True:
            sim.tick()


if __name__ == "__main__":
    main()
