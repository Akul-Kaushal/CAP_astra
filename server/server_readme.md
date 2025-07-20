# Server Setup & Operation Commands 

1. Clone or Navigate to the Project Directory
```bash
cd PROJECT_ASTRA/server
```

2. Install Python Dependencies
```bash
pip install -r ../requirements.txt
```

3. Set Your Gemini API Key
```bash
touch ../.env
echo "GEMINI_API_KEY=your_key_here" >> ../.env
```

4. Generate Embeddings from Manuals
```bash
python gemini_embedding.py
```

5. Run a Sample Query to Gemini with Context
```bash
python z_test.py
```

6. (Optional) Run the FastAPI Server (for /ask and /upload)
```bash
uvicorn server:app --reload --port 8000
```

## Directory structure
``` plaintext
/server/
  ├─ logger.py              
  ├─ gemini_embedding.py    
  ├─ query_gemini.py        ⬅ Used to perform Gemini-based question answering
  ├─ semantic_search.py     ⬅ Used by gemini_embedding/query_gemini
  └─ server.py              ⬅ FastAPI server (optional, for voice/camera interaction)
```
