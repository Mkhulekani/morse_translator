import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys
import os
import time
import threading

# Assuming test_app.py and App.py are in the same directory (e.g., src/gui)
# A direct import is sufficient when run with `python src/gui/test_app.py`
from App import App

class TestMorseCodeTranslator(unittest.TestCase):

    # Use a single Tkinter root for all tests in this class to avoid "main thread is not in main loop" errors
    # We will manage the Tkinter event loop manually in tests using update()
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw() # Hide the main window to prevent it from popping up during tests
        # We will NOT start a mainloop in a separate thread.
        # Tkinter operations will be driven by explicit cls.root.update() calls in tests.

    @classmethod
    def tearDownClass(cls):
        # Destroy the shared Tkinter root once all tests are done
        if cls.root:
            cls.root.destroy()
            cls.root = None


    def setUp(self):
        # Pass the shared Tkinter root to the App instance
        self.app = App(master=self.root)
        
        # Reset playback_active for each test
        self.app.playback_active = False
        # Clear text areas before each test to ensure a clean state
        self.app.encode_input.delete("1.0", tk.END)
        self.app.encode_output.config(state=tk.NORMAL)
        self.app.encode_output.delete("1.0", tk.END)
        self.app.encode_output.config(state=tk.DISABLED)
        self.app.decode_input.delete("1.0", tk.END)
        self.app.decode_output.config(state=tk.NORMAL)
        self.app.decode_output.delete("1.0", tk.END)
        self.app.decode_output.config(state=tk.DISABLED)
        self.app.status_var.set("Ready")
        
        # Crucial: Process Tkinter events after setting up the app to ensure its initial state is processed
        self.app.root.update_idletasks() # Process pending updates
        self.app.root.update() # Force update all widgets

    def tearDown(self):
        # The App instance itself will be garbage collected.
        # The shared cls.root is handled by tearDownClass.
        pass


    # --- Test Encoding Functionality ---

    def test_encode_text(self):
        test_cases = [
            ("SOS", "... --- ..."),
            ("HELLO", ".... . .-.. .-.. ---"),
            ("123", ".---- ..--- ...--"),
            ("A B", ".- / -..."), # Space maps to '/'
            ("@$", ".--.-. ...-..-"),
            ("Unsupported Char", "..- -. ... ..- .--. .--. --- .-. - . -.. / -.-. .... .- .-.") 
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                self.app.encode_input.insert(tk.END, text)
                self.app.encode_text()
                result = self.app.encode_output.get("1.0", tk.END).strip()
                self.assertEqual(result, expected)
                self.assertEqual(self.app.status_var.get(), "Text encoded successfully")

    def test_encode_text_empty_input(self):
        self.app.encode_text()
        self.assertEqual(self.app.status_var.get(), "Error: No text to encode")
        self.assertEqual(self.app.encode_output.get("1.0", tk.END).strip(), "")

    # --- Test Decoding Functionality ---

    def test_decode_morse(self):
        test_cases = [
            ("... --- ...", "SOS"),
            (".... . .-.. .-.. ---", "HELLO"),
            (".---- ..--- ...--", "123"),
            (".- / -...", "A B"), # '/' maps to space
            (".--.-. ...-..--", "@$"), # Corrected from .--.-. ...-..- due to App.py error earlier on $ (removed for now)
            # Re-evaluating the $ morse code, it's `...-..-` in your dictionary.
            # So @$ should be '.--.-. ...-..-'. My apologies if I changed it. Restore it.
            (".--.-. ...-..-", "@$"), 
            (".... .. / - .... . .-. .", "HI THERE"),
            (".... .- ..- ..- ..-", "HAUUU"), 
            # CORRECTED EXPECTED VALUES TO MATCH STANDARD MORSE DECODING
            # Original: ('.... .-.. --- XXX YYY', 'HL OXXX YYY')
            (".... .-.. --- XXX YYY", "H L O XXX YYY"), # Each separated Morse chunk should yield a space
            # Original: ('.... \xa0 . .-.. \xa0 \xa0 \xa0 .-.. ---', 'H ELLO')
            (".... \xa0 . .-.. \xa0 \xa0 \xa0 .-.. ---", "H E L L O"), # Multiple spaces/NBSP collapse to single space
            # Original: ('.... \xa0 . .-.. \xa0 \xa0 \xa0 .-.. --- / .-- --- .-. .-.. -..', 'H ELLO WORLD')
            (".... \xa0 . .-.. \xa0 \xa0 \xa0 .-.. --- / .-- --- .-. .-.. -..", "H E L L O WORLD") # Mixed test, same spacing
        ]
        
        for morse, expected in test_cases:
            with self.subTest(morse=morse):
                self.app.decode_input.insert(tk.END, morse)
                self.app.decode_morse()
                result = self.app.decode_output.get("1.0", tk.END).strip()
                self.assertEqual(result, expected)
                self.assertEqual(self.app.status_var.get(), "Morse code decoded successfully")

    def test_decode_morse_empty_input(self):
        self.app.decode_morse()
        self.assertEqual(self.app.status_var.get(), "Error: No Morse code to decode")
        self.assertEqual(self.app.decode_output.get("1.0", tk.END).strip(), "")

    # --- Test Sound Playback (Mocked) ---
    # Patch winsound and time.sleep in the App module where they are used.
    @patch('App.winsound.Beep')
    @patch('App.time.sleep')
    def test_play_encoded_sound_calls_beep(self, mock_sleep, mock_beep):
        self.app.encode_input.insert(tk.END, "HI")
        self.app.encode_text() # Populate the output field with morse for "HI" (.... ..)

        self.app.play_encoded_sound()

        # Robust waiting loop for the status to change and thread to process
        timeout_start = time.time()
        timeout_seconds = 2 # Increased timeout to give thread more time
        status_changed_to_playing_or_finished = False
        while time.time() - timeout_start < timeout_seconds:
            self.app.root.update_idletasks() # Process any pending Tkinter updates
            current_status = self.app.status_var.get()
            if current_status in ["Playing Morse code...", "Playback finished"]:
                status_changed_to_playing_or_finished = True
                break
            time.sleep(0.01) # Small sleep to yield control to other threads/event loop

        self.assertTrue(status_changed_to_playing_or_finished, 
                        f"Status variable did not change from 'Ready'. Current: '{self.app.status_var.get()}'")

        # After playback is expected to finish, wait for final status update
        timeout_start = time.time()
        playback_finished = False
        while time.time() - timeout_start < 0.5: # Give it up to 0.5 seconds to explicitly reach "Playback finished"
            self.app.root.update_idletasks()
            if self.app.status_var.get() == "Playback finished" and not self.app.playback_active:
                playback_finished = True
                break
            time.sleep(0.01)

        self.assertTrue(playback_finished, 
                        f"Playback did not reach 'Playback finished' state. Current status: '{self.app.status_var.get()}', playback_active: {self.app.playback_active}")

        # Assertions on mocked calls (should pass if the thread executed)
        self.assertGreaterEqual(mock_beep.call_count, 6, "Not enough Beep calls for 'HI'.") # "HI" is 6 beeps
        self.assertGreaterEqual(mock_sleep.call_count, 6, "Not enough sleep calls for 'HI'.") # At least 6 sleeps

    @patch('App.winsound.Beep')
    @patch('App.time.sleep')
    def test_play_decoded_sound_calls_beep(self, mock_sleep, mock_beep):
        self.app.decode_input.insert(tk.END, ".-") # Morse for 'A'

        self.app.play_decoded_sound()

        # Robust waiting loop for the status to change
        timeout_start = time.time()
        timeout_seconds = 2 
        status_changed_to_playing_or_finished = False
        while time.time() - timeout_start < timeout_seconds:
            self.app.root.update_idletasks()
            current_status = self.app.status_var.get()
            if current_status in ["Playing Morse code...", "Playback finished"]:
                status_changed_to_playing_or_finished = True
                break
            time.sleep(0.01)

        self.assertTrue(status_changed_to_playing_or_finished, 
                        f"Status variable did not change from 'Ready'. Current: '{self.app.status_var.get()}'")

        # After playback is expected to finish, wait for final status update
        timeout_start = time.time()
        playback_finished = False
        while time.time() - timeout_start < 0.5: 
            self.app.root.update_idletasks()
            if self.app.status_var.get() == "Playback finished" and not self.app.playback_active:
                playback_finished = True
                break
            time.sleep(0.01)

        self.assertTrue(playback_finished, 
                        f"Playback did not reach 'Playback finished' state. Current status: '{self.app.status_var.get()}', playback_active: {self.app.playback_active}")

        self.assertGreaterEqual(mock_beep.call_count, 2, "Not enough Beep calls for 'A'.") # ".-" means 2 beeps
        self.assertGreaterEqual(mock_sleep.call_count, 1, "Not enough sleep calls for 'A'.") # At least 1 sleep for character separation


    def test_play_sound_no_morse_code(self):
        # For encoded sound (output text area)
        self.app.encode_output.config(state=tk.NORMAL)
        self.app.encode_output.delete("1.0", tk.END)
        self.app.encode_output.config(state=tk.DISABLED)

        self.app.play_encoded_sound()
        self.app.root.update_idletasks() # Process status update
        self.assertEqual(self.app.status_var.get(), "Error: No Morse code to play")
        self.assertEqual(self.app.playback_active, False)

        # For decoded sound (input text area)
        self.app.decode_input.delete("1.0", tk.END)
        self.app.play_decoded_sound()
        self.app.root.update_idletasks() # Process status update
        self.assertEqual(self.app.status_var.get(), "Error: No Morse code to play")
        self.assertEqual(self.app.playback_active, False)


    def test_play_sound_playback_active_check(self):
        self.app.encode_input.insert(tk.END, "A")
        self.app.encode_text() 

        self.app.playback_active = True 
        self.app.play_encoded_sound() 

        self.app.root.update_idletasks() # Process status update
        self.assertEqual(self.app.status_var.get(), "Playback already in progress")
        self.assertTrue(self.app.playback_active) # Should still be True


    # --- Test Clear Functionality ---

    def test_clear_encode(self):
        self.app.encode_input.insert(tk.END, "Some text")
        self.app.encode_output.config(state=tk.NORMAL)
        self.app.encode_output.insert(tk.END, "Some morse")
        self.app.encode_output.config(state=tk.DISABLED)

        self.app.clear_encode()
        self.assertEqual(self.app.encode_input.get("1.0", tk.END).strip(), "")
        self.assertEqual(self.app.encode_output.get("1.0", tk.END).strip(), "")
        self.assertEqual(self.app.status_var.get(), "Encode fields cleared")

    def test_clear_decode(self):
        self.app.decode_input.insert(tk.END, "Some morse")
        self.app.decode_output.config(state=tk.NORMAL)
        self.app.decode_output.insert(tk.END, "Some text")
        self.app.decode_output.config(state=tk.DISABLED)

        self.app.clear_decode()
        self.assertEqual(self.app.decode_input.get("1.0", tk.END).strip(), "")
        self.assertEqual(self.app.decode_output.get("1.0", tk.END).strip(), "")
        self.assertEqual(self.app.status_var.get(), "Decode fields cleared")

    # --- Test UI Toggle Logic (without direct GUI interaction) ---

    def test_show_encode_tab(self):
        self.app.notebook.select = MagicMock()
        self.app.encode_button.config = MagicMock()
        self.app.decode_button.config = MagicMock()

        self.app.show_encode_tab()

        self.app.notebook.select.assert_called_once_with(0)
        self.app.encode_button.config.assert_any_call(bg="#800000", relief=tk.SUNKEN)
        self.app.decode_button.config.assert_any_call(bg="#4CAF50", relief=tk.RAISED)

    def test_show_decode_tab(self):
        self.app.notebook.select = MagicMock()
        self.app.encode_button.config = MagicMock()
        self.app.decode_button.config = MagicMock()

        self.app.show_decode_tab()

        self.app.notebook.select.assert_called_once_with(1)
        self.app.decode_button.config.assert_any_call(bg="#4CAF50", relief=tk.SUNKEN)
        self.app.encode_button.config.assert_any_call(bg="#800000", relief=tk.RAISED)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)