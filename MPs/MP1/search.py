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
        "astar_multi": astar_multi,
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
        num_states +=1
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
        # num_states += 1
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
        nonlocal num_states
        if tempnode == End:
            flag = 1
            return

        else:
            # it has been visited
            visit[tempnode[0]][tempnode[1]] = 1
            path.append(tempnode)
            num_states +=1
            # find its possible neighbors
            valid_neighbors = maze.getNeighbors(tempnode[0], tempnode[1])
            for pos_node in valid_neighbors:
                if visit[pos_node[0]][pos_node[1]] == 0:
                    if flag == 0:
                        dfs_handler(pos_node)
            if flag == 0:
                visit[tempnode[0]][tempnode[1]] = 0
                path.pop()

    dfs_handler(tempnode)
    print(visit)
    # num_states = len(path)
    path.append(End)
    return path, num_states


# The support function used in greedy's heapq for the priority decision of distance
def distGet(End, curnode):
    dist = abs(End[0] - curnode[0]) + abs(End[1] - curnode[1])
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
    heapq.heappush(prio_q, (distGet(End, Start), Start))

    while len(prio_q) != 0:
        ele = heapq.heappop(prio_q)
        tempnode = ele[1]
        num_states += 1

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
            heapq.heappush(prio_q, (distGet(End, pos_nodes), pos_nodes))

    # now the tempnode reach to End; we need back trace and push it into a stack for
    # path print; so count the num_states
    while tempnode != Start:
        path.append(tempnode)
        next_node = father[tempnode[0]][tempnode[1]]
        # num_states += 1
        tempnode = next_node
    path.append(Start)
    path.reverse()

    return path, num_states


def astar(maze):
    num_states = 0
    path = []
    # receive the parameters from maze
    Rows = maze.getDimensions()[0]
    Columns = maze.getDimensions()[1]
    # use to store whether this point have been visited
    visit = [[0 for i in range(Columns)] for j in range(Rows)]
    # use to record the back trace
    father = [[0 for i in range(Columns)] for j in range(Rows)]
    path_len = [[0 for i in range(Columns)] for j in range(Rows)]
    Start = maze.getStart()  # the coordinate to start
    objectives = maze.getObjectives()  # find all objectives

    prio_q = q.PriorityQueue()

    father[Start[0]][Start[1]] = Start  # set start's self to be its father
    # print(manhattan_min(objectives,Start))
    prio_q.put((manhattan_min(objectives, Start), Start))

    while prio_q:
        ele = prio_q.get()

        tempnode = ele[1]
        num_states += 1
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
            prio_q.put((manhattan_min(objectives, pos_nodes) + path_len[pos_nodes[0]][pos_nodes[1]], pos_nodes))
    # print("here")
    # now the tempnode reach to End; we need back trace and push it into a stack for
    # path print; so count the num_states
    while tempnode != Start:
        path.append(tempnode)
        next_node = father[tempnode[0]][tempnode[1]]
        tempnode = next_node
    path.append(Start)
    path.reverse()
    return path, num_states


# the function to create mst over the objectives;
# root is the root node(tuple); Objectives is the list of tuples with objects
def mst(index, Objectives):
    n = len(Objectives)
    not_in_list = [i for i in range(n)]
    connected_Matrix = [[0 for i in range(n)] for j in range(n)]
    dist_Matrix = [[0 for i in range(n)] for j in range(n)]
    # construct the dist_Matrix first
    for i in range(n):
        for j in range(i+1):
            dist_Matrix[i][j] = distGet(Objectives[i], Objectives[j])
            dist_Matrix[j][i] = distGet(Objectives[j], Objectives[i])
        connected_Matrix[i][i] = 1

    contained = [index]
    not_in_list.remove(index)

    while len(not_in_list) > 0:
        min_idx = not_in_list[0]
        min_cor_idx = contained[0]
        min_dist = dist_Matrix[min_idx][min_cor_idx]
        # for each idx we make the compare
        for idx in not_in_list:
            for orgidx in contained:
                if dist_Matrix[idx][orgidx] < min_dist:
                    min_idx = idx
                    min_cor_idx = orgidx
                    min_dist = dist_Matrix[idx][orgidx]
        connected_Matrix[min_idx][min_cor_idx] = 1
        connected_Matrix[min_cor_idx][min_idx] = 1
        contained.append(min_idx)
        not_in_list.remove(min_idx)


    return connected_Matrix


def astar_multi(maze):
    tpath = []
    num_states = 0
    # receive the parameters from maze
    Rows = maze.getDimensions()[0]
    Columns = maze.getDimensions()[1]

    # Objectives is the list of tuples with objects
    Objectives = maze.getObjectives()

    # then we find the closest objects and start inserting path
    Start_Point = maze.getStart()
    index = 0
    min_dist = distGet(Start_Point, Objectives[0])
    for i in range(len(Objectives)):
        if distGet(Start_Point, Objectives[i]) < min_dist:
            index = i
            min_dist = distGet(Start_Point, Objectives[i])

    Matrix = mst(index, Objectives)

    # now index holds the closest index to Start Point
    # We have two parts in finding the path
    # 1. find the path from Start Point to Objectives[index]
    # 2. traverse in the Objectives' MST to complete the path

    # support function in astar_multi to find the minimum path between SP and EP, added to the path
    def Path_Add(SP, EP):
        path = []
        num_states = 0
        # use to store whether this point have been visited
        visit = [[0 for i in range(Columns)] for j in range(Rows)]
        # use to record the back trace
        father = [[0 for i in range(Columns)] for j in range(Rows)]
        path_len = [[0 for i in range(Columns)] for j in range(Rows)]

        prio_q = q.PriorityQueue()
        father[SP[0]][SP[1]] = SP  # set start's self to be its father
        prio_q.put((distGet(SP, EP), SP))

        while prio_q:
            ele = prio_q.get()
            tempnode = ele[1]
            num_states += 1
            # now we find the final EP
            if tempnode == EP:
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
                prio_q.put((distGet(pos_nodes, EP) + path_len[pos_nodes[0]][pos_nodes[1]], pos_nodes))
        # now start print node to path
        while tempnode != SP:
            path.append(tempnode)
            next_node = father[tempnode[0]][tempnode[1]]
            tempnode = next_node
        path.append(SP)
        path.reverse()
        return path, num_states

    # first add the path from start to nearest obj
    temp_path, temp_num_states = Path_Add(Start_Point, Objectives[index])
    tpath = tpath + temp_path
    num_states += temp_num_states

    # then is the recursive part to traverse the tree
    def RecurTree(Matrix, cur_idx, last_idx):
        nonlocal tpath
        nonlocal num_states
        # find the possible next_node first
        pos_next_set = []
        for i in range(len(Matrix)):
            if Matrix[cur_idx][i] == 1 and i != cur_idx and i != last_idx:
                pos_next_set.append(i)
        # then find the path to these nodes
        for pos_index in pos_next_set:
            pathi, i_numstates = Path_Add(Objectives[cur_idx], Objectives[pos_index])
            tpath = tpath + pathi
            num_states += i_numstates

            # then recursive in the new node
            RecurTree(Matrix, pos_index, cur_idx)

            # when get back, add the reversed path
            pathi.reverse()
            tpath = tpath + pathi
            num_states += i_numstates

    RecurTree(Matrix, index, len(Objectives) + 1)

    return tpath, num_states
