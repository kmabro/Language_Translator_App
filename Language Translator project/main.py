import customtkinter as ctk
import requests
import pyperclip
import json
from langdetect import detect
import time
import urllib.parse
import re
from tkinter import ttk
import threading
import os

# List of RTL languages for proper text alignment
RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur', 'ps', 'sd', 'ku', 'dv', 'ug']

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator by KM")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Set dark appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Define supported languages for LibreTranslate
        self.supported_languages = [
            {"code": "en", "name": "English"},
            {"code": "ar", "name": "Arabic"},
            {"code": "bn", "name": "Bengali"},
            {"code": "zh", "name": "Chinese"},
            {"code": "nl", "name": "Dutch"},
            {"code": "fi", "name": "Finnish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "el", "name": "Greek"},
            {"code": "he", "name": "Hebrew"},
            {"code": "hi", "name": "Hindi"},
            {"code": "hu", "name": "Hungarian"},
            {"code": "id", "name": "Indonesian"},
            {"code": "ga", "name": "Irish"},
            {"code": "it", "name": "Italian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "fa", "name": "Persian"},
            {"code": "pl", "name": "Polish"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "pa", "name": "Punjabi"},
            {"code": "ro", "name": "Romanian"},
            {"code": "ru", "name": "Russian"},
            {"code": "es", "name": "Spanish"},
            {"code": "sv", "name": "Swedish"},
            {"code": "tl", "name": "Tagalog"},
            {"code": "ta", "name": "Tamil"},
            {"code": "te", "name": "Telugu"},
            {"code": "th", "name": "Thai"},
            {"code": "tr", "name": "Turkish"},
            {"code": "uk", "name": "Ukrainian"},
            {"code": "ur", "name": "Urdu"},
            {"code": "vi", "name": "Vietnamese"},
            {"code": "ps", "name": "Pashto"},
            {"code": "af", "name": "Afrikaans"},
            {"code": "sq", "name": "Albanian"},
            {"code": "am", "name": "Amharic"},
            {"code": "hy", "name": "Armenian"},
            {"code": "az", "name": "Azerbaijani"},
            {"code": "eu", "name": "Basque"},
            {"code": "be", "name": "Belarusian"},
            {"code": "bs", "name": "Bosnian"},
            {"code": "bg", "name": "Bulgarian"},
            {"code": "ca", "name": "Catalan"},
            {"code": "ceb", "name": "Cebuano"},
            {"code": "ny", "name": "Chichewa"},
            {"code": "co", "name": "Corsican"},
            {"code": "hr", "name": "Croatian"},
            {"code": "cs", "name": "Czech"},
            {"code": "da", "name": "Danish"},
            {"code": "eo", "name": "Esperanto"},
            {"code": "et", "name": "Estonian"},
            {"code": "tl", "name": "Filipino"},
            {"code": "fy", "name": "Frisian"},
            {"code": "gl", "name": "Galician"},
            {"code": "ka", "name": "Georgian"},
            {"code": "gu", "name": "Gujarati"},
            {"code": "ht", "name": "Haitian Creole"},
            {"code": "ha", "name": "Hausa"},
            {"code": "haw", "name": "Hawaiian"},
            {"code": "hmn", "name": "Hmong"},
            {"code": "is", "name": "Icelandic"},
            {"code": "ig", "name": "Igbo"},
            {"code": "jw", "name": "Javanese"},
            {"code": "kn", "name": "Kannada"},
            {"code": "kk", "name": "Kazakh"},
            {"code": "km", "name": "Khmer"},
            {"code": "ku", "name": "Kurdish"},
            {"code": "ky", "name": "Kyrgyz"},
            {"code": "lo", "name": "Lao"},
            {"code": "la", "name": "Latin"},
            {"code": "lv", "name": "Latvian"},
            {"code": "lt", "name": "Lithuanian"},
            {"code": "lb", "name": "Luxembourgish"},
            {"code": "mk", "name": "Macedonian"},
            {"code": "mg", "name": "Malagasy"},
            {"code": "ms", "name": "Malay"},
            {"code": "ml", "name": "Malayalam"},
            {"code": "mt", "name": "Maltese"},
            {"code": "mi", "name": "Maori"},
            {"code": "mr", "name": "Marathi"},
            {"code": "mn", "name": "Mongolian"},
            {"code": "my", "name": "Myanmar (Burmese)"},
            {"code": "ne", "name": "Nepali"},
            {"code": "no", "name": "Norwegian"},
            {"code": "or", "name": "Odia (Oriya)"},
            {"code": "sd", "name": "Sindhi"},
            {"code": "si", "name": "Sinhala"},
            {"code": "sk", "name": "Slovak"},
            {"code": "sl", "name": "Slovenian"},
            {"code": "so", "name": "Somali"},
            {"code": "st", "name": "Southern Sotho"},
            {"code": "su", "name": "Sundanese"},
            {"code": "sw", "name": "Swahili"},
            {"code": "tg", "name": "Tajik"},
            {"code": "tt", "name": "Tatar"},
            {"code": "tk", "name": "Turkmen"},
            {"code": "ug", "name": "Uyghur"},
            {"code": "uz", "name": "Uzbek"},
            {"code": "xh", "name": "Xhosa"},
            {"code": "yi", "name": "Yiddish"},
            {"code": "yo", "name": "Yoruba"},
            {"code": "zu", "name": "Zulu"}
        ]
        
        # Create language mappings
        self.language_list = [lang["name"] for lang in self.supported_languages]
        self.name_to_code = {lang["name"]: lang["code"] for lang in self.supported_languages}
        self.code_to_name = {lang["code"]: lang["name"] for lang in self.supported_languages}
        
        # Define colors
        self.bg_color = "#000000"  # Black background
        self.text_area_bg = "#1A1A1A"  # Dark gray for text areas
        self.button_color = "#800080"  # Purple for buttons
        self.button_hover_color = "#9932CC"  # Brighter purple for hover
        self.text_color = "#FFFFFF"  # White text
        self.border_color = "#333333"  # Dark gray borders
        self.error_color = "#FF6B6B"  # Red for errors
        self.success_color = "#4CAF50"  # Green for success
        
        # Create main frame with black background
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create title with white text
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Language Translator", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.text_color
        )
        self.title_label.pack(pady=10)
        
        # Create content frame with black background
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_color)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=0)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=0)
        
        # Source language frame with dark background
        self.source_lang_frame = ctk.CTkFrame(self.content_frame, fg_color=self.text_area_bg)
        self.source_lang_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Source language dropdown
        self.source_lang_var = ctk.StringVar(value="Auto")
        source_options = ["Auto"] + self.language_list
        self.source_lang_dropdown = ctk.CTkOptionMenu(
            self.source_lang_frame,
            values=source_options,
            variable=self.source_lang_var,
            fg_color=self.button_color,
            button_color=self.button_color,
            button_hover_color=self.button_hover_color,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.source_lang_dropdown.pack(side="left", padx=10, pady=5)
        
        # Source language clear button
        self.clear_source_btn = ctk.CTkButton(
            self.source_lang_frame,
            text="Clear",
            width=80,
            command=self.clear_source,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.clear_source_btn.pack(side="right", padx=10, pady=5)
        
        # Target language frame
        self.target_lang_frame = ctk.CTkFrame(self.content_frame, fg_color=self.text_area_bg)
        self.target_lang_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Target language dropdown
        self.target_lang_var = ctk.StringVar(value="English")
        self.target_lang_dropdown = ctk.CTkOptionMenu(
            self.target_lang_frame,
            values=self.language_list,
            variable=self.target_lang_var,
            fg_color=self.button_color,
            button_color=self.button_color,
            button_hover_color=self.button_hover_color,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.target_lang_dropdown.pack(side="left", padx=10, pady=5)
        
        # Target language copy button
        self.copy_target_btn = ctk.CTkButton(
            self.target_lang_frame,
            text="Copy",
            width=80,
            command=self.copy_translation,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.copy_target_btn.pack(side="right", padx=10, pady=5)
        
        # Source text box with dark theme and scrollbar
        self.source_textbox = ctk.CTkTextbox(
            self.content_frame,
            width=400,
            height=300,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color=self.text_area_bg,
            text_color=self.text_color,
            border_width=1,
            border_color=self.border_color,
            scrollbar_button_color=self.button_color,
            scrollbar_button_hover_color=self.button_hover_color,
            wrap="word"  # Enable word wrapping
        )
        self.source_textbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure text alignment to left
        self.source_textbox.configure(padx=10, pady=10)
        
        # Target text box with dark theme and scrollbar
        self.target_textbox = ctk.CTkTextbox(
            self.content_frame,
            width=400,
            height=300,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color=self.text_area_bg,
            text_color=self.text_color,
            border_width=1,
            border_color=self.border_color,
            scrollbar_button_color=self.button_color,
            scrollbar_button_hover_color=self.button_hover_color,
            wrap="word"  # Enable word wrapping
        )
        self.target_textbox.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure text alignment to left
        self.target_textbox.configure(padx=10, pady=10)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.content_frame, fg_color=self.bg_color)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Translate button with tooltip
        self.translate_btn = ctk.CTkButton(
            self.button_frame,
            text="Translate",
            command=self.translate_text,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            height=40,
            width=150,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            corner_radius=10
        )
        self.translate_btn.pack(side="left", padx=10)
        
        # Remove or comment out the tooltip line below
        # self.translate_btn_tooltip = ToolTip(self.translate_btn, "Click to translate")
        
        # Clear All button
        self.clear_all_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear All",
            command=self.clear_all,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            height=40,
            width=150,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            corner_radius=10
        )
        self.clear_all_btn.pack(side="left", padx=10)
        
        # Status bar with white text
        self.status_var = ctk.StringVar(value="Ready")
        self.status_bar = ctk.CTkLabel(
            self.main_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.text_color
        )
        self.status_bar.pack(pady=5)
        
        # Loading spinner (hidden by default)
        self.spinner_label = ctk.CTkLabel(
            self.content_frame,
            text="⟳",
            font=ctk.CTkFont(size=24),
            text_color=self.button_color
        )
        self.spinner_label.place(relx=0.5, rely=0.5, anchor="center")
        self.spinner_label.lower()  # Place behind other widgets
        self.spinner_label.configure(fg_color="transparent")
        self.spinner_visible = False
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-Return>", lambda event: self.translate_text())
        
        # API endpoints to try (in order)
        self.api_endpoints = [
            "https://libretranslate.de/translate",
            "https://translate.terraprint.co/translate",
            "https://translate.astian.org/translate",
            "https://translate.argosopentech.com/translate"
        ]
        
        # Add error message label (hidden by default)
        self.error_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.error_color,
            fg_color=self.text_area_bg,
            corner_radius=5
        )
        self.error_label.place(relx=0.5, rely=0.7, anchor="center")
        self.error_label.lower()  # Place behind other widgets
        
        # Add event binding for language selection to handle RTL languages
        self.target_lang_var.trace_add("write", self.handle_language_direction)
        
        # DeepL API key (set to None by default)
        self.deepl_api_key = None
        
        # Try to load DeepL API key from config file
        self.load_api_keys()

    def load_api_keys(self):
        """Load API keys from config file"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                    self.deepl_api_key = config.get("deepl_api_key")
        except Exception as e:
            print(f"Error loading API keys: {str(e)}")

    def handle_language_direction(self, *args):
        """Handle text direction based on selected language"""
        target_lang_name = self.target_lang_var.get()
        if target_lang_name in self.language_list:
            target_lang_code = self.name_to_code[target_lang_name]
            
            # Clear existing text
            current_text = self.target_textbox.get("1.0", "end-1c")
            self.target_textbox.delete("1.0", "end")
            
            # Set text direction based on language
            if target_lang_code in RTL_LANGUAGES:
                # Configure RTL text alignment properly
                self.target_textbox.tag_configure("rtl", justify="right")
                self.target_textbox.tag_remove("ltr", "1.0", "end")
                self.target_textbox.tag_add("rtl", "1.0", "end")
                # Force right alignment for the entire text box
                self.target_textbox.configure(justify="right")
            else:
                # Configure LTR text alignment
                self.target_textbox.tag_configure("ltr", justify="left")
                self.target_textbox.tag_remove("rtl", "1.0", "end")
                self.target_textbox.tag_add("ltr", "1.0", "end")
                # Reset to left alignment for the entire text box
                self.target_textbox.configure(justify="left")
            
            # Restore text
            self.target_textbox.insert("1.0", current_text)

    def show_error(self, message, duration=5000):
        """Show error message with fade effect"""
        # Configure error label
        self.error_label.configure(text=message)
        self.error_label.lift()  # Bring to front
        
        # Schedule hiding the error message
        self.root.after(duration, self.hide_error)

    def hide_error(self):
        """Hide error message"""
        self.error_label.configure(text="")
        self.error_label.lower()  # Send to back

    def translate_with_deepl(self, text, source_lang='auto', target_lang='en'):
        """
        Translation method using DeepL API
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
            
        Returns:
            str: Translated text or error message
        """
        if not self.deepl_api_key:
            return None  # Skip if no API key
        
        self.status_var.set("Trying DeepL translation...")
        self.root.update()
        
        try:
            # DeepL API endpoint
            url = "https://api-free.deepl.com/v2/translate"
            
            # Prepare headers with API key
            headers = {
                "Authorization": f"DeepL-Auth-Key {self.deepl_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare payload
            payload = {
                "text": [text],
                "target_lang": target_lang.upper()
            }
            
            # Add source language if not auto
            if source_lang != 'auto':
                payload["source_lang"] = source_lang.upper()
            
            # Make the request
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'translations' in data and len(data['translations']) > 0:
                    return data['translations'][0]['text']
            
            return None  # Return None to try next method
        except Exception as e:
            print(f"DeepL API error: {str(e)}")
            return None  # Return None to try next method

    def translate_with_google(self, text, source_lang='auto', target_lang='en'):
        """
        Translation method using Google Translate API (unofficial)
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
            
        Returns:
            str: Translated text or error message
        """
        self.status_var.set("Trying Google translation...")
        self.root.update()
        
        try:
            # Construct the URL
            url = "https://translate.googleapis.com/translate_a/single"
            
            # Prepare parameters
            params = {
                "client": "gtx",
                "sl": source_lang,
                "tl": target_lang,
                "dt": "t",
                "q": text
            }
            
            # Make the request
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                # Parse the response
                result = response.json()
                
                # Extract translated text
                translated_text = ""
                if result and len(result) > 0 and result[0]:
                    for sentence in result[0]:
                        if sentence and len(sentence) > 0:
                            translated_text += sentence[0]
                    
                    return translated_text
            
            return None  # Return None to try next method
        except Exception as e:
            print(f"Google Translate API error: {str(e)}")
            return None  # Return None to try next method

    def show_spinner(self):
        """Show and animate the loading spinner"""
        if not self.spinner_visible:
            self.spinner_visible = True
            self.spinner_label.lift()  # Bring to front
            self.animate_spinner()
    
    def hide_spinner(self):
        """Hide the loading spinner"""
        self.spinner_visible = False
        self.spinner_label.lower()  # Send to back
    
    def animate_spinner(self):
        """Animate the spinner with rotation"""
        if self.spinner_visible:
            # Rotate the spinner character
            current_text = self.spinner_label.cget("text")
            rotation_chars = ["⟳", "⟲", "↻", "↺"]
            current_index = rotation_chars.index(current_text) if current_text in rotation_chars else 0
            next_index = (current_index + 1) % len(rotation_chars)
            self.spinner_label.configure(text=rotation_chars[next_index])
            
            # Schedule the next animation frame
            self.root.after(150, self.animate_spinner)
    
    def highlight_output(self):
        """Highlight the output area with a brief glow effect"""
        # Save original colors
        original_border = self.target_textbox.cget("border_color")
        
        # Change to highlight color
        highlight_color = "#A020F0"  # Bright purple
        self.target_textbox.configure(border_color=highlight_color)
        
        # Schedule return to original colors
        def reset_colors():
            self.target_textbox.configure(border_color=original_border)
        
        # Final reset
        self.root.after(1500, reset_colors)
    
    def translate_with_mymemory(self, text, source_lang='auto', target_lang='en'):
        """
        Translation method using MyMemory API
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
            
        Returns:
            str: Translated text or error message
        """
        self.status_var.set("Trying MyMemory translation...")
        self.root.update()
        
        try:
            # Construct the URL
            url = "https://api.mymemory.translated.net/get"
            
            # Handle auto detection for MyMemory
            if source_lang == 'auto':
                try:
                    # Use langdetect to detect the language
                    detected_lang = detect(text)
                    source_lang = detected_lang
                except Exception:
                    # If detection fails, default to English
                    source_lang = 'en'
            
            # Prepare parameters
            params = {
                "q": text,
                "langpair": f"{source_lang}|{target_lang}"
            }
            
            # Make the request
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'responseData' in data and 'translatedText' in data['responseData']:
                    return data['responseData']['translatedText']
            
            return None  # Return None to try next method
        except Exception as e:
            print(f"MyMemory API error: {str(e)}")
            return None  # Return None to try next method
    
    def translate_with_libre(self, text, source_lang='auto', target_lang='en'):
        """
        Translation method using LibreTranslate API
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
            
        Returns:
            str: Translated text or error message
        """
        # Try each endpoint in order
        for endpoint in self.api_endpoints:
            try:
                # Update status with current endpoint
                endpoint_name = endpoint.split('/')[2]
                self.status_var.set(f"Trying {endpoint_name}...")
                self.root.update()
                
                # Handle auto detection for LibreTranslate
                if source_lang == 'auto':
                    try:
                        # First detect the language
                        detect_url = endpoint.replace('/translate', '/detect')
                        detect_payload = {'q': text}
                        detect_response = requests.post(detect_url, json=detect_payload, timeout=10)
                        
                        if detect_response.status_code == 200:
                            detect_data = detect_response.json()
                            if detect_data and len(detect_data) > 0:
                                source_lang = detect_data[0]['language']
                        else:
                            # If detection fails, default to English
                            source_lang = 'en'
                    except Exception:
                        # If detection fails, default to English
                        source_lang = 'en'
                
                # Prepare payload for the translation request
                payload = {
                    'q': text,
                    'source': source_lang,
                    'target': target_lang,
                    'format': 'text'
                }
                
                # Make POST request to the API
                response = requests.post(endpoint, json=payload, timeout=15)
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    if 'translatedText' in result:
                        return result['translatedText']
            except Exception as e:
                print(f"LibreTranslate API error ({endpoint}): {str(e)}")
                continue  # Try next endpoint
        
        return None  # Return None if all endpoints failed
    
    def translate_text(self):
        """Translate text using multiple services with fallback"""
        # Get text from source textbox
        text = self.source_textbox.get("1.0", "end-1c").strip()
        
        # Check if text is empty
        if not text:
            self.show_error("Please enter text to translate")
            return
        
        # Get source and target languages
        source_lang_name = self.source_lang_var.get()
        target_lang_name = self.target_lang_var.get()
        
        # Convert language names to codes
        source_lang = "auto" if source_lang_name == "Auto" else self.name_to_code.get(source_lang_name, "auto")
        target_lang = self.name_to_code.get(target_lang_name, "en")
        
        # Show spinner during translation
        self.show_spinner()
        self.status_var.set("Translating...")
        self.root.update()
        
        # Clear previous translation
        self.target_textbox.delete("1.0", "end")
        
        # Create a thread for translation to prevent UI freezing
        def translation_thread():
            try:
                # Try multiple translation services in order
                translation = None
                
                # 1. Try DeepL if API key is available
                if self.deepl_api_key:
                    translation = self.translate_with_deepl(text, source_lang, target_lang)
                
                # 2. Try Google Translate if DeepL failed
                if not translation:
                    translation = self.translate_with_google(text, source_lang, target_lang)
                
                # 3. Try MyMemory if Google failed
                if not translation:
                    translation = self.translate_with_mymemory(text, source_lang, target_lang)
                
                # 4. Try LibreTranslate if MyMemory failed
                if not translation:
                    translation = self.translate_with_libre(text, source_lang, target_lang)
                
                # Check if translation was successful
                if translation:
                    # Update UI in the main thread
                    self.root.after(0, lambda: self.update_translation(translation, target_lang))
                else:
                    # Show error message if all translation services failed
                    self.root.after(0, lambda: self.show_translation_error())
            except Exception as e:
                # Show error message if an exception occurred
                error_msg = str(e)
                self.root.after(0, lambda: self.show_error(f"Translation error: {error_msg}"))
            finally:
                # Hide spinner when translation is complete
                self.root.after(0, self.hide_spinner)
        
        # Start translation thread
        threading.Thread(target=translation_thread, daemon=True).start()
    
    def update_translation(self, translation, target_lang):
        """Update the target textbox with the translation"""
        # Clear previous translation
        self.target_textbox.delete("1.0", "end")
        
        # Insert translation
        self.target_textbox.insert("1.0", translation)
        
        # Apply RTL or LTR formatting based on target language
        if target_lang in RTL_LANGUAGES:
            # Configure RTL text alignment properly
            self.target_textbox.tag_configure("rtl", justify="right")
            self.target_textbox.tag_add("rtl", "1.0", "end")
            # Force right alignment for the entire text box
            self.target_textbox.configure(justify="right")
        else:
            # Configure LTR text alignment
            self.target_textbox.tag_configure("ltr", justify="left")
            self.target_textbox.tag_add("ltr", "1.0", "end")
            # Reset to left alignment for the entire text box
            self.target_textbox.configure(justify="left")
        
        # Highlight the output area
        self.highlight_output()
        
        # Update status
        self.status_var.set("Translation complete")
    
    def show_translation_error(self):
        """Show error message when translation fails"""
        self.show_error("Translation failed. Please try again later or try a different language.")
        self.status_var.set("Translation failed")
    
    def clear_source(self):
        """Clear source text box"""
        self.source_textbox.delete("1.0", "end")
        self.status_var.set("Source text cleared")
    
    def clear_all(self):
        """Clear all text boxes"""
        self.source_textbox.delete("1.0", "end")
        self.target_textbox.delete("1.0", "end")
        self.status_var.set("All text cleared")
    
    def copy_translation(self):
        """Copy translation to clipboard"""
        translation = self.target_textbox.get("1.0", "end-1c")
        if translation:
            pyperclip.copy(translation)
            self.status_var.set("Translation copied to clipboard")
        else:
            self.status_var.set("Nothing to copy")

# Main application
if __name__ == "__main__":
    root = ctk.CTk()
    app = TranslatorApp(root)
    root.mainloop()