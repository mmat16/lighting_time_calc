import requests
from bs4 import BeautifulSoup as bs
import datetime


class LightingTimeCalc:

    sunTime = {
        "sunrise": datetime.datetime.now(),
        "sunset": datetime.datetime.now(),
    }
    totalLightingTime = datetime.datetime.now()

    @classmethod
    def __getTimeByName(cls, name, soup):
        Time = soup.find("ul",
                         class_="today-list list-group list-unstyled "
                         "px-0").find("div", attrs={
                             "data-name": name
                         }).text
        return Time

    @classmethod
    def __cookSoup(cls):
        response = requests.get(url="https://voshod-solnca.ru/sun/москва")
        response.encoding = "utf-8"
        return bs(response.text, "lxml")

    @classmethod
    def __getSunTimes(cls):
        soup = cls.__cookSoup()
        sunrise = cls.__getTimeByName(name="sunrise", soup=soup)
        sunset = cls.__getTimeByName(name="sunset", soup=soup)
        return sunrise, sunset

    @classmethod
    def __getDayLength(cls):
        dayLength = (cls.sunTime["sunset"] - cls.sunTime["sunrise"]).seconds
        dayLength /= 3600
        dayLength = round(dayLength, 1)
        return dayLength

    def __init__(self):
        sunTime = self.__getSunTimes()
        self.sunTime["sunrise"] = datetime.datetime.strptime(
            sunTime[0], "%H:%M:%S")
        self.sunTime["sunset"] = datetime.datetime.strptime(
            sunTime[1], "%H:%M:%S")
        self.totalLightingTime = datetime.datetime.strptime(
            input("total hours "
                  "lighting ("
                  "ex. 12): "), "%H")
        self.totalDayTime = self.__getDayLength()

    def RequiredAddLightDuration(self):
        if self.totalDayTime > self.totalLightingTime.hour:
            return None
        return self.totalLightingTime - datetime.timedelta(
            hours=self.totalDayTime)

    def divideAdditionalTime(self):
        timeRequired = self.RequiredAddLightDuration()
        if timeRequired:
            timeRequired = timeRequired.time()
            if timeRequired.minute >= 30:
                return (timeRequired.hour + 1) / 2.0
            return timeRequired.hour / 2.0
        return None

    def getTimesToTurnLights(self):
        additionalTime = self.divideAdditionalTime()
        startTime = self.sunTime["sunrise"] - datetime.timedelta(
            hours=additionalTime)
        endTime = self.sunTime["sunset"] + datetime.timedelta(
            hours=additionalTime)
        return startTime.time(), endTime.time()
