import customtkinter as ctk
from tkinter import filedialog, messagebox
from music21 import stream, note, chord, instrument
import random
import pygame
import os

# --------------- Basic Setup ---------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎵 AI Music Generator (Simple Version)")
app.geometry("650x480")

# Initialize pygame mixer
try:
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

generated_file = "generated_music/simple_song.mid"

# --------------- Functions ---------------

def generate_music():
    """Generate random notes using rule-based pseudo-AI."""
    safe_folder = "generated_music"
    os.makedirs(safe_folder, exist_ok=True)

    scales = ["C", "D", "E", "F", "G", "A", "B"]
    octaves = [3, 4, 5]
    durations = [0.25, 0.5, 1.0]
    output_notes = []

    for i in range(60):
        if random.random() < 0.25:
            # Create chord (3 random notes)
            notes_in_chord = random.sample(scales, 3)
            chord_notes = [note.Note(n + str(random.choice(octaves))) for n in notes_in_chord]
            new_chord = chord.Chord(chord_notes)
            new_chord.offset = i * 0.5
            new_chord.storedInstrument = instrument.Piano()
            output_notes.append(new_chord)
        else:
            n = note.Note(random.choice(scales) + str(random.choice(octaves)))
            n.offset = i * 0.5
            n.quarterLength = random.choice(durations)
            n.storedInstrument = instrument.Piano()
            output_notes.append(n)

    midi_stream = stream.Stream(output_notes)
    midi_stream.write("midi", fp=generated_file)
    messagebox.showinfo("✅ Success", f"Music generated and saved as:\n{generated_file}")

def play_music():
    """Play the generated song"""
    if not os.path.exists(generated_file):
        messagebox.showerror("Error", "Please generate music first!")
        return
    if not AUDIO_AVAILABLE:
        messagebox.showerror("Error", "Audio device not available.")
        return
    pygame.mixer.music.load(generated_file)
    pygame.mixer.music.play()
    status_label.configure(text="🎧 Playing music...")

def stop_music():
    if AUDIO_AVAILABLE:
        pygame.mixer.music.stop()
    status_label.configure(text="⏹️ Music stopped")

# --------------- UI Layout ---------------

title_label = ctk.CTkLabel(app, text="🎶 AI Music Generator (Rule-Based)", font=("Arial Rounded MT Bold", 24))
title_label.pack(pady=20)

generate_btn = ctk.CTkButton(app, text="🎹 Generate Music", width=200, height=40, command=generate_music)
generate_btn.pack(pady=10)

play_btn = ctk.CTkButton(app, text="▶️ Play Music", width=200, height=40, command=play_music)
play_btn.pack(pady=10)

stop_btn = ctk.CTkButton(app, text="⏹️ Stop Music", width=200, height=40, command=stop_music)
stop_btn.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Welcome to AI Music Generator", text_color="lightblue", font=("Arial", 14))
status_label.pack(pady=15)

footer = ctk.CTkLabel(app, text="Made with ❤️ by Mala | Simplified AI Logic", font=("Arial", 12))
footer.pack(side="bottom", pady=10)

app.mainloop()
