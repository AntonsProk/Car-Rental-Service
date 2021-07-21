# Car Rental Service
Task was to write a Car Rental Service with basic functionalities.

What can it do? 
* Accept 2 types of customers: "gold" members(pledge is not required) and regular members(pledge required). Both get CRS ID cards that vary in the ID number pattern.
* To have many different types of vehicles with a unique ID number for each vehicle.
* Money is paid in cash only. Cash back is be returned in the most optimal way.
* Check car availabilty and member possibility to rent a new car. (Only one vehicle per person could be given)
* Has multiple vehicles of each (sub) type in the park. So, it's: 2 x M1, 2 x M2, 2 x T, 2 x G and so on.
* Provide customers with information on vehicle location in the park (for instance, A-19 or Z-2) and the secret pin which shall be used to unlock the vehicle.

# Getting Started 
Install following packages(if they are missing) before running the code...

## Installation 
```bash
pip install pandas
pip install numpy
pip install random
pip install string
pip install datetime

```
Download the Project zip file, extract and use Command prompt to navigate to project directory.

## Assignment Results

To start the program type following command in the Command prompt

```python
python Car Rental Service.py
```
Follow the instruction in the console.

```What do you want to do? Rent or Return?```
Only 2 options are accepted, else the exception is triggered.

#### Rent Path
1. Asks a name of member to check if he exists in the system
- If person does not exist add him to the system and assign the desired Membership type 
- If person is already in the system -> check if he already rents a car.
2. Asks user the desired car type. (e.g. L2, M1, SA etc.)
3. Checks if any car of this type is available (each type has at least 2 unique cars with different carID)
4. Gives member an option to choose one the available cars by typing the exact car ID (e.g. C_ID_126)
5. Asks for how long the car is going to be rented. 
6. Estimates the price and assigns the pledge(in case "regular" membership) 
7. Provides information about car parking spot and randomly generated unlocking pass

#### Return Path
1. Asks the car ID that is wished to be returned (important to remember what was the car ID )
2. Asks to confirm the name of the renter
3. Asks to enter the exact time car was held by the member (Format HH:MM. e.g. 05:21)
4. Calculates the final renting fees based on the "delay" history and membership type. Additionally, cents in final renting fees always round UP.
5. Asks to enter the amount to be paid 
6. Calculates the cash back, taking into account that all banknotes and coins are accepted. 
7. When money is paid and cash back is returend the car releases and becomes available for next user.
Request Example:


# Future Improvements

1. Create a function to visually display available cars
2. Introduce different authentication based on membership type
3. Introduce "Deley" reset function with new month
4. Add a function to add new cars to garage

