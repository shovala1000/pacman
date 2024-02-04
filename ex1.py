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
WALL = 99
PLAYER_EATEN_BY_GHOST = 88
INVALID_STATE = "Error99"


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
        actions = (UP, RIGHT, DOWN, LEFT)
        successors = []
        for action in actions:
            new_state = self.result(state, action)
            if new_state != INVALID_STATE:
                successors.append((action, new_state))
        return tuple(successors)

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
            state_list = list(state)
            for row in range(len(state)):
                state_list[row] = list(state[row])
            # Check if Pacman encounters a dot or a ghost, and update the state accordingly
            new_state = self.update_state_for_pacman(state_list, pacman_position, new_pacman_position)

            if new_state == INVALID_STATE:
                return INVALID_STATE
            # print(new_state)

            # Move ghosts based on Manhattan distance and order: red, blue, yellow and green
            for ghost in (RED, BLUE, YELLOW, GREEN):
                ghost_x, ghost_y = self.find_position(state_list, ghost)
                if ghost_x is None or ghost_y is None:
                    ghost = ghost + 1
                    ghost_x, ghost_y = self.find_position(state_list, ghost)  # Ghost with dot
                # If ghost exist
                if new_state != INVALID_STATE and ghost_x is not None and ghost_y is not None:
                    new_state = self.move_ghost(new_state, ghost, new_pacman_position, ghost_movements, ghost_x,
                                                ghost_y)
                    # print(new_state)

            if new_state == INVALID_STATE:
                return INVALID_STATE
            else:
                for i in range(len(new_state)):
                    new_state[i] = tuple(new_state[i])
                new_state = tuple(new_state)
                # print(type(new_state))
                return new_state
        else:
            # If the new position is invalid, return the current state
            return INVALID_STATE

    def is_state_valid(self, state):
        for row in state:
            if PLAYER_EATEN_BY_GHOST in row:
                return False
        return True

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

    def update_state_for_pacman(self, state_list, current_position, new_position):
        """Update the state when Pacman encounters a dot or a ghost."""
        ghost_list = [RED, BLUE, GREEN, YELLOW, RED_DOT, BLUE_DOT, GREEN_DOT, YELLOW_DOT]

        current_x, current_y = current_position
        new_x, new_y = new_position

        # Check if Pacman encounters a ghost at the new position
        if state_list[new_x][new_y] in ghost_list:
            return INVALID_STATE
        else:
            # Move Pacman to the new position
            state_list[current_x][current_y] = EMPTY_SLOT
            state_list[new_x][new_y] = PACMAN

        # for i in range(len(state_list)):
        #     state_list[i] = tuple(state_list[i])
        # return tuple(state_list)
        return state_list

    def move_ghost(self, state_list, ghost, pacman_position, ghost_movements, ghost_x, ghost_y):
        if state_list == INVALID_STATE:
            print("problemmmmmmm")
        if state_list == ((51, 10, 10, 10), (10, 99, 99, 11), (77, 10, 10, 10), (20, 10, 10, 10)):
            print("")
        """Move ghosts based on Manhattan distance and order."""
        ghost_list = [RED, BLUE, GREEN, YELLOW]
        ghost_list_with_dot = [RED_DOT, BLUE_DOT, GREEN_DOT, YELLOW_DOT]
        # Calculate the Manhattan distance to Pacman for each possible movement
        distances = [self.manhattan_distance((ghost_x + dx, ghost_y + dy), pacman_position)
                     for dx, dy in ghost_movements]
        # Distances not empty
        flag_error = 4  # Number of len(distances)
        while flag_error:
            # Choose the movement with the minimum distance
            min_distance_index = distances.index(min(distances))
            dx, dy = ghost_movements[min_distance_index]
            max_distance_val = max(distances)
            # Move the ghost to the new position
            new_ghost_x, new_ghost_y = ghost_x + dx, ghost_y + dy
            if self.is_valid_position((new_ghost_x, new_ghost_y), state_list):

                # New position have a ghost
                if (state_list[new_ghost_x][new_ghost_y] in ghost_list
                        or state_list[new_ghost_x][new_ghost_y] in ghost_list_with_dot):
                    distances[min_distance_index] = max_distance_val + 1
                    flag_error = flag_error - 1
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
                if state_list[new_ghost_x][new_ghost_y] == DOT:
                    state_list[new_ghost_x][new_ghost_y] = ghost_with_dot
                #     New position is empty
                elif state_list[new_ghost_x][new_ghost_y] == EMPTY_SLOT:
                    state_list[new_ghost_x][new_ghost_y] = ghost_without_dot
                    # New position have a pacman
                elif state_list[new_ghost_x][new_ghost_y] == PACMAN:
                    return INVALID_STATE
                    # state_list[new_ghost_x][new_ghost_y] = PLAYER_EATEN_BY_GHOST
                else:
                    print("state_list", state_list)
                    print("ERROR1 - state_list[", new_ghost_x, "][", new_ghost_y, "]: ",
                          state_list[new_ghost_x][new_ghost_y])

                # Old position have a dot
                if ghost in ghost_list_with_dot:
                    state_list[ghost_x][ghost_y] = DOT
                else:
                    state_list[ghost_x][ghost_y] = EMPTY_SLOT

                return state_list

            else:
                distances[min_distance_index] = max_distance_val + 1
                flag_error = flag_error - 1
        return state_list

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
        ghost_list_with_dot = [RED_DOT, BLUE_DOT, GREEN_DOT, YELLOW_DOT]

        # Calculate the remainder dots
        state = node.state
        count = 0
        for row in state:
            for elem in row:
                if elem == DOT or elem in ghost_list_with_dot:
                    count += 1
        return count


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
