#!/bin/bash

APP_NAME="SoundToClick"
INSTALL_DIR="$HOME/.config/hypr/soundtoclick"
BIN_DIR="$HOME/.local/bin"
APP_ENTRY="$HOME/.local/share/applications/soundtoclick.desktop"
GITHUB_REPO="https://github.com/ghvbb/Sound-To-Click.git"

echo "========================================="
echo "      $APP_NAME Installer / Updater"
echo "========================================="

# سؤال المستخدم تثبيت جديد أم تحديث
echo "Do you want to (1) Install or (2) Update? [1/2]: "
read -r choice

if [[ "$choice" == "2" ]]; then
    if [ -d "$INSTALL_DIR" ]; then
        echo "Updating $APP_NAME from GitHub..."
        git -C "$INSTALL_DIR" pull || git clone "$GITHUB_REPO" "$INSTALL_DIR"
    else
        echo "No previous installation found. Installing new version."
    fi
fi

# إنشاء المجلدات
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$HOME/sounds"

# تثبيت dependencies
echo "Installing system dependencies..."
if ! command -v espeak-ng &>/dev/null; then
    if [ -f /etc/arch-release ]; then
        sudo pacman -S --needed espeak-ng tk python-pip git -y
    elif [ -f /etc/debian_version ]; then
        sudo apt install espeak-ng python3-tk python3-pip git -y
    elif [ -f /etc/fedora-release ]; then
        sudo dnf install espeak-ng python3-tkinter python3-pip git -y
    fi
fi

# إنشاء virtual environment
echo "Creating Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install deep-translator gTTS pyttsx3 arabic-reshaper python-bidi colorama

# نسخ ملفات المشروع
echo "Copying project files..."
cp -r main.py "$INSTALL_DIR/"

# إنشاء الاختصارات
echo "Creating executables..."
cat <<EOF > "$BIN_DIR/sound-tui"
#!/bin/bash
"$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/main.py" --tui
EOF

cat <<EOF > "$BIN_DIR/sound-gui"
#!/bin/bash
"$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/main.py"
EOF

chmod +x "$BIN_DIR/sound-tui" "$BIN_DIR/sound-gui"

# ضبط PATH تلقائيًا
echo "Would you like to add $BIN_DIR to your PATH? [yes/no]: "
read -r add_path
if [[ "$add_path" =~ ^(yes|y)$ ]]; then
    echo "Which shell do you use? (bash/fish/zsh): "
    read -r shell_type
    case $shell_type in
        bash) CONFIG_FILE="$HOME/.bashrc" ;;
        zsh) CONFIG_FILE="$HOME/.zshrc" ;;
        fish) CONFIG_FILE="$HOME/.config/fish/config.fish" ;;
        *) CONFIG_FILE="$HOME/.bashrc"; echo "Unknown shell, defaulting to bash." ;;
    esac

    if ! grep -q "$BIN_DIR" "$CONFIG_FILE"; then
        if [[ "$shell_type" == "fish" ]]; then
            echo "set -Ux PATH $BIN_DIR \$PATH" >> "$CONFIG_FILE"
        else
            echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$CONFIG_FILE"
        fi
        echo "PATH updated in $CONFIG_FILE"
    fi
fi

# إنشاء ملف desktop
echo "Creating desktop entry..."
cat <<EOF > "$APP_ENTRY"
[Desktop Entry]
Name=$APP_NAME
Comment=Pro Translator & TTS
Exec=$BIN_DIR/sound-gui
Icon=audio-x-generic
Type=Application
Categories=Utility;Multimedia;
Terminal=false
EOF

chmod +x "$APP_ENTRY"

echo "========================================="
echo "$APP_NAME installation completed!"
echo "TUI: sound-tui"
echo "GUI: Launch $APP_NAME from your application menu or run sound-gui"
echo "Audio output directory: $HOME/sounds"
echo "========================================="

