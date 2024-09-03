import tkinter as tk  #GUI
import weather as w  #weather.py
import requests  #requests for user location
import datetime as dt


class Application:
    def __init__(self, window, windspeed, Bcolor, Hcolor, filepath, Condition, location, temperature,
                 dailyWeather):  #Initialize the Screen

        self.window = window
        self.canvas = tk.Canvas(  #Create Window
            self.window,
            bg=Bcolor,
            height=1000,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)  #Header for style
        self.canvas.create_rectangle(
            0.0,
            0.0,
            1200.0,
            134.0,
            fill=Hcolor,
            outline="")

        self.canvas.create_rectangle(  #Bottom for 5 day forecast (Just the Background for it)
            0,
            800,
            1200,
            1000,
            fill=Hcolor,
            outline="")

        self.canvas.create_text( #Quick Title
            183.0,
            21.0,
            anchor="nw",
            text="Aaron's Weather Application",
            fill="#000000",
            font=("Arial", 54),
        )

        self.condition = tk.PhotoImage( #Photo of Weather Conditions (Icons. See GUI Elements folder)
            file=(filepath))
        Conditions = self.canvas.create_image(
            550.0,
            240.0,
            image=self.condition,
        )

        self.canvas.create_text( #Weather Condition
            410,
            334.0,
            anchor="nw",
            text=Condition,
            font=("Inter SemiBold", 60)
        )

        self.canvas.create_text( #Location being searched
            409.0,
            430.0,
            anchor="nw",
            text=location,
            fill="#000000",
            font=("Inter SemiBold", 32 * -1)
        )

        self.canvas.create_text( #Temperature of place, both in C and F
            409.0,
            460.0,
            anchor="nw",
            text=(temperature),
            fill="#000000",
            font=("Inter SemiBold", 32 * -1)
        )

        self.canvas.create_text( #Current Windspeed of the area
            409.0,
            500.0,
            anchor="nw",
            text=(windspeed),
            fill="#000000",
            font=("Inter SemiBold", 32 * -1)
        )

        self.entry_1 = tk.Entry( #User text field. Used for seeing other Cities
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=781.0,
            y=160.0,
            width=342.0,
            height=54.0
        )
        self.button_image_1 = tk.PhotoImage( #Button and image (for style). Commits message to weather.py
            file=("GUI Elements/button_1.png"))
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.buttonClick(),
            relief="flat"
        )
        self.button_1.place(
            x=781.0,
            y=234.0,
            width=347.0,
            height=48.0
        )

        self.txt = tk.Label( #Error handling label for wrong inputs/regular errors.
            text="",
            font=("Inter SemiBold", 12),
            bg=Bcolor,
            fg="red"
        )
        self.txt.place(
            x=781.0,
            y=300.0,
        )
        y = 50 #Just for style
        for index, row in dailyWeather.head(5).iterrows():  # 5 Day Forecast
            date = str(row['date'])[:10]
            weather_code = row['weather_code']
            temperature_max = row['temperature_2m_max']
            temperature_min = row['temperature_2m_min']
            temperature_max = int(temperature_max)
            temperature_min = int(temperature_min)
            temp = (temperature_max + temperature_min) / 2.0 #Average Temp for the day
            tempf = (temp * 1.8) + 32 # C to F
            tempf = int(tempf)
            temp = str(tempf) + " F"

            # Assuming w.getCondition() returns the weather condition based on weather_code
            filepath, Condition = w.getCondition(weather_code) #Returns weather based on weather codes
            self.canvas.create_text(
                y,
                850,
                anchor="nw",
                text=Condition,
                font=("Inter SemiBold", 12)
            )
            self.canvas.create_text(
                y,
                825,
                anchor="nw",
                text=date,
                font=("Inter SemiBold", 12)
            )
            self.canvas.create_text(
                y,
                875,
                anchor="nw",
                text=temp,
                font=("Inter SemiBold", 12)
            )
            y = y + 250 #Spaces out the forecast

        window.mainloop()

    def buttonClick(self):  #Interacts with hidden text to show unsucessful entries, and text box
        location = self.entry_1.get()
        print(location)
        if location == "":
            self.txt.config(text="Please enter a location")
            return 0
        try:
            windspeed, Bcolor, Hcolor, filepath, Condition, location, temperature, dailyWeather = init_variables(
                location)
            self.window.destroy()
            window = tk.Tk()
            window.geometry("1200x1000")
            app = Application(window, windspeed, Bcolor, Hcolor, filepath, Condition, location, temperature,
                              dailyWeather)
            window.mainloop()

        except:
            self.txt.config(
                text="An Error has occured. Please try again, or make sure the spelling is correct about the inputted town")
        return 1


def init_variables(location): #Initialize the variables for __innit__()
    userlocation = w.get_coords(location) #City to Coordinates
    currentWeather, dailyWeather = w.get_weather(userlocation)  # Weather for location Returned, both Daily and Current

    #Windspeed / Formatting
    windspeed = currentWeather.Variables(2).Value()
    windspeed = int(windspeed)
    windspeed = str(windspeed) + " MPH Winds"

    # Current temperature and Celcius to Farenheight calculated
    temperature_c = currentWeather.Variables(0).Value()
    temperature_c = round(temperature_c, 2)
    temperature_f = (temperature_c * 1.8) + 32
    temperature_f = '{0:.2f}'.format(temperature_f)
    temperature = str(temperature_c) + "°C   " + str(temperature_f) + "°F"

    filepath, Condition = w.getCondition(currentWeather)

    # Current time for colors
    try:
        time = dt.datetime.now().time()
        hour = time.hour

        if 0 <= hour <= 4:  #Evening: Purple
            Hcolor = "#8a24d8"
            Bcolor = "#c779fc"
        elif 5 <= hour <= 11:  #Yellow: Morning
            Hcolor = "#ca9c00"
            Bcolor = "#e5c65e"
        elif 12 <= hour <= 17:  #Orange: Afternoon
            Hcolor = "#ea8d37"
            Bcolor = "#ffc38b"
        else:  #Evening: Purple
            Hcolor = "#8a24d8"
            Bcolor = "#c779fc"
        print("time successful")
    except:
        Hcolor = "#ea8d37"
        Bcolor = "#ffc38b"

    return windspeed, Bcolor, Hcolor, filepath, Condition, location, temperature, dailyWeather


if __name__ == "__main__":
    # Get IP address details
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()

        # Extract city name
        locationC = data['city']
        locationS = data['region']
        location = locationC + ", " + locationS  # Formatted for get_coords() in weather.py

    except:  # Error, but continues program, default value used
        location = "Los Angeles, California"
        print(
            "User location not found. Using default location - Los Angeles, California")
    windspeed, Bcolor, Hcolor, filepath, Condition, location, temperature, dailyWeather = init_variables(location)
    window = tk.Tk()
    window.geometry("1200x1000")
    app = Application(window, windspeed, Bcolor, Hcolor, filepath, Condition, location, temperature, dailyWeather)
    window.mainloop()
