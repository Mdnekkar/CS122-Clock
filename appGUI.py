import tkinter as tk
from tkinter import messagebox

class HydrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydration App")
        self.root.geometry("400x600")
        self.root.configure(bg="#ADD8E6")
        self.default_Intake = 64 #in oz
        self.daily_Intake = self.default_Intake
        self.water_Intake = 0
        self.humidity = 0
        self.create_widgets()

    def create_widgets(self):
        #daily Intake display
        self.intake_label = tk.Label(self.root,
                                     text=f"Water Intake Goal: {self.daily_Intake} oz",
                                     fg="black",
                                     bg="#ADD8E6",
                                     font=("Arial", 20)
                                     )
        self.intake_label.pack(pady=(20,10))

        #water intake Entry and button
        self.water_entry = tk.Entry(self.root)
        self.water_entry.pack(pady=(10,5))
        tk.Button(self.root, text="Add Water Intake",
                  command=self.add_Water_Intake
                  ).pack(pady=(5,20))

        #Display current water intake
        self.progress_label = tk.Label(self.root,
                                       text=f"Current Intake: {self.water_Intake} oz",
                                       fg="black",
                                       bg="#ADD8E6",
                                       font=("Arial", 20)
                                       )
        self.progress_label.pack(pady=(10, 20))

    def add_Water_Intake(self):
        try:
            amount = int(self.water_entry.get())
            self.water_Intake += amount
            self.progress_label.config(text=f"Current Intake {self.water_Intake} oz")
            self.water_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")


    def set_intake(self):
        pass

    def get_humidity(self):
        pass

    def get_activity(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = HydrationApp(root)
    root.mainloop()