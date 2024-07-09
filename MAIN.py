import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np

class DualVideoPlayer:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

        # Ratine video
        self.ratine_label = ttk.Label(root)
        self.ratine_label.grid(row=0, column=0, padx=10, pady=10)
        self.ratine_cap = None
        self.ratine_playing = False
        self.ratine_start_frame = 0

        # WebCam video
        self.webcam_label = ttk.Label(root)
        self.webcam_label.grid(row=0, column=1, padx=10, pady=10)
        self.webcam_cap = None
        self.webcam_playing = False
        self.webcam_start_frame = 0

        black_frame = np.zeros((320, 640, 3), dtype=np.uint8)
        black_frame_img = Image.fromarray(black_frame)
        black_frame_imgtk = ImageTk.PhotoImage(image=black_frame_img)
        self.ratine_label.imgtk = black_frame_imgtk
        self.ratine_label.configure(image=black_frame_imgtk)
        self.webcam_label.imgtk = black_frame_imgtk
        self.webcam_label.configure(image=black_frame_imgtk)


    def load_ratine_video(self, file_path, start_frame=0):
        self.ratine_cap = cv2.VideoCapture(file_path)
        self.ratine_start_frame = start_frame
        if self.ratine_cap.isOpened():
            self.ratine_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    def load_webcam_video(self, file_path, start_frame=0):
        self.webcam_cap = cv2.VideoCapture(file_path)
        self.webcam_start_frame = start_frame
        if self.webcam_cap.isOpened():
            self.webcam_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    def update_frames(self):
        if self.ratine_playing and self.ratine_cap:
            ret, frame = self.ratine_cap.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.ratine_label.imgtk = imgtk
                self.ratine_label.configure(image=imgtk)
            else:
                self.ratine_cap.set(cv2.CAP_PROP_POS_FRAMES, self.ratine_start_frame)

        if self.webcam_playing and self.webcam_cap:
            ret, frame = self.webcam_cap.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)
            else:
                self.webcam_cap.set(cv2.CAP_PROP_POS_FRAMES, self.webcam_start_frame)

        self.root.after(20, self.update_frames)

    def play(self):
        self.ratine_playing = True
        self.webcam_playing = True

    def pause(self):
        self.ratine_playing = False
        self.webcam_playing = False

    def release(self):
        if self.ratine_cap:
            self.ratine_cap.release()
        if self.webcam_cap:
            self.webcam_cap.release()

def load_ratine_video(player, start_frame_entry):
    file_path = filedialog.askopenfilename(title="Select Ratine Video")
    start_frame = int(start_frame_entry.get())
    if file_path:
        player.load_ratine_video(file_path, start_frame)

def load_webcam_video(player, start_frame_entry):
    file_path = filedialog.askopenfilename(title="Select WebCam Video")
    start_frame = int(start_frame_entry.get())
    if file_path:
        player.load_webcam_video(file_path, start_frame)

def main():
    root = tk.Tk()
    root.title("Dual Video Player")

    width, height = 640, 320  # Desired size of video display area

    player = DualVideoPlayer(root, width, height)

    # Ratine controls
    ratine_frame = ttk.Frame(root)
    ratine_frame.grid(row=1, column=0, padx=10, pady=10)
    
    ratine_start_frame = ttk.Entry(ratine_frame)
    ratine_start_frame.grid(row=0, column=1, padx=5, pady=5)
    ratine_start_frame.insert(0, "0")

    ratine_start_label = ttk.Label(ratine_frame, text="Start frame:")
    ratine_start_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    load_ratine_button = ttk.Button(ratine_frame, text="Load Ratine Video", command=lambda: load_ratine_video(player, ratine_start_frame))
    load_ratine_button.grid(row=1, column=1, padx=5, pady=5, sticky="W")

    # WebCam controls
    webcam_frame = ttk.Frame(root)
    webcam_frame.grid(row=1, column=1, padx=10, pady=10)

    webcam_start_frame = ttk.Entry(webcam_frame)
    webcam_start_frame.grid(row=0, column=1, padx=5, pady=5)
    webcam_start_frame.insert(0, "0")
    
    webcam_start_label = ttk.Label(webcam_frame, text="Start frame:")
    webcam_start_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")
    
    load_webcam_button = ttk.Button(webcam_frame, text="Load WebCam Video", command=lambda: load_webcam_video(player, webcam_start_frame))
    load_webcam_button.grid(row=1, column=1, padx=5, pady=5, sticky="W")

    # Play/Pause controls
    control_frame = ttk.Frame(root)
    control_frame.grid(row=2, column=0, columnspan=2, pady=10)

    play_button = ttk.Button(control_frame, text="Play", command=player.play)
    play_button.grid(row=0, column=0, padx=5)

    pause_button = ttk.Button(control_frame, text="Pause", command=player.pause)
    pause_button.grid(row=0, column=1, padx=5)

    def on_closing():
        player.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    player.update_frames()

    root.mainloop()

if __name__ == "__main__":
    main()
