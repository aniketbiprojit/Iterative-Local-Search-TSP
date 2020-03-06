def euclidean(a, b):
    x, y = 0, 1
    return (((a[x]-b[x])**2)+((a[y]-b[y])**2))**0.5

def route_dist(route,coordinates):
    dist=0
    for i in range(1,len(route)):
        dist+=euclidean(coordinates[route[i]],coordinates[route[i-1]])
    return dist

def nearest_neighbour(coordinates):
    x, y = 0, 1

    visited = [False]*len(coordinates)
    i = 1
    dist = 0
    order = [i]
    import math
    while(sum(visited) < 52):
        visited[i] = True
        dmin = math.inf
        for j in range(len(coordinates)):
            if(visited[j] == False):
                d = euclidean(coordinates[j], coordinates[i])
                if(d < dmin):
                    dmin = d
                    k = j
        i = k
        order.append(k)
        dist += dmin
        visited[k] = True
    return order, dist

def opt_2_swap(route,i,k):
    r1=route[:i]
    r2=route[i:k]
    r2=r2[::-1]
    r3=route[k:]
    return(r1+r2+r3)

with open('berlin52.txt', 'r') as f:
    l = f.readlines()

berlin_52 = [list(map(int, i.strip().split()))[:] for i in l]
from random import random,shuffle,seed,randint
seed(0)
shuffle(berlin_52)
# print(berlin_52)

route, dist = nearest_neighbour(berlin_52)
print("Distance from Nearest Neighbour:",dist)

def local_search(route,epochs,coordinates):
    # count=0
    dist=route_dist(route,coordinates)
    # while(count<epochs):
    #     new_route=route[:]
    #     a,b=randint(0,len(route)-1),randint(0,len(route)-1)
    #     a,b=min(a,b),max(a,b)
    #     new_route=opt_2_swap(route,a,b)
    #     new_dist=route_dist(new_route,coordinates)
    #     # print(new_dist)
    #     if(new_dist<dist):
    #         dist=new_dist
    #         route=new_route
    #         count=0
    #     count+=1

    for i in range(len(berlin_52)):
        for j in range(i,len(berlin_52)):
            new_route=opt_2_swap(route[:],i,j)
            new_dist=route_dist(new_route,berlin_52)

            if(new_dist<dist):
                dist=new_dist
                route=new_route
    return route

def double_bridge(route):
    i=randint(0,len(route)-1)//4
    j=i+randint(0,len(route)-1)//4
    k=j+randint(0,len(route)-1)//4
    #abcd adcb
    route_1=route[:i]+route[k:]
    route_2=route[j:k]+route[i:j]
    return route_1+route_2

def pertubation(route):
    new_route=route[:]
    new_route=double_bridge(new_route)
    
    return new_route

def search(route,max_iter,coordinates):
    route=local_search(route,50,coordinates)
    dmin=route_dist(route,coordinates)

    print("Distance after 2-Opt Approach:",dmin)
    for i in range(max_iter):
        new_route=route[:]
        new_route=pertubation(new_route)
        new_route=local_search(new_route,50,coordinates)    
        d=route_dist(new_route,coordinates)
        if(d<dmin):
            dmin=d
            route=new_route    

    print("Distance after Iterated 2-Opt Approach:",dmin)
    return route

(search(route,50,berlin_52))