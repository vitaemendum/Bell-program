import time
import os
import winsound
import threading
from tkinter import *
from tkinter import filedialog

class Sound:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

NORMAL_TIMES = [
    Sound(8, 0), Sound(8, 45), Sound(8, 50), Sound(9, 35), Sound(9, 45), Sound(10, 30),
    Sound(10, 35), Sound(11, 20), Sound(12, 0), Sound(12, 45), Sound(12, 50), Sound(13, 35),
    Sound(13, 45), Sound(14, 4), Sound(14, 35), Sound(15, 20), Sound(15, 30), Sound(16, 15)
]

SHORTENED_TIMES = [
    Sound(8, 0), Sound(8, 30), Sound(8, 35), Sound(9, 5), Sound(9, 10), Sound(9, 40),
    Sound(9, 45), Sound(10, 15), Sound(10, 20), Sound(10, 50), Sound(10, 55), Sound(11, 25),
    Sound(11, 30), Sound(12, 0)
]

class BellScheduler:
    def __init__(self, master):
        self.master = master
        self.master.title("Lesson Times Selection")
        self.master.geometry('400x300')

        self.bell_sound_file = "bell.wav"
        
        # create radio buttons for lesson times selection
        self.lesson_times = NORMAL_TIMES
        self.var = StringVar(value="normal")
        Radiobutton(self.master, text="Netrumpintos (45 min.)", variable=self.var, value="normal", command=self.set_lesson_times).pack(anchor=W)
        Radiobutton(self.master, text="Trumpintos (30 min.)", variable=self.var, value="shortened", command=self.set_lesson_times).pack(anchor=W)
        
        self.upload_button = Button(self.master, text="Upload Sound", command=self.choose_sound_file)
        self.upload_button.pack()
        self.file_name_label = Label(self.master, text="", font=("Arial", 10))
        self.file_name_label.pack()
        
        self.start_button = Button(self.master, text="Start Bell Scheduler", command=self.start_scheduler)
        self.start_button.pack()
        
        self.stop_button = Button(self.master, text="Stop Bell Scheduler", command=self.stop_scheduler, state=DISABLED)
        self.stop_button.pack()
        
        self.scheduler_running = False
        self.sheduler_thread = None
        
    def play_bell_sound(self,sound_file):
        """Play the specified bell sound file."""
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    def set_lesson_times(self):
        """Set the lesson times based on the selected radio button."""
        if self.var.get() == "normal":
            self.lesson_times = NORMAL_TIMES
        else:
            self.lesson_times = SHORTENED_TIMES

    def choose_sound_file(self):
        """Open a file dialog to choose a sound file and update the file name label."""
        file_path = filedialog.askopenfilename()
        if file_path:
            # Disable the upload button and change the text color to gray
            self.upload_button.config(state=DISABLED, foreground='gray')
            # Set the text of the file name label to the selected file name
            file_name = os.path.basename(file_path)
            self.file_name_label.config(text=f"Selected file: {file_name}")
            self.bell_sound_file = file_path
        else:
            self.upload_button.config(state=DISABLED, foreground='gray')
            self.file_name_label.config(text=f"Selected file: bell.wav")
            self.bell_sound_file = "bell.wav"

    def start_scheduler(self):
        """Start the bell scheduler."""
        if not self.scheduler_running:
            self.scheduler_running = True
            self.start_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.start()
        else:
            print("Scheduler is already running.")

    def stop_scheduler(self):
        """Stop the bell scheduler."""
        if self.scheduler_running:
            self.scheduler_running = False
            self.scheduler_thread.join()
            self.scheduler_thread = None
            self.stop_button.config(state=DISABLED)
            self.start_button.config(state=NORMAL)
            self.upload_button(state=NORMAL)
        else:
            print("Scheduler is not running.")

    def run_scheduler(self):
        """Run the bell scheduler in a separate thread."""
        while self.scheduler_running:
            current_time = time.localtime()
            for sound in self.lesson_times:
                if current_time.tm_hour == sound.hour and current_time.tm_min == sound.minute:
                    self.play_bell_sound(self.bell_sound_file)
                    time.sleep(30) # wait 30 second between each sound

root = Tk()
bell_scheduler = BellScheduler(root)
root.mainloop()