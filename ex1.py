import search
import math
import utils

id = "No numbers - I'm special!"

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77
DOT = 11
RIGHT = "R"
LEFT = "L"
DOWN = "D"
UP = "U"
EMPTY_SLOT = 10
""" Rules 
WALL = 9
PLAYER_EATEN_BY_GHOST = 88
PACMAN = 77
RED_GHOST_WITH_PILL = 21
BLUE_GHOST_WITH_PILL = 31
YELLOW_GHOST_WITH_PILL = 41
GREEN_GHOST_WITH_PILL = 51


"""


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman: 
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman."""

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        actions = ("R", "D", "L", "U")
        successors = []
        for action in actions:
            new_state = self.calculate_successor_state(state, action)
            # print((action, new_state))
            successors.append((action, new_state))
        # print(tuple(successors))
        return tuple(successors)

    def calculate_successor_state(self, state, action):
        # Find the position of Pacman in the current state
        pacman_position = self.find_position(state, PACMAN)

        # Define possible movements for ghosts in the specified order
        ghost_movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Calculate the new position for Pacman based on the action
        new_pacman_position = self.calculate_new_position(pacman_position, action)

        # Check if the new position is within the bounds of the game board
        if self.is_valid_position(new_pacman_position, state):
            # Check if Pacman encounters a pill, and update the state accordingly
            new_state = self.update_state_for_pacman(state, pacman_position, new_pacman_position)
            # print(new_state)
            # Move ghosts based on Manhattan distance and order
            for ghost in (RED, BLUE, YELLOW, GREEN):
                ghost_x, ghost_y = self.find_position(state, ghost)
                if ghost_x is not None and ghost_y is not None:
                    new_state = self.move_ghost(new_state, ghost, new_pacman_position, ghost_movements, ghost_x,
                                                ghost_y)
                    # print(new_state)
            return new_state
        else:
            # If the new position is invalid, return the current state
            return state

    def find_position(self, state, element):
        """Find the position of an element in the state."""
        for i, row in enumerate(state):
            for j, value in enumerate(row):
                if value == element:
                    return (i, j)
        return (None, None)

    def calculate_new_position(self, position, action):
        """Calculate the new position based on the action."""
        x, y = position
        if action == "R":
            return (x, y + 1)
        elif action == "D":
            return (x + 1, y)
        elif action == "L":
            return (x, y - 1)
        elif action == "U":
            return (x - 1, y)

    def is_valid_position(self, position, state):
        """Check if the new position is valid."""
        x, y = position
        return 0 <= x < len(state) and 0 <= y < len(state[0])

    def update_state_for_pacman(self, state, current_position, new_position):
        """Update the state when Pacman encounters a pill."""
        state_matrix = list(state)
        for i in range(len(state_matrix)):
            state_matrix[i] = list(state_matrix[i])

        current_x, current_y = current_position
        new_x, new_y = new_position

        # Check if Pacman encounters a pill at the new position
        if state_matrix[new_x][new_y] == DOT:
            # Remove the pill from the old position
            state_matrix[current_x][current_y] = EMPTY_SLOT

            # Move Pacman to the new position
            state_matrix[new_x][new_y] = PACMAN
        # else:
        #     # If no pill is encountered, Pacman remains in the same state
        #     return tuple(state_matrix)
        for i in range(len(state_matrix)):
            state_matrix[i] = tuple(state_matrix[i])
        return tuple(state_matrix)

    def move_ghost(self, state, ghost, pacman_position, ghost_movements, ghost_x, ghost_y):
        """Move ghosts based on Manhattan distance and order."""
        state_matrix = list(state)
        for i in range(len(state_matrix)):
            state_matrix[i] = list(state_matrix[i])

        # Calculate the Manhattan distance to Pacman for each possible movement
        distances = [self.manhattan_distance((ghost_x + dx, ghost_y + dy), pacman_position)
                     for dx, dy in ghost_movements]
        # TODO: אם תזוזת הרוח ל2- כיוונים מקרבת אותה לשחקן באותה מידה, אז סדר העדיפויות לתזוזה צריך להיות: ימינה, למטה, שמאלה ולבסוף למעלה.
        # Choose the movement with the minimum distance
        min_distance_index = distances.index(min(distances))
        dx, dy = ghost_movements[min_distance_index]

        # TODO: רוח לא יכולה לעבור למשבצת שנמצאת בה רוח אחרת או קיר. )משמע: בשום מצב שתי רוחות לא יכולות להימצא באותה משבצת.(
        # TODO: הערה: מצב כישלון במשחק )רוח אכלה את השחקן( אין להמשיך לפתח את המצבים על ענף זה.
        # Move the ghost to the new position
        new_ghost_x, new_ghost_y = ghost_x + dx, ghost_y + dy
        state_matrix[ghost_x][ghost_y] = EMPTY_SLOT
        state_matrix[new_ghost_x][new_ghost_y] = ghost

        for i in range(len(state_matrix)):
            state_matrix[i] = tuple(state_matrix[i])
        return tuple(state_matrix)

    def manhattan_distance(self, pos1, pos2):
        """Calculate the Manhattan distance between two positions."""
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def result(self, state, move):
        """given state and an action and return a new state"""
        print("state:\n", state)
        print("move:\n", move)
        utils.raiseNotDefined()

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        for row in state:
            for cell in row:
                if cell == DOT:
                    # print("Some Dots left - goal_test returns False")
                    return False
        return True
        utils.raiseNotDefined()

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        # Calculate the Manhattan distance to the nearest dot
        pacman_position = self.find_position(node.state, PACMAN)
        dots_positions = [self.find_position(node.state, DOT) for row in node.state]
        nearest_dot_distance = min(
            self.manhattan_distance(pacman_position, dot) for dot in dots_positions if dot is not None)
        return nearest_dot_distance
        utils.raiseNotDefined()


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
