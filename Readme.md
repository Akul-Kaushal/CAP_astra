# Project ASTRA (Advanced Smart Task Recognition and Assistance)

Project ASTRA is an AI-powered Smart Home Assistant designed to **recognize user intent**, **interpret gestures**, and **assist in real-time tasks** using a Raspberry Pi. It combines **LLM-based RAG**, **computer vision**, **IoT integration**, and **AR projection guidance** to build the next generation of interactive assistants.


## Features (In Progress)

- **Smart RAG** (Retrieval-Augmented Generation) with Gemini API
- **Semantic Search** over text manuals using vector embeddings
- **Gesture Recognition** for intuitive hands-free interaction
- **Task Guidance** via projected augmented reality
- **Modular architecture** for scalability and component separation



## 🗂️ Project Structure

```plaintext
PROJECT_ASTRA/
├── client/
│   └── client.py               # CLI/local interface for user queries
├── data/
│   └── *.txt                   # Task instruction manuals (e.g., cooking.txt)
├── logs/
│   └── query_log.jsonl         # Stored prompt-response logs
├── server/
│   ├── server.py               # FastAPI backend
│   ├── gemini_api.py           # Gemini API wrapper
│   ├── semantic_search.py      # Semantic search logic
│   └── gemini_embedding.py     # Embedding generation logic
├── shared/                     # Shared utilities/configs (for future use)
├── .env                        # API key and environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and guide
```



## Setup Instructions

1. **Clone the Repository**

```bash
Copy
git clone https://github.com/Akul-Kaushal/CAP_astra.git
cd CAP_astra
Create and Activate Virtual Environment
```

```bash
Copy
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
Copy
pip install -r requirements.txt
```

3. **Set Environment Variables**

Create a .env file:

```env
Copy
GEMINI_API_KEY=your_api_key_here
```

## Contributing to ASTRA
Here's how to do it right:

✅ Fork & Commit Instructions
Fork this repository using the GitHub "Fork" button.

1. **Clone your forked repo locally:**

```bash
Copy
git clone https://github.com/YOUR_USERNAME/PROJECT_ASTRA.git
cd PROJECT_ASTRA
```

2. **Create a new branch for your feature or fix:**

```bash
Copy
git checkout -b your-feature-name
```

3. **Make your changes only in your fork.**

```bash
Copy
git add .
git commit -m "Add: Description of your change"
git push origin your-feature-name
```

4. **Open a Pull Request (PR) from your fork to the original repository:**

```plaintext
Title: Clearly describe your change

Description: Add context, motivation, or screenshots if needed
```



## Future Plans
- Integrate OpenCV-based gesture recognition

- Add dynamic task execution for IoT devices

- Support real-time AR overlays using projection mapping

- Deploy as local service on Raspberry Pi with web UI

