import speech_recognition as sr
from translate import Translator
import pyttsx3
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext, ttk

def create_circle_button(master, text, command):
    canvas = tk.Canvas(master, width=100, height=100, bg='light blue', highlightthickness=0)
    canvas.create_oval(10, 10, 90, 90, fill='white', outline='light blue')
    
    if len(text) > 15:  
        font_size = 8
    else:
        font_size = 10  
    
    label = tk.Label(master, text=text, bg='white', fg='black', borderwidth=0, relief='flat', 
                     cursor='hand2', font=('Arial', font_size))
    
    label.bind('<Button-1>', lambda event, cmd=command: cmd())
    label.bind('<Enter>', lambda e: canvas.itemconfig(1, fill='black'))
    label.bind('<Leave>', lambda e: canvas.itemconfig(1, fill='white'))
    
    canvas.create_window(50, 50, window=label)
    return canvas, label

class VoiceToTextApp:
    def __init__(self, root):
        self.recognizer = sr.Recognizer()
        self.root = root
        self.queue = queue.Queue()  
        self.running = True  
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.title('Voice to Text App')
        self.engine = pyttsx3.init()
        self.root.configure(bg='light blue')
        
        self.start_canvas, self.start_button = create_circle_button(root, '\nStart\nListening\n', self.start_listening)
        self.start_canvas.pack(pady=10)

        self.stop_canvas, self.stop_button = create_circle_button(root, '\nStop\nListening\n', self.stop_listening)
        self.stop_button.config(fg='gray')
        self.stop_canvas.pack(pady=10)

        self.language_options = {
            'Afrikaans': 'af',
            'Arabic': 'ar',
            'Bengali': 'bn',
            'Chinese': 'zh-cn',
            'Dutch': 'nl',
            'English': 'en',
            'French': 'fr',
            'German': 'de',
            'Greek': 'el',
            'Hindi': 'hi',
            'Italian': 'it',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Spanish': 'es',
            'Swahili': 'sw',
            'Swedish': 'sv',
            'Tagalog': 'tl',
            'Turkish': 'tr',
            'Ukrainian': 'uk',
            'Vietnamese': 'vi',
        }

        self.lang_var = tk.StringVar(root)
        self.lang_var.set('English')  # default language

        self.dropdown = ttk.Combobox(root, textvariable=self.lang_var, values=list(self.language_options.keys()))
        self.dropdown.bind('<<ComboboxSelected>>', self.on_language_change)
        self.dropdown.pack(pady=10)

        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, bg='white', fg='black')
        self.output_area.pack(pady=20)

        self.translation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, bg='white', fg='black')
        self.translation_area.pack(pady=20)
        self.translation_area.config(state=tk.DISABLED)

        self.translate_canvas, self.translate_button = create_circle_button(root, '\nTranslate\n', self.translate_typed_text)
        self.translate_canvas.pack(pady=10)

        self.speak_canvas, self.speak_button = create_circle_button(root, '\nRead\nTranslation\n', self.speak_translation)
        self.speak_canvas.pack(pady=10)

        self.listening = False
        self.last_transcribed_text = None
        self.root.after(100, self.check_queue)

    def handle_queue_messages(self):
        while self.running:
            try:
                message = self.queue.get_nowait()
                if message == 'update_gui':
                    self.root.update()
                    self.update_button_color()
                elif message == 'update_button_color':
                    self.update_button_color()
                elif isinstance(message, str): 
                    self._update_text_gui(message)
            except queue.Empty:
                break


    def check_queue(self):
        self.handle_queue_messages()
        self.root.after(100, self.check_queue)

    def on_closing(self):
        self.running = False
        self.engine.stop() 
        self.root.destroy()

    def translate_typed_text(self):
        text = self.output_area.get('1.0', tk.END).strip()
        if text:
            self.last_transcribed_text = text
            self.update_translation_of_last_text()

    def on_language_change(self, event=None):
        if self.last_transcribed_text:
            self.update_translation_of_last_text()

    def update_text(self, text):
        self.queue.put(text)

    def _update_text_gui(self, text):
        self.output_area.insert(tk.END, text + '\n')

    def update_button_color(self):
        if self.listening:
            self.start_canvas.itemconfig(1, fill='red')
        else:
            self.start_canvas.itemconfig(1, fill='white')

    def update_translation(self, text):
        self.translation_area.config(state=tk.NORMAL)
        self.translation_area.delete('1.0', tk.END)  
        self.translation_area.insert(tk.END, text)
        self.translation_area.config(state=tk.DISABLED)
        self.last_translation = text  

    def speak_translation(self):
        self.speak_button.config(fg='gray')
        if hasattr(self, 'last_translation'):
            self.engine.say(self.last_translation)
            self.engine.runAndWait()
        self.speak_button.config(fg='black')

    def update_translation_of_last_text(self):
        target_language = self.language_options[self.lang_var.get()]
        translator = Translator(to_lang=target_language)
        translation = translator.translate(self.last_transcribed_text)
        self.update_translation(translation)

    def start_listening(self):
        print('Start Listening called')
        self.listening = True
        self.start_button.config(fg='red') 
        self.stop_button.config(fg='black', state=tk.NORMAL) 
        threading.Thread(target=self.listen).start()
        self.update_button_color()

    def stop_listening(self):
        print('Stop Listening called')
        self.listening = False
        self.stop_button.config(fg='gray', state=tk.DISABLED) 
        self.start_button.config(fg='black') 
        self.update_button_color()

    def listen(self):
        with sr.Microphone() as source:
            while self.listening:
                if not self.listening:
                    continue
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
                    self.update_text(text)
                except sr.UnknownValueError:
                    self.update_text('Sorry, could not recognize the audio. Please speak more clearly.')
                except sr.RequestError:
                    self.update_text('API unavailable. Please check your internet connection.')
                except sr.WaitTimeoutError:
                    pass
                self.queue.put('update_gui')
                self.queue.put('update_button_color')

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = VoiceToTextApp(root)
    app.run()
