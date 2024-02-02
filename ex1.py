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
RED_DOT = 21
BLUE_DOT = 31
YELLOW_DOT = 41
GREEN_DOT = 51
WALL = 9
PLAYER_EATEN_BY_GHOST = 88
INVALID_STATE = "Error"


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
        actions = (RIGHT, DOWN, LEFT, UP)
        successors = []
        for action in actions:
            new_state = self.result(state, action)
            if new_state != INVALID_STATE:
                successors.append((action, new_state))
        return tuple(successors)

    def is_state_valid(self, state):
        for row in state:
            if PLAYER_EATEN_BY_GHOST in row:
                return False
        return True

    def result(self, state, move):
        """given state and an action and return a new state"""
        # Find the position of Pacman in the current state
        pacman_position = self.find_position(state, PACMAN)

        # Define possible movements for ghosts in the specified order: right, down, left, up
        ghost_movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Calculate the new position for Pacman based on the action
        new_pacman_position = self.calculate_new_position(pacman_position, move)

        # Check if the new position is within the bounds of the game board
        if self.is_valid_position(new_pacman_position, state):
            # Check if Pacman encounters a dot or a ghost, and update the state accordingly
            new_state = self.update_state_for_pacman(state, pacman_position, new_pacman_position)
            if new_state == INVALID_STATE:
                return INVALID_STATE
            # Move ghosts based on Manhattan distance and order: red, blue, yellow and green
            for ghost in (RED, BLUE, YELLOW, GREEN):
                ghost_x, ghost_y = self.find_position(state, ghost)
                # If ghost exist
                if ghost_x is not None and ghost_y is not None:
                    new_state = self.move_ghost(new_state, ghost, new_pacman_position, ghost_movements, ghost_x,
                                                ghost_y)
                    # print(new_state)
            return new_state
        else:
            # If the new position is invalid, return the current state
            return INVALID_STATE

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
        if action == RIGHT:
            return (x, y + 1)
        elif action == DOWN:
            return (x + 1, y)
        elif action == LEFT:
            return (x, y - 1)
        elif action == UP:
            return (x - 1, y)

    def is_valid_position(self, position, state):
        """Check if the new position is valid."""
        x, y = position
        return 0 <= x < len(state) and 0 <= y < len(state[0]) and state[x][y] is not WALL

    def update_state_for_pacman(self, state, current_position, new_position):
        """Update the state when Pacman encounters a dot or a ghost."""
        ghost_list = [RED, BLUE, GREEN, YELLOW, RED_DOT, BLUE_DOT, GREEN_DOT, YELLOW_DOT]
        state_matrix = list(state)
        for i in range(len(state_matrix)):
            state_matrix[i] = list(state_matrix[i])

        current_x, current_y = current_position
        new_x, new_y = new_position

        # Check if Pacman encounters a ghost at the new position
        if state_matrix[new_x][new_y] in ghost_list:
            return INVALID_STATE
        else:
            # Move Pacman to the new position
            state_matrix[current_x][current_y] = EMPTY_SLOT
            state_matrix[new_x][new_y] = PACMAN

        for i in range(len(state_matrix)):
            state_matrix[i] = tuple(state_matrix[i])
        return tuple(state_matrix)

    def move_ghost(self, state, ghost, pacman_position, ghost_movements, ghost_x, ghost_y):
        """Move ghosts based on Manhattan distance and order."""
        ghost_list = [RED, BLUE, GREEN, YELLOW]
        ghost_list_with_dot = [RED_DOT, BLUE_DOT, GREEN_DOT, YELLOW_DOT]
        # Calculate the Manhattan distance to Pacman for each possible movement
        distances = [self.manhattan_distance((ghost_x + dx, ghost_y + dy), pacman_position)
                     for dx, dy in ghost_movements]
        # Distances not empty
        while distances:
            # Choose the movement with the minimum distance
            min_distance_index = distances.index(min(distances))
            dx, dy = ghost_movements[min_distance_index]

            # Move the ghost to the new position
            new_ghost_x, new_ghost_y = ghost_x + dx, ghost_y + dy
            if self.is_valid_position((new_ghost_x, new_ghost_y), state):
                state_matrix = list(state)
                for i in range(len(state_matrix)):
                    state_matrix[i] = list(state_matrix[i])

                # New position have a ghost
                if (state[new_ghost_x][new_ghost_y] in ghost_list
                        or state[new_ghost_x][new_ghost_y] in ghost_list_with_dot):
                    distances.pop(min_distance_index)
                    continue
                ghost_with_dot = ghost
                ghost_without_dot = ghost
                if ghost in ghost_list_with_dot:
                    ghost_index = ghost_list_with_dot.index(ghost)
                    ghost_without_dot = ghost_list[ghost_index]
                else:
                    ghost_index = ghost_list.index(ghost)
                    ghost_with_dot = ghost_list_with_dot[ghost_index]

                # New position have a dot
                if state_matrix[new_ghost_x][new_ghost_y] == DOT:
                    state_matrix[new_ghost_x][new_ghost_y] = ghost_with_dot
                #     New position is empty
                elif state_matrix[new_ghost_x][new_ghost_y] == EMPTY_SLOT:
                    state_matrix[new_ghost_x][new_ghost_y] = ghost_without_dot
                    # New position have a pacman
                elif state_matrix[new_ghost_x][new_ghost_y] == PACMAN:
                    return INVALID_STATE
                    distances.pop(min_distance_index)
                    continue
                    # state_matrix[new_ghost_x][new_ghost_y] = PLAYER_EATEN_BY_GHOST
                    #     TODO: STOP THIS BRANCH
                else:
                    print("ERROR1")

                # Old position have a dot
                if ghost in ghost_list_with_dot:
                    state_matrix[ghost_x][ghost_y] = DOT
                else:
                    state_matrix[ghost_x][ghost_y] = EMPTY_SLOT

                for i in range(len(state_matrix)):
                    state_matrix[i] = tuple(state_matrix[i])
                return tuple(state_matrix)

            else:
                distances.pop(min_distance_index)
        return state

    def manhattan_distance(self, pos1, pos2):
        """Calculate the Manhattan distance between two positions."""
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        ghost_list_with_dot = [RED_DOT, BLUE_DOT, GREEN_DOT, YELLOW_DOT]
        for row in state:
            for cell in row:
                if cell == DOT or cell in ghost_list_with_dot:
                    return False
        return True

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        # Calculate the remainder dots
        state = node.state
        count = 0
        for row in state:
            for elem in row:
                if elem == DOT:
                    count += 1
        return count
        utils.raiseNotDefined()


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
