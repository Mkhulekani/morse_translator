# R2-D2 Morse Code Translator

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/gui-tkinter-orange)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)
![Tested](https://img.shields.io/badge/tests-unittest-green)

A fun and interactive Morse Code Translator desktop app inspired by **R2-D2** from Star Wars. Encode text into Morse code, decode Morse code back to readable text, and even hear the output as beeps!

---

## 🚀 Features

- **Encode** text into Morse code
- **Decode** Morse code into readable text
- **Play** Morse code audio using system beeps
- **User Interface** built with Tkinter
- Visual feedback for dots and dashes
- **Dark Theme UI** with distinct color styling
- **Test Suite** using `unittest` with mocked sound playback

---

## 🛠 Requirements

- Python 3.8 or newer
- Windows OS (due to use of `winsound`)
- Optional: `unittest` for running test suite

---

## 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/morse-r2d2-translator.git
    cd morse-r2d2-translator
    ```

2. **Run the app**:
    ```bash
    python App.py
    ```

3. **Run the tests**:
    ```bash
    python test_app.py
    ```

---

## 🧪 Tests

The app includes a comprehensive test suite in `test_app.py`:

- Text to Morse and Morse to Text translation
- Sound playback (mocked)
- UI behavior like tab switching and clear buttons

Run all tests using:

```bash
python test_app.py
🧠 How It Works
Each character maps to a Morse code using a dictionary.

Encoding: Converts input text to Morse and displays it.

Decoding: Splits Morse input (using space and /) to identify original text.

Sound playback: Uses winsound.Beep() for . and - with delays between elements.

📂 Project Structure
bash
Copy
Edit
├── App.py           # Main GUI app
├── test_app.py      # Unit tests
├── README.md        # Project description
⚠️ Notes
This app currently only supports Windows because winsound is a Windows-only module. For cross-platform support, consider using playsound, pydub, or pygame.

Be sure to have focus on the app when testing sound for proper GUI response.

🙌 Acknowledgments
Inspired by R2-D2 and the Rebel Alliance. May the Force be with your code! ✨

📜 License
MIT License. See LICENSE file for details.

vbnet
Copy
Edit

Let me know if you want to include screenshots, installation packages, or convert this into a GitH
