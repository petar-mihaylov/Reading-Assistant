import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import requests, json
from sklearn.decomposition import PCA
from ebooklib import epub
from bs4 import BeautifulSoup
import chromadb
import ollama
import numpy as np

def load_epub(file_path):
    book = epub.read_epub(file_path)
    texts = []
    for item in book.get_items():
        if item.get_type() == 9:
            soup = BeautifulSoup(item.content, "html.parser")
            texts.append(soup.get_text())
    return texts

def chunk_text(text, chunk_size=512):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def generate_embedding(text):
    res = ollama.embeddings(model="llama3.2", prompt=text)
    return res["embedding"]

file_path = "/home/mihailov/Downloads/CanWeTrustTheGospels.epub"
book_text = " ".join(load_epub(file_path))
chunks = chunk_text(book_text)

embeddings = [generate_embedding(chunk) for chunk in chunks]
pca_model = PCA(n_components=50)
reduced_embeddings = pca_model.fit_transform(embeddings)

client = chromadb.PersistentClient(path="./chroma_db")
try:
    client.delete_collection("epub_book")
except Exception:
    pass
collection = client.create_collection(name="epub_book")
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        embeddings=[reduced_embeddings[i].tolist()],
        documents=[chunk]
    )

def retrieve_relevant_chunks(query, top_k=3):
    q_embed = generate_embedding(query)
    q_reduced = pca_model.transform([q_embed])[0].tolist()
    results = collection.query(query_embeddings=[q_reduced], n_results=top_k)
    return results["documents"][0]

def generate_response(query):
    context = " ".join(retrieve_relevant_chunks(query))
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    url = "http://localhost:11434/api/generate"  # Adjust if necessary
    payload = {"model": "llama3.2", "prompt": prompt, "stream": True}
    response = requests.post(url, json=payload, stream=True)
    full_output = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                full_output += data.get("response", "")
                if data.get("done"):
                    break
            except Exception:
                continue
    return full_output

query = "How does the author answet the debate about Jesus' resurection?"
print("Answer:", generate_response(query))
