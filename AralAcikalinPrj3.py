#Aral Açıkalın 20161701036
#written using python version 3.8.0 64-bit


import math
import random
from timeit import default_timer as timer
#pip install pandas will donwload this library
import pandas


def randomExp(lambd):
    '''Creating a random inter-arival time in seconds'''  
    #creates a random inter-arrival variable 
    #dividing lambda by 60 gives the rate of cars arriving per second so inter-arrival time is in seconds
    nextArrival=random.expovariate(lambd/60) 
    return nextArrival

def simulation(lambda1,lambda2,lambda3,mean1,debug):
    '''
    takes 3 lambda values and 1 mean value for 3 lanes and 1 toll booth then 
    simulates the system, if as a 5th input true is given it generates the simulation as table
    '''  
    #for counting the percentage of cars arriving from the different roads
    lane1CarCount=0
    lane2CarCount=0
    lane3CarCount=0


    #for holding the last arrival times for lanes
    lastArrivalLane1=0
    lastArrivalLane2=0
    lastArrivalLane3=0

    #this array holds all the infos of cars
    #stores respectively; 
    #arrival-time, service-time, service begin time, queue time, service end time, time in sistem.
    cars=[[0,0,0,0,0,0,0,0]] #initialized with all 0's because when checking for the last cars service end time it should be 0 in order to not effect the simulation.
    #this array holds the next inter-arrival time for 3 lanes.
    car=[0,0,0]
    #this block of code creates first 3 inter-arrival time.
    lane1=randomExp(lambda1)
    car[0]=lane1
    lane2=randomExp(lambda2)
    car[1]=lane2
    lane3=randomExp(lambda3)
    car[2]=lane3

    for i in range(1,1000001):
        #this for begins from 1st index because when checking for last cars service end time 0-1 gives out of bounds error for the array.
        #for the same reason it also ends on +1 the desired number.

        #these if/if-else blocks generates a new car inter-arrival time when the last car in lane serviced
        if not(lastArrivalLane1+lane1 in car):
            lane1=randomExp(lambda1)
            car[0]=lastArrivalLane1+lane1
            
        elif not(lastArrivalLane2+lane2 in car):
            lane2=randomExp(lambda2)
            car[1]=lastArrivalLane2+lane2

        elif not(lastArrivalLane3+lane3 in car):
            lane3=randomExp(lambda3)
            car[2]=lastArrivalLane3+lane3
            
        #here we check which car is next to get serviced.
        if(car[0]<car[1] and car[0]<car[2]):
            serviceTime=randomExp(mean1)
            lastArrivalLane1=car[0]
            idleTime=0
            prevServiceEndTime=cars[i-1][4]

            #if booth is idle then we calculate idle time by arrival time- previous service end time 
            if(prevServiceEndTime<lastArrivalLane1):

                #if booth is idle then service begins immidiatly when car arrives
                serviceBegins=lastArrivalLane1
                idleTime=lastArrivalLane1-prevServiceEndTime
            else:
                #otherwise service begins after previous service ends
                serviceBegins=cars[i-1][4]

            queueTime=serviceBegins-lastArrivalLane1
            serviceEndTime=serviceBegins+serviceTime
            timeinSystem=queueTime+serviceTime
            whichlane="Lane 1"
            cars.append([lastArrivalLane1,serviceTime,serviceBegins,queueTime,serviceEndTime,timeinSystem,idleTime,whichlane])

            lane1CarCount+=1 #for calculating propobality cars coming from this lane
            car[0]=0 #this car enters service

        elif(car[1]<car[0] and car[1]<car[2]):
            serviceTime=randomExp(mean1)
            lastArrivalLane2=car[1]
            idleTime=0
            prevServiceEndTime=cars[i-1][4]

            if(prevServiceEndTime<lastArrivalLane2):
                #if booth is idle service begins at arrival time of the var
                serviceBegins=lastArrivalLane2
                idleTime=lastArrivalLane2-prevServiceEndTime
            else:
                #otherwise service begins after previous service ends
                serviceBegins=cars[i-1][4]

            queueTime=serviceBegins-lastArrivalLane2
            serviceEndTime=serviceBegins+serviceTime
            timeinSystem=queueTime+serviceTime
            whichlane="Lane 2"
            cars.append([lastArrivalLane2,serviceTime,serviceBegins,queueTime,serviceEndTime,timeinSystem,idleTime,whichlane])

            lane2CarCount+=1 #for calculating propobality cars coming from this lane
            car[1]=0 #this car enters service
        elif(car[2]<car[0] and car[2]<car[1]):
            serviceTime=randomExp(mean1)
            lastArrivalLane3=car[2]
            idleTime=0
            prevServiceEndTime=cars[i-1][4]

            if(prevServiceEndTime<lastArrivalLane3):
                #if booth is idle service begins at arrival time of the var
                serviceBegins=lastArrivalLane3
                idleTime=lastArrivalLane3-prevServiceEndTime
            else:
                #otherwise service begins after previous service ends
                serviceBegins=cars[i-1][4]

            queueTime=serviceBegins-lastArrivalLane3
            serviceEndTime=serviceBegins+serviceTime
            timeinSystem=queueTime+serviceTime
            whichlane="Lane 3"
            #stores every calculated data for the car that serviced in an array as an array.
            cars.append([lastArrivalLane3,serviceTime,serviceBegins,queueTime,serviceEndTime,timeinSystem,idleTime,whichlane])

            lane3CarCount+=1 #for calculating propobality cars coming from this lane
            car[2]=0  #this car enters service

    #install pandas library by pip install pandas
    if(debug==True):
        #setting panda to show more than 10 rows of table and to show more than 5 collumns
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        pandas.set_option('display.width', None)
        pandas.set_option('display.max_colwidth', -1)
        #giving cars array and setting the name of the collumns.
        table = pandas.DataFrame(cars, columns = ["Arrival Time","Service Time","Service Begin Time","Queue Time","Service Ending Time","Time in System","Server Idle Time","Lane"]) 
        
        print(table.head(90),"\n")
        


    queTimeSum=0
    countCars=-1 #starts from -1 because I add a empty element into the cars array in order to initialize for the first time
    #this for statement is for calculating average queue time
    for car in cars:
        queTimeSum+=car[3]
        countCars+=1
    queTimeAverage=queTimeSum/countCars
    timeinSystemSum=0

    #this for statement is for calculating average time in system
    for car in cars:
        timeinSystemSum+=car[5]
    averageTimeinSystemTime=timeinSystemSum/countCars
    
    percentlane1=(lane1CarCount/countCars)*100
    percentlane2=(lane2CarCount/countCars)*100
    percentlane3=(lane3CarCount/countCars)*100
    
    print("Number of Cars: ",countCars)
    print("Average Time in System: ",averageTimeinSystemTime," seconds.")
    print("Average Queue Time: ",queTimeAverage, " seconds.")
    print("Lane 1 Percentage: ",percentlane1,"%")
    print("Lane 2 Percentage: ",percentlane2,"%")
    print("Lane 3 Percentage: ",percentlane3,"%")


def main():
    lambda1=int(input("Enter λ1: ")) 
    lambda2=int(input("Enter λ2: "))
    lambda3=int(input("Enter λ3: "))
    mean=int(input("Enter µ: "))
    debug=bool(int(input("Is Debug Mode (0 means false, 1 means true): ")))

    start=timer() #for outputing the run time of the code
    simulation(lambda1,lambda2,lambda3,mean,debug)
    print("")
    print("Time Elapsed: ",timer()-start," seconds.")

main()