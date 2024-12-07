import tkinter as tk
from tkinter import messagebox


class HydrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydration App")
        self.root.geometry("400x600")

        # Water variables
        self.dailyIntake = 64  # oz
        self.currentIntake = 0
        self.reminderInterval = 60*60*1000 #default is 1hr in milliseconds

        # Init screens
        self.mainFrame = None
        self.intakeFrame = None
        self.reminderFrame = None

        #init label
        self.goalLabel = None
        self.currentIntakeLabel = None
        self.intervalLabel = None

        # Creating the screens
        self.create_mainFrame()
        self.create_intakeFrame()
        self.create_reminderFrame()


        self.show_frame(self.mainFrame)

        #starting reminder function
        #self.set_reminder()


    def show_frame(self, frame):
        if frame == self.mainFrame: #disable when returning to main
            self.customIntakeEntry.unbind("<Return>")

        if frame == self.intakeFrame: #allow use of return button on intake frame
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

        #buttons
        tk.Button(self.mainFrame, text="Set Custom Water Intake",
                  command=lambda: self.show_frame(self.intakeFrame),
                  width=20
                  ).pack(pady=(200,0))

        tk.Button(self.mainFrame, text="Change Reminder Interval",
                  command=lambda: self.show_frame(self.reminderFrame),
                  width=20
                  ).pack()

    def create_intakeFrame(self):
        self.intakeFrame = tk.Frame(self.root, bg="#ADD8E6")
        tk.Label(self.intakeFrame,
                 text="Enter your custom water intake (oz)"
                 ).pack(pady=(50,250))

        self.customIntakeEntry = tk.Entry(self.intakeFrame)
        self.customIntakeEntry.pack(pady=(0,5))

        self.customIntakeEntry.bind("<Return>", lambda event: self.set_customIntake()) #allows use of enter button
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
                  text="Every 10 seconds (demo)",
                  width=15,
                  command=lambda: self.updateReminderInterval(10)
                  ).pack()

        self.intervalLabel = (tk.Label(self.reminderFrame, text=f"Interval is set to: {self.reminderInterval}.",
                                       bg="#ADD8E6", fg='red'))
        self.intervalLabel.pack(pady=(5,80))

        tk.Button(self.reminderFrame, text="Return to main menu",
                  command=lambda: self.show_frame(self.mainFrame),
                  width=15
                  ).pack()


    def set_customIntake(self):
        try:
            amount = int(self.customIntakeEntry.get())
            self.dailyIntake = amount
            self.customIntakeEntry.delete(0, tk.END)
            self.updateDailyIntakeLabel()
            self.show_frame(self.mainFrame)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def updateDailyIntakeLabel(self): #to update daily intake suggestion label
        self.goalLabel.config(text=f"Daily Water Intake Goal: {self.dailyIntake} oz")

    def updateReminderInterval(self, interval):
        self.reminderInterval = int(interval * 1000) #converted to milliseconds
        self.intervalLabel.config(text=f"Interval has changed to: {self.reminderInterval}.")
        print("Reminder Interval is", self.reminderInterval)

    def set_reminder(self):
        reminder = "Time to drink water"
        messagebox.showinfo("Reminder", reminder)
        print('reminder sent')
        self.root.after(self.reminderInterval, self.set_reminder)

if __name__ == "__main__":
    root = tk.Tk()
    app = HydrationApp(root)
    root.mainloop()
