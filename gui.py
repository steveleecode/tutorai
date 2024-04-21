import sys
import time
from PySide6.QtWidgets import * #pip install PySide6
from PySide6.QtCore import QTimer, Qt, QRect, QPropertyAnimation
import google.generativeai as genai #pip install google-generativeai

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TutorAI")
        self.setFixedSize(640, 480)  # Adjuss the window size

        self.main = QWidget(self)
        self.main.setGeometry(0, 0, 800, 600)  # Adjust the size as needed
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
        #textInput.setFontPointSize(12)

        self.sendButton = QPushButton(self.main)
        self.sendButton.setGeometry(525, 423, 87, 34)
        self.sendButton.setText("Send")
        self.sendButton.setStyleSheet("border: 2px solid white; border-radius: 15px; color: white;")
        self.sendButton.clicked.connect(self.send_message)
        #roundButton1.setIconSize(24)
        
        self.start_model()

    def start_model(self):
        #SETUP AI
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
        something they were previously talking about or a new idea."""

        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",  safety_settings=safety_settings, system_instruction=instruction)
        self.chat = self.model.start_chat(history=[])



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
        else:
            self.timer.stop()


    def send_message(self):
        question = self.messageInput.text()
        if question:
            self.chat_history.append("You: " + question)
            response = self.chat.send_message(question)
            self.print_text_animated("\n\nTutorAI: " + response.text.replace("**", ""))
            self.messageInput.clear()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
