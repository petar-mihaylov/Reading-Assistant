import ebooklib
from ebooklib import epub
import ollama
from bs4 import BeautifulSoup
import base64
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()

# Extract text and images from EPUB
def extract_epub_content(epub_path):
    book = epub.read_epub(epub_path)
    text_content = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text_content.append(soup.get_text())  # Extract text

    return "\n".join(text_content)

# Q&A with LLaMA
def ask_question(book_text, question):
    response = ollama.chat(model="llama3.2", messages=[
        {"role": "system", "content": "Answer the question based on the given text."},
        {"role": "user", "content": f"Context: {book_text}\nQuestion: {question}"}
    ])
    return response['message']['content']

# Voice input
def listen_for_question():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            question = recognizer.recognize_google(audio)
            print(f"🗣️ You asked: {question}")
            return question
        except sr.UnknownValueError:
            print("❌ Could not understand the question.")
        except sr.RequestError:
            print("❌ Speech recognition service unavailable.")
        return None

# Speak response
def speak_answer(answer):
    print(f"🔊 AI: {answer}")
    engine.say(answer)
    engine.runAndWait()

# Main function
def process_epub(epub_path):
    book_text = extract_epub_content(epub_path)

    while True:
        question = listen_for_question()
        if question and question.lower() in ["exit", "quit", "stop"]:
            print("👋 Exiting...")
            break
        if question:
            answer = ask_question(book_text, question)
            speak_answer(answer)

# Run the script
epub_file = "/home/mihailov/Downloads/CanWeTrustTheGospels.epub"  # Replace with your EPUB file
process_epub(epub_file)
