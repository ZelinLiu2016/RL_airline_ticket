import random
import numpy as np
GAMMA = 0.8
Q = np.zeros((6,6))
R=np.asarray([[-1,-1,-1,-1,0,-1],
   [-1,-1,-1,0,-1,100],
   [-1,-1,-1,0,-1,-1],
   [-1,0, 0, -1,0,-1],
   [0,-1,-1,0,-1,100],
   [-1,0,-1,-1,0,100]])


def getMaxQ(state):
    return max(Q[state, :])


def generateNext(state):
    candidate = []
    for i in xrange(6):
        if R[state][i] >= 0:
            candidate.append(i)
    ran = random.randint(0, len(candidate)-1)
    return candidate[ran]


def QLearning(state):
    if state == 5:
        return
    nextState = generateNext(state)
    Q[state][nextState] = R[state][nextState] + GAMMA * getMaxQ(nextState)
    QLearning(nextState)


if __name__ == "__main__":
    for step in range(1, 10000):
        print "Episode %d" % step
        start = random.randint(0,5)
        QLearning(start)
    print Q
