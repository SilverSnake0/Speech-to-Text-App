# Speech to Text App

### Description:

The "Speech to Text App" is a simple user-friendly GUI application that translates spoken language into text in real-time. It provides users with the option to convert the transcribed text into different languages and have the translated text read out loud. This app was made as a fun project to explore and learn how similar voice-to-text and translation apps are created.

![voice to text app snapshot](\speech_to_text_screenshot.png)

### Features:

- Real-time Speech to Text Conversion: Convert your speech into written text in real-time with the intuitive user interface.
- Multi-Language Support: Choose from a wide range of languages for conversion, including but not limited to Afrikaans, Arabic, Bengali, Chinese, Dutch, English, French, German, Greek, Hindi, Italian, Japanese, Korean, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Turkish, Ukrainian, and Vietnamese.
- Text Translation: After transcribing your speech, you have the option to translate the written text into your chosen language.
- Voice Readout of Translation: Once translated, the app can read out the translated text.

### Dependencies:

- speech_recognition: Used for the core functionality of converting speech to text.
- pyttsx3: Provides the text-to-speech conversion feature.
- translate: Allows translation of transcribed text to various languages.
- tkinter: Used for creating the GUI.
- threading and queue: For handling asynchronous tasks without freezing the GUI.

### Usage:

You can start speaking by clicking the "Start Listening" button and stop it using the "Stop Listening" button. After your speech has been transcribed, choose a target language from the dropdown menu and click "Translate" to get the translated text. Finally, you can use the "Read Translation" button to hear the translated text. You can also directly enter the text into the first empty box for translation.

### Installation:

To set up the "Speech to Text App", make sure you have python and pip installed, and all the necessary dependencies installed. You can usually install these dependencies using pip by entering these commands in the terminal:

`pip install speechrecognition pyttsx3 translate tkinter`

Once you have all dependencies set up, simply download the script from this repository and run it. To start the application, simply run the script by opening the terminal, change directory into the folder the app is located, then enter `python speech_to_text.py`

### Known Issues:

- Read Translation Feature: The read translation feature is not accurate or may not work for certain languages.
- Performance Lag: There may be occasional lag when converting speech to text. This can be attributed to the time taken for processing audio data and the dependency on external online services (like Google's speech-to-text service), especially when there's a slow or unstable internet connection.

### Privacy:

This app values user privacy. All translations and voice transcriptions are conducted in real-time and are not stored on our servers unless the user intentionally saves them. The app utilizes [Google's translation API](https://cloud.google.com/translate/data-usage) for specific features; users are advised to familiarize themselves with Google's data usage policies. While efforts are made to protect user data, we cannot ensure absolute security. By using the app, users acknowledge potential risks and agree not to hold the app or its developers liable for any issues, damages, or losses. The app is released under the MIT License.
