import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils import preprocess_audio, transcribe

audio_file_path = None  # Global variable to store file path

def browse_audio():
    global audio_file_path
    audio_file_path = filedialog.askopenfilename(
        title="Choose Audio File",
        filetypes=(("WAV Audio", ".wav"), ("All Files", ".*"))
    )
    if audio_file_path:
        file_label = os.path.basename(audio_file_path)
        status_display.config(text=f"✔ Selected: {file_label}", fg="#0066cc")

        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.config(state='disabled')

def convert_audio_to_text():
    global audio_file_path
    if not audio_file_path:
        messagebox.showwarning("File Missing", "Please select a WAV file to proceed.")
        return
    try:
        status_display.config(text="🔁 Processing...", fg="#555")
        root.update()

        prepared_file = preprocess_audio(audio_file_path)
        transcription_result = transcribe(prepared_file)

        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, transcription_result)
        output_text.config(state='disabled')

        status_display.config(text="✅ Transcription Done.", fg="green")
    except Exception as err:
        messagebox.showerror("Transcription Error", str(err))
        status_display.config(text="❌ Error occurred during transcription.", fg="red")

# ---------- GUI Configuration ----------
root = tk.Tk()
root.title("🧠 Voice to Text AI Tool")
root.geometry("720x540")
root.configure(bg="#f0f0f0")

# Heading
heading = tk.Label(root, text="AI-Powered Voice Transcriber", font=("Calibri", 20, "bold"), bg="#f0f0f0", fg="#222")
heading.pack(pady=(25, 10))

# Content Frame
container = tk.Frame(root, bg="#f0f0f0")
container.pack(padx=25, pady=10, fill="both", expand=True)

# Upload Button
upload_button = tk.Button(
    container, text="🎵 Select WAV File", command=browse_audio,
    font=("Calibri", 13), bg="#1976D2", fg="white",
    activebackground="#1565C0", padx=12, pady=6, relief="flat", cursor="hand2"
)
upload_button.pack(pady=6)

# Transcription Button
transcribe_button = tk.Button(
    container, text="📄 Generate Text", command=convert_audio_to_text,
    font=("Calibri", 13), bg="#388E3C", fg="white",
    activebackground="#2E7D32", padx=12, pady=6, relief="flat", cursor="hand2"
)
transcribe_button.pack(pady=6)

# Output Text Box
output_text = tk.Text(container, wrap="word", height=12, font=("Calibri", 12), padx=12, pady=12, relief="sunken", bd=1)
output_text.pack(fill="both", expand=True, padx=10, pady=10)
output_text.config(state='disabled')

# Status Area
status_display = tk.Label(root, text="", font=("Calibri", 10), bg="#f0f0f0", fg="blue")
status_display.pack(pady=5)

# Credits
footer_note = tk.Label(root, text="Developed by Atul Kumar", font=("Calibri", 9), bg="#f0f0f0", fg="gray")
footer_note.pack(side="bottom", pady=12)

# Main loop
root.mainloop()
