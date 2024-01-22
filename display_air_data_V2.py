#!/usr/bin/env python

'''
need to run script with:
        --led-cols = 64 and
        --led-brightness = 50

'''

from samplebase import SampleBase
from rgbmatrix import graphics
import time
import sys
import pandas as pd
import requests
import json
import xmltodict
from datetime import datetime, timedelta
import urllib.parse


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Bonjour")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/francois/rpi-rgb-led-matrix/fonts/5x7.bdf") # works well, 4 lines
        textColor = graphics.Color(125,125,125) #R,B,G nice blue hue 
        
        # my_text = self.args.text
        
        while True:
            offscreen_canvas.Clear()
            graphics.DrawText(offscreen_canvas, font, 0, 6, textColorUV, firstLine)
            graphics.DrawText(offscreen_canvas, font, 0, 14, textColorNO, secondLine)
            graphics.DrawText(offscreen_canvas, font, 0, 22, textColorCO, thirdLine)
            graphics.DrawText(offscreen_canvas, font, 0, 31, textColorPM10, fourthLine)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
    # prepare start and end time for URL formatting
    # datetime object containing current date and time
    now = datetime.now()
    # print("now =", now)
    nowString = now.strftime("%Y-%m-%dT%H:%M:%S")
    startPeriod = now - timedelta(hours=1.5)
    startString = startPeriod.strftime("%Y-%m-%dT%H:%M:%S")
    startPeriod = urllib.parse.quote(startString) + "%2B10%3A00"
    print("date and time Now =", nowString)
    endPeriod = nowString + "%2B10"
    endPeriod = urllib.parse.quote(nowString) + "%2B10%3A00"
    # assemble formatted URL
    urlBase = "https://airquality.des.qld.gov.au/v1/stations/woo/parameters/measurements?"
    startDate = "start_date=" + startPeriod  # 2023-11-03T06%3A00%3A00%2B10%3A00&
    addSpecialChar = "&"
    endDate = "end_date=" + endPeriod  # 2023-11-03T15%3A00%3A00%2B10%3A00&
    urlTail = "&pagesize=1000&pagenumber=1"
    url = urlBase + startDate + "&" + endDate + urlTail
    # print(url)
   
    # A GET request to the API
    response = requests.get(url)
    # put response in list of dict
    response_json = response.json()
    # convert JSON to dataframe
    df = pd.DataFrame(response_json)
    # cleanup date time in dataframe
    # original date format is in zulu time, convert to brisbane
    df['date_measured'] = pd.to_datetime(df['date_measured'])
    df['date_measured'] = df['date_measured'].dt.tz_convert('Australia/Brisbane')
    # combien de date de mesure
    dateMeasured = df['date_measured'].nunique()
    # response_json[0].keys()
    print("Measurement Time: " + df['date_measured'][0].strftime("%Y-%m-%d %H:%M"))
    # sort parameter and parameter name based on parameter ID
    df = df.sort_values(by='parameter_id')
    paramDict = {1: "Wind Direction", 2: "Wind Speed", 8: "Carbon Monoxide", 9: "Humidity", 10: "Temperature", 16: "NO2",
                 18: "PM10", 27: "Rainfall", 31: "PM2.5"}
    df['parameter_name'] = df['parameter_id'].map(paramDict)
    
    temperature = df[df['parameter_name'] == "Temperature"]["mvalue"].values[0]
    humidity = df[df['parameter_name'] == "Humidity"]["mvalue"].values[0]
    PM10 = df[df['parameter_name'] == "PM10"]["mvalue"].values[0]
    PM25 = df[df['parameter_name'] == "PM2.5"]["mvalue"].values[0]
    rainfall = df[df['parameter_name'] == "Rainfall"]["mvalue"].values[0]
    NO2 = df[df['parameter_name'] == "NO2"]["mvalue"].values[0]
    CO = df[df['parameter_name'] == "Carbon Monoxide"]["mvalue"].values[0]
    
     #url UV from ARPANSA
    urlUV = 'https://uvdata.arpansa.gov.au/xml/uvvalues.xml'
    responseUV = requests.get(urlUV)
    
    decodedResp = responseUV.content.decode('utf-8')
    temp = json.loads(json.dumps(xmltodict.parse(decodedResp)))
    # clean xml output
    datalist = temp['stations']['location']
    df = pd.DataFrame(datalist)
    dfBris = df.loc[df['@id'] == 'Brisbane'].reset_index()
    brisUV = float(dfBris.loc[0]['index'])
    
    # pick color based on values
    if CO < 9:
        textColorCO = graphics.Color(0,0,125) # green
    elif CO >= 9 and CO <= 25:
        textColorCO = graphics.Color(125,0,125) # Red and green
    elif CO > 25:
        textColorCO = graphics.Color(125,0, 0) # Red
    
    if NO2 < 0.12:
        textColorNO = graphics.Color(0,0,125) #green
    elif NO2 >= 0.12:
        textColorNO = graphics.Color(125,0, 0) # Red
    
    if PM10 <  40 :
        textColorPM10 = graphics.Color(0,0,125) #green
    elif PM10 >= 40 and PM10 <= 100:
        textColorPM10 = graphics.Color(125,0,125) # Red and green
    elif PM10 > 100:
        textColorPM10 = graphics.Color(125,0, 0) # Red
        
    if brisUV < 3:
        textColorUV = graphics.Color(0,0,125) #green
    elif brisUV >= 3 and brisUV <= 8 :
        textColorUV = graphics.Color(125,0,125) #red, green
    elif brisUV > 8:
        textColorUV = graphics.Color(125,0,0) #red
    
    print("Temperature:" + str(temperature) + "C")
    print("Humidity:" + str(humidity) + "%")
    print("Rainfall:" + str(rainfall) + "mm")
    print("Nitrogen dioxide:" + str(NO2) + "ppm")
    print("Carbon monoxide:" + str(CO) + "ppm")
    print("Particle PM10:" + str(PM10) + "\u03BC" + "g/m3")
    print("Particle PM2.5:" + str(PM25) + "\u03BC" + "g/m3")
    print("UV index: " + str(brisUV) )
    
    run_text = RunText()
    firstLine =  "UVidx:" + str(brisUV)  #"Line1,is it too long"
    secondLine = "NO:" + str(NO2) + "ppm"
    thirdLine = "CO:" + str(CO) + "ppm"
    fourthLine = "PM10:" + str(PM10) + "\u03BC" + "g" #"g/m3"
    
    # if (not run_text.process()):
        # run_text.print_help()
    run_text.process()

