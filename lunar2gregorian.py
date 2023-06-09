
from datetime import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
import pandas as pd
from pprint import pprint
from tabulate import tabulate

#Rewriting using object oriented programming approach 
#class 1: convert_date
class convert_date:
    def __init__(self, year_start, year_end, month, day, name):
        self.year_start = year_start
        self.year_end = year_end
        self.month = month
        self.day = day
        self.name = name
        self.birthdates = []
        self.valid_list = []
        self.valid_list_with_repeats = []

    
    #check if the input date falls on a leap month (chinese lunar calendar thing), returns list of True/False
    def is_valid_lunar_date(self):
        for year in range(self.year_start, self.year_end+1): #can handle years 1900 to 2100 for range we do +1
            try:   
                lunar = Lunar(year, self.month, self.day, isleap=True)
                #print(f'You will have two birthdays in the year {year}! One on the initial month (month {self.month}) and one on the leap month (2nd month {self.month})')
                self.valid_list.append((year, True))
            except DateNotExist:
                self.valid_list.append((year, False))

        #pprint(self.valid_list)
        return self.valid_list
    

    #create a list for each year, one birthday for nonleap months and two for leap months
    def create_birthday_list(self):
        for index in convert_date.is_valid_lunar_date(self):
            #conditional will print two birthdays if valid is true, one for initial month and one for leap month 
            if index[1] == True:
                #set lunar date and isleap parameter with opposite boolean (True->False) for initial birthday
                lunar2 = Lunar(index[0], self.month, self.day, isleap=not index[1])
                #print(lunar2)

                solar = str(Converter.Lunar2Solar(lunar2))
                #print(f'{solar} initial birthday')
                #print(lunar2.to_date(), type(lunar2.to_date())) #convert to datetime.date format
                self.birthdates.append(str(lunar2.to_date()))
                self.valid_list_with_repeats.append(True)
                

                #set lunar date and isleap parameter with original boolean (True) for leap month birthdate
                lunar = Lunar(index[0], self.month, self.day, isleap=index[1])
                #print(lunar)

                solar = str(Converter.Lunar2Solar(lunar))
                #print(f'{solar} leap month birthday')
                #print(lunar.to_date(), type(lunar.to_date())) #convert to datetime.date format
                self.birthdates.append(str(lunar.to_date()))
                self.valid_list_with_repeats.append(True)
            else:
                #when the date does not land on a leap month (valid==false)
                lunar = Lunar(index[0], self.month, self.day, isleap=index[1])
                #print(lunar)

                solar = str(Converter.Lunar2Solar(lunar))
                #print(solar)
                #print(lunar.to_date()) #convert to datetime.date format
                self.birthdates.append(str(lunar.to_date()))
                self.valid_list_with_repeats.append(False)
        
        #pprint(self.birthdates)
        birthdate_len = len(self.birthdates)
        return self.birthdates, birthdate_len


#class 2: to_dataframe
class to_dataframe(convert_date):

    #creating empty dataframe with headers   
    def empty_dataframe(self): 
        column_names = ['Subject','Start Date', 'Start Time','Description']
        df = pd.DataFrame(columns = column_names)
        return df
    
    #appending all columns to our dataframe (except description)
    def append_subject_startdate_starttime(self):
        df = to_dataframe.empty_dataframe(self)
        birthdate_list, birthdate_list_len = self.create_birthday_list()

        df['Subject'] = [f'{self.name}s birthday' for subject in range(birthdate_list_len)]

        # Use pandas.to_datetime() to convert string to datetime format (only keeping date portion)
        df["Start Date"] = birthdate_list
        df["Start Date"] = pd.to_datetime(df["Start Date"]).dt.date 

        df['Start Time'] = ['9:00:00' for starttime in range(birthdate_list_len)]
        return df
        
    #short function that attaches the appropriate suffix based on the number   
    def suffix(self, d): 
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
        

    #display different description message based on whether or not the birthday lands on a leap month    
    def append_description(self):
        df = to_dataframe.append_subject_startdate_starttime(self)

        #messages for regular birthdays and leap month birthdays
        birthdate_year = pd.to_datetime(df["Start Date"]).dt.year #df[Start Date] that only contains the year portion

        desc_list = []
        for index in range(len(self.valid_list_with_repeats)):
            if self.valid_list_with_repeats[index]==False:
                desc_list.append(f'Its {self.name}s birthday today in the chinese lunar calendar ({birthdate_year.iloc[index]}, {self.month}{self.suffix(self.month)} month, {self.day}{self.suffix(self.day)} day)!')
            else:
                desc_list.append(f'Its {self.name}s birthday today in the chinese lunar calendar ({birthdate_year.iloc[index]}, {self.month}{self.suffix(self.month)} month, {self.day}{self.suffix(self.day)} day)! This is one of two birthdays {self.name} will have this year since their birthday lands on a leap month.')  
        
        df['Description'] = desc_list
        return df
        
    
    def display_and_save_to_csv(self):
        df = to_dataframe.append_description(self)
        column_names = ['Subject','Start Date', 'Start Time','Description']

        #sample table
        print(tabulate(df, headers=column_names, tablefmt='psql'))

        #save as csv
        df.to_csv('lunar_to_gregorian_birthdays.csv', index = False)

        return tabulate(df)


jason_bday = to_dataframe(1900, 2100, 8, 3, 'Jason')
#jason_bday.empty_dataframe()
#print(jason_bday.is_valid_lunar_date())
print(jason_bday.display_and_save_to_csv())

