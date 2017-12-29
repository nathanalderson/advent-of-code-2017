#!/usr/bin/env python3
import collections
import time
import math

def main():
    board = get_board("input")
    root = DominoeState(board)
    print("part 1:", root.solve(depthFirstSearch, score1))
    part2 = root.solve(depthFirstSearch, score2)
    part2 = round((part2 - math.floor(part2))*100000, 4)
    print("part 2:", part2)

def get_board(filename):
    with open(filename, "r") as f:
        tuples = [tuple(line.strip().split("/")) for line in f.readlines()]
        dominoes = tuple([(int(x), int(y)) for x,y in tuples])
        return Board(dominoes)


class Board():
    def __init__(self, dominoes, end = 0):
        self.bag = dominoes
        self.end = end

    def move(self, dominoe):
        if dominoe in self.bag:
            if dominoe[0] == self.end:
                end = dominoe[1]
            elif dominoe[1] == self.end:
                end = dominoe[0]
            else:
                raise ValueError("Illegal move")
            return Board(tuple(d for d in self.bag if d != dominoe), end)
        else:
            raise ValueError("No such dominoe")

    def possible_moves(self):
        return tuple([dom for dom in self.bag if dom[0] == self.end or dom[1] == self.end])

    def __str__(self):
        return "Board<end={},left={}>".format(self.end, len(self.bag))


# from http://www.kosbie.net/cmu/fall-11/15-112/handouts/ai-search/notes-ai-search.html
class Stack(object):
    def __init__(self):    self.dq = collections.deque()    
    def push(self, value): self.dq.append(value)
    def pop(self):         return self.dq.pop()
    def isEmpty(self):     return len(self.dq) == 0


def score1(state):
    score = 0
    for m in state.listMoves():
        score += m[0] + m[1]
    return score

def score2(state):
    moves = state.listMoves()
    length = len(moves)
    strength = sum(m[0] + m[1] for m in moves)
    return length + (strength * .00001)

# from http://www.kosbie.net/cmu/fall-11/15-112/handouts/ai-search/notes-ai-search.html
def depthFirstSearch(state, scorer):
    """Returns list of moves to get to a goal state."""
    if state.isGoal():
        return [ ]
    time0 = time.time()
    seen = set()
    stack = Stack()
    stack.push(state)
    best = 0
    while not stack.isEmpty():
        state = stack.pop()
        for child in state.getChildren():
            if child.isGoal():
                best = max(scorer(child), best)
            if child not in seen:
                seen.add(child)
                stack.push(child)
    return best

# from http://www.kosbie.net/cmu/fall-11/15-112/handouts/ai-search/notes-ai-search.html
class State(object):
    # override these methods for your game's state
    def isGoal(self):      raise NotImplementedError
    def getChildren(self): raise NotImplementedError

    # override this if you want A* to work:
    def minStepsToGoal(self): raise NotImplementedError

    # override these if your board is not a 2d list
    # or if you need more than .board to determine equality
    def __hash__(self):
        return hash2dList(self.board)
    def __eq__(self, other):
        if (isinstance(other, State)):
            return (self.board == other.board)
        else:
            return (self is None and other is None)

    # do not (generally) override these methods and variables
    instances = 0  # counts the total # of State objects created

    def __init__(self, parent=None, move=None):
        self.parent = parent
        self.move = move  # how to get here from the parent state
        self.depth = 0 if (parent == None) else (1+parent.depth)
        State.instances += 1
        if (State.instances % 100000 == 0): print(State.instances)
        elif (State.instances % 10000 == 0): print("*", end="")
        elif (State.instances % 1000 == 0): print(".", end="")

    def listMoves(self):
        """Return a list of this state, its parent, etc, where
           this state is the last element in the list."""
        moves = collections.deque()
        state = self
        while (state.parent != None):
            moves.appendleft(state.move)
            state = state.parent
        return list(moves)

    def solve(self, solver, scorer):
        print("Solving with solver =", solver.__name__)
        self.parent = None   # so move list of soln stops here
        self.depth = 0       # so depth counting starts here
        State.instances = 0  # reset count of instances created
        solutionPath = None
        score = solver(self, scorer)
        print("   states created:", State.instances)
        return score

class DominoeState(State):
    def __init__(self, board, *args, **kwargs):
        self.board = board
        super().__init__(*args, **kwargs)

    def isGoal(self):
        return len(self.board.possible_moves()) == 0

    def getChildren(self):
        return [DominoeState(self.board.move(m), self, m) for m in self.board.possible_moves()]

    def __hash__(self):
        return self.board.__hash__()

if __name__ == "__main__":
    main()

