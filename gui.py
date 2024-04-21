import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal, QObject, QTimer
from PySide6.QtGui import QTextCursor
import queue
import threading
import google.generativeai as genai
import pyttsx3

class AI(QObject):
    response_received = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.result_queue = queue.Queue()
        self.start_model()

    def start_model(self):
        genai.configure(api_key="AIzaSyC8OjyoyM3UUU9G8gTs3jzSSnfwYjiei6M")
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        instruction = """In this chat, respond as if you are talking to a student. If you are asked who you are, respond that you are TutorAI, 
        and you are here to help. If the conversation starts to go off task from things that are educational, try to gently lean the conversation back toward either
        something they were previously talking about or a new idea. If a student speaks another language, switch your language to make it so they can understand you and don't
        say anything else in English unless they switch."""
        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", safety_settings=safety_settings, system_instruction=instruction)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, question):
        response = self.chat.send_message(question)
        self.result_queue.put(response)
        self.response_received.emit(response.text.replace("**", "").replace("#", ""))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TutorAI")
        self.setFixedSize(640, 480)
        self.tts = False

        self.main = QWidget(self)
        self.main.setGeometry(0, 0, 800, 600)
        self.main.setStyleSheet("background-color: #131624;")

        self.rectangle1 = QWidget(self.main)
        self.rectangle1.setGeometry(10, 10, 621, 460)
        self.rectangle1.setStyleSheet("background-color: #1e2338; border-radius: 15px;")

        self.chat_history = QTextEdit(self.rectangle1)
        self.chat_history.setGeometry(10, 10, 610, 400)
        self.chat_history.setStyleSheet("color: #ffffff; background-color: transparent;")
        self.chat_history.setReadOnly(True)

        self.rectangle2 = QWidget(self.main)
        self.rectangle2.setGeometry(24, 418, 594, 43)
        self.rectangle2.setStyleSheet("background-color: #131624; border-radius: 15px;")

        self.messageInput = QLineEdit(self.rectangle2)
        self.messageInput.setGeometry(8, 13, 483, 17)
        self.messageInput.setStyleSheet("color: #ffffff; background-color: transparent;")
        self.messageInput.returnPressed.connect(self.send_message)

        self.sendButton = QPushButton(self.main)
        self.sendButton.setGeometry(525, 423, 87, 34)
        self.sendButton.setText("Send")
        self.sendButton.setStyleSheet("border: 2px solid white; border-radius: 15px; color: white;")
        self.sendButton.clicked.connect(self.send_message)
        
        self.ttsButton = QPushButton(self.main)
        self.ttsButton.setGeometry(580, 380, 34, 34)
        self.ttsButton.setText("TTS")
        self.ttsButton.setStyleSheet("border: 2px solid black; border-radius: 15px; color: black;")
        self.ttsButton.clicked.connect(self.toggle_tts)
        

        self.ai = AI()
        self.ai.response_received.connect(self.display_response)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_response)
        self.timer.start(100)  # Check every 100 ms for a new response

    def send_message(self):
        question = self.messageInput.text()
        if question:
            self.chat_history.append("You: " + question)
            self.chat_history.append("\nTutorAI is thinking...")
            self.ai_thread = threading.Thread(target=self.ai.send_message, args=(question,))
            self.ai_thread.start()
            self.messageInput.clear()
            
    def toggle_tts(self):
        if self.tts == False:
            self.tts = True
            self.ttsButton.setStyleSheet("border: 2px solid white; border-radius: 15px; color: white;")
        else:
            self.tts = False
            self.ttsButton.setStyleSheet("border: 2px solid black; border-radius: 15px; color: black;")

    def display_response(self, response):
        self.print_text_animated("\nTutorAI: " + response)
        if self.tts:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id) 
            engine.say(self.full_text[9:])
            engine.runAndWait()


    def print_text_animated(self, text):
        self.current_text = ""
        self.full_text = text
        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_text)
        self.timer.start(10)  # Adjust the interval for typing speed

    def animate_text(self):
        if self.index < len(self.full_text):
            self.current_text += self.full_text[self.index]
            self.chat_history.insertPlainText(self.full_text[self.index])  # Append new text horizontally
            self.index += 1
            #scrolls to bottom
            self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        else:
            self.timer.stop()
            self.remove_thinking_message()

    def remove_thinking_message(self):
        # Find the position of "TutorAI is thinking..."
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.Start)
        while cursor.movePosition(QTextCursor.NextBlock):
            if "TutorAI is thinking..." in cursor.block().text():
                # Remove the "TutorAI is thinking..." message
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                break

    def check_for_response(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
