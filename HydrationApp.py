import random
import api_functions
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class HydrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydration App")
        self.root.geometry("450x650")

        # Water variables
        self.humidity_affect = 0 # default 0, can be changed later
        self.lifestyle_affect = 0 # default 0, can be changed later
        self.activity_affect = 0 # defaul 0, can be changed later
        self.dailyIntake = 64 + self.humidity_affect + self.activity_affect + self.lifestyle_affect  # oz
        

        self.currentIntake = 0
        self.reminderInterval = 60*60*1000 #default is 1hr in milliseconds
        self.afterID = None

        # Init screens
        self.mainFrame = None
        self.intakeFrame = None
        self.reminderFrame = None
        self.lifestyleFrame = None
        self.humidityFrame = None

        #init label
        self.goalLabel = None
        self.currentIntakeLabel = None
        self.intervalLabel = None

        # Creating the screens
        self.create_mainFrame()
        self.create_intakeFrame()
        self.create_reminderFrame()
        self.create_lifestyleFrame()
        self.create_humidityFrame()


        self.show_frame(self.mainFrame)

        #starting reminder function
        self.set_reminder()



    def show_frame(self, frame):
        if frame == self.mainFrame: #allow use of button on main screen
            self.customIntakeEntry.unbind("<Return>")
            self.currentIntakeEntry.bind("<Return>", lambda event: self.set_currentIntake())

        if frame == self.intakeFrame: #allow use of return button on intake frame
            self.currentIntakeEntry.unbind("<Return>")
            self.customIntakeEntry.bind("<Return>", lambda event: self.set_customIntake())

        for w in self.root.winfo_children():
            w.pack_forget()

        frame.pack(fill="both", expand=True)
        self.root.update_idletasks()

    def create_mainFrame(self):
        self.mainFrame = tk.Frame(self.root, bg="#ADD8E6")
        #labels
        self.goalLabel = tk.Label(self.mainFrame, text=f"Daily Water Intake Goal: {self.dailyIntake} oz")
        self.goalLabel.pack(pady=(70,1))

        self.currentIntakelabel = tk.Label(self.mainFrame, text=f"Current Intake: {self.currentIntake} oz")
        self.currentIntakelabel.pack(pady=(1,10))

        #progress bar for water intake
        style = ttk.Style()
        style.theme_use("clam")  # Use a modern theme
        style.configure(
            "Blue.Vertical.TProgressbar",
            troughcolor="white",
            background="#1E90FF",  # DeepSkyBlue for the filled part
            thickness=20
        )

        # Progress bar for water intake
        self.progressBar = ttk.Progressbar(
            self.mainFrame,
            orient="vertical",
            length=200,
            mode="determinate",
            style="Blue.Vertical.TProgressbar"
        )
        self.progressBar.pack(pady=(10, 0))

        #buttons
        tk.Button(self.mainFrame, text="Set Custom Water Intake",
                  command=lambda: self.show_frame(self.intakeFrame),
                  width=30
                  ).pack(pady=(20,0))

        tk.Button(self.mainFrame, text="Change Reminder Interval",
                  command=lambda: self.show_frame(self.reminderFrame),
                  width=30
                  ).pack()

        tk.Button(self.mainFrame,
                  text="Update Lifestyle and Workout",
                  command=lambda: self.show_frame(self.lifestyleFrame),
                  width=30
                  ).pack()

        tk.Button(self.mainFrame,
                  text="Update Location",
                  command=lambda: self.show_frame(self.humidityFrame),
                  width=30
                  ).pack()

        self.currentIntakeEntry = (tk.Entry(self.mainFrame, width=20))
        self.currentIntakeEntry.pack(pady=(60,1))
        
        tk.Button(self.mainFrame,
                  text="Add to Water Log",
                  command=self.set_currentIntake,
                  width=30
                  ).pack()



    def create_intakeFrame(self):
        self.intakeFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.intakeFrame,
                 text="Enter your custom water intake (oz)"
                 ).pack(pady=(50,250))

        self.customIntakeEntry = tk.Entry(self.intakeFrame)
        self.customIntakeEntry.pack(pady=(0,5))
        tk.Button(self.intakeFrame,
                  text="Set custom intake",
                  command=self.set_customIntake,
                  width=20
                  ).pack(pady=0)

        tk.Button(self.intakeFrame,
                  text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=20
                  ).pack()

    def create_reminderFrame(self):
        self.reminderFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.reminderFrame, text="Choose your reminder interval below").pack(pady=(50,250))

        tk.Button(self.reminderFrame,
                  text="Every 30 min",
                  width=15,
                  command=lambda: self.updateReminderInterval(30*60)
                  ).pack()

        tk.Button(self.reminderFrame,
                  text="Every 1 hr",
                  width=15,
                  command=lambda: self.updateReminderInterval(60*60)
                  ).pack()

        tk.Button(self.reminderFrame,
                  text="Every 2 hrs",
                  width=15,
                  command=lambda: self.updateReminderInterval(2*60*60)
                  ).pack()

        tk.Button(self.reminderFrame,
                  text="Every 5 seconds (demo)",
                  width=15,
                  command=lambda: self.updateReminderInterval(5)
                  ).pack()

        self.intervalLabel = (tk.Label(self.reminderFrame, text=f"Interval is set to: {self.reminderInterval}.",
                                       bg="#ADD8E6", fg='red'))
        self.intervalLabel.pack(pady=(5,80))

        tk.Button(self.reminderFrame, text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=15
                  ).pack()
        
    

    # Lifestyle Frame
    def create_lifestyleFrame(self):
        self.lifestyleFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.lifestyleFrame, text="Activity in Daily Life", width=40).pack(pady=(50, 30))
        tk.Button(self.lifestyleFrame, text="Sedentary (e.g. desk job)", width=30, command=lambda: self.set_lifestyle("Sedentary")).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="Light (e.g. only a bit of walking)", width=30, command=lambda: self.set_lifestyle("Light")).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="Moderate (e.g. moving often)", width=30, command=lambda: self.set_lifestyle("Moderate")).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="High (e.g. physical labor)", width=30, command=lambda: self.set_lifestyle("High")).pack(pady=(0, 50))


        tk.Label(self.lifestyleFrame, text="Workout Intensity", width=40).pack(pady=(50, 30))
        tk.Button(self.lifestyleFrame, text="Light (casual or leisure activities)", width=30, command=lambda: self.set_physical_activity("Light")).pack(pady=(0,0))
        tk.Button(self.lifestyleFrame, text="Moderate (can hold a conversation)", width=30, command=lambda: self.set_physical_activity("Moderate")).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="Intense (difficulty conversing)", width=30, command=lambda: self.set_physical_activity("Intense")).pack(pady=(0, 100))

        tk.Button(self.lifestyleFrame,
                  text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=15
                  ).pack()

    
    # Humidity Frame
    def create_humidityFrame(self): #to do
        self.humidityFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.humidityFrame, text="Update Location", width=30).pack(pady=(50, 15))

        # Label and entry for City
        city_label = tk.Label(self.humidityFrame, text="Enter your current city:")
        city_label.pack(pady=5)  # Space between the label and text box

        self.city_entry = tk.Entry(self.humidityFrame)
        self.city_entry.pack(pady=5)  # Space between the text box and next widget

        # Label and entry for State
        state_label = tk.Label(self.humidityFrame, text="Enter your current state (if applicable):")
        state_label.pack(pady=5)

        self.state_entry = tk.Entry(self.humidityFrame)
        self.state_entry.pack(pady=5)

        # Label and entry for Country
        country_label = tk.Label(self.humidityFrame, text="Enter your current country:")
        country_label.pack(pady=5)

        self.country_entry = tk.Entry(self.humidityFrame)
        self.country_entry.pack(pady=5)

        submit_button = tk.Button(self.humidityFrame, text="Submit", command=self.get_location_data)
        submit_button.pack(pady=10)
                
        tk.Button(self.humidityFrame,
                  text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=20
                  ).pack()
        


# Updating stuff
    def set_customIntake(self):
        try:
            amount = int(self.customIntakeEntry.get())
            self.dailyIntake = amount
            self.customIntakeEntry.delete(0, tk.END)
            self.updateDailyIntakeLabel()
            self.updateProgressBar()
            self.show_frame(self.mainFrame)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")


    def set_currentIntake(self):
        try:
            amount = int(self.currentIntakeEntry.get())
            self.currentIntake += amount
            self.currentIntakeEntry.delete(0, tk.END)
            self.updateCurrentIntakeLabel()
            self.updateProgressBar()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def updateProgressBar(self):
        progress = min((self.currentIntake / self.dailyIntake) * 100, 100)
        self.progressBar['value'] = progress
    
    # Updating user's activity levels 
    def set_lifestyle(self, level):
        activity_levels = {"Sedentary": 0, "Light": 8, "Moderate": 12, "High": 24}
        self.lifestyle_affect = activity_levels.get(level, 0)
        self.dailyIntake = 64 + self.humidity_affect + self.activity_affect + self.lifestyle_affect
        self.updateDailyIntakeLabel()
        messagebox.showinfo("Lifestyle Set", f"Your lifestyle is set to {level}. Daily intake updated!")

    # Updating the physcial activity in settings
    def set_physical_activity(self, level):
        activity_levels = {"Light": 8, "Moderate": 12, "Intense": 16}
        self.activity_affect = activity_levels.get(level, 0)
        self.dailyIntake = 64 + self.humidity_affect + self.activity_affect + self.lifestyle_affect
        self.updateDailyIntakeLabel()
        messagebox.showinfo("Workout Activity Set", f"Your lifestyle is set to {level}. Daily intake updated!")


    def get_location_data(self):
        try:
            the_city = self.city_entry.get().strip()
            the_state = self.state_entry.get().strip()
            the_country = self.country_entry.get().strip()

            if not the_city or not the_country:
                messagebox.showwarning("Error", "City and Country are required fields.")
                return
            
            if not the_state: 
                coordinates = api_functions.verify_location_and_get_coordinates(city=the_city, country=the_country)
            else:
                coordinates = api_functions.verify_location_and_get_coordinates(city=the_city, state=the_state, country=the_country)

            if coordinates == 0: 
                messagebox.showerror("Error", "Could not verify location. Please input a valid city and country.")
                return
            else:
                latidude = coordinates[0]
                longitude = coordinates[1]

                weather_data = api_functions.convert_coordinates_to_humidity(lat=latidude, lon=longitude)

                humidity = weather_data[0]
                f_temp = weather_data[1]

                if humidity < 30 or humidity > 60:
                    self.humidity_affect = self.dailyIntake * 0.1
                    self.dailyIntake = 64 + self.activity_affect + self.humidity_affect
            messagebox.showinfo("Location Updated", "Your location has been taken into account.")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occured: {e}.")

        


#updating labels
    def updateCurrentIntakeLabel(self): # to update current intake label
        self.currentIntakelabel.config(text=f"Current Intake: {self.currentIntake} oz")

    def updateDailyIntakeLabel(self): #to update daily intake suggestion label
        self.goalLabel.config(text=f"Daily Water Intake Goal: {self.dailyIntake} oz")


# reminder stuff
    def updateReminderInterval(self, interval):
        self.reminderInterval = int(interval * 1000) #converted to milliseconds
        if self.afterID is not None:
            self.root.after_cancel(self.afterID)
            self.afterID = None
            self.afterID = self.root.after(self.reminderInterval, self.set_reminder)
            self.intervalLabel.config(text=f"Interval has changed to: {self.reminderInterval}.")
            print("Reminder Interval is", self.reminderInterval)

    def set_reminder(self):
        self.afterID = self.root.after(self.reminderInterval, self.sendReminder)

    def sendReminder(self):
        reminder = ["Time to drink water and you know it",
                    "Sipping water like a pro",
                    "Stay hydrated, stay healthy",
                    "Hydration leads to healthy skin glow",
                    "Water is the best way to quench your thirst",
                    "Hydrate, Refresh, Repeat",
                    "Keep it cool, stay hydrated",
                    "Hydration is key to better health",
                    "Drink Water, feel better"]

        print('reminder sent')
        messagebox.showinfo("Reminder", reminder[random.randint(0, len(reminder)-1)])
        self.set_reminder()

if __name__ == "__main__":
    root = tk.Tk()
    app = HydrationApp(root)
    root.mainloop()
