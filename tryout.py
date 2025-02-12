import tkinter as tk
from tkinter import scrolledtext
import ollama

def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_box.insert(tk.END, f"You: {user_input}\n", "user")
    entry.delete(0, tk.END)
    
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": user_input}])
    reply = response["message"]["content"]
    chat_box.insert(tk.END, f"LLaMA: {reply}\n", "llama")
    chat_box.yview(tk.END)

# GUI Setup
root = tk.Tk()
root.title("LLaMA 3.2 Chatbox")
root.geometry("400x500")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='normal', height=20, width=50)
chat_box.tag_configure("user", foreground="blue")
chat_box.tag_configure("llama", foreground="green")
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, width=40)
entry.pack(pady=5, padx=10, side=tk.LEFT, expand=True, fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5, padx=10, side=tk.RIGHT)

root.mainloop()
