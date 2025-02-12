Project Documentation: AI for Extracting and Interacting with Text from EPUB Books
Functionality
The system extracts text from EPUB books, generates embeddings, and answers questions based on these embeddings.

Architecture
Text is extracted from EPUB, embeddings are generated using LLaMA 3.2, stored in ChromaDB, and voice command interaction is enabled.

Implementation
Text is extracted from the EPUB, split into chunks, embeddings are generated using LLaMA 3.2, and stored in ChromaDB.

Data Model
Text chunks and their embeddings are stored in ChromaDB with unique identifiers.

Used Datasets
EPUB files are used for text extraction, and LLaMA 3.2 is used for generating embeddings.

Configuration
The project runs on Python 3.11 in a Linux environment using a virtual environment (venv).

Used Technologies and Libraries
ebooklib for EPUB processing, BeautifulSoup for parsing, Ollama for LLaMA, and ChromaDB for storage.

Problems and Solutions
Text splitting into manageable chunks and using ChromaDB for fast data retrieval.

References
ebooklib: For working with EPUB files.
ChromaDB: For storing embeddings.
Ollama API: For using LLaMA 3.2.
BeautifulSoup: For HTML parsing.
