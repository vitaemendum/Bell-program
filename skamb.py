import datetime
import time
import os
import winsound
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Sound:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

NORMAL_TIMES = [
    Sound(8, 0), Sound(8, 45), Sound(8, 50), Sound(9, 35), Sound(9, 45), Sound(10, 30),
    Sound(10, 35), Sound(11, 20), Sound(12, 0), Sound(12, 45), Sound(12, 50), Sound(13, 35),
    Sound(13, 45), Sound(14, 30), Sound(14, 35), Sound(15, 20), Sound(15, 30), Sound(16, 15)
]

SHORTENED_TIMES = [
    Sound(8, 0), Sound(8, 30), Sound(8, 35), Sound(9, 5), Sound(9, 10), Sound(9, 40),
    Sound(9, 45), Sound(10, 15), Sound(10, 20), Sound(10, 37), Sound(10, 55), Sound(11, 25),
    Sound(11, 30), Sound(12, 0)
]

class BellScheduler:
    def __init__(self, master):
        self.master = master
        self.master.title("Lesson Times Selection")
        self.master.geometry('300x450')

        self.bell_sound_file = None
        
        # create radio buttons for lesson times selection
        self.lesson_times = {
            "Monday": NORMAL_TIMES,
            "Tuesday": NORMAL_TIMES,
            "Wednesday": NORMAL_TIMES,
            "Thursday": NORMAL_TIMES,
            "Friday": NORMAL_TIMES
        }
        
        self.labels = {}
        self.radio_buttons = {}
        
        for i, day in enumerate(self.lesson_times.keys()):
            label = Label(self.master, text=day)
            label.grid(row=i, column=0, padx=10, pady=10)
            self.labels[day] = label
            
            var = StringVar()
            rb1 = Radiobutton(self.master, text="Normal", variable=var, value="Normal", command=lambda day=day: self.set_lesson_times(day, var.get()))
            rb1.grid(row=i, column=1, padx=10, pady=10)
            rb2 = Radiobutton(self.master, text="Shortened", variable=var, value="Shortened", command=lambda day=day: self.set_lesson_times(day, var.get()))
            rb2.grid(row=i, column=2, padx=10, pady=10)
            self.radio_buttons[day] = (rb1, rb2)
        
        # create button to start the schedule
        self.uploud_button = Button(self.master, text="Uploud sound", command=self.choose_sound_file)
        self.uploud_button.grid(row=len(self.lesson_times), column=1, pady=10)
        
        self.file_name_label = Label(self.master, text="default: bell.wav")
        self.file_name_label.grid(row=len(self.lesson_times)+1, column=1, pady=10)
        
        # create button to start the schedule
        self.start_button = Button(self.master, text="Start Schedule", command=self.start_scheduler)
        self.start_button.grid(row=len(self.lesson_times)+2, column=1, pady=10)

        # create button to start the schedule
        self.stop_button = Button(self.master, text="Stop Schedule", command=self.stop_scheduler)
        self.stop_button.grid(row=len(self.lesson_times)+3, column=1, pady=10)
        
        self.scheduler_running = False
        self.sheduler_thread = None
        
    def play_bell_sound(self, sound_file):
        """Play the specified bell sound file or the default bell sound if sound_file is None."""
        if sound_file is None:
            sound_file = "bell.wav"
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
        
    def set_lesson_times(self, day, selection):
        if selection == "Normal":
            self.lesson_times[day] = NORMAL_TIMES
        elif selection == "Shortened":
            self.lesson_times[day] = SHORTENED_TIMES
    
    def choose_sound_file(self):
        """Open a file dialog to choose a sound file and update the file name label."""
        file_path = filedialog.askopenfilename()
        if file_path:
            # Set the text of the file name label to the selected file name
            file_name = os.path.basename(file_path)
            self.file_name_label.config(text=f"Selected file: {file_name}")
            self.bell_sound_file = file_path
        else:
            self.file_name_label.config(text=f"Selected file: bell.wav")
            self.bell_sound_file = "bell.wav"

    def start_scheduler(self):
        """Start the bell scheduler."""
        if not self.scheduler_running:
            self.scheduler_running = True
            self.start_button.config(state=DISABLED)
            self.uploud_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)
            for rb in self.radio_buttons.values():
                rb[0].config(state=DISABLED)
                rb[1].config(state=DISABLED)
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.start()
        else:
            print("Scheduler is already running.")

    def stop_scheduler(self):
        """Stop the bell scheduler."""
        if self.scheduler_running:
            self.scheduler_running = False
            self.start_button.config(state=NORMAL)
            self.uploud_button.config(state=NORMAL)
            for rb in self.radio_buttons.values():
                rb[0].config(state=NORMAL)
                rb[1].config(state=NORMAL)
        else:
            messagebox.showerror("Error", "Scheduler is not running!")
        
    def run_scheduler(self):
        """Check the current time and play the bell sound if there is a match."""
        while self.scheduler_running:
            now = datetime.datetime.now()
            day = now.strftime("%A")
            lesson_times = self.lesson_times[day]
            if lesson_times:
                for lesson_time in lesson_times:
                    if now.hour == lesson_time.hour and now.minute == lesson_time.minute:
                        self.play_bell_sound(self.bell_sound_file)
                        break
            time.sleep(60)


root = Tk()
bell_scheduler = BellScheduler(root)
root.mainloop()