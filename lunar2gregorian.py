
import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
import pandas as pd
from pprint import pprint

#mom's birthday is lunar: 8th month, 7th day

birthdates = []

def lunar2gregorian(year_start, year_end, month, day):

    for year in range(year_start, year_end+1): #can handle years 1900 to 2100 for range we do +1
        
        #check if the input date falls on a leap month (chinese lunar calendar thing)
        def is_valid_lunar_date(year, month, day):
            try:   
                lunar = Lunar(year, month, day, isleap=True)
                print(f'You will have two birthdays in the year {year}! One in the initial month (month {month}) and one in the leap month (2nd month {month})')
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
            print(lunar2)

            solar = str(Converter.Lunar2Solar(lunar2))
            print(f'{solar} initial birthday')

            #set lunar date and isleap parameter with 'valid' for leap month birthdate
            lunar = Lunar(year, month, day, isleap=valid)
            print(lunar)

            solar = str(Converter.Lunar2Solar(lunar))
            print(f'{solar} leap month birthday')
        else:
            #when the date does not land on a leap month (valid==false)
            lunar = Lunar(year, month, day, isleap=valid)
            print(lunar)

            solar = str(Converter.Lunar2Solar(lunar))
            print(solar)
            

        #now need to find a way to convert the solar date string to date format (probably use pandas)
        #method below works but is pretty damn ugly
'''
        #extract year, month, day from converted date
            #solar[11:15] #year
            #solar[23:24] #month
            #solar[-3:-1] #day

        #converting into proper date format
        newStr = solar[23:24]+"/"+solar[-3:-1]+"/"+solar[11:15]
        newStr = newStr.replace("=", "") 
        #print(newStr)

        birthdates.append(newStr)
        
    pprint(birthdates)
'''
'''
df = pd.DataFrame()
df["Start Date"] = birthdates
df.to_csv('mom_birthday_calendar.csv', index = False)
'''


lunar2gregorian(1900, 2100, 8, 7)
