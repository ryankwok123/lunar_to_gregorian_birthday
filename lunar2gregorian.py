
import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
import pandas as pd
from pprint import pprint
from tabulate import tabulate

#this script can only handle years 1900-2100
#mom's birthday is lunar: 8th month, 7th day

birthdates = []
valid_list = []

def lunar2gregorian(year_start, year_end, month, day, name):

    for year in range(year_start, year_end+1): #can handle years 1900 to 2100 for range we do +1
        
        #check if the input date falls on a leap month (chinese lunar calendar thing)
        def is_valid_lunar_date(year, month, day):
            try:   
                lunar = Lunar(year, month, day, isleap=True)
                print(f'You will have two birthdays in the year {year}! One on the initial month (month {month}) and one on the leap month (2nd month {month})')
                return True
            except DateNotExist:
                return False

        #store output of is_valid_lunar_date
        valid = is_valid_lunar_date(year, month, day)
        #print(valid)  

        #conditional will print two birthdays if valid is true, one for initial month and one for leap month 
        if valid == True:
            #set lunar date and isleap parameter with not 'valid' for initial birthday
            lunar2 = Lunar(year, month, day, isleap=not valid)
            #print(lunar2)

            solar = str(Converter.Lunar2Solar(lunar2))
            print(f'{solar} initial birthday')
            print(lunar2.to_date(), type(lunar2.to_date())) #convert to datetime.date format
            birthdates.append(lunar2.to_date())
            valid_list.append(valid)


            #set lunar date and isleap parameter with 'valid' for leap month birthdate
            lunar = Lunar(year, month, day, isleap=valid)
            #print(lunar)

            solar = str(Converter.Lunar2Solar(lunar))
            print(f'{solar} leap month birthday')
            print(lunar.to_date(), type(lunar.to_date())) #convert to datetime.date format
            birthdates.append(lunar.to_date())
            valid_list.append(valid)
        else:
            #when the date does not land on a leap month (valid==false)
            lunar = Lunar(year, month, day, isleap=valid)
            #print(lunar)

            solar = str(Converter.Lunar2Solar(lunar))
            #print(solar)
            print(lunar.to_date(), type(lunar.to_date())) #convert to datetime.date format
            birthdates.append(lunar.to_date())
            valid_list.append(valid)


    #now we convert the solar date string to date format     
    #creating empty dataframe with headers     
    column_names = ['Subject','Start Date', 'Start Time','Description']
    df = pd.DataFrame(columns = column_names)

    #appending columns to our dataframe
    df['Subject'] = [f'{name}s birthday' for subject in range(len(birthdates))]
    df['Start Date'] = birthdates
    df['Start Time'] = ['9:00:00' for starttime in range(len(birthdates))]  

    #display different description message based on whether or not the birthday lands on a leap month
    def description():
        desc_list = []
        for index in range(len(valid_list)):
            if valid_list[index]==False:
                desc_list.append(f'Its {name}s birthday today in the chinese lunar calendar!')
            else:
                desc_list.append(f'Its {name}s birthday today in the chinese lunar calendar! This is one of two birthdays {name} will have this year since their birthday has landed on a leap month.')  
        
        return desc_list
    df['Description'] = description()  
    

    # Use pandas.to_datetime() to convert string to datetime format (only keeping date portion)
    df["Start Date"] = pd.to_datetime(df["Start Date"]).dt.date 
    

    pprint(tabulate(df, headers=column_names, tablefmt='psql'))
    print(df.dtypes)

'''


df = pd.DataFrame()
df["Start Date"] = birthdates
df.to_csv('mom_birthday_calendar.csv', index = False)
'''


lunar2gregorian(1900, 2100, 8, 7, 'Mom')
