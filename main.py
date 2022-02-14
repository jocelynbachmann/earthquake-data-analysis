#!/usr/bin/env python
# coding: utf-8

# In[1]:


from cs103 import *
from typing import NamedTuple, List, Optional
import csv
import matplotlib.pyplot as plt

##################
# Data Definitions
   
Earthquake = NamedTuple('Earthquake', [('year', int), # in range [1960, 2021]
                                       ('magnitude', float), # in range [2.5, 9.9]
                                       ('deaths', int)]) # in range [0, ...)
# interp. an earthquake with a year of occurence ('year'), magnitude ('magnitude') and the
# number of deaths that were caused ('deaths'). 

E1 = Earthquake(1960, 7.8, 63)
E2 = Earthquake(1987, 6.2, 2)
E3 = Earthquake(2010, 7, 316000)
E4 = Earthquake(2016, 4.9, 0)
E5 = Earthquake(2017, 8.2, 98)

@typecheck
def fn_for_earthquake(e: Earthquake) -> ...:
    return ...(e.year,
               e.magnitude,
               e.deaths)


# List[Earthquake]
# interp. a list of Earthquakes

LOE0 = []
LOE1 = [E1, E2, E3, E4, E5]
LOE2 = [E2, E4]
LOE3 = [E1, E3, E5]
LOE4 = [E4]

@typecheck
def fn_for_loe(loe: List[Earthquake]) -> ...:
    # description of the acc
    acc = ... # type: ...
    for e in loe:
        ...(fn_for_earthquake(e), acc)
        
    return acc


# In[2]:


###########
# Functions

###############
## Main Function
##############
@typecheck
def magnitudes_and_deaths(fn: str) -> None:
    """
    reads the earthquake data from the given filename (fn), and plots (on a bar chart) 
    the average magnitudes of earthquakes for each of the following time periods:
    1961-1970, 1971-1980, 1981-1990, 1991-2000, 2001-2010, 2011-2020
    """
    return plot_magnitude_and_deaths(read(fn))  


###############
## Read Function
##############
@typecheck
def read(fn: str) -> List[Earthquake]:
    """    
    reads information from file name fn and returns a list of Earthquake data
    """
    loe = [] # type: List[Earthquake]

    with open(fn) as csvfile:
        
        reader = csv.reader(csvfile)
        for skip in range(0, 2):
            next(reader) # skip 2 header lines

        for row in reader:
            e = Earthquake(parse_int(row[1]), # represents an int[1960, 2021]
                           parse_float(row[13]), # represents a float[2.5, 9.9]
                           check_for_none(parse_int(row[15]))) # represents an int[0, ...)
            loe.append(e)
    
    return loe


## Helper for Read Function
@typecheck
def check_for_none(d: Optional[int]) -> int:
    """
    returns 0 if d is None, and returns d otherwise
    """
    if d is None:
        return 0
    else:
        return d

###############
## Analyze Function
##############
@typecheck
def plot_magnitude_and_deaths(loe: List[Earthquake]) -> None:
    """
    displays a bar chart with average magnitude and average deaths for the time periods:
    1961-1970, 1971-1980, 1981-1990, 1991-2000, 2001-2010, 2011-2020 shown side by side
    """
    
    # width of each bar
    bar_width = 4
    
    # middle coordinates for magnitude bars 
    middle_of_bars_magnitude = num_sequence(final_average_magnitudes(loe), 4, bar_width + 6)
    
    # middle coordinate for deaths bars
    middle_of_bars_deaths = num_sequence(final_average_magnitudes(loe), bar_width - 4, bar_width + 6)
    
    # bar opacity
    opacity = 0.5
    
    # create bar chart
    rects1 = plt.bar(middle_of_bars_magnitude, 
                     final_average_magnitudes(loe),  
                     bar_width,
                     alpha=opacity,                  
                     align='edge',
                     color='b',                      
                     label='Average Magnitude')

    rects2 = plt.bar(middle_of_bars_deaths, 
                     final_average_deaths(loe), 
                     bar_width,
                     alpha=opacity,
                     align='edge',
                     color='r',                       
                     label='Average Deaths')
    
    # axes labels and chart title 
    plt.xlabel('Time Frame (range of years)')
    plt.ylabel('Avg. Magnitude (x10) and Avg. Deaths (in 10s)')
    plt.title('Average Magnitude and Average Deaths of Earthquakes')

    # axes ranges
    plt.axis([0, 65, 0, 135])

    # x axis tick labels
    tick_labels = ['1961-1970', '1971-1980', '1981-1990', '1991-2000', '2001-2010', '2011-2020']
    plt.xticks(middle_of_bars_magnitude, tick_labels, rotation=45)
    
    # legend
    plt.legend(loc='upper right')
    
    # show the plot
    plt.show()
    
    return None
    
###############
## Helper Functions
##############
@typecheck
def num_sequence(values: List[float], initial: float, gap: float) -> List[float]:
    """
    returns a list of numbers in the form [initial, initial + gap, initial + 2*gap, ...] 
    of the same length as values (e.g. the number of items in the list returned is equal
    to the number of items in values, with the first value being initial, the gap being 
    the gap between values). For example, [4, 6, 8, 10] for 4 values, initial == 4 and
    gap == 2
    """
    nums = []  # type: List[float]
    
    next_num = initial
    
    for val in values:
        nums.append(next_num)
        next_num = next_num + gap
    
    return nums


###############
## Magnitude Helper Section
##############

@typecheck
def final_average_magnitudes(loe: List[Earthquake]) -> List[float]:
    """
    returns a list of the average magnitudes corresponding to the periods: 1961-1970,
    1971-1980, 1981-1990, 1991-2000, 2001-2010, 2011-2020 (in that order)
    """
    magnitude_1970 = magnitude_for_years(loe, 1961, 1970)
    magnitude_1980 = magnitude_for_years(loe, 1971, 1980)
    magnitude_1990 = magnitude_for_years(loe, 1981, 1990)
    magnitude_2000 = magnitude_for_years(loe, 1991, 2000)
    magnitude_2010 = magnitude_for_years(loe, 2001, 2010)
    magnitude_2020 = magnitude_for_years(loe, 2011, 2020)
    
    return [magnitude_1970, 
            magnitude_1980, 
            magnitude_1990,
            magnitude_2000,
            magnitude_2010,
            magnitude_2020]

@typecheck
def magnitude_for_years(loe: List[Earthquake], min_year: int, max_year: int) -> float:
    """
    returns the average magnitude of all earthquakes that occured between min_year and
    max_year
    """
    correct_years = filter_for_years(loe, min_year, max_year)
    magnitudes = filter_for_magnitude(correct_years)
    average_magnitude = average(magnitudes)
    
    return average_magnitude

@typecheck
def filter_for_magnitude(loe: List[Earthquake]) -> List[float]:
    """
    return a list of the magnitudes of the earthquakes in loe
    """
    magnitudes = [] # type: List[float]
    for e in loe:
        magnitudes.append(get_modified_magnitude(e))
        
    return magnitudes

@typecheck
def get_modified_magnitude(e: Earthquake) -> float:
    """
    returns the magnitude of e mutiplied by 100 
    """
    return round((e.magnitude * 10), 1)

###############
## Deaths Helper Section
##############

@typecheck
def final_average_deaths(loe: List[Earthquake]) -> List[float]:
    """
    returns a list of the average deaths caused by earthquakes in the periods: 
    1961-1970, 1971-1980, 1981-1990, 1991-2000, 2001-2010, 2011-2020 (in that order)
    """
    deaths_1970 = deaths_for_years(loe, 1961, 1970)
    deaths_1980 = deaths_for_years(loe, 1971, 1980)
    deaths_1990 = deaths_for_years(loe, 1981, 1990)
    deaths_2000 = deaths_for_years(loe, 1991, 2000)
    deaths_2010 = deaths_for_years(loe, 2001, 2010)
    deaths_2020 = deaths_for_years(loe, 2011, 2020)
    
    return [deaths_1970, 
            deaths_1980, 
            deaths_1990,
            deaths_2000,
            deaths_2010,
            deaths_2020]

@typecheck
def deaths_for_years(loe: List[Earthquake], min_year: int, max_year: int) -> float:
    """
    returns the average deaths of caused by all earthquakes that occured between 
    min_year and max_year
    """
    correct_years = filter_for_years(loe, min_year, max_year)
    deaths = filter_for_deaths(correct_years)
    average_deaths = average(deaths)
    
    return average_deaths

@typecheck
def filter_for_deaths(loe: List[Earthquake]) -> List[float]:
    """
    return a list of the number of deaths caused by the earthquakes in loe
    """
    deaths = [] # type: List[int]
    for e in loe:
        deaths.append(get_modified_deaths(e))
        
    return deaths

@typecheck
def get_modified_deaths(e: Earthquake) -> float:
    """
    returns the number of deaths caused by e in thousands (i.e. divided by 1000)
    """
    return round((e.deaths/10), 4)


###############
## Helpers for both Magnitude and Deaths
##############

@typecheck
def filter_for_years(loe: List[Earthquake], min_year: int, max_year: int) -> List[Earthquake]:
    """
    returns a list of only the earthquakes in loe that occured between min_year and max_year
    """
    years = []  # type: List[Earthquake]
    for e in loe:
        if min_year <= get_year(e) <= max_year:
            years.append(e)
    
    return years

@typecheck
def get_year(e: Earthquake) -> int:
    """
    returns the year that e occured in
    """
    return e.year

@typecheck
def average(lof: List[float]) -> float:
    """
    returns the average of the values in lof. If lof is empty, returns 0.0. 
    """
    sum = 0.0 # type: float
    for f in lof:
        sum = sum + f
    if len(lof) == 0.0:
        return 0.0 
    else:
        return sum/len(lof)

    
# Examples and tests for magnitudes_and_deaths
start_testing()
expect(magnitudes_and_deaths('data/earthquake_data_test1.csv'), None) # see Test 1
expect(magnitudes_and_deaths('data/earthquake_data_test2.csv'), None) # see Test 2
summary()

# Examples and tests for read
start_testing()
expect(read('data/earthquake_data_test1.csv'), [E1, E2, E3, Earthquake(2016, 4.9, 0), E5])
expect(read('data/earthquake_data_test2.csv'), [E1, Earthquake(1961, 7.6, 0), 
                                           Earthquake(1962, 5.9, 4), 
                                           Earthquake(1963, 4.5, 4), 
                                           Earthquake(1964, 5.2, 8), 
                                           Earthquake(1965, 5.5, 4)])
summary()

# Examples and tests for check_for_none
start_testing()
expect(check_for_none(None), 0)
expect(check_for_none(1), 1)
expect(check_for_none(87652), 87652)
summary()

# Examples and tests for plot_magnitude_and_deaths
start_testing()
expect(plot_magnitude_and_deaths(LOE0), None) # see Test 3
expect(plot_magnitude_and_deaths(LOE2), None) # see Test 4
expect(plot_magnitude_and_deaths([Earthquake(1965, 3.6, 0), 
                                  Earthquake(1978, 7.9, 1000), 
                                  Earthquake(1986, 6.2, 225), 
                                  Earthquake(1989, 7.5, 2345), 
                                  Earthquake(1994, 5.6, 31), 
                                  Earthquake(2006, 6.5, 564), 
                                  Earthquake(2017, 6.8, 43)]), None) # see Test 5
summary()

# Examples and tests for num_sequence
start_testing()
expect(num_sequence([], 5, 10), [])
expect(num_sequence([1, 10, 3], 5, 10), [5, 15, 25])
expect(num_sequence([1, 10, 3], 0.5, 3.5), [0.5, 4.0, 7.5])
summary()

# Examples and tests for final_average_magnitudes
start_testing()
expect(final_average_magnitudes([]), [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
expect(final_average_magnitudes([Earthquake(1961, 2.5, 0), 
                                 Earthquake(1965, 4.2, 3), 
                                 Earthquake(1971, 7.9, 1000), 
                                 Earthquake(1980, 4.3, 0)]), [33.5, 61.0, 0.0, 
                                                              0.0, 0.0, 0.0]) 
expect(final_average_magnitudes([Earthquake(1965, 3.6, 0), 
                                 Earthquake(1978, 7.9, 2000), 
                                 Earthquake(1986, 6.2, 625), 
                                 Earthquake(1989, 7.5, 2345), 
                                 Earthquake(1994, 5.6, 31), 
                                 Earthquake(2006, 6.5, 564), 
                                 Earthquake(2017, 6.8, 43)]), [36.0, 79.0, 68.5, 
                                                               56.0, 65.0, 68.0])
summary()

# Examples and tests for magnitude_for_years
start_testing()
expect(magnitude_for_years(LOE0, 1970, 1980), 0.0)
expect(magnitude_for_years(LOE1, 1960, 1980), 78.0)
expect(magnitude_for_years(LOE1, 1960, 2010), 70.0)
summary()

# Examples and tests for filter_for_magnitude
start_testing()
expect(filter_for_magnitude(LOE0), [])
expect(filter_for_magnitude(LOE1), [78.0, 62.0, 70.0, 49.0, 82.0])
expect(filter_for_magnitude(LOE2), [62.0, 49.0])
expect(filter_for_magnitude([Earthquake(1985, 0, 0)]), [0.0])
summary()

# Examples and tests for get_modified_magnitude
start_testing()
expect(get_modified_magnitude(E1), 78.0)
expect(get_modified_magnitude(E4), 49.0)
expect(get_modified_magnitude(Earthquake(1985, 0, 0)), 0.0)
summary()

# Examples and tests for final_average_deaths
start_testing()
expect(final_average_deaths([]), [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000])
expect(final_average_deaths([Earthquake(1961, 2.5, 0), 
                             Earthquake(1965, 4.2, 3), 
                             Earthquake(1971, 7.9, 1000), 
                             Earthquake(1980, 4.3, 0)]), [0.1500, 50.0000, 0.0000, 
                                                          0.0000, 0.0000, 0.0000]) 
expect(final_average_deaths([Earthquake(1965, 3.6, 0), 
                             Earthquake(1978, 7.9, 2000), 
                             Earthquake(1986, 6.2, 625), 
                             Earthquake(1989, 7.5, 2345), 
                             Earthquake(1994, 5.6, 31), 
                             Earthquake(2006, 6.5, 564), 
                             Earthquake(2017, 6.8, 43)]), [0.0000, 200.0000, 148.5000, 
                                                           3.1000, 56.4000, 4.3000])
summary()

# Examples and tests for deaths_for_years
start_testing()
expect(deaths_for_years(LOE0, 1970, 1980), 0.0000)
expect(deaths_for_years(LOE1, 1960, 1980), 6.3000)
expect(deaths_for_years(LOE1, 1960, 2010), 10535.5000)
summary()

# Examples and tests for filter_for_deaths
start_testing()
expect(filter_for_deaths(LOE0), [])
expect(filter_for_deaths(LOE1), [6.3000, 0.2000, 31600.0000, 0.0000, 9.8000])
expect(filter_for_deaths(LOE2), [0.2000, 0.0000])
expect(filter_for_deaths([Earthquake(1985, 0, 0)]), [0.0000])
summary()

# Examples and tests for get_modified_deaths
start_testing()
expect(get_modified_deaths(E1), 6.3000)
expect(get_modified_deaths(E3), 31600.0000)
expect(get_modified_deaths(Earthquake(1985, 0, 0)), 0.0000)
summary()

# Examples and tests for filter_for_years
start_testing()
expect(filter_for_years(LOE0, 1963, 1973), [])
expect(filter_for_years(LOE1, 1960, 1970), [E1])
expect(filter_for_years(LOE1, 1961, 2010), [E2, E3])
summary()
       
# Examples and tests for get_year 
start_testing()
expect(get_year(E1), 1960)  
expect(get_year(E5), 2017)  
expect(get_year(E3), 2010)
summary()

# Examples and tests for average
start_testing()
expect(average([250, 300, 400, 600, 800]), 470)
expect(average([25]), 25)
expect(average([2.6, 8.5, 9.8]), 20.9/3)
summary()



# ### Final Graph/Chart
# In[3]:
magnitudes_and_deaths('data/earthquake_data.csv')

