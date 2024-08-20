import os
import pygame
import tkinter as tk
from tkinter import filedialog, Listbox, END
from mutagen.mp3 import MP3
from threading import Thread

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Player")
        self.root.geometry("500x400")

        pygame.mixer.init()

        self.current_song = None
        self.is_paused = False
        self.playlist = []

        self.create_widgets()

    def create_widgets(self):
        self.song_listbox = Listbox(self.root, selectmode=tk.SINGLE, width=50, height=15)
        self.song_listbox.pack(pady=20)

        controls_frame = tk.Frame(self.root)
        controls_frame.pack()

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=10)

        self.prev_button = tk.Button(controls_frame, text="Prev", command=self.prev_song)
        self.prev_button.grid(row=0, column=3, padx=10)

        self.next_button = tk.Button(controls_frame, text="Next", command=self.next_song)
        self.next_button.grid(row=0, column=4, padx=10)

        self.add_button = tk.Button(self.root, text="Add Songs", command=self.add_songs)
        self.add_button.pack(pady=20)

    def play_music(self):
        if self.current_song is None:
            self.select_song(0)
        if not self.is_paused:
            pygame.mixer.music.load(self.playlist[self.current_song])
            pygame.mixer.music.play(loops=0)
        else:
            pygame.mixer.music.unpause()
        self.is_paused = False

    def pause_music(self):
        if not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_paused = False

    def next_song(self):
        self.select_song((self.current_song + 1) % len(self.playlist))

    def prev_song(self):
        self.select_song((self.current_song - 1) % len(self.playlist))

    def select_song(self, index):
        if index >= 0 and index < len(self.playlist):
            self.current_song = index
            self.song_listbox.selection_clear(0, END)
            self.song_listbox.selection_set(self.current_song)
            self.play_music()

    def add_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for file in files:
            self.playlist.append(file)
            song_name = os.path.basename(file)
            self.song_listbox.insert(END, song_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
