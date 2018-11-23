import queue
import copy
import heapq
import sys
sys.setrecursionlimit(100000)

dx =[1,0,0,-1]
dy=[0,1,-1,0]

class PriorityQueue:
    pq=[]
    elements={}
    task=0

    def insert(self , priority,x_val,y_val):
        entry = [priority, self.task,x_val,y_val]
        self.elements[self.task]=entry
        heapq.heappush(self.pq, entry)
        self.task += 1

    def delete(self,task):
        entry = self.elements[task]
        entry[-1] = None

    def pop(self):
        while self.pq:
            priority, task, x_val , y_val = heapq.heappop(self.pq)
            if task != None:
                del self.elements[task]
                return priority, x_val , y_val
        raise KeyError('Pop from an empty Priority Queue')

    def size(self):
        return len(self.elements)



def text_write(where , out_list,ans,row,col):
    f = open( where + "_output.txt", 'w')

    for i in range(1,row+1):
        for j in range(1,col+1):
            data ="%d " %out_list[i][j]
            f.write(data)
        f.write("\n")
    f.write("---\n")
    data2 = "length = %d\n" %ans[0]
    f.write(data2)
    data3 = "time = %d" %ans[1]
    f.write(data3)
    f.close()



def text_info(where):
    f = open("./input/" + where+".txt" , 'r')
    line = f.readline()
    line = line.replace("\n", "")
    result = line.split(" ")
    a=[int(result[0]),int(result[1]),int(result[2])]
    return a

def text_read(where,row,col):
    f = open("./input/"+where+".txt", 'r')
    line = f.readline()
    list1 = [[0 for cols in range(col + 1)] for rows in range(row + 1)]
    a = 1
    line2 = f.readline()
    while line2:
        line2 = line2.replace("\n", "")
        result2 = line2.split(" ")
        for v in range(col):
            list1[a][v + 1] = int(result2[v])
        line2 = f.readline()
        a += 1
    f.close()
    return list1

def position_check(pos , out_list , row , col):
    for r in range(1,row+1):
        for c in range(1,col+1):
            if out_list[r][c] == 3 or out_list[r][c] == 6 or out_list[r][c] == 4:
                pos.append([r,c])
    return pos

def bfs(start ,end, out_list , row , col , ans):
    des = [[0 for c in range(col+1)] for r in range(row+1)]
    visit = [[0 for c in range(col+1)] for r in range(row+1)]
    q = queue.Queue()
    q.put(start)
    visit[start[0]][start[1]]=1;
    des[start[0]][start[1]]=0;
    ans[1] +=1
    while not q.empty():
        if visit[end[0]][end[1]] ==1:
            break
        cur_task = q.get()
        x=cur_task[0]
        y=cur_task[1]
        for k in range (4):
            nx = x + dx[k]
            ny = y + dy[k]
            if nx >= 1 and nx <=row and ny >=1 and ny<=col and out_list[nx][ny] != 1:
                if visit[nx][ny] != 1:
                    visit[nx][ny] =1
                    des[nx][ny] = des[x][y] +1
                    q.put([nx,ny])
                    ans[1] += 1

    ans[0] += des[end[0]][end[1]]
    num = des[end[0]][end[1]]
    target = [end[0],end[1]]

    for n in range(num,0,-1):
        tx=target[0]
        ty=target[1]
        out_list[tx][ty]=5
        for k in range(4):
            ntx=tx+dx[k]
            nty=ty+dy[k]
            if ntx >= 1 and ntx <= row and nty >= 1 and nty <= col and out_list[ntx][nty] != 1:
                if des[ntx][nty] == n-1:
                    target=[ntx,nty]
    return out_list

def IDS(start , end , out_list , row , col , ans):
    des = [[0 for c in range(col + 1)] for r in range(row + 1)]
    find=[0]
    limit = 0
    while find[0] != 1:
        limit +=1
        visit = [[0 for c in range(col + 1)] for r in range(row + 1)]
        des[start[0]][start[1]] = 0;
        visit[start[0]][start[1]] = 1

        dfs(start, end, out_list, row, col, ans, limit, des, visit, find)

    ans[0] += limit
    num=limit
    target = [end[0],end[1]]

    for n in range(num, 0, -1):
        tx = target[0]
        ty = target[1]
        out_list[tx][ty] = 5
        for k in range(4):
            ntx = tx + dx[k]
            nty = ty + dy[k]
            if ntx >= 1 and ntx <= row and nty >= 1 and nty <= col and out_list[ntx][nty] != 1:
                if des[ntx][nty] == n - 1:
                    target = [ntx, nty]

    return out_list

def dfs(start , end , out_list , row , col ,ans , limit,des,visit,find):
    if visit[end[0]][end[1]] == 1:
        find[0]=1
        return
    x=start[0]
    y=start[1]
    for k in range(4):
        nx = x+dx[k]
        ny=y+dy[k]
        if nx >= 1 and nx <= row and ny >= 1 and ny <= col and out_list[nx][ny] != 1:
            if visit[nx][ny] != 1:
                if des[x][y]+1 <=limit:
                    visit[nx][ny]=1
                    des[nx][ny] = des[x][y]+1
                    next_start=[nx,ny]
                    ans[1]+=1
                    dfs(next_start , end , out_list , row , col , ans , limit, des , visit,find)

def astar(start , end , out_list , row , col , ans):
    des = [[0 for c in range(col + 1)] for r in range(row + 1)]
    visit = [[0 for c in range(col + 1)] for r in range(row + 1)]
    visit[start[0]][start[1]] = 1;
    des[start[0]][start[1]] = 0;

    pq2 = PriorityQueue()
    while pq2.size() !=0:
        pq2.pop()
    manhattan_d = abs(start[0]-end[0])+abs(start[1]-end[1])
    pq2.insert(manhattan_d,start[0],start[1])
    while pq2.size() != 0:
        if visit[end[0]][end[1]] == 1:
            break
        priority, x_val, y_val = pq2.pop()
        for k in range(4):
            nx = x_val + dx[k]
            ny = y_val + dy[k]
            if nx >= 1 and nx <= row and ny >= 1 and ny <= col and out_list[nx][ny] != 1:
                if visit[nx][ny] != 1:
                    visit[nx][ny]=1
                    des[nx][ny]=des[x_val][y_val]+1
                    d=abs(nx-end[0])+abs(ny-end[1])+des[nx][ny]
                    pq2.insert(d,nx,ny)
                    ans[1] += 1

    ans[0] += des[end[0]][end[1]]
    num = des[end[0]][end[1]]
    target = [end[0], end[1]]

    for n in range(num,0,-1):
        tx=target[0]
        ty=target[1]
        out_list[tx][ty]=5
        for k in range(4):
            ntx=tx+dx[k]
            nty=ty+dy[k]
            if ntx >= 1 and ntx <= row and nty >= 1 and nty <= col and out_list[ntx][nty] != 1:
                if des[ntx][nty] == n-1:
                    target=[ntx,nty]
    return out_list

def greedy(start , end , out_list , row , col , ans):
    des = [[0 for c in range(col + 1)] for r in range(row + 1)]
    visit = [[0 for c in range(col + 1)] for r in range(row + 1)]
    visit[start[0]][start[1]] = 1;
    des[start[0]][start[1]] = 0;

    pq2 = PriorityQueue()
    while pq2.size() !=0:
        pq2.pop()
    manhattan_d = abs(start[0]-end[0])+abs(start[1]-end[1])
    pq2.insert(manhattan_d,start[0],start[1])
    while pq2.size() != 0:
        if visit[end[0]][end[1]] == 1:
            break
        priority, x_val, y_val = pq2.pop()
        for k in range(4):
            nx = x_val + dx[k]
            ny = y_val + dy[k]
            if nx >= 1 and nx <= row and ny >= 1 and ny <= col and out_list[nx][ny] != 1:
                if visit[nx][ny] != 1:
                    visit[nx][ny]=1
                    des[nx][ny]=des[x_val][y_val]+1
                    d=abs(nx-end[0])+abs(ny-end[1])
                    pq2.insert(d,nx,ny)
                    ans[1] += 1

    ans[0] += des[end[0]][end[1]]
    num = des[end[0]][end[1]]
    target = [end[0], end[1]]

    for n in range(num,0,-1):
        tx=target[0]
        ty=target[1]
        out_list[tx][ty]=5
        for k in range(4):
            ntx=tx+dx[k]
            nty=ty+dy[k]
            if ntx >= 1 and ntx <= row and nty >= 1 and nty <= col and out_list[ntx][nty] != 1:
                if des[ntx][nty] == n-1:
                    target=[ntx,nty]
    return out_list


def test_floor():
    where = "test1"
    info = text_info(where)
    row = info[1]
    col = info[2]
    out_list = text_read(where , row , col)
    pos = []
    pos = position_check(pos,out_list, row , col)
    deepcopy_copy1 = copy.deepcopy(out_list)
    deepcopy_copy2 = copy.deepcopy(out_list)
    ans=[0,0]

    #path1=bfs(pos[0],pos[1],deepcopy_copy1,row,col,ans)
    #path2=bfs(pos[1],pos[2],deepcopy_copy2,row,col,ans)

    #path1 = IDS(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = IDS(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = astar(pos[0],pos[1],deepcopy_copy1,row,col,ans)
    #path2 = astar(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    path1 = greedy(pos[0],pos[1],deepcopy_copy1,row,col,ans)
    path2 = greedy(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    for i in range(1, row):
        for j in range(1, col + 1):
            if path1[i][j] == 5 or path2[i][j] == 5:
                out_list[i][j] = 5

    text_write(where, out_list, ans, row, col)


def fifth_floor():
    where = "fifth_floor"
    info = text_info(where)
    row = info[1]
    col = info[2]
    out_list = text_read(where, row, col)
    pos = []
    pos = position_check(pos, out_list, row, col)
    deepcopy_copy1 = copy.deepcopy(out_list)
    deepcopy_copy2 = copy.deepcopy(out_list)
    ans = [0, 0]
    #path1 = bfs(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = bfs(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = IDS(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = IDS(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = astar(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = astar(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    path1 = greedy(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    path2 = greedy(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    for i in range(1, row):
        for j in range(1, col + 1):
            if path1[i][j] == 5 or path2[i][j] == 5:
                out_list[i][j] = 5

    text_write(where, out_list, ans, row, col)


def forth_floor():
    where = "fourth_floor"
    info = text_info(where)
    row = info[1]
    col = info[2]
    out_list = text_read(where, row, col)
    pos = []
    pos = position_check(pos, out_list, row, col)
    deepcopy_copy1 = copy.deepcopy(out_list)
    deepcopy_copy2 = copy.deepcopy(out_list)
    ans = [0, 0]

    #path1 = bfs(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = bfs(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = IDS(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = IDS(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = astar(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = astar(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    path1 = greedy(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    path2 = greedy(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    for i in range(1, row):
        for j in range(1, col + 1):  # col 한개 안하면... 뭔가 될듯 ㅋㅋ
            if path1[i][j] == 5 or path2[i][j] == 5:
                out_list[i][j] = 5

    text_write(where, out_list, ans, row, col)


def third_floor():
    where = "third_floor"
    info = text_info(where)
    row = info[1]
    col = info[2]
    out_list = text_read(where, row, col)
    pos = []
    pos = position_check(pos, out_list, row, col)
    deepcopy_copy1 = copy.deepcopy(out_list)
    deepcopy_copy2 = copy.deepcopy(out_list)
    ans = [0, 0]

    #path1 = bfs(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = bfs(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = IDS(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = IDS(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = astar(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = astar(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    path1 = greedy(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    path2 = greedy(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    for i in range(1, row):
        for j in range(1, col + 1):  # col 한개 안하면... 뭔가 될듯 ㅋㅋ
            if path1[i][j] == 5 or path2[i][j] == 5:
                out_list[i][j] = 5

    text_write(where, out_list, ans, row, col)

def second_floor():
    where = "second_floor"
    info = text_info(where)
    row = info[1]
    col = info[2]
    out_list = text_read(where, row, col)
    pos = []
    pos = position_check(pos, out_list, row, col)
    deepcopy_copy1 = copy.deepcopy(out_list)
    deepcopy_copy2 = copy.deepcopy(out_list)
    ans = [0, 0]

    #path1 = bfs(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = bfs(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = IDS(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = IDS(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = astar(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = astar(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    path1 = greedy(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    path2 = greedy(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    for i in range(1, row):
        for j in range(1, col + 1):
            if path1[i][j] == 5 or path2[i][j] == 5:
                out_list[i][j] = 5

    text_write(where, out_list, ans, row, col)

def first_floor():
    where = "first_floor"
    info = text_info(where)
    row = info[1]
    col = info[2]
    out_list = text_read(where, row, col)
    pos = []
    pos = position_check(pos, out_list, row, col)
    deepcopy_copy1 = copy.deepcopy(out_list)
    deepcopy_copy2 = copy.deepcopy(out_list)
    ans = [0, 0]

    #path1 = bfs(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = bfs(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = IDS(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = IDS(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    #path1 = astar(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    #path2 = astar(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    path1 = greedy(pos[0], pos[1], deepcopy_copy1, row, col, ans)
    path2 = greedy(pos[1], pos[2], deepcopy_copy2, row, col, ans)

    for i in range(1, row):
        for j in range(1, col + 1):  # col 한개 안하면... 뭔가 될듯 ㅋㅋ
            if path1[i][j] == 5 or path2[i][j] == 5:
                out_list[i][j] = 5

    text_write(where, out_list, ans, row, col)

#test_floor()
fifth_floor()
forth_floor()
third_floor()
second_floor()
first_floor()

