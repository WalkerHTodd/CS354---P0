"""Grid-world robot controller.

Walker Todd - CS354 BumperBot

FAILURE TO UPDATE THIS DOCSTRING BLOCK WITH THE RELEVANT INFORMATION
WILL RESULT IN A SCORE OF ZERO ON THE ASSIGNMENT.

My approach for this project was to kind of mimic the pattern of the roomba
and every time a obstacle is hit it would rotate around the obstacle.  I 
also did if it got trapped in an area in whcih it has already has been it 
would randomize out until it found an open spot to go and continue the 
pattern
Author: Walker Todd

Honor Code and Acknowledgments:
    This work complies with the JMU Honor Code.
    I recieved help from you and that was it

"""
import random
from util import Location
from util import get_neighbor


class Robot:
    """A simple Robot in a 2D grid world.

    Provides a public instance variable named `obstacles` that is a
    set containing the coordinates of all obstacles that have been
    observed.

    """

    def __init__(self):
        # Initialize instance variables here.
        self.obstacles = set()
        self.exploredtiles = set()
        self.previouslocation = None
        self.currentdirection = 0
        # self.previousdirections = []

    def step(self, loc: Location) -> int:
        """Process the current location and select the next action.
        Parameters:
            loc: a Location is a two-entry tuple where entry 0
                contains x-coordinate and entry 1 contains the y-coordinate.
        Returns:
             An integer in the range 0-3 indicating which direction the robot
             will move.
        """
        #   Args:
        # loc: A tuple representing the x, y coordinates of a location.
        # direction: An integer in the range 0-3, were 0 = North, 1 = East
        #     2 = South and 3 = West
        self.exploredtiles.add(loc)

        # Checking if it has moved if it hasnt then we know there is 
        # an obstacle
        next_action = None
        if self.previouslocation == loc:
            self.obstacles.add(get_neighbor(loc, self.currentdirection))
            self.exploredtiles.add(get_neighbor(loc, self.currentdirection))

            self.currentdirection = (self.currentdirection - 1) % 4
            next_action = self.currentdirection
            # print("Object Found")

        # Checking each direction and if it is open go there
        if get_neighbor(loc, (self.currentdirection + 1) % 4) not in self.exploredtiles:
            next_action = (self.currentdirection + 1) % 4
            self.currentdirection = next_action
  
        elif get_neighbor(loc, (self.currentdirection + 2) % 4) not in self.exploredtiles:
            next_action = (self.currentdirection + 2) % 4
            self.currentdirection = next_action

        elif get_neighbor(loc, (self.currentdirection) % 4) not in self.exploredtiles:
            next_action = (self.currentdirection) % 4
            self.currentdirection = next_action 

        elif get_neighbor(loc, (self.currentdirection + 3) % 4) not in self.exploredtiles:
            next_action = (self.currentdirection + 3) % 4
            self.currentdirection = next_action
            
        elif get_neighbor(loc, (self.currentdirection + 4) % 4) not in self.exploredtiles:
            next_action = (self.currentdirection + 4) % 4
            self.currentdirection = next_action
        
        # Edge Case - If it gets stuck in a hole then it will 
        # randomize until it gets out
        neighbors = [get_neighbor(loc, i) 
                     for i in range(4) if get_neighbor(loc, i) in self.exploredtiles]
        
        if len(neighbors) > 3:
            # print("Are you getting here?")
            next_action = random.randint(0, 3)
            self.currentdirection = next_action
            neighbors = None

        self.previouslocation = loc

        return next_action
     
        # "Random case"
        # next_action = random.randint(0, 3)
        # if get_neighbor(loc, next_action) == loc:
        #     self.obstacles = loc
        # return next_action

        