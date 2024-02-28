class Subject:
    # Both of the following two methods take an
    # observer as an argument; that is, the observer
    # to be registered ore removed.
    def registerObserver(observer):
        pass
    def removeObserver(observer):
        pass
    
    # This method is called to notify all observers
    # when the Subject's state (measurements) has changed.
    def notifyObservers():
        pass
    
# The observer class is implemented by all observers,
# so they all have to implemented the update() method. Here
# we're following Mary and Sue's lead and 
# passing the measurements to the observers.
class Observer:
    def update(self, temp, humidity, pressure):
        pass


# WeatherData now implements the subject interface.
class WeatherData(Subject):
    
    def __init__(self):        
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
    
    
    def registerObserver(self, observer):
        # When an observer registers, we just 
        # add it to the end of the list.
        self.observers.append(observer)
        
    def removeObserver(self, observer):
        # When an observer wants to un-register,
        # we just take it off the list.
        self.observers.remove(observer)
    
    def notifyObservers(self):
        # We notify the observers when we get updated measurements 
        # from the Weather Station.
        for ob in self.observers:
            ob.update(self.temperature, self.humidity, self.pressure)
    
    def measurementsChanged(self):
        self.notifyObservers()
    
    def setMeasurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        
        self.measurementsChanged()
    
    # other WeatherData methods here.


class CurrentConditionsDisplay(Observer):
    
    def __init__(self, weatherData):        
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        
        self.weatherData = weatherData # save the ref in an attribute.
        weatherData.registerObserver(self) # register the observer 
                                           # so it gets data updates.
    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()
        
    def display(self):
        print("<====================== Current conditions ======================>")
        print("Current conditions:", self.temperature, 
              "F degrees and", self.humidity,"[%] humidity",
              "and pressure", self.pressure)
        
# TODO: implement StatisticsDisplay class and ForecastDisplay class.
class StatisticsDisplay(Observer):
    def __init__(self, weatherData):
        self.maxTemp = 0.0
        self.minTemp = 200
        self.tempSum = 0.0
        self.numReadings = 0
        self.weatherData = weatherData
        weatherData.registerObserver(self)
    
    def update(self, temperature, humidity, pressure):
        self.tempSum += temperature
        self.numReadings += 1

        self.maxTemp = max(self.maxTemp, temperature)
        self.minTemp = min(self.minTemp, temperature)
        
        self.display()

    def display(self):
        print("<====================== Weather Statistics ======================>")
        print("Avg/Max/Min temperature = " + str(self.tempSum / self.numReadings) +
              "/" + str(self.maxTemp) + "/" + str(self.minTemp))

class ForecastDisplay(Observer):
    def __init__(self, weatherData):
        self.currentPressure = 29.92
        self.lastPressure = 0.0
        self.forecastTemp = 0.0
        self.forecastHumidity = 0.0
        self.forecastPressure = 0.0
        self.weatherData = weatherData
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.lastPressure = self.currentPressure
        self.currentPressure = pressure
        self.forecastTemp = temperature + 0.11 * humidity + 0.2 * pressure
        self.forecastHumidity = humidity - 0.9 * humidity
        self.forecastPressure = pressure + 0.1 * temperature - 0.21 * pressure
        self.display()

    def display(self):
        print(f"Forecast Temp: {self.forecastTemp}F")
        print(f"Forecast Humidity: {self.forecastHumidity}%")
        print(f"Forecast Pressure: {self.forecastPressure}inHg")
        print("General Forecast: ", end="")
        if self.currentPressure > self.lastPressure:
            print("Improving weather on the way!")
        elif self.currentPressure == self.lastPressure:
            print("More of the same")
        else:
            print("Watch out for cooler, rainy weather")

    
    
class WeatherStation:
    def main(self):
        weather_data = WeatherData()
        current_display = CurrentConditionsDisplay(weather_data)
        
        # TODO: Create two objects from StatisticsDisplay class and 
        # ForecastDisplay class. Also, register them to the concrete instance
        # of the Subject class so they get the measurements' updates.
        statistics_display = StatisticsDisplay(weather_data)
        forecast_display = ForecastDisplay(weather_data)
        
        # The StatisticsDisplay class should keep track of the min/average/max
        # measurements and display them.
        statistics_display.update(80, 65, 30.4)
        statistics_display.display()
        
        # The ForecastDisplay class shows the weather forecast based on the current
        # temperature, humidity and pressure. Use the following formulas :
        # forcast_temp = temperature + 0.11 * humidity + 0.2 * pressure
        # forcast_humadity = humidity - 0.9 * humidity
        # forcast_pressure = pressure + 0.1 * temperature - 0.21 * pressure
        forecast_display.update(80, 65, 30.4)
        forecast_display.display()
        
        weather_data.setMeasurements(80, 65,30.4)
        weather_data.setMeasurements(82, 70,29.2)
        weather_data.setMeasurements(78, 90,29.2)
        
        # un-register the observer
        weather_data.removeObserver(current_display)
        weather_data.setMeasurements(120, 100,1000)
    
        


if __name__ == "__main__":
    w = WeatherStation()
    w.main()