'''
Created on Dec 9, 2022

@author: Fred
'''
import year0calc
from months import months, y1, y3
from datetime import datetime, date

class ColignyCal():
    '''
    Taking a datetime object containing a given date as the input, this class
    converts the data to the Coligny calendar. In the future, will be able to
    do some other stuff with that.
    '''

    def __init__(self, date):
        '''
        Inputs
        ------
        date : datetime
            A datetime object contianing the year, month and day that we are
            converting
            
        Attributes
        ----------
        druid : ephem.Object
            The observer used for any astronomical calculations. This is a copy
            of the imported druid var from year0calc
        moon : ephem.Moon
            The moon, same as above
        sun : ephem.FixedBody
            As above, for the sun
        days_gone : int
            The number of days that have passed since the beginning of the
            Coligny calendar, October 21 1019 BCE
        cycle : int
            The current cycle of the Coligny calendar
        curr_days : int
            Initially, the number of days that have passed in the current 5 year cycle.
            Later, this number will reduce gradually as we split it off into
            years, months and weeks.
        year : int
            The current year of the cycle, an integer 1-5
        month : int
            The current month of the calendar year, represented as an integer
            from 1-12 or, in years 1 and 3, 1-13
        month_name : str
            The name of the current month. Defined in the same breath as month so
            should always be accurate
        lucky : bool
            Is it a lucky month?
        week : int
            each month of the coligny calendar is composed of 6 weeks. This identifies
            which week it is. Math is likely to be a bit off as some months are 29 days
            so
            TODO: Come up with a better algorithm for this
        day : int
            The current day of the week
            
        Methods
        -------
        get_days
            Quickly finds the number of days that have passed since the beginning
            of the Coligny calendar
        get_cycle
            Identifies the current cycle of the coligny calendar by doing math
            to the days stored in days_gone 
        get_year
            Identifies the current year of the current cycle, as well as its
            name
        get_month
            Compares current year to a list, checking for leap months.
            Then, computes the current month and divines any leftover days which,
            as usual, are sent to curr_days
        get_week
            Some very simple division on our remaining days to identify the current
            week.
        '''
        
        #I'm too lazy so we're figuring out how many days in a 5 year cycle now
        self.days_in_cycle = 60 #start with 60, because 2 leap months of 30 days
        for y in range(1,13):
            if months[y][0]:
                self.days_in_cycle += 30*5 #each month happens 5 times sooo
            else:
                self.days_in_cycle += 29*5
        
        self.gregdate = date
        self.druid = year0calc.druid.copy() #just cloning some druids nothing to see here
        self.moon = year0calc.moon.copy()
        self.sun = year0calc.sun.copy()
        self.days_gone = self.get_days(date)
        self.cycle, self.curr_days = self.get_cycle()
        self.year = self.get_year()
        self.month, self.month_name, self.lucky = self.get_month()
        self.week = self.get_week()
        
    def __len__(self):
        return self.days_gone
    
    def __repr__(self):
        if self.renewal_check():
            m_string = "Cycle {}, Year {}, {}'s Renewal, Week {}, Day {}".format(self.cycle,
                                                                             self.year,
                                                                             self.month_name,
                                                                             self.week,
                                                                             self.day)
        else:
            m_string = "Cycle {}, Year {}, {}, Week {}, Day {}".format(self.cycle,
                                                                   self.year,
                                                                   self.month_name,
                                                                   self.week,
                                                                   self.day)
            
        if self.lucky:
            m_string += "\nThis is a lucky month!"
            
        return m_string
        
    def get_days(self, date):
        '''
        Identifies the number of days that have passed since the beginning of
        CE until our target time.
        Then applies the number of days that have passed since the start of the
        Coligny calendar (identified by taking the Julian Date of the Coligny's
        start and subtracting the Julian Date's offset)
        '''
        julian_offset = 1721424
        day_zero_julian = 1349527
        
        date = date.toordinal()
        date = date + (day_zero_julian - julian_offset)
        return date
    
    def get_cycle(self):
        '''
        '''                
        #now we identify how many cycles have passed
        #and how many days of the current cycle remain
        days_curr_cycle = self.days_gone % self.days_in_cycle
        cycles = int(self.days_gone / self.days_in_cycle)
        
        return cycles, days_curr_cycle
        
    def get_year(self):
        '''
        '''
        year = 1
        days_left = self.curr_days
        for c in range(1,6):
            days = 0
            #years 1 and 3 have 30 more days
            if c == 1 or c == 3:
                days += 30
            #first, we need to figure out how many days in the year we're checking...
            for y in range(1,13):
                if months[y][0]:
                    days += 30
                else:
                    days += 29
            #now, let's check if the current days are more than this year
            if days_left >= days:
                year += 1
                days_left -= days
        
        self.curr_days = days_left
        return year
        
    def get_month(self):
        '''
        '''
        days_left = self.curr_days
        month = 0
        if self.year != 1 and self.year != 3: #if the year is standard
            for m in range(1,13):
                days_in_month = 0
                if months[m][0]:
                    days_in_month = 30
                else:
                    days_in_month = 29
                if days_left >= days_in_month:
                    month = m
                    name = months[m][1]
                    luck = bool(months[m][0])
                    days_left -= days_in_month
        elif self.year == 1:
            for m in range(1,14):
                days_in_month = 0
                if y1[m][0]:
                    days_in_month = 30
                else:
                    days_in_month = 29
                if days_left >= days_in_month:
                    month = m
                    name = y1[m][1]
                    luck = bool(y1[m][0])
                    days_left -= days_in_month
        elif self.year == 3:
            for m in range(1,14):
                days_in_month = 0
                if y3[m][0]:
                    days_in_month = 30
                else:
                    days_in_month = 29
                if days_left >= days_in_month:
                    month = m
                    name = y3[m][1]
                    luck = bool(y3[m][0])
                    days_left -= days_in_month
        else: #error message, we can just use print because why not
            print("The time eater has consumed all. Better luck next epoch. (Impossible year passed to get_month")
            
        self.curr_days = days_left
        return month, name, luck

    def get_week(self):
        week = int(self.curr_days / 5)
        if week > 1:
            self.curr_days -= 5 * week
            if self.curr_days == 0:
                self.day = 1
            else:
                self.day = self.curr_days
        
        return week
        
    def renewal_check(self):
        if self.week > 3:
            return True
        else:
            return False
    
if __name__ == '__main__':
    test = date.today() #today is good enough for testing lol
    test = ColignyCal(test)
    print("Today is " + str(test))
    year = int(input("Pick a year: "))
    month = int(input("Pick a month: "))
    day = int(input("Pick a day: "))
    test = datetime(year, month, day)
    print("Your chosen date has been converted:")
    print(ColignyCal(test))