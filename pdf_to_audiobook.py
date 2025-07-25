import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pyttsx3
from gtts import gTTS
import os
import tempfile
import threading

class PDFToAudiobookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Audiobook Converter")
        self.engine = pyttsx3.init()
        self.text = ""
        self._build_gui()

    def _build_gui(self):
        tk.Label(self.root, text="PDF to Audiobook", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Button(self.root, text="Load PDF", command=self.load_pdf).pack(pady=5)
        tk.Button(self.root, text="Play Audio", command=self.play_audio).pack(pady=5)
        tk.Button(self.root, text="Export MP3", command=self.export_audio).pack(pady=5)

        # Volume Control
        tk.Label(self.root, text="Volume").pack()
        self.volume_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.volume_slider.set(70)
        self.volume_slider.pack()

        # Rate Control
        tk.Label(self.root, text="Speed").pack()
        self.rate_slider = tk.Scale(self.root, from_=100, to=300, orient=tk.HORIZONTAL)
        self.rate_slider.set(150)
        self.rate_slider.pack()

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.text = self.extract_text(file_path)
            if not self.text.strip():
                messagebox.showwarning("Empty PDF", "No readable text found in this PDF.")
            else:
                messagebox.showinfo("Success", "PDF loaded and text extracted!")

    def extract_text(self, path):
        doc = fitz.open(path)
        all_text = ""
        for page in doc:
            text = page.get_text().strip()
            if text:
                all_text += text + "\n"
        return all_text

    def play_audio(self):
        if not self.text:
            messagebox.showerror("No Text", "Please load a PDF first.")
            return

        def run_speech():
            self.engine.setProperty('volume', self.volume_slider.get() / 100)
            self.engine.setProperty('rate', self.rate_slider.get())
            self.engine.say(self.text)
            self.engine.runAndWait()

        threading.Thread(target=run_speech).start()

    def export_audio(self):
        if not self.text:
            messagebox.showerror("No Text", "Please load a PDF first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                 filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            try:
                tts = gTTS(self.text)
                tts.save(save_path)
                messagebox.showinfo("Success", f"Audio saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudiobookApp(root)
    root.mainloop()
