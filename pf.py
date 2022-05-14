from cmath import nan
from datetime import date
from matplotlib.pyplot import vlines
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import argrelextrema



def main():
    # Reads the ticker data
    df = yf.Ticker("AAPL").history(start="2018-01-01", end="2020-01-01")

    # Shorter tf for testing purposes
    tdf = df.loc['2018-01-02':'2018-12-31']

    # Finds swing highs and lows
    n=4
    tdf['min'] = tdf.iloc[argrelextrema(tdf.Low.values, np.less_equal,
                    order=n)[0]]['Low']
    tdf['max'] = tdf.iloc[argrelextrema(tdf.High.values, np.greater_equal,
                    order=n)[0]]['High']

    tdf_index = list(range(0, len(tdf.index)))
    tdf['count'] = tdf_index
    # Pairing lows and highs
    foundHigh = False
    foundLow = False
    pf_width = []
    pf_width_midpoint = []
    pf_width_midpoint_time = []
    oneToTwo = []
    median_point = []
    median_line = []
    top_pf = []
    bottom_pf = []
    swingHigh = np.nan
    swingLow = np.nan
    swingHigh_time = np.nan
    swingLow_time = np.nan
    highCount = 0
    lowCount = 0
    idx = 0
    idx_low = 0
    idx_high = 0
    for index, row in tdf.iterrows():
        # Checks if there is a swing high
        if(pd.notnull(row['max']) and foundHigh==False):
            # Found a swing high
            swingHigh = row['max']
            date_to_use = str(index).split(' ')
            swingHigh_time = date_to_use[0]
            foundHigh = True
            idx_high = row['count']

            # Check to see if a swing low is found
            if(foundLow==True):
                # The width of the pf. points 2 and 3
                width_line = [(swingLow_time, swingLow), (swingHigh_time, swingHigh)]
                pf_width.append(width_line)
                # The midpoint of the width
                pf_width_midpoint.append((swingHigh+swingLow)/2)
                if(abs(idx_high+idx_low) % 2 == 0):
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2
                    print(width_midpoint)
                    #TODO Need to do this correctly. Find slope and plot where the midpoint would be.
                else:
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2
                    print(width_midpoint)

                # Finds point 1. Line from point 1 to midpoint of point 2 and 3. Finds the slope to draw the mdeian line.  
                if (swingLow_time > swingHigh_time) and (lowCount > 0):
                    med_price = median_low
                    med_time_str = tdf[tdf['min'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    median_point.append(median_low)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['min'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])                 

                elif (swingLow_time < swingHigh_time) and (highCount > 0):
                    med_price = median_high
                    med_time_str = tdf[tdf['max'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    median_point.append(median_high)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['max'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])
                else:
                    med_price = np.nan
                    med_time = np.nan
                    median_point.append(np.nan)

                # Resets the flag
                foundHigh = False
                foundLow = False
            
            # Updates median line
            median_high = row['max']
            # Increments counter
            highCount += 1
        # Checks to see if there have been consecutive swing highs
        elif(pd.notnull(row['max']) and foundHigh==True):
            if (row['max'] > swingHigh):
                swingHigh=row['max']
                date_to_use = str(index).split(' ')
                swingHigh_time = date_to_use[0]
                idx_high = row['count']
            else:
                med_point = int(abs(idx_high-idx_low)/2)
                middle_time = tdf.index[med_point]
                date_to_use = str(middle_time).split(' ')

            # Check to see if a swing low is found
            if(foundLow==True):
                # The width of the pf. points 2 and 3
                width_line = [(swingLow_time, swingLow), (swingHigh_time, swingHigh)]
                pf_width.append(width_line)
                # The midpoint of the width
                pf_width_midpoint.append((swingHigh+swingLow)/2)
                if(abs(idx_high+idx_low) % 2 == 0):
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    print(width_midpoint)
                    width_midpoint = (swingHigh + swingLow)/2
                else:
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2
                    print(width_midpoint)

                # Finds point 1
                if (swingLow_time > swingHigh_time) and (lowCount > 0):
                    med_price = median_low
                    med_time_str = tdf[tdf['min'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    median_point.append(median_low)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['min'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])

                elif (swingLow_time < swingHigh_time) and (highCount > 0):
                    med_price = median_high
                    med_time_str = tdf[tdf['max'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    median_point.append(median_high)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['max'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])

                else:
                    med_price = np.nan
                    med_time = np.nan
                    median_point.append(np.nan)

                foundHigh = False
                foundLow = False
            
            # Updates median line
            median_high = row['max']
            # Increments counter
            highCount += 1
        # Checks to see if there is a swing low
        elif(pd.notnull(row['min']) and foundLow==False):
            # Found a swing low
            swingLow = row['min']
            date_to_use = str(index).split(' ')
            swingLow_time = date_to_use[0]
            foundLow = True
            idx_low = row['count']

            # Check to see if a swing high is found
            if(foundHigh==True):
                # The width of the pf. points 2 and 3
                width_line = [(swingLow_time, swingLow), (swingHigh_time, swingHigh)]
                pf_width.append(width_line)
                # The midpoint of the width
                pf_width_midpoint.append((swingHigh+swingLow)/2)
                if(abs(idx_high+idx_low) % 2 == 0):
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2
                else:
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2

                # Finds point 1
                if (swingLow_time > swingHigh_time) and (lowCount > 0):
                    med_price = median_low
                    med_time_str = tdf[tdf['min'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    print(tdf.iloc[med_point]['Close'])
                    print(width_midpoint)
                    median_point.append(median_low)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['min'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])

                elif (swingLow_time < swingHigh_time) and (highCount > 0):
                    med_price = median_high
                    med_time_str = tdf[tdf['max'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    print(tdf.iloc[med_point]['Close'])
                    print(width_midpoint)
                    median_point.append(median_high)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['max'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])
                    
                else:
                    med_price = np.nan
                    med_time = np.nan
                    median_point.append(np.nan)

                foundHigh = False
                foundLow = False
            
            # Updates median line
            median_low = row['min']
            # Increments counter
            lowCount += 1
        # Checks to see if there have been consecutive swing lows
        elif(pd.notnull(row['min']) and foundLow==True):
            if (row['min'] < swingLow):
                swingLow=row['min']
                date_to_use = str(index).split(' ')
                swingLow_time = date_to_use[0]
                idx_low = row['count']
            
            # Check to see if a swing high is found
            if(foundHigh==True):
                # The width of the pf. points 2 and 3
                width_line = [(swingLow_time, swingLow), (swingHigh_time, swingHigh)]
                pf_width.append(width_line)
                # The midpoint of the width
                pf_width_midpoint.append((swingHigh+swingLow)/2)
                if(abs(idx_high+idx_low) % 2 == 0):
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2
                else:
                    med_point = int(abs(idx_high+idx_low)/2)
                    middle_time = tdf.index[med_point]
                    date_med = str(middle_time).split(' ')
                    width_midpoint = (swingHigh + swingLow)/2

                # Finds point 1
                if (swingLow_time > swingHigh_time) and (lowCount > 0):
                    med_price = median_low
                    med_time_str = tdf[tdf['min'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    print(tdf.iloc[med_point]['Close'])
                    print(width_midpoint)
                    median_point.append(median_low)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['min'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])

                elif (swingLow_time < swingHigh_time) and (highCount > 0):
                    med_price = median_high
                    med_time_str = tdf[tdf['max'] == med_price].index.values
                    med_time = str(med_time_str[0]).split("T")
                    oneToTwo.append([(med_time[0], med_price), (date_med[0], width_midpoint)])
                    print(tdf.iloc[med_point]['Close'])
                    print(width_midpoint)
                    median_point.append(median_high)

                    # Finds the median line
                    # Find the slope
                    x1 = tdf[tdf['max'] == med_price]['count'].values
                    x2 = med_point
                    y1 = med_price
                    y2 = width_midpoint

                    slope = (y2-y1)/(x2-x1)
                    print("slope " + str(slope))

                    # Calculates the median line
                    x3 = tdf["count"].iloc[-1]
                    y3 = (slope*(x3-x2)) + y2

                    last_time = str(tdf.index[-1]).split(' ')
                    median_line.append([(date_med[0], y2), (last_time[0], y3[0])])

                    # Calculates the top of the pf
                    top_x1 = tdf[tdf['max'] == swingHigh]['count'].values
                    top_y1 = swingHigh
                    top_y2 = (slope*(x3-top_x1) + top_y1)
                    top_pf.append([(swingHigh_time, swingHigh), (last_time[0], top_y2[0])])

                    # Calculates the bottom of the pf
                    bottom_x1 = tdf[tdf['min'] == swingLow]['count'].values
                    bottom_y1 = swingLow
                    bottom_y2 = (slope*(x3-bottom_x1) + bottom_y1)
                    bottom_pf.append([(swingLow_time, swingLow), (last_time[0], bottom_y2[0])])

                else:
                    med_price = np.nan
                    med_time = np.nan
                    median_point.append(np.nan)

                foundHigh = False
                foundLow = False

            # Updates median line
            median_low = row['min']
            # Increments counter
            lowCount += 1  
        
        idx += 1

    
    
    # Color for different lines
    print("=================")
    print(oneToTwo)
    width_color = ['b' for i in range(len(pf_width))]
    med_color = ['r' for i in range(len(oneToTwo))]
    median_line_color = ['r' for i in range(len(median_line))]
    top_pf_color = ['b' for i in range(len(top_pf))]
    bottom_pf_color = ['b' for i in range(len(bottom_pf))]
    
    # Plots swing highs and lows
    apd = [mpf.make_addplot(tdf['max'],type='scatter'), mpf.make_addplot(tdf['min'],type='scatter'),]
    mpf.plot(tdf, type="candle", addplot=apd,alines=dict(alines=pf_width+oneToTwo+median_line+top_pf+bottom_pf, colors=width_color+med_color+median_line_color+top_pf_color+bottom_pf_color))
    # mpf.plot(tdf, type="candle", addplot=apd, alines=pf_width+oneToTwo, colors=width_color+med_color)
    mpf.plot(tdf, type="candle", addplot=apd)

if __name__ == "__main__":
    main()