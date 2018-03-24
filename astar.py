'''
Tristan Giles - 2018

Implementation of the A-Star algorithm for a square/rectangular grid.
Supports timing using the timit module

Happy Mazing!
'''

import heapq, math
from timeit import default_timer as timer

infinity = float('inf')

class AStar():

    def __init__(self, start, grid, height, width):
        self.start = start
        self.grid = grid
        self.height = height
        self.width = width

    #NOTE This is a node representing a square on the grid
    class searchNode():
        def __init__(self, position, fscore=infinity, gscore=infinity, parent=None):
            self.fscore = fscore
            self.gscore = gscore
            self.position = position
            self.parent = parent

        #NOTE This __lt__ override helps organize the heap when inserting new nodes
        def __lt__(self, comparator):
            return self.fscore < comparator.fscore

    #NOTE Method to create and retrieve search nodes
    class searchNodeMaker(dict):
        def __missing__(self, node):
            newNode = AStar.searchNode(node)
            self.__setitem__(node, newNode)
            return newNode

    def get_heuristic(self, end):
        #NOTE Euclidian distance heuristic
        (x1, y1) = self.start
        (x2, y2) = end
        return math.hypot(x2 - x1, y2 - y1)

    def get_node_neighbours(self, node):
        #NOTE Get's the 4 grid neighbours of the node (Change here if you want diagonal action too)
        (x, y) = node
        return [(dx, dy) for (dx, dy) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] if 0 <= dx < self.width and 0 <= dy < self.height and self.grid[dy][dx] == 1]

    def get_path(self, endPoint):
        current = endPoint
        path = []
        while current.position != self.start:
            path.append(current.position)
            current = current.parent
        path.append(self.start)
        return list(reversed(path))

    def computePath(self, end):
        #NOTE list of nodes to check
        openList = []
        currentSearchNode = AStar.searchNode(self.start, fscore=self.get_heuristic(end), gscore=0)
        nodeMaker = AStar.searchNodeMaker()
        heapq.heappush(openList, currentSearchNode)
        #NOTE List of nodes that have been checked
        closedList = []
        while openList:
            #NOTE Pop the lowest fscore (to-go + been from or gScore + hScore) and set it as current
            currentSearchNode = heapq.heappop(openList)
            #NOTE If it's the end, reconstruct the path
            if currentSearchNode.position == end:
                return self.get_path(currentSearchNode)
            else:
                #NOTE Append the current node to the closed list (It's checked, and will have it's neighbours checked) and get the neighbours
                closedList.append(currentSearchNode)
                neighbours = [nodeMaker[tocheck] for tocheck in self.get_node_neighbours(currentSearchNode.position)]
                for neighbour in neighbours:
                    #NOTE the score of this neighbour is the current gScore + 1
                    newGscore = currentSearchNode.gscore + 1
                    #NOTE If not been checked and it's gScore score is more than just 1 move, remove it from the open list
                    if neighbour in openList and newGscore < neighbour.gscore:
                        openList.remove(neighbour)
                    #NOTE If the neighbour gScore score is more and also in the checked list, remove it from the checked list
                    if newGscore < neighbour.gscore and neighbour in closedList:
                        closedList.remove(neighbour)
                    #NOTE If the node is in neither list, set it's scores and add it to the to-be checked list
                    if neighbour not in openList and neighbour not in closedList:
                        neighbour.gscore = newGscore
                        neighbour.fscore = neighbour.gscore + self.get_heuristic(neighbour.position)
                        neighbour.parent = currentSearchNode
                        heapq.heappush(openList, neighbour)
                    heapq.heapify(openList)
        #NOTE No path was found, return none
        return None


if __name__ == '__main__':
    start = timer()
    test_grid = [[1,0,1,1,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [1,1,1,0,1]]

    #NOTE Usage is AStar(StartPointTuple, GridMatrix, HeightUnits, WidthUnits).computePath(EndPointTuple)
    path = AStar((0,0), test_grid, 5, 5).computePath((4, 4))

    print(path)
    print("Time = {}".format(timer()-start))
