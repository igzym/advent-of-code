import os
import util
import numpy as np
from collections import defaultdict
import copy
from typing import Tuple, List, Set, Optional  # need to upgrade python to 3.12 for modern typing syntax

from util import debug

script_name = os.path.basename(__file__)
day_number = 6

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


Position = Tuple[int, int]
State = Tuple[Position, str]

class Guard:
    UP: str = "^"
    DOWN: str = "v"
    LEFT: str = "<"
    RIGHT: str = ">"

    mapm = None
    initial_position: Position = None
    initial_dir = None

    # directions in the order of turning to the right
    dir_cycle = [UP, RIGHT, DOWN, LEFT]


    def initialize_map(lines: List[str]) -> None:  # NOTE: class method
        if not lines:
            raise ValueError("empty data set on input")

        lines_mtx = util.to_matrix(lines)
        m = len(lines_mtx)
        n = len(lines_mtx[0])

        # the map of the area, indicating empty spaces and obstacles
        Guard.mapm = np.zeros(shape=(m, n), dtype=int)

        for i in range(m):
            for j in range(n):
                c = lines_mtx[i][j]
                if c == "#":
                    Guard.mapm[i, j] = 1  # obstacle in map
                elif c in Guard.dir_cycle:
                    Guard.initial_position = i, j
                    Guard.initial_dir = c


    def __init__(self, state: Optional[State]=None) -> None:
        if Guard.mapm is None:
            raise AssertionError("class variables have not been initialized")

        if state is not None:
            self.position, self.dir = state
        else:
            self.position = Guard.initial_position
            self.dir = Guard.initial_dir

        self.extra_obstacle: Position = None

    def next_pos(self) -> Position:
        # calculate next position if we were to move
        # return the coordinates
        i, j = self.position
        if self.dir == Guard.UP:
            i -=1
        elif self.dir == Guard.DOWN:
            i += 1
        elif self.dir == Guard.LEFT:
            j -= 1
        elif self.dir == Guard.RIGHT:
            j += 1
        return i, j


    def is_pos_unobstructed(self, position: Position) -> bool:
        # does given position contain an obstacle?
        if position == self.extra_obstacle:  # we play with extra obstacles in part 2
            return False
        i, j = position
        return self.mapm[i, j] == 0
    

    def set_extra_obstacle(self, position: Position) -> bool:
        self.extra_obstacle = position


    def is_off_map(self, i: int, j: int) -> bool:
        m, n = self.mapm.shape
        if i < 0 or i >= m:
            return True
        if j < 0 or j >= n:
            return True
        return False


    def new_direction(self) -> str:
        gsi = Guard.dir_cycle.index(self.dir)
        return Guard.dir_cycle[(gsi + 1) % len(Guard.dir_cycle)]


    def turn(self) -> None:
        # change direction by turning to right
        self.dir = self.new_direction()


    def about_to_exit(self) -> bool:
        # am I on the edge of the map and facing the direction
        # such that next move would leave the map?
        i, j = self.next_pos()
        return self.is_off_map(i, j)
    
    def is_facing_obstacle(self) -> bool:
        np = self.next_pos()
        return not self.is_pos_unobstructed(np)


    def move(self) -> None:
        # change the state, either change the position if possible
        # or turn
        position = self.next_pos()
        if self.is_pos_unobstructed(position):
            self.position = position
        else:
            self.turn()
        assert self.is_pos_unobstructed(self.position)


    def count_of_visited_positions(self) -> int:
        return len(self.visited)


    def __str__(self) -> str:
        return f"Guard at {self.position}, dir: {self.dir}"


def main(lines, part):
    result = 0

    Guard.initialize_map(lines)
    guard = Guard()
    debug("map")        
    debug(guard.mapm)
    debug("guard state", guard)

    # let the guard follow its path until it leaves the map
    # unique positions visited (part 1 question)
    visited_positions: Set[Position] = set()
    path_trace: List[Position] = [] # sequential list of positons, not necessarily unique, for debugging
    # register all the states (position and direction) it passes through (needed for part 2)
    visited_states: Set[State] = set()  # unique visited states
    visited_states_list: List[State] = []  # unique visited states in order of visit
    while True:
        debug("part 1: guard in positon", guard)
        visited_positions.add(guard.position)
        path_trace.append(guard.position)
        state = guard.position, guard.dir
        if state not in visited_states:
            visited_states.add(state)
            visited_states_list.append(state)
        if guard.about_to_exit():
            # next move, the guard will exit, stop iterating
            #debug("guard about to leave the grid, stop iteration", guard)
            print("part 1: leaving map in state", guard)
            break
        guard.move()


    if part == 1:
        result = len(visited_positions)
    else:
        # part 2
        # for each state (position and direction) the guard visits, place an extra obstacle
        # just in front and let the guard run until it leaves the map or cycles
        # if a cycle is detected (revisiting the same state), the obstacle is added to the set
        # of solutions

        state_idx = 0
        obstacles_found: Set[Position] = set()
        N = len(visited_states_list) - 1
        # skip the last of the visited states because that one is just before going off the map
        for position, dir in visited_states_list[:-1]:

            state_idx += 1
            guard_for_obstacle_sim = Guard((position, dir))
            debug("guard for obstacle simulation", guard_for_obstacle_sim)

            # this can happen only on the last visited state, which we excluded from the loop
            assert not guard_for_obstacle_sim.about_to_exit()

            if guard_for_obstacle_sim.is_facing_obstacle():
                # already facing an obstacle
                debug("this state is already facing an obstacle, stop", guard_for_obstacle_sim)
                continue

            obstacle_position = guard_for_obstacle_sim.next_pos()
            debug("assuming obstacle at", obstacle_position)
            if obstacle_position == Guard.initial_position:
                debug(f"cannot place obstacle at {obstacle_position} because it's the guard's initial position")
                continue
            if obstacle_position in obstacles_found:
                debug(f"obstacle {obstacle_position} already identified as cycle-inducing")
                continue

            # let the guard run with the extra obstacle in place
            # until exit or until it returns to the initial state
            guard = Guard()
            guard.set_extra_obstacle(obstacle_position)
            # visited_states_2: Set[State] = set()
            # then iterate until you get off the grid or cycle
            cycle_len = 0
            visited_states_2: Set[State] = set()
            while True:
                debug("... inner guard", guard)
                if guard.about_to_exit():
                    debug("... simulated guard going off map, stop", guard)
                    break
                state = guard.position, guard.dir
                if state in visited_states_2:
                    result += 1
                    debug(f"{result:4}: ({state_idx}/{N}) FOUND cycle for {obstacle_position} of length {cycle_len}")
                    obstacles_found.add(obstacle_position)
                    break
                visited_states_2.add(state)
                guard.move()
                cycle_len += 1

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
