import sys
import os
import threading
from tkinter import Tk, Text, Button, ttk, messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyttsx3
import arabic_reshaper
from bidi.algorithm import get_display

LANG_MAP = {
    "English": "en",
    "Arabic": "ar",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Portuguese": "pt",
    "Turkish": "tr",
    "Chinese": "zh-cn"
}

class TranslatorEngine:
    def translate(self, text, src, dest):
        return GoogleTranslator(source=src, target=dest).translate(text)

class SpeechEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 145)
        except Exception:
            self.engine = None

    def generate(self, text, lang, mode, path):
        if mode == "Online":
            gTTS(text=text, lang=lang).save(path)
            return
        if mode == "Offline" and self.engine:
            self.engine.save_to_file(text, path)
            self.engine.runAndWait()
            return
        raise RuntimeError("Speech engine unavailable")

    def play(self, path):
        if not path or not os.path.exists(path):
            raise RuntimeError("Audio not found")
        if sys.platform.startswith("linux"):
            os.system(f"xdg-open '{path}'")
        elif sys.platform == "darwin":
            os.system(f"open '{path}'")
        else:
            os.system(f'start "" "{path}"')

class SoundToClickApp:
    def __init__(self):
        self.translator = TranslatorEngine()
        self.speaker = SpeechEngine()
        self.save_dir = os.path.expanduser("~/sounds")
        os.makedirs(self.save_dir, exist_ok=True)
        self.last_audio = None

    def fix_arabic(self, text, lang):
        if lang != "ar":
            return text
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def process(self, text, src, dest, mode):
        translated = self.translator.translate(text, src, dest)
        fixed = self.fix_arabic(translated, dest)
        path = os.path.join(self.save_dir, "sound.mp3")
        self.speaker.generate(translated, dest, mode, path)
        self.last_audio = path
        return fixed

    def gui_mode(self):
        root = Tk()
        root.title("SoundToClick")
        root.geometry("560x640")
        root.configure(bg="#1e1e1e")
        root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TCombobox", padding=4)

        ttk.Label(root, text="Input Text").pack(pady=(20, 6))
        input_box = Text(root, height=5, width=52, bg="#2a2a2a", fg="white", insertbackground="white", relief="flat")
        input_box.pack()

        frame_lang = ttk.Frame(root)
        frame_lang.pack(pady=14)

        ttk.Label(frame_lang, text="From").grid(row=0, column=0, padx=6)
        src_box = ttk.Combobox(frame_lang, values=list(LANG_MAP.keys()), state="readonly", width=18)
        src_box.set("English")
        src_box.grid(row=0, column=1, padx=6)

        ttk.Label(frame_lang, text="To").grid(row=0, column=2, padx=6)
        dest_box = ttk.Combobox(frame_lang, values=list(LANG_MAP.keys()), state="readonly", width=18)
        dest_box.set("Arabic")
        dest_box.grid(row=0, column=3, padx=6)

        ttk.Label(root, text="Mode").pack(pady=(10, 6))
        mode_box = ttk.Combobox(root, values=["Online", "Offline"], state="readonly", width=48)
        mode_box.set("Online")
        mode_box.pack()

        ttk.Label(root, text="Translated Text").pack(pady=(16, 6))
        result_box = Text(root, height=5, width=52, bg="#252525", fg="white", relief="flat", state="disabled")
        result_box.pack()

        status = ttk.Label(root, text="")
        status.pack(pady=10)

        def run_task():
            try:
                text = input_box.get("1.0", "end").strip()
                if not text:
                    raise RuntimeError("Empty text")
                src = LANG_MAP[src_box.get()]
                dest = LANG_MAP[dest_box.get()]
                mode = mode_box.get()
                translated = self.process(text, src, dest, mode)

                result_box.config(state="normal")
                result_box.delete("1.0", "end")
                result_box.insert("1.0", translated)
                result_box.config(state="disabled")

                status.config(text="Audio generated successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                translate_btn.config(state="normal")
                play_btn.config(state="normal")

        def translate():
            translate_btn.config(state="disabled")
            play_btn.config(state="disabled")
            status.config(text="Processing...")
            threading.Thread(target=run_task, daemon=True).start()

        def play_audio():
            try:
                self.speaker.play(self.last_audio)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        translate_btn = Button(root, text="Translate and Generate Voice", command=translate, bg="#3a7afe", fg="white", relief="flat", width=28)
        translate_btn.pack(pady=(22, 10))

        play_btn = Button(root, text="Play Sound", command=play_audio, bg="#2e2e2e", fg="white", relief="flat", width=28)
        play_btn.pack()

        root.mainloop()

    def tui_mode(self):
        while True:
            os.system("clear")
            text = input("Text: ").strip()
            if not text:
                break
            src = input("From language code: ").strip()
            dest = input("To language code: ").strip()
            mode = input("Mode Online or Offline: ").strip().capitalize()
            try:
                translated = self.process(text, src, dest, mode)
                print(translated)
                print(self.last_audio)
            except Exception as e:
                print(e)
            if "no" in input("Again yes or no: ").lower():
                break

if __name__ == "__main__":
    app = SoundToClickApp()
    if len(sys.argv) > 1 and sys.argv[1] == "--tui":
        app.tui_mode()
    else:
        app.gui_mode()

