# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import queue
import heapq
import queue as q

# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # return path, num_states_explored; output init
    num_states = 0
    path = []
    # receive the parameters from maze
    Rows = maze.getDimensions()[0]
    Columns = maze.getDimensions()[1]

    # use to store whether this point have been visited
    visit = [[0 for i in range(Columns)] for j in range(Rows)]
    # use to record the back trace
    father = [[0 for i in range(Columns)] for j in range(Rows)]

    Start = maze.getStart()  # the coordinate to start
    End = maze.getObjectives()[0]  # we just need the first one to get
    q = queue.Queue()  # to store the traverse processes
    father[Start[0]][Start[1]] = Start  # set start's self to be its father
    q.put(Start)

    while not q.empty():
        tempnode = q.get()
        # if we find the final output; break and ready to insert
        if tempnode == End:
            break
        # it's not end; then set it visited and find its valid neighbor
        visit[tempnode[0]][tempnode[1]] = 1
        valid_neighbors = maze.getNeighbors(tempnode[0], tempnode[1])
        for pos_nodes in valid_neighbors:
            # if the valid neighbor has been visited; just skip
            if visit[pos_nodes[0]][pos_nodes[1]]:
                continue
            # now it has been visited
            visit[pos_nodes[0]][pos_nodes[1]] = 1
            # set its father to tempnode
            father[pos_nodes[0]][pos_nodes[1]] = tempnode
            q.put(pos_nodes)

    # now the tempnode reach to End; we need back trace and push it into a stack for
    # path print; so count the num_states
    while tempnode != Start:
        path.append(tempnode)
        next_node = father[tempnode[0]][tempnode[1]]
        num_states += 1
        tempnode = next_node
    path.append(Start)
    path.reverse()

    return path, num_states


def dfs(maze):
    num_states = 0
    path = []
    # receive the parameters from maze
    Rows = maze.getDimensions()[0]
    Columns = maze.getDimensions()[1]

    # use to store whether this point have been visited
    visit = [[0 for i in range(Columns)] for j in range(Rows)]

    Start = maze.getStart()  # the coordinate to start
    End = maze.getObjectives()[0]  # we just need the first one to get
    tempnode = Start
    flag = 0
    def dfs_handler(tempnode):
        nonlocal visit
        nonlocal path
        nonlocal maze
        nonlocal flag
        if tempnode == End:
            flag = 1
            return

        else:
            # it has been visited
            visit[tempnode[0]][tempnode[1]] = 1
            path.append(tempnode)
            # find its possible neighbors
            valid_neighbors = maze.getNeighbors(tempnode[0], tempnode[1])
            for pos_node in valid_neighbors:
                if visit[pos_node[0]][pos_node[1]] == 0:
                    if flag == 0:
                        dfs_handler(pos_node)
            if flag==0:
                visit[tempnode[0]][tempnode[1]] = 0
                path.pop()

    dfs_handler(tempnode)
    print(visit)
    num_states = len(path)
    path.append(End)
    return path, num_states


# The support function used in greedy's heapq for the priority decision of distance
def distGet(End, curnode):
    dist = abs(End[0]-curnode[0]) + abs(End[1]-curnode[1])
    return dist

# The function to find the closest object in maze to the node.
def manhattan_min(objectives, node):
    minn = distGet(objectives[0], node)
    for i in objectives[1:]:
        new_dist = distGet(i, node)
        if minn > new_dist:
            minn = new_dist
            
    return minn
        
def greedy(maze):
    # return path, num_states_explored; output init
    num_states = 0
    path = []
    # receive the parameters from maze
    Rows = maze.getDimensions()[0]
    Columns = maze.getDimensions()[1]

    # use to store whether this point have been visited
    visit = [[0 for i in range(Columns)] for j in range(Rows)]
    # use to record the back trace
    father = [[0 for i in range(Columns)] for j in range(Rows)]

    Start = maze.getStart()  # the coordinate to start
    End = maze.getObjectives()[0]  # we just need the first one to get

    father[Start[0]][Start[1]] = Start  # set start's self to be its father
    prio_q = []
    heapq.heappush(prio_q, (distGet(End,Start), Start))

    while len(prio_q) != 0:
        ele = heapq.heappop(prio_q)
        tempnode = ele[1]
        # if we find the final output; break and ready to insert
        if tempnode == End:
            break
        # it's not end; then set it visited and find its valid neighbor
        visit[tempnode[0]][tempnode[1]] = 1
        valid_neighbors = maze.getNeighbors(tempnode[0], tempnode[1])
        for pos_nodes in valid_neighbors:
            # if the valid neighbor has been visited; just skip
            if visit[pos_nodes[0]][pos_nodes[1]]:
                continue
            # now it has been visited
            visit[pos_nodes[0]][pos_nodes[1]] = 1
            # set its father to tempnode
            father[pos_nodes[0]][pos_nodes[1]] = tempnode
            heapq.heappush(prio_q, (distGet(End,pos_nodes), pos_nodes))

    # now the tempnode reach to End; we need back trace and push it into a stack for
    # path print; so count the num_states
    while tempnode != Start:
        path.append(tempnode)
        next_node = father[tempnode[0]][tempnode[1]]
        num_states += 1
        tempnode = next_node
    path.append(Start)
    path.reverse()

    return path, num_states


    
def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states=0
    path=[]
    # receive the parameters from maze
    Rows = maze.getDimensions()[0]
    Columns = maze.getDimensions()[1]
    # use to store whether this point have been visited
    visit = [[0 for i in range(Columns)] for j in range(Rows)]
    # use to record the back trace
    father = [[0 for i in range(Columns)] for j in range(Rows)]
    path_len= [[0 for i in range(Columns)] for j in range(Rows)]
    Start = maze.getStart()  # the coordinate to start
    objectives = maze.getObjectives()  # find all objectives
    
    prio_q=q.PriorityQueue()
    
    father[Start[0]][Start[1]] = Start  # set start's self to be its father
    # print(manhattan_min(objectives,Start))
    prio_q.put((manhattan_min(objectives,Start),Start))
    
    while prio_q:
        ele = prio_q.get()
        
        tempnode = ele[1]
        
        # print("tempnode: ")
        # print(tempnode)
        if tempnode in objectives:
            break
        # it's not end; then set it visited and find its valid neighbor
        
        visit[tempnode[0]][tempnode[1]] = 1
        valid_neighbors = maze.getNeighbors(tempnode[0], tempnode[1])
        for pos_nodes in valid_neighbors:
            # print(pos_nodes,path_len[tempnode[0]][tempnode[1]]+1)
            if visit[pos_nodes[0]][pos_nodes[1]]:
                continue
            # now it has been visited
            visit[pos_nodes[0]][pos_nodes[1]] = 1
            # set its father to tempnode
            path_len[pos_nodes[0]][pos_nodes[1]] = path_len[tempnode[0]][tempnode[1]] + 1
            father[pos_nodes[0]][pos_nodes[1]] = tempnode
            prio_q.put((manhattan_min(objectives, pos_nodes)+path_len[pos_nodes[0]][pos_nodes[1]], pos_nodes))
    # print("here")
    # now the tempnode reach to End; we need back trace and push it into a stack for
    # path print; so count the num_states
    while tempnode != Start:
        path.append(tempnode)
        next_node = father[tempnode[0]][tempnode[1]]
        num_states += 1
        tempnode = next_node
    path.append(Start)
    path.reverse()
    return path, num_states

# def astr_multi(maze):


    
