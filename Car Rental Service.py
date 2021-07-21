import numpy as np
import pandas as pd 
import random
import string
from datetime import date

carDF=pd.read_excel('CRS_file.xlsx')
membersDF=pd.read_excel('CRS_members.xlsx')

#Function To add new member to CRS_members.csv
def add_member(new_member, new_mType, DF):
    #Generating unique ID numbers for every member
    new_ID_Gold = ("G-" + str((int(np.random.random(size=1)*1000000)))+"-"+''.join(random.choice(string.ascii_letters) for x in range(2)).upper())
    new_ID_Regular = ("N-"+ str((int(np.random.random(size=1)*100000000))))
    #Creating temporary dataframe for later appending to the main "Member" dataframe
    if new_mType.lower() == "gold":
        tempDF = pd.DataFrame([[new_member, "Gold", new_ID_Gold,0,0]], columns=list(['Name','Type','ID','Last_delays','Holds_cars']))
    elif new_mType.lower() == "regular":
        tempDF = pd.DataFrame([[new_member, "Regular", new_ID_Regular,0,0]], columns=list(['Name','Type','ID','Last_delays','Holds_cars']))   
    #Update the Memebers file
    DF=DF.append(tempDF, ignore_index=True)
    DF.to_excel('CRS_members.xlsx',index=False)

#Function To check if the member already exists in CRS_members.csv
def check_member(member_name):
    allowed_to_rent=True
    #Check if person exists to check if he already borrows a car, otherwise create a new member with clean history 
    if (member_name in set(membersDF["Name"])):
        #Check if persons alreay borrows a car
        if membersDF.loc[membersDF['Name'] == member_name,'Holds_cars'].any():
            print("Member already hold 1 car")
            allowed_to_rent=False
        else:
            print("You can get a car")
            allowed_to_rent=True
    else: #Creates new member with a provided name
        print("Member does not exist, he/she will be added to the system.")
        print()
        val_input=input("Do you want to select GOLD membership? Y/N ") #Takes extra input for assigning to correct member type 
        if val_input.lower()=="y":
            add_member(member_name,"Gold",membersDF)
        elif val_input.lower()=="n":
            add_member(member_name,"Regular",membersDF)
        else:
            print("Incorrect input. Should be either Y or N")
    return(allowed_to_rent)#returns status output to provide as input in for "if else" in main loop

#Function if desired car is available. Scans the CRS_file.csv for extract car information.
def check_car_availabilty(desired_type):#Takes desired car type + subtype as input (e.g. L2 or M1)
    status=True
    car_type = desired_type[:1]#Substrings to check car availability 
    car_subtype =str(desired_type[1:])
    df_carType=carDF[carDF["Car Type"]==car_type.upper()]#Sets all type to lower case to avoid case sensitivity
    if car_subtype in ["A","B","C","D"]:#Introduces an extra loop for car types that has letters as subtypes.
        df_carSubtype=df_carType[df_carType["Car Subtype"]==car_subtype]
    else:
        df_carSubtype=df_carType[df_carType["Car Subtype"]==int(car_subtype)]
    if len(df_carSubtype)>0:
        if np.sum(df_carSubtype["Availabilty"])==0:#Check car availability
            print("No available cars")
            status=False
        else:
            for idx, val in enumerate (df_carSubtype["Availabilty"]):
                if val!=0:
                    print("This car is available: "+ str(df_carSubtype["Car ID"].values[idx]))      
    else: print("Vehicle SubType does not exist")
    return(status)#Returns the status for the main program loop

#Correcting fees to round UP cents as its given in the assignment
def correctedFees(renting_payment):
    last_digit=int(renting_payment*100) % 10
    #Based on the last digit selects if payment should be adjusted in order to be rounded UP. 
    if(last_digit<=5 and last_digit!=0):
        correctedFees=round((renting_payment+0.05),1)
    else:
        correctedFees=round((renting_payment),1)
    print("Renting Fees: "+ str(correctedFees)+"Euro")
    return correctedFees 

#Calculating the most optimal way to divide a sum in the diffent banknots and coins. 
def cashBack(fees):
    #Assigning banknots and coins to be used    
    for i in [50,20,10,5,2,1,0.5,0.2]:#One by one trys different banknots, until there is no money left.
        num_t = fees//i
        if fees!=i:
            print(str(i)+" Euros - "+ str(int(num_t))+" times")         
        else:
            print(str(i)+"Euros - "+ str(1)+" times")
        fees = round((fees-num_t*i),2)

#Renting a car function  
def rent_car(car_ID_rent, renter_name, renting_time):
    carDF=pd.read_excel('CRS_file.xlsx')
    membersDF=pd.read_excel('CRS_members.xlsx')  
    #Assigning correct pledge
    pledge=300#by default the maximum pledge is set. If it is "gold" member ->pledge removed. If "regular" member -> pledge can change.
    if membersDF.loc[membersDF['Name'] == renter_name,'Type'].values.tolist()[0]=="Gold":
        pledge=0
    else:
        car_class=carDF.loc[carDF['Car ID'] == car_ID_rent,'Car Type'].values[0] #Check class of car to assign correct pledge
        if car_class=="L" or car_class=="M" or car_class=="N":
            #Changing pledge based on car class
            pledge=100

    #Change values in Car and Members Dataframes
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Date of Rent']=date.today()
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Rented for']=renting_time
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Availabilty']=0
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Current Holder']=renter_name
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Pledge paid']=pledge
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Returned after']='0:0'
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Final Renting Fees']=0.0
    membersDF.loc[membersDF['Name'] == renter_name,'Holds_cars']=1
    
    print("This pledge is assigned: "+str(pledge)+"Euro")
    
    #Calculates what would person need to pay if car is returned in time!
    time_separator=renting_time.find(":")
    hours_requested=int(renting_time[:time_separator])
    minutes_requested=int(renting_time[time_separator+1:])
    total_min_requested=hours_requested*60+minutes_requested
    #Select a correct hour rate for an individual member
    if membersDF.loc[membersDF['Name'] == renter_name,'Type'].all()=="Gold":
        rate='Hour_rate_G'
    else:
        rate='Hour_rate_R'  
    #Calculates rate without knowing if person will be late or not. 
    if total_min_requested <=240:
        to_pay=240 * (carDF.loc[carDF['Car ID'] == car_ID_rent, rate]/60.0)
    else: 
        to_pay=total_min_requested * (carDF.loc[carDF['Car ID'] == car_ID_rent, rate]/60.0)
    
    corrected_Fee=correctedFees(round(to_pay.values[0],2))
    carDF.loc[carDF['Car ID'] == car_ID_rent, 'Estimated Renting Fees']=corrected_Fee
        
    print("Car Successfully rented!")
    print("Parking spot: "+ str(carDF.loc[carDF['Car ID'] == car_ID_rent,'Parking Spot'].values[0]))
    print("Unlock pass: " + str(int(np.random.random(size=1)*100000)))#Random generating unlock pass
    carDF.loc[carDF['Car ID'] == car_ID_rent,'Unlock Pass']=int(np.random.random(size=1)*100000)
    #Update Files
    carDF.to_excel('CRS_file.xlsx',index=False)
    membersDF.to_excel('CRS_members.xlsx',index=False)

#Returning the rented car function 
def return_car(rented_car_ID):
    carDF=pd.read_excel('CRS_file.xlsx')
    membersDF=pd.read_excel('CRS_members.xlsx') 
    #Confirming if the correct user returning a car
    name=str(carDF.loc[carDF['Car ID'] == rented_car_ID,'Current Holder'].values[0])
    if name!="Null":
        confirmation=input("Are you "+ str(carDF.loc[carDF['Car ID'] == rented_car_ID,'Current Holder'].values[0])+"? Y/N ")
    else:
        confirmation="N"
    if confirmation.lower()=="y":#If person is not confirmed, the function is skipped
        if membersDF.loc[membersDF['Name'] == name,'Type'].all()=="Gold":
            rate='Hour_rate_G'
        else:
            rate='Hour_rate_R'
        print()
        print("Car holder verified")
        returned_after=input("How long did you have a car? Format HH:MM ") #Collects input about renting period
        carDF.loc[carDF['Car ID'] == rented_car_ID,'Returned after']=returned_after
        
        #Calculating the difference between Requested time and Rented time. If rented time bigger assigns fine. 
        time_separator=returned_after.find(":")
        hours_returned=int(returned_after[:time_separator])
        minutes_returned=int(returned_after[time_separator+1:])
        total_min_returned=hours_returned*60+minutes_returned
        
        renting_time=carDF.loc[carDF['Car ID'] == rented_car_ID,'Rented for'].values[0]
        time_separator=renting_time.find(":")
        hours_requested=int(renting_time[:time_separator])
        minutes_requested=int(renting_time[time_separator+1:])
        total_min_requested=hours_requested*60+minutes_requested

        time_dif=total_min_returned-total_min_requested
        to_pay=fine=0
        #Calculating Renting Fees
        if time_dif>0:
            to_pay=total_min_requested * (carDF.loc[carDF['Car ID'] == rented_car_ID, rate]/60.0)
            #Fine is forgiven with certain conditions
            if membersDF.loc[membersDF['Name'] == name, 'Last_delays'].values[0]>=4 or membersDF.loc[membersDF['Name'] == name, 'Type'].values[0]!="Gold":
                fine=(time_dif * carDF.loc[carDF['Car ID'] == rented_car_ID, rate])
            to_pay=to_pay+ fine
            to_pay=correctedFees(round(to_pay.values[0],2))
            carDF.loc[carDF['Car ID'] == rented_car_ID, 'Final Renting Fees']=to_pay
            membersDF.loc[membersDF['Name'] == name, 'Last_delays']=membersDF.loc[membersDF['Name'] == name, 'Last_delays']+1 #Adds a delay day to the CRS_members.csv
            
        else:
            if total_min_returned <=240:
                to_pay=240 * (carDF.loc[carDF['Car ID'] == rented_car_ID, rate]/60.0)
                to_pay=correctedFees(round(to_pay.values[0],2))
                carDF.loc[carDF['Car ID'] == rented_car_ID, 'Final Renting Fees']=to_pay
                
            else:
                
                to_pay=carDF.loc[carDF['Car ID'] == rented_car_ID, 'Estimated Renting Fees'].values[0]
                carDF.loc[carDF['Car ID'] == rented_car_ID, 'Final Renting Fees']=to_pay
                
        #change + pledge which has to be returned back to the renter
        print("Final Renting Fees: "+str(to_pay)+"Euro")
        pledge=int(carDF.loc[carDF['Car ID'] == rented_car_ID, 'Pledge paid'].values.tolist()[0])     
        change=input("Enter your sum to be paid: ")
        change=round(float(change)-to_pay+pledge,2)
        print("Change to be returned + pledge: " + str(change)+"Euro")
        cashBack(change)
        #Car is released from the member and availabilty status changed
        membersDF.loc[membersDF['Name'] == name, 'Holds_cars']=0 
        carDF.loc[carDF['Car ID'] == rented_car_ID, 'Previous Holder']=carDF.loc[carDF['Car ID'] == rented_car_ID, 'Current Holder']
        carDF.loc[carDF['Car ID'] == rented_car_ID, 'Current Holder']="Null"
        carDF.loc[carDF['Car ID'] == rented_car_ID, 'Availabilty']=1
        carDF.to_excel('CRS_file.xlsx',index=False)
        membersDF.to_excel('CRS_members.xlsx',index=False)
        print("Car is returned!")
    else:
        print("Car holder is not verified")

#___________________________________START___________________________________________________ 
print("Welcome at SlimmerAI Car Rental Service!")
answer="y"
while(answer.lower()=="y"):
    action = input("What do you want to do? Rent or Return?  ")
    if action.lower()=="rent":
        name_input=input("Please enter your name to see if you exist in the system: ")
        print()
        if check_member(name_input):
            car_type_input=input("What type of car you are looking for? ")
            print()

            if(check_car_availabilty(car_type_input)):
                car_ID=input("Please enter the ID of a car ? ")
                requested_Time=input("For how long you are planning to rent? Minimum renting time 4:00 (Format HH:MM)  ")
                timeSeparator=requested_Time.find(":")
                hours=int(requested_Time[:timeSeparator])
                if (hours<=4):
                    rent_car(car_ID,name_input,"4:00")
                else:
                    rent_car(car_ID,name_input,requested_Time)
            else:
                break
        else:
            print("Return car before taking a new one")
    elif action.lower()=="return":
        car_ID=input("Please enter the ID of a car ? (e.g C_ID_126) ")
        return_car(car_ID)
    else:
        print("Incorrect input. Try again")
    
    answer=input("Do you want to perform another operations? Y/N ")
