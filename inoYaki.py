import itertools
import random
#----------------------------↓solver_greedy.py------------------------------
import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    print("-----print greedyTour-----")
    print(tour)
    return tour
#----------------------------↑solver_greedy.py------------------------------
def makeTour(cities):#道順の初期値をランダムに(テキトーに決めてくれる)
    firstTour=[]
    citiesNumber=len(cities)
    citiesNumberIndex=list(range(0,citiesNumber))
    while True:
        if citiesNumberIndex==[]:
            break
        choicedNumber=random.choice(citiesNumberIndex)
        firstTour.append(choicedNumber)
        citiesNumberIndex.remove(choicedNumber)
    return firstTour


def calcuDist(cities,tour):#道順を与えると、トータル距離を計算してくれる
    allDist=0
    param=0
    while param < len(tour)-1:
        city1Number=tour[param]
        city2Number=tour[param+1]
        allDist+=distance(cities[city1Number],cities[city2Number])
        param+=1
    allDist+=distance(cities[tour[0]],cities[tour[len(tour)-1]]) #distance of first city to last city
    return allDist


def annealingoptimize(cities,firstTour,firstDist,distGreedy,T=10000, cool=0.99):#hill climb(?) or yakinamasi部分

    #初期値
    totalDist=firstDist
    tour=firstTour
    while T>0.0001:
        #値を交換する二つのindexの組み合わせをランダムに決める
        #下記テキトーな二つのcityを入れ替えるための操作
        citiesNumber=len(cities)
        citiesNumberIndex=(list(range(0,citiesNumber)))
        choicedCombi=random.sample(citiesNumberIndex,2)
        index0=choicedCombi[0]
        index1=choicedCombi[1]
        a=tour[index0] #選ばれたindexのcity
        b=tour[index1] #選ばれたindexのcity2
        calculatedTour=[]

        for city in tour:
            calculatedTour.append(city)
        
        calculatedTour[index1]=a
        calculatedTour[index0]=b
        #このcalculatedTourがテキトーに二点のcityを入れ替えた後の道順
        newTotalDist=calcuDist(cities,calculatedTour)
        #↓これの#消すと焼きなましに(?)、pの決め方テキトーです、ググってテキトーに決めた
        #p= pow(math.e, -abs(newTotalDist-totalDist)/T)

        if newTotalDist<totalDist: #or random.random()<p: ←これの#消すと焼きなましに(?)
            tour=calculatedTour
            totalDist=newTotalDist

        T=T*cool
    
    if totalDist>distGreedy:#Greedyより結果が悪かったらやり直す
        makeTour(cities)
        annealingoptimize(cities,tour,firstDist,distGreedy)
    else:
        print("-------print totalDist--------")
        print(totalDist)
        print("--------the best tour by hill climb---------")
        print(tour)
        allDist=calcuDist(cities,tour)
        print("---print all Dist----")
        print(totalDist)
        return tour
        

#----------------------------↓forMain ------------------------------
if __name__ == '__main__':
    #assert len(sys.argv) > 1
    #tour = solve(read_input(sys.argv[1]))
    #print_tour(tour)
    assert len(sys.argv) > 1
    cities=read_input(sys.argv[1])
    tourGreedy = solve(cities)
    distGreedy=calcuDist(cities,tourGreedy)
    print("-----print distGreedy------")
    print(distGreedy)#ここまでgreedyの実行(別にgreedyの実行は必要ないです、greedyによる算出結果が欲しかっただけ)

    firstTour=makeTour(cities)
    firstDist=calcuDist(cities,firstTour)
    annealingoptimize(cities,firstTour,firstDist,distGreedy)
   
#----------------------------↑forMain------------------------------


#-----------------コメント-------------------
#よくわからない....
#なんか16以上がかなり重くなる...
#何回か実行すると割と良さげな値が出る(?)
#多分、greedyよりよくなかったらやり直すってとこが重そう
#月以降、あんまり時間取れないからあげちゃった
#勝手にやってごめん...
#何なら無視しちゃって大丈夫だよー！！！

#-----------------コメント-------------------