# Har en lösning på varenda här kända bugg, men tiden räcker inte till as Galois famously said
# OK Roytard! Max 10 stations at'da time! For now anywhey cuz like.. do you want the program to "RAM" up ya A-SS ?!?
# Kan existera bugg med station = 0
# This is GREEN HEALTHY CODE FYI!!!
import pandas as pd
from pandas.io.json import json_normalize
import json, requests
#import matplotlib.dates as dts
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs

import numpy as np
from tkinter import *
import datetime



"""
url = "https://opendata-download-metobs.smhi.se/api/version/%s/parameter/%s/station/%s/period/%s/data.%s" % ("latest","1","159880","latest-months","csv")
print(url)
df = pd.read_csv(url, skiprows=9, usecols=[0,1,2,3,5],sep=";")
print(df)
"""

def select_parameter():
    #parameter_value = input("Select attribute")
    url = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/3.json?print=pretty"
    r = requests.get(url)
    data = r.json()
    print(data.keys())
    #print(data["station"])
    station_lst = pd.DataFrame(data["station"], columns=["name", "owner", "ownerCategory", "id", "height", "latitude","longitude", "active", "from", "to", 'key', 'updated', 'title', 'summary'], )
    #head = station_lst.head()
    return station_lst

def get_parameters():
    url = "https://opendata-download-metobs.smhi.se/api/version/latest.json?print=pretty"
    r = requests.get(url)
    data = r.json()
    print(data.keys())
    key_lst = pd.DataFrame(data["resource"], columns=['key', 'updated', 'title', 'summary', 'link', 'resource'])
    #print(key_lst.head())
    return key_lst

def get_weather_data(url):
    #url = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station/92400/period/corrected-archive/data.csv"
    #df = pd.read_csv(url, usecols=['Datum', 'Tid (UTC)', 'Lufttemperatur'], sep=';', names=['Datum',	'Tid (UTC)', 'Lufttemperatur', 'Kvalitet'])
    try:
        df = pd.read_csv(url, header= None, names=['Datum',	'Tid', 'Lufttemperatur', 'Kvalitet'], sep=";")
        newindex = 1 + df[df['Datum'] == 'Datum'].index.item() # LOVE
        #df.set_index(['Datum'])
        dfB = df[newindex:]
        #print(df.columns('Datum'))
        #print (dfB)
        return dfB
    except:
        print("Parameter does not exist for the selected station.")
    
    

# THE FOX SAYS EEEHHEHEHEHE
class station:
    def __init__(self):
        # Always choose the latest SMHI version even tho they recomends against it//
        self._version_number = "latest"
        # Default parameter = Lufttemperatur
        # accepterade värden är de för momentanvärderna ty annars blir le dataframes uppfuckat as fuck
        # 1, 4, 6, 7, 8, 9, 10, 12, 16, --/24
        self._parameter_number = 16
        # Default station = Karlskrona (65090)
        self._station_number = "65090"
        # Default period = corrected-archive
        self._period = "corrected-archive"

    # Setters
    def set_parameter(self, parameter):
        self._parameter_number = parameter
    def set_station(self, station):
        self._station_number = station
    def set_period(self, period):
        self._period = period

    def update_url(self):
        None
        
    # Getters
    # returns dataframe
    def get_available_parameters(self):
        url = "https://opendata-download-metobs.smhi.se/api/version/%s.json?print=pretty" %(self._version_number)
        r = requests.get(url)
        data = r.json()
        print(data.keys())
        key_lst = pd.DataFrame(data["resource"], columns=['key', 'updated', 'title', 'summary', 'link', 'resource'])
        return key_lst

    def get_available_stations(self):
        url = "https://opendata-download-metobs.smhi.se/api/version/%s/parameter/%s.json?print=pretty" %(self._version_number, self._parameter_number)
        r = requests.get(url)
        data = r.json()
        station_lst = pd.DataFrame(data["station"], columns=["name", "owner", "ownerCategory", "id", "height", "latitude","longitude", "active", "from", "to", 'key', 'updated', 'title', 'summary'], )
        return station_lst

    def get_available_timespan(self):
        return "https://opendata-download-metobs.smhi.se/api/version/%s/parameter/%s/station/%s/period.json?print=pretty" %(self._version_number, self._parameter_number, self._station_number)
        # returns csv
    def get_station_url(self):
        return "https://opendata-download-metobs.smhi.se/api/version/%s/parameter/%s/station/%s/period/%s/data.csv" % (self._version_number, self._parameter_number, self._station_number, self._period)

        
def menu(station_lst):
    if is_running is not True:
        return

    user_input = input("""
    ____MENU____
    0: Graph Data
    1: Change period
    2: Change station
    3: Change parameter
    4: Add station (max 10)
    5: Remove station
    6: Exit
    Choice: """)
    return user_input
 

def create_new_station():
    None


def change_period(dataframe, start_date, end_date, start_hour, end_hour):
    ret_lst = []
    
    start_date = dataframe[dataframe['Datum'].str.match(start_date)]
    ret_lst.append([start_date, start_date.index[0]])
    
    end_date = dataframe[dataframe['Datum'].str.match(end_date)]
    ret_lst.append([end_date, end_date.index[0]])
    
    start_hour = [start_hour, start_date.index[start_date['Tid'] == start_hour].tolist()]
    ret_lst.append(start_hour)

    end_hour = [end_hour, end_date.index[end_date['Tid'] == end_hour].tolist()]
    ret_lst.append(end_hour)

    return ret_lst


def create_graph(dataframe, period):
            fig, ax = plt.subplots()
            ax.set_title("Online Weather")
            ax.set_ylabel("Lufttemperatur")
            ax.set_xlabel("Datum")

            x_values = dataframe[period[2][1][0]:period[3][1][0]]['Datum'].tolist()
            y_values = dataframe[period[2][1][0]:period[3][1][0]]['Lufttemperatur'].tolist()
            
            x = []
            y = []
            for a in range(0, len(y_values), 18):
                x.append(x_values[a])
                y.append(float(y_values[a]))
            ax.plot(x, y)
            ax.grid(True)
            ax.set_ylim(0.0 , 100.0)
            fig.autofmt_xdate()
            plt.show()


#===========================================
# ____MAIN____
#===========================================
if __name__ == "__main__":
    # Default station = Karlskrona --- could automatically be the users current coordinates with a future update ---
    station_1 = station()
    station_lst = [station_1]
    df = get_weather_data(station_1.get_station_url())

    # Default period
    periodlist = change_period(df, "2015-01-01", "2016-02-01", "00:00:00", "00:00:00")

    #df.apply(lambda r : pd.datetime.combine(datetime.date(r['Datum']), datetime.time(r['Tid'])).time(), 1)
    #df['DateTime']
    # print(df.head())
    #====================
    # Loop  with menu...
    #====================

    is_running = True
    while is_running:
        usr_choice = menu(station_lst)
#====================================================================
# Härifrån är det icke klart
#====================================================================
        # 0: Graph Data
        if str(usr_choice) == '0':
                create_graph(df, periodlist)
            # print(df.head())
            # df = get_weather_data(station_1.get_station_url())
            # df['Datum'] = df['Datum'].apply(lambda x: pd.Timestamp(x).strftime('%B-%d-%Y %I:%M %p'))
            # df['Datum'] = pd.to_datetime(df['Datum'])
            # df.loc[:,'Datum'] = pd.to_datetime(df.Datum.astype(str)+' '+df.Tid.astype(str))
            # print(df.head())
            # df.Datum = pd.to_numeric(df.Datum)
            # df.plot(figsize=(15,4))
            # df.plot(x="Datum", y="Lufttemperatur", style='.')
#====================================================================
#====================================================================
#====================================================================        
        # 1: Change period
        elif str(usr_choice) == '1':
            start_date_input = input("Start date (YYYY-MM-DD): ")
            end_date_input = input("End date (YYYY-MM-DD): ")
            start_hour_input = input("From hour on start date (HH:MM:SS) ")
            end_hour_input = input("To hour on end date (HH:MM:SS): ")
            periodlist = change_period(df, start_date_input, end_date_input, start_hour_input, end_hour_input)
            

#====================================================================
# Till Hit
#====================================================================
#====================================================================
# Alltså ETTAN och TVÅAN
#====================================================================
        # 2: Change station
        elif str(usr_choice) == '2':
            if len(station_lst) <= 1:
                available_stations = station_1.get_available_stations()
                
                root = Tk()
                root.title("Station Selection")
                scrollbar = Scrollbar(root)
                scrollbar.pack(side=RIGHT, fill=Y)

                l = Listbox(root, width=30, height=35, selectmode= BROWSE)  
                for s in range(len(available_stations.values.tolist())):
                    l.insert(s, available_stations['name'][s])
                l.pack()

                l.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=l.yview)

                
                # Insider Function
                def cursor_select():
                    clicked_item = l.curselection()
                    #print(clicked_item[0])
                    #print(available_stations['id'].iloc[[clicked_item[0]]])
                    station_1.set_station(available_stations['id'].iloc[clicked_item[0]])
                    #print(new_station)
                    root.destroy()

                button = Button(root, text= "select", command=cursor_select)
                button.pack()
                root.geometry("300x600+120+120")
                root.mainloop()
                
            else:
                input("Which station do you want to change")

        # 3: Change Parameter
        elif str(usr_choice) == '3':
            user_input = input(
    """
    ____PARAMETERS____
    1: Lufttemperatur
    2: Vindhastighet
    3: Nederbördsmängd
    4: Total molnmängd
    5: Solskenstid
    6: Relativ Luftfuktighet
    Choice: """)
            if str(user_input) == '1':
                station_1.set_parameter('1')
                print("\nParameter changed to Lufttemperatur")
            elif str(user_input) == '2':
                station_1.set_parameter('4')
                print("\nParameter changed to Vindhastighet")
            elif str(user_input) == '3':
                station_1.set_parameter('7')
                print("\nParameter changed to Nederbördsmängd")
            elif str(user_input) == '4':
                station_1.set_parameter('16')
                print("\nParameter changed to Total molnmängd")
            elif str(user_input) == '5':
                station_1.set_parameter('10')
                print("\nParameter changed to Solskenstid")
            elif str(user_input) == '6':
                station_1.set_parameter('6')
                print("\nParameter changed to Relativ Luftfuktighet")
            else:
                print("INVALID INPUT!!!")

        # 4: Add station
        elif str(usr_choice) == '4':
            create_new_station()

        # 5: Remove Station
        elif str(usr_choice) == '5':
            None
        # 6: Exit
        elif str(usr_choice) == '6':
            is_running = False
        else:
            print("__Invalid User Input!__")

    print("exit")
