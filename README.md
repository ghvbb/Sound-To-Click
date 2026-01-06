# SoundToClick - Translator & TTS App

A powerful Translator and Text-to-Speech application supporting 20+ languages.
Built by **ghvbb**. Support the Omarchy Community.

## Features
- **GUI & TUI Modes**
- **Online (Google Translate) & Offline (espeak/pyttsx3) support**
- **Output formats:** .mp3, .wav, .mp4
- **20+ Languages:** Arabic, English, French, German, Dutch, British English, etc.

## 1. System Requirements

Before running the Python script, install the system-level dependencies for audio and GUI support.

### Arch Linux / Manjaro (pacman & yay)
```bash
sudo pacman -S python python-pip tk espeak-ng ffmpeg
# If using yay
yay -S python-gtts python-pyttsx3
```
### Fedora / Nobara (dnf)

```bash
sudo dnf install python3 python3-pip python3-tkinter espeak-ng ffmpeg
```

### Debian / Ubuntu (apt)

```bash
sudo apt install python3 python3-pip python3-tk espeak-ng ffmpeg
```

### Void Linux (xbps)

```bash
sudo xbps-install -S python3 python3-pip tk espeak-ng ffmpeg
```

### Pip Install
```bash
pip install deep-translator gTTS pyttsx3 arabic-reshaper python-bidi python-vlc --break-system-packages
```

# Installation 
- Save the python code as main.py.

- Save the bash code as install.sh.

- Make the installer executable and run it:
```bash
chmod +x install.sh
./install.sh
```


By : ghvbb on github

Love You (: 
