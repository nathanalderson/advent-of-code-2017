#!/usr/bin/env python3

def main():
    bag = get_bag("input")

def get_bag(filename):
    with open(filename, "r") as f:
        tuples = [tuple(line.strip().split("/")) for line in f.readlines()]
        ints = [(int(x), int(y)) for x,y in tuples]
        return Bag(ints)

class Board():
    def __init__(self, dominoes):
        self.doms = dominoes
        self.end = 0
    def pull(self, val):
        for dom in self.doms:
            if dom[0] == val:
                self.doms.remove(dom)
                return dom[1]
            elif dom[1] == val:
                self.doms.remove(dom)
                return dom[0]
        else:
            return None
    def isEmpty(self):
        return len(self.doms) == 0

if __name__ == "__main__":
    main(

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
        if (State.instances % 100000 == 0): print State.instances
        elif (State.instances % 10000 == 0): print "*",
        elif (State.instances % 1000 == 0): print ".",

    def listMoves(self):
        """Return a list of this state, its parent, etc, where
           this state is the last element in the list."""
        moves = collections.deque()
        state = self
        while (state.parent != None):
            moves.appendleft(state.move)
            state = state.parent
        return list(moves)

    def solve(self, solver):
        print "Solving with solver =", solver.__name__
        self.parent = None   # so move list of soln stops here
        self.depth = 0       # so depth counting starts here
        State.instances = 0  # reset count of instances created
        solutionPath = None
        try:
            solutionPath = solver(self)
            print "   None!" if (solutionPath == None) else "   Solved!"
        except Exception as err:
            print "  ", (str(err) or type(err))
        print "   states created:", State.instances
        return solutionPath

