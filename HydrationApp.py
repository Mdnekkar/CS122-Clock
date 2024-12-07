import random
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class HydrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydration App")
        self.root.geometry("450x650")

        # Water variables
        self.dailyIntake = 64  # oz
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
                  width=20
                  ).pack(pady=(20,0))

        tk.Button(self.mainFrame, text="Change Reminder Interval",
                  command=lambda: self.show_frame(self.reminderFrame),
                  width=20
                  ).pack()

        tk.Button(self.mainFrame,
                  text="Lifestyle / Activity Settings",
                  command=lambda: self.show_frame(self.lifestyleFrame),
                  width=20
                  ).pack()

        tk.Button(self.mainFrame,
                  text="Humidity Stuff",
                  command=lambda: self.show_frame(self.humidityFrame),
                  width=20
                  ).pack()

        self.currentIntakeEntry = (tk.Entry(self.mainFrame, width=20))
        self.currentIntakeEntry.pack(pady=(60,1))
        tk.Button(self.mainFrame,
                  text="Add to Water Log",
                  command=self.set_currentIntake,
                  width=20
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

    def create_lifestyleFrame(self): #to do
        self.lifestyleFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.lifestyleFrame, text="Lifestyle settings", width=10).pack(pady=(50, 30))
        tk.Button(self.lifestyleFrame, text="Sedentary", width=10).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="Light", width=10).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="Moderate", width=10).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="High", width=10).pack(pady=(0, 50))



        tk.Label(self.lifestyleFrame, text="Physical Activity", width=10).pack(pady=(50, 10))
        tk.Button(self.lifestyleFrame, text="Cardio", width=10).pack(pady=(0,0))
        tk.Button(self.lifestyleFrame, text="Sports", width=10).pack(pady=(0, 0))
        tk.Button(self.lifestyleFrame, text="Weight Lifting", width=10).pack(pady=(0, 100))
        tk.Button()


        tk.Button(self.lifestyleFrame,
                  text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=15
                  ).pack()


    def create_humidityFrame(self): #to do
        self.humidityFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.humidityFrame, text="humidity frame").pack(pady=(50, 250))

        tk.Button(self.humidityFrame,
                  text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=20
                  ).pack()

#updating stuff

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
