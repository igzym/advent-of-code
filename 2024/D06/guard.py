import os
import util
import numpy as np
from collections import defaultdict
from typing import Tuple, List, Set, Optional  # need to upgrade python to 3.12 for modern typing syntax

from util import debug

script_name = os.path.basename(__file__)
day_number = 5

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


Position = Tuple[int, int]


class Guard:
    UP: str = "^"
    DOWN: str = "v"
    LEFT: str = "<"
    RIGHT: str = ">"

    # directions in the order of turning to the right
    dir_cycle = [UP, RIGHT, DOWN, LEFT]


    def __init__(self, lines: List[str]) -> None:
        if not lines:
            raise ValueError("empty data set on input")
        
        lines_mtx = util.to_matrix(lines)
        m = len(lines_mtx)
        n = len(lines_mtx[0])

        # the map of the area, indicating empty spaces and obstacles
        self.mapm = np.zeros(shape=(m, n), dtype=int)

        self.position: Position = None  # current positon of the guard
        self.dir: str = None  # current direction of the guard

        for i in range(m):
            for j in range(n):
                c = lines_mtx[i][j]
                if c == "#":
                    self.mapm[i, j] = 1  # obstacle in map
                elif c in Guard.dir_cycle:
                    self.position: Position = i, j  # guard position
                    self.dir = c
        # save guard's starting position and direction
        self.initial_position: Position = self.position
        self.initial_dir = self.dir

        self.visited: Set[Position] = set()  # visited positions
        self.visited.add(self.position)

        self.visited_in_dir = defaultdict(set)  # set of direction in which given position was visited
        self.visited_in_dir[self.position].add(self.dir)

        self.additional_obstacles: Set[Position] = set()  # locations of possible additional obstacles identified so far


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
        i, j = position
        return self.mapm[i, j] == 0


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


    def move(self) -> None:
        # change the state, either change the position if possible
        # or turn
        position = self.next_pos()
        if self.is_pos_unobstructed(position):
            self.position = position
            self.visited.add(self.position)
            self.visited_in_dir[self.position].add(self.dir)
            debug("move to", self.position, "in dir", self.dir)
        else:
            self.turn()
            self.visited_in_dir[self.position].add(self.dir)
            self.print_state()
            debug("turn in", self.position, "in dir", self.dir)


    def count_of_visited_positions(self) -> int:
        return len(self.visited)


    def __str__(self) -> str:
        return f"Guard at {self.position}, dir: {self.dir}"


    def print_state(self, obs_pos: Optional[Position]=None) -> None:
        m, n = self.mapm.shape
        pmtx = []
        for i in range(m):
            pmtx.append(["."] * n)
        for i in range(m):
            for j in range(n):
                if self.mapm[i, j] != 0:
                    pmtx[i][j] = "#"
                else:
                    if (i, j) in self.visited_in_dir:
                        dirs = self.visited_in_dir[(i, j)]
                        vert = Guard.UP in dirs or Guard.DOWN in dirs
                        hori = Guard.LEFT in dirs or Guard.RIGHT in dirs
                        if vert and hori:
                            pmtx[i][j] = '+'
                        elif vert:
                            pmtx[i][j] = "|"
                        elif hori:
                            pmtx[i][j] = "-"
                        else:
                            pmtx[i][j] = "?"
        i0, j0 = self.initial_position
        pmtx[i0][j0] = self.initial_dir
        if obs_pos is not None:
            iobs, jobs = obs_pos
            pmtx[iobs][jobs] = "O"

        for r in pmtx:
            debug("".join(r))


def main(lines, part):
    result = 0

    guard = Guard(lines)
    debug("map")        
    debug(guard.mapm)
    debug("guard state", guard)


    if part == 1:
        while True:
            debug(result, "in state", guard)
            i, j = guard.position
            if guard.about_to_exit():
                # next move, the guard will exit, stop iterating
                result = guard.count_of_visited_positions()
                debug("exiting", guard)
                break
            # generate next move
            guard.move()
    else:
        # part 2
        while True:
            debug(result, "in state", guard)

            if guard.about_to_exit():
                debug(result, "about to exit", guard)
                break

            # have I been on this location in the past
            # but going in the direction I would go if I turned
            # right?
            past_dirs = guard.visited_in_dir[guard.position]
            if past_dirs:
                debug("seen", guard.position, "in directions", past_dirs)

            nd = guard.new_direction()
            # was I in this state but in "next turn" direction?
            if nd in past_dirs:
                debug(f"... was in direction after turn, '{nd}', in this position alrady")
                # see if we generate a cycle by placing an obstcle just in front of the
                # current guard position
                obstacle_position = guard.next_pos()
                if obstacle_position  == guard.initial_position:
                    continue  # we cannot place an obstacle on guards initial location
                if not guard.is_pos_unobstructed(obstacle_position):
                    continue  # there is already an obstacle
                if obstacle_position in guard.additional_obstacles:
                    continue  # we have already considered and addition of an obstacle here
                # looks like we identified a potential new obstacle
                guard.additional_obstacles.add(obstacle_position)
                result += 1
                debug(result, "potential new obstacle", obstacle_position, guard.additional_obstacles)
                guard.print_state(obstacle_position)
                ## XXX next idea: was in direction after turn on the same line...
            # generate next move
            guard.move()

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
