import ollama
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_epub(file_path):
    book = epub.read_epub(file_path)
    text = []
    for item in book.get_items():
        if item.get_type() == 9:  # EPUB document type (text)
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text.append(soup.get_text())
    return text  # Return list of pages

def chat_loop(model, book_pages):
    messages = []
    book_content = '\n'.join(book_pages)
    system_prompt = ("You have read this whole book. Now you have it as your memory. "
                     "If I ask you, you need to recite it, every character correctly. "
                     "If I don't ask about the book, you don't mention it. "
                     "You are a general LLM with this book as your knowledge. "
                     "Be an assistant to me and if I ask you, read me pages from the book.")
    messages.append({"role": "system", "content": system_prompt})
    
    print("Chat started. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        if "read me the first" in user_input.lower() and "pages" in user_input.lower():
            try:
                num_pages = int(user_input.split(" ")[-2])  # Extract number from input
                response = '\n\n'.join(book_pages[:num_pages])
            except:
                response = "I couldn't determine the number of pages. Please specify again."
        else:
            messages.append({"role": "user", "content": user_input})
            response = ollama.chat(model=model, messages=messages)['message']['content']
            messages.append({"role": "assistant", "content": response})
        
        print(f"LLM: {response}")

if __name__ == "__main__":
    model_name = 'llama3.2'
    epub_path = "/home/mihailov/Downloads/CanWeTrustTheGospels.epub"  # Change to your EPUB file path
    book_pages = extract_text_from_epub(epub_path)
    chat_loop(model_name, book_pages)
