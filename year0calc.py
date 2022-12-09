'''
Created on Dec 9, 2022

A smelly method used for finding the phase of the moon at its zenith on a given day.

From this method, we are able to identify the following candidates for a potential
starting date of the Coligny Calendar:

1) October 21, 1019 BCE
2) November 20, 1019 BCE
3) October 17, 1019 BCE

#1 and #2 are identified using pyephem's next_new_moon function throughout the
month of October. These are dates in which the moon reaches an angle of 0
relative to the sun.

#3 is a contender because it has the lowest possible angle at its peak,
with 7.7 degrees at 19:19:14

Option #2 has been discounted, as it is too far away from our proposed
starting point of early November/Samhain relative to the other options.

Ultimately, the decision between #1 and #3 was made by comparing the relative
illuminations of the moon. Under option #1, only 1.9% of the moon was illuminated.
Under option #3, 28% of the moon was illuminated.

It stands to reason that an ancient druid standing in the center of Stonehenge
would observe the night as having a full moon for the entirety of the night of October 21st.

In such a situation, the ancient celts might mark that night as the first of Samonios.
So, calculations done to convert to the Coligny calendar will assume that
October 21st, 1019 BCE is when the Coligny calendar begins.

@author: Fred
'''
import ephem, math

#Day one of the first recorded lunar cycle of our calendar, to be imported elsewhere
year_0 = "-1019/10/21"
    #establishing our observer for all calculations, the coordinates provided are for Stonehenge
druid = ephem.Observer()
druid.lat = 51.1789
druid.long = 1.8262
druid.elevation = 100
#establishing celestial bodies for all calculations
moon = ephem.Moon()
sun = ephem.FixedBody()
sun._ra = ephem.hours("12:00")
sun._dec = ephem.degrees("0:0")

def find_phase(date):
    druid.date = date
   
    #identifying when the moon will reach its peak for the given date
    moon.compute(druid)
    peak_time = druid.next_rising(moon, start=date)
    date = peak_time
    
    #recalculating moon and sun with the new date and time
    moon.compute(druid)
    sun.compute(druid)
    
    #This isn't used for anything but we'll hold onto it
    illum = moon.moon_phase * 100
    
    #We identify the moon's angle relative to the sun
    lunar_angle = (math.acos(math.sin(moon.alt) * math.sin(sun.alt) + math.cos(moon.alt) * math.cos(sun.alt) * math.cos(moon.az - sun.az)))*100
        
    if lunar_angle <= 45:
        result = "Moon is New (" + str(lunar_angle) + "): " + str(date)
    elif lunar_angle > 45 and lunar_angle <= 135:
        result = "Moon is in First Quarter (" + str(lunar_angle) + "): " + str(date)
    elif lunar_angle > 135 and lunar_angle <= 225:
        result = "Moon is Full (" + str(lunar_angle) + "): " + str(date)
    elif lunar_angle > 225 and lunar_angle < 360:
        result = "Moon is in Third Quarter (" + str(lunar_angle) + "): " + str(date)
    else:
        result = "Fenrir has eaten the sun. Consult your grimoires on how to survive Ragnarok. Angle: " + str(lunar_angle)
        
    next_new = ephem.next_new_moon(date)
    
    result = str(date) + "\n" + result + "\n Next new moon projected: " + str(next_new) + "\n" + "Illumination: " + str(illum) + "\n"
        
    return result
    
if __name__ == "__main__":
    year = input("Year: ")
    month = input("Month: ")
    checkdate = ephem.date(year + '/' + month + '/1')

    for _ in range(32):
        check = find_phase(checkdate)
        if check:
            print(check)
        else:
            None
        checkdate = ephem.date(checkdate + (24 * ephem.hour))