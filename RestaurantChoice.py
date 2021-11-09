import csv
import geopy.distance
import time
import os

global file

class Restaurant:
    #__slots__=['name','loc','type','rating','price','reviews']
    def __init__(self,name,loc,type,rating,price,reviews):
        self.name=name
        self.loc=loc
        self.type=type
        self.rating=rating
        self.price=price
        self.reviews=reviews
    def __repr__(self):
        return '{'+str(self.name)+', '+str(self.loc)+', '+str(self.type)+', '+str(self.rating)+', '+str(self.reviews)+'}'
def init():
    global file
    file=input("Enter file:\n")
    lat=input("Enter your current GPS latitude:\n")
    long=input("Enter your current GPS longitude:\n")
    restaurants=readData(file,lat,long)
    types=['American','BBQ','Brunch','Cajun','Chinese','Italian','Mediterranean','Sandwich','Other','Any']
    prices=['Any','1','2','3']
    main(types,restaurants)
def readData(file,lat,long):
    data=csv.reader(open(file,"r"))
    next(data,None)
    restaurants=[]
    for res in data:
        if res is not None:
            try:
                restaurants.append(Restaurant(res[0],findDistance(lat,long,res[1],res[2]),res[3],res[4],res[5],res[6]))
            except:
                pass
    return restaurants
def findDistance(latH,longH,lat,long):
    homeLoc=latH,longH
    loc=lat,long
    return round(geopy.distance.distance(homeLoc,loc).miles,2)  
    pass
def main(types,restaurants):
    print("Restaurants\n---------------------------\n1. Compare restaurants \n2. Add a new student\n3. Change a restaurant\n4. Delete a Restaurant\n5. Quit the Program\n")
    try:
        choice=int(input("Enter your choice:"))
    except:
        choice=menuChoiceFail(types,restaurants)
    if not(0<choice and choice<6):
        choice=menuChoiceFail(types,restaurants)
    if choice==1:
        inputs(types,restaurants)
    elif choice==2:
        addData(types)
    elif choice==3:
        changeData(file)
    elif choice==4:
        delRes()
    elif choice==5:
        raise SystemExit
def menuChoiceFail(types,restaurants):
    choice=""
    while True:
        try:
            choice=int(input("Enter your choice:"))
            if 0<choice and choice<6:
                return choice
        except:
            pass
def inputs(types,restaurants):
    print("The types of food are",types)
    type=input("What type of food do you want?\n")
    while True:
        try:
            price=int(input("How much do you want to pay from 1-3?\n"))
            if  0<price<4 or price==-1:
                break
        except:
            print("Enter an integer from 1-3")
    while True:
        try:
            range=float(input("How many miles are you willing to travel?\n"))
            break
        except:
            print("Enter a number")
    restaurants=limit(restaurants,type,price,range)
def limit(restaurants,type,price,range):
    if type!="Any":
        restaurants=limitType(restaurants,type)
    if -1<price<4:
        restaurants=limitPrice(restaurants,price)
    if range>-1:
        restaurants=limitRange(restaurants,range)
    show(restaurants,type)
def limitType(restaurants,type):
    bad=[]
    other=['French/Carribean','Indian','Peruvian','Seafood','Spanish','Vegan','Vegetarian','Vietnamese']
    if type=="Other":
        for res in restaurants:
            if str(res.type) not in other:
                bad.append(res)
        for res in bad:
            restaurants.remove(res)
    else:
        for res in restaurants:
            if str(res.type)!=str(type):
                bad.append(res)
        for res in bad:
            restaurants.remove(res)
    return restaurants
def limitPrice(restaurants,price):
    bad=[]
    for res in restaurants:
        if int(res.price)!=int(price):
            bad.append(res)
    for res in bad:
        restaurants.remove(res)
    return restaurants
def limitRange(restaurants,range):
    bad=[]
    for res in restaurants:
        if float(res.loc)>float(range):
            bad.append(res)
    for res in bad:
        restaurants.remove(res)
    return restaurants
def show(restaurants,type):
    os.system("cls")
    if len(restaurants)==0:
        print("Please broaden your search criteria")
        init()
    restaurants.sort(key=lambda x: (float(x.rating),int(x.reviews)),reverse=True)
    if type=="Other":
        for ren in restaurants[:-1]:
            print("{}({})".format(ren.name,ren.type),end=", ")
        print("{}{}".format(restaurants[len(restaurants)-1].name,restaurants[len(restaurants)-1].type))
    else:
        for ren in restaurants[:-1]:
            print("{}({}/5)".format(ren.name,ren.rating),end=", ")
        print("{}({}/5)".format(restaurants[len(restaurants)-1].name,restaurants[len(restaurants)-1].rating))
def addData(types):
    resName=input("Enter Restaurant's Name:\n")
    resLat=input("Enter Restaurant's GPS latitude:\n")
    resLong=input("Enter Restaurant's GPS longitude:\n")
    print("Food Types: {}".format(types))
    resType=input("Enter Restaurant's food type:\n")
    resRating=input("Enter Restaurant's Rating:\n")
    resPrice=input("Enter Restaurnat's Price rating:\n")
    resReviews=input("Enter Restaurant's reviews:\n")
    fields=[resName,resLat,resLong,resType,resRating,resPrice,resReviews]
    with open(file,'a') as f:
        writer=csv.writer(f,delimiter=',')
        writer.writerow(fields)
        f.close()
    print("Added {}.".format(resName))
    init()
def changeData():
    options=["Latitude","Longitude","Type","Rating","Price","Reviews"]
    restaurants=readData(file)
    names=[]
    for res in restaurants:
        names.append(res.name)
    print(names)
    changeName=input("What restaurant would you like to change?\n")
    while changeName not in names:
        print(names)
        changeName=input("What restaurant would you like to change?\n")
    print(options)
    choice=input("What field would you like to change?\n")
    while choice not in options:
        print(options)
        choice=input("What field would you like to change?\n")
    if choice=="Latitude":
        choice=1
    elif choice=="Longitude":
        choice=2
    elif choice=="Type":
        choice=3
    elif choice=="Rating":
        choice=4
    elif choice=="Price":
        choice=5
    elif choice=="Reviews":
        choice=6
    change=input("What would you like to change it to?\n")
    with open(file,'r') as f:
        read=csv.reader(f)
        lines=[]
        for row in read:
            lines.append(row)
        count=0
        print(lines)
        for res in lines:
            try:
                if res[0]==changeName:
                    found=count
                    res[choice]=change
                    print(res[choice])
            except:
                print("error")
            count+=1
        f.close()
    writeToFile(lines)
def delRes():
    restaurants=readData()
    names=[]
    for res in restaurants:
        names.append(res.name)
    print(names)
    changeName=input("What restaurant would you like to remove?\n")
    while changeName not in names:
        print(names)
        changeName=input("What restaurant would you like to remove?\n")
    with open(file,'r') as f:
        read=csv.reader(f)
        lines=[]
        for row in read:
            lines.append(row)
        print("\nPRINTING LINES NOW\n")
        print(lines)
        count=0
        for res in lines:
            try:
                if res[0]==changeName:
                    found=count
            except:
                print("error")
            count+=1
        lines.pop(found)
        f.close()
        writeToFile(lines)
def removeBlank():
    try:
        file_object = open(file, 'r')
        lines = csv.reader(file_object, delimiter=',', quotechar='"')
        flag = 0
        data=[]
        for line in lines:
            if line == []:
                flag =1
                continue
            else:
                data.append(line)
        file_object.close()
        if flag ==1: #if blank line is present in file
            file_object = open(file, 'w')
            for line in data:
                str1 = ','.join(line)
                file_object.write(str1+"\n")
            file_object.close() 
    except Exception as e:
        print("Exception: {}".format(e))
def writeToFile(lines):
    with open(file,'w') as f:
        writer=csv.writer(f,delimiter=',')
        fields=["","","","","","",""]
        for row in lines:
            fields[0]=row[0]
            fields[1]=row[1]
            fields[2]=row[2]
            fields[3]=row[3]
            fields[4]=row[4]
            fields[5]=row[5]
            fields[6]=row[6]
            writer.writerow(fields)
        f.close()
    removeBlank()
    init()


init()