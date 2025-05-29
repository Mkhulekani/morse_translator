import tkinter as tk
from tkinter import ttk, messagebox
import winsound  # For Windows sound - alternative for other OS
import time
import threading

class App:
    # Modified to accept an optional master (Tkinter root)
    def __init__(self, master=None):
        self.morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....-', '7': '--...',
            '8': '---..', '9': '----.',
            '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
            '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
            '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
            '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
            '$': '...-..-', '@': '.--.-.', ' ': '/'
        }
        
        self.reverse_morse_dict = {v: k for k, v in self.morse_code_dict.items()}
        
        # Use provided master if available, otherwise create a new Tkinter root
        self.root = master if master else tk.Tk()
        
        self.root.title("R2-D2 Morse Code Translator")
        self.root.geometry("600x550")
        self.root.resizable(False, False) # Keep this as per original
        
        self.bg_color = "#2b2b2b"
        self.fg_color = "#f0f0f0"
        self.accent_color = "#4ec9b0"
        self.error_color = "#ff5555"
        self.sound_active_color = "#00FF00"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
        
        self.playback_active = False
        
    def create_widgets(self):
        # ... (rest of create_widgets remains unchanged)
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=10)
        
        tk.Label(
            header_frame,
            text="R2-D2 Morse Code Translator",
            font=("Arial", 20, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        ).pack()
        
        tk.Label(
            header_frame,
            text="Send secret messages like a true Rebel!",
            font=("Arial", 10),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack()
        
        top_button_frame = tk.Frame(self.root, bg=self.bg_color)
        top_button_frame.pack(pady=5)
        
        self.encode_button = tk.Button(
            top_button_frame,
            text="Encode",
            command=self.show_encode_tab,
            bg="#800000",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            bd=2
        )
        self.encode_button.pack(side=tk.LEFT, padx=5)
        
        self.decode_button = tk.Button(
            top_button_frame,
            text="Decode",
            command=self.show_decode_tab,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            bd=2
        )
        self.decode_button.pack(side=tk.LEFT, padx=5)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.create_encode_tab(self.notebook)
        self.create_decode_tab(self.notebook)
        
        self.show_encode_tab()
        
        feedback_frame = tk.Frame(self.root, bg=self.bg_color)
        feedback_frame.pack(pady=10)
        
        self.dot_feedback = tk.Button(
            feedback_frame,
            text="Dot",
            state=tk.DISABLED,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 10, "bold"),
            width=8,
            relief=tk.SUNKEN
        )
        self.dot_feedback.pack(side=tk.LEFT, padx=5)
        
        self.dash_feedback = tk.Button(
            feedback_frame,
            text="Dash",
            state=tk.DISABLED,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 10, "bold"),
            width=8,
            relief=tk.SUNKEN
        )
        self.dash_feedback.pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 8),
            fg=self.fg_color,
            bg=self.bg_color
        )
        status_bar.pack(fill=tk.X, padx=5, pady=5)
        
    def show_encode_tab(self):
        self.notebook.select(0)
        self.encode_button.config(bg="#800000", relief=tk.SUNKEN)
        self.decode_button.config(bg="#4CAF50", relief=tk.RAISED)
        
    def show_decode_tab(self):
        self.notebook.select(1)
        self.decode_button.config(bg="#4CAF50", relief=tk.SUNKEN)
        self.encode_button.config(bg="#800000", relief=tk.RAISED)
        
    def create_encode_tab(self, notebook):
        # ... (unchanged)
        encode_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(encode_tab, text="Encode")
        
        input_frame = tk.Frame(encode_tab, bg=self.bg_color)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(
            input_frame,
            text="Enter text to encode:",
            font=("Arial", 12),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(anchor=tk.W)
        
        self.encode_input = tk.Text(
            input_frame,
            height=5,
            width=50,
            font=("Arial", 10),
            bg="#3c3f41",
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.encode_input.pack(fill=tk.X)
        
        button_frame = tk.Frame(encode_tab, bg=self.bg_color)
        button_frame.pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Convert",
            command=self.encode_text,
            bg="#800000",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Play Sound",
            command=self.play_encoded_sound,
            bg="#800000",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_encode,
            bg="#5c5c5c",
            fg=self.fg_color,
            font=("Arial", 10),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        output_frame = tk.Frame(encode_tab, bg=self.bg_color)
        output_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(
            output_frame,
            text="Morse Code:",
            font=("Arial", 12),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(anchor=tk.W)
        
        self.encode_output = tk.Text(
            output_frame,
            height=5,
            width=50,
            font=("Arial", 10),
            bg="#3c3f41",
            fg=self.fg_color,
            state=tk.DISABLED
        )
        self.encode_output.pack(fill=tk.X)
        
    def create_decode_tab(self, notebook):
        # ... (unchanged)
        decode_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(decode_tab, text="Decode")
        
        input_frame = tk.Frame(decode_tab, bg=self.bg_color)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(
            input_frame,
            text="Enter Morse code to decode:",
            font=("Arial", 12),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(anchor=tk.W)
        
        tk.Label(
            input_frame,
            text="(Separate letters with space, words with '/')",
            font=("Arial", 8),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(anchor=tk.W)
        
        self.decode_input = tk.Text(
            input_frame,
            height=5,
            width=50,
            font=("Arial", 10),
            bg="#3c3f41",
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.decode_input.pack(fill=tk.X)
        
        button_frame = tk.Frame(decode_tab, bg=self.bg_color)
        button_frame.pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Convert",
            command=self.decode_morse,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Play Sound",
            command=self.play_decoded_sound,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_decode,
            bg="#5c5c5c",
            fg=self.fg_color,
            font=("Arial", 10),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        output_frame = tk.Frame(decode_tab, bg=self.bg_color)
        output_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(
            output_frame,
            text="Decoded Text:",
            font=("Arial", 12),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(anchor=tk.W)
        
        self.decode_output = tk.Text(
            output_frame,
            height=5,
            width=50,
            font=("Arial", 10),
            bg="#3c3f41",
            fg=self.fg_color,
            state=tk.DISABLED
        )
        self.decode_output.pack(fill=tk.X)
        
    def encode_text(self):
        text = self.encode_input.get("1.0", tk.END).strip().upper()
        if not text:
            self.status_var.set("Error: No text to encode")
            return
            
        try:
            morse_code_elements = []
            for char in text:
                if char in self.morse_code_dict:
                    morse_code_elements.append(self.morse_code_dict[char])
                else:
                    morse_code_elements.append(char)  # Keep unsupported characters as-is
            
            morse_text = ' '.join(morse_code_elements)
            
            self.encode_output.config(state=tk.NORMAL)
            self.encode_output.delete("1.0", tk.END)
            self.encode_output.insert(tk.END, morse_text)
            self.encode_output.config(state=tk.DISABLED)
            
            self.status_var.set("Text encoded successfully")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def decode_morse(self):
        morse_code_input = self.decode_input.get("1.0", tk.END).strip().replace('\xa0', ' ')
        if not morse_code_input:
            self.status_var.set("Error: No Morse code to decode")
            return
            
        try:
            decoded_words = []
            words_morse = morse_code_input.split('/')
            
            for word_morse in words_morse:
                # Use .split() without args to handle multiple spaces and leading/trailing spaces
                characters_morse = word_morse.strip().split() # This splits by any whitespace and removes empty strings
                
                decoded_chars = []
                for char_morse in characters_morse:
                    if char_morse in self.reverse_morse_dict:
                        decoded_chars.append(self.reverse_morse_dict[char_morse])
                    else:
                        decoded_chars.append(char_morse) # Keep unknown codes as-is
                
                # Join characters to form a word with single spaces between them.
                decoded_words.append(' '.join(decoded_chars))
            
            # Join words with a single space. Filter(None, ...) handles empty strings if multiple '/' were present.
            decoded_str = ' '.join(filter(None, decoded_words)).strip()
            
            self.decode_output.config(state=tk.NORMAL)
            self.decode_output.delete("1.0", tk.END)
            self.decode_output.insert(tk.END, decoded_str)
            self.decode_output.config(state=tk.DISABLED)
            
            self.status_var.set("Morse code decoded successfully")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def play_encoded_sound(self):
        # Get the morse_text on the main thread before starting the new thread
        morse_text = self.encode_output.get("1.0", tk.END).strip()
        
        if not morse_text:
            self.status_var.set("Error: No Morse code to play")
            return
            
        if self.playback_active:
            self.status_var.set("Playback already in progress")
            return
            
        self.playback_active = True
        self.status_var.set("Playing Morse code...")
        
        # Pass morse_text, dot_feedback, and dash_feedback to the new thread
        threading.Thread(target=self._play_morse_sound, args=(morse_text, self.dot_feedback, self.dash_feedback), daemon=True).start()
    
    def play_decoded_sound(self):
        # Get the morse_text on the main thread before starting the new thread
        morse_text = self.decode_input.get("1.0", tk.END).strip()
        
        if not morse_text:
            self.status_var.set("Error: No Morse code to play")
            return
            
        if self.playback_active:
            self.status_var.set("Playback already in progress")
            return
            
        self.playback_active = True
        self.status_var.set("Playing Morse code...")
        
        # Pass morse_text, dot_feedback, and dash_feedback to the new thread
        threading.Thread(target=self._play_morse_sound, args=(morse_text, self.dot_feedback, self.dash_feedback), daemon=True).start()
    
    def _play_morse_sound(self, morse_text, dot_btn, dash_btn):
        # All Tkinter widget manipulations must be scheduled via root.after
        # Sound playing and time.sleep can happen directly in the thread.
        try:
            for char in morse_text:
                if not self.playback_active:
                    break
                    
                if char == '.':
                    self.root.after(0, lambda: dot_btn.config(bg=self.sound_active_color))
                    winsound.Beep(800, 200)
                    self.root.after(0, lambda: dot_btn.config(bg=self.bg_color))
                    time.sleep(0.1)
                elif char == '-':
                    self.root.after(0, lambda: dash_btn.config(bg=self.sound_active_color))
                    winsound.Beep(600, 400)
                    self.root.after(0, lambda: dash_btn.config(bg=self.bg_color))
                    time.sleep(0.1)
                elif char == ' ':
                    time.sleep(0.3)
                elif char == '/':
                    time.sleep(0.7)
            
            self.root.after(0, lambda: dot_btn.config(bg=self.bg_color))
            self.root.after(0, lambda: dash_btn.config(bg=self.bg_color))

        finally:
            self.playback_active = False
            self.root.after(0, lambda: self.status_var.set("Playback finished"))
    
    def clear_encode(self):
        self.encode_input.delete("1.0", tk.END)
        self.encode_output.config(state=tk.NORMAL)
        self.encode_output.delete("1.0", tk.END)
        self.encode_output.config(state=tk.DISABLED)
        self.status_var.set("Encode fields cleared")
    
    def clear_decode(self):
        self.decode_input.delete("1.0", tk.END)
        self.decode_output.config(state=tk.NORMAL)
        self.decode_output.delete("1.0", tk.END)
        self.decode_output.config(state=tk.DISABLED)
        self.status_var.set("Decode fields cleared")
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        self.playback_active = False
        self.root.destroy()

if __name__ == "__main__":
    app = App()
    app.run()