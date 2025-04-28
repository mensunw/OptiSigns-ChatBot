# Chunking Strategy 
When creating the Vector Store, I relied on OpenAI’s default chunking behavior. OpenAI automatically splits each uploaded Markdown file into smaller chunks optimized for semantic search, typically about 800 tokens per chunk and an overlap of 400 tokens (from OpenAI's official documentation). Embeddings were generated using the text-embedding-3-large model (256 dimensions), and the Assistant retrieves up to 20 relevant chunks per query.

# Example Chatbot Output
![optisign-chatbot-example](https://github.com/user-attachments/assets/262c0fbc-1763-42ef-83df-23e5102ada36)
