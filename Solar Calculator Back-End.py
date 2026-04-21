#User Log In (Replace with front-end input)
loggedIn = "False"
while(loggedIn == "False"):
    userName = str(input("What is your username? "))
    passWord = str(input("What is your password? "))
    if(userName == "Test" and passWord == "Test"):
        print("Welcome Back!")
        loggedIn = "True"
    else:
        print("Incorrect Username or Password")


#User Provided Information
previousBill = float(input("What was your previous bill? $"))
billingPeriod = str(input("What is the billing period? Quaterly/Monthly "))
solarsystemSize = float(input("What is the size of the solar system? kW "))

#Calculate Average Daily Usage
if(billingPeriod == "Quaterly"):
    actualUsage = previousBill - (1.25 * 90)
    averageDailyUsage = round((actualUsage/0.28)/90, 2)
elif(billingPeriod == "Monthly"):
    actualUsage = previousBill - (1.25 * 30)
    averageDailyUsage = round((actualUsage/0.28)/30, 2)

#Replace with Map Intergration (Use average daily when testing)
dailysolarGeneration = float(input("How much solar power could your area generate? kWh "))

#Calculate Savings Impact
averageDailyGeneration = solarsystemSize * dailysolarGeneration #Calculate the average power generated per day
if(averageDailyGeneration > averageDailyUsage): #If Daily Generation is GREATER than Daily Usage
    averageDifference = round(averageDailyGeneration - averageDailyUsage, 2) #Calculate the excess of power generated
    averageDailySavings = round(averageDifference * 0.08, 2) #Calculate the average daily profit based on excess power generated
    if(billingPeriod == "Quaterly"):
        averageBillingPeriodProfit = averageDailySavings * 90 #Calcualte average profit based on excess power
    elif(billingPeriod == "Monthly"):
        averageBillingPeriodProfit = averageDailySavings * 30 #Calcualte average profit based on excess power
    totalSavings = averageBillingPeriodProfit + previousBill #Calculate total savings
    print("You could be making up to $", totalSavings)
elif(averageDailyGeneration < averageDailyUsage): #If Daily Genertaion is LESS than Daily Usage
    percentagePowerCover = (averageDailyGeneration/averageDailyUsage) * 100 #Calculate perctange of bill solar power covers
    percentageBillDifference = (percentagePowerCover / 100) * previousBill #Calculate value based on provided bill amount
    print("You Could be Saving $", round(percentageBillDifference, 2), "on your bill!")

#Calculate Yearly Values if Daily Generation exceeds Daily Usage
if(averageDailyGeneration > averageDailyUsage):
    averageYearlyGeneration = round(averageDifference * 365, 2) #Calculate Yearly Excess Solar Power Generation
    averageyearlyEarning = averageYearlyGeneration * 0.08 #Calculate Yearly profit based on excess power
    print("You will generate", averageYearlyGeneration, "per year in excess")
    print("You could be earning an extra", round(averageyearlyEarning, 2), "per year")
