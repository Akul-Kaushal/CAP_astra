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
├── client/                     # Client-side logic for input & interaction
│   ├── routes/                  # Client-side route handlers
│   ├── uploads/                 # Client-side uploaded data
│   ├── client_readme.md         # Documentation for client module
│   ├── gesture_camera.py        # Handles camera input for gesture control
│   ├── gesture_control.py       # Gesture recognition & mapping logic
│   ├── parser.py                # Data parsing and processing logic
│   ├── speech.py                # Speech recognition and handling
│   └── vision_input.py          # Vision-based input processing
│
├── server/                     # Backend logic and routes
│   ├── data/                   # Server-side stored data
│   ├── image/                  # Temporary uploaded image storage
│   ├── routes/                 # API route definitions
│   │   ├── ask_image.py         # Endpoint for image-based Gemini queries
│   │   ├── ask.py               # Endpoint for text-based queries
│   │   ├── notion_route.py      # Endpoint for Notion integration
│   │   └── upload.py            # Endpoint for file uploads
│   ├── embedding_index.pkl      # Precomputed embedding index (pickle)
│   ├── gemini_api.py            # Wrapper for Gemini API calls
│   ├── gemini_embedding.py      # Embedding generation logic
│   ├── image.py                 # Image processing utilities
│   ├── logger.py                # Logging utilities
│   ├── notion.py                # Notion API integration logic
│   ├── pdf_reader.py            # PDF parsing and reading utilities
│   ├── semantic_search.py       # Semantic search functionality
│   ├── server_readme.md         # Server-side README / documentation
│   ├── server.py                # FastAPI backend entry point
│   ├── z_generating_pickle.py   # Script to generate embeddings pickle
│   └── z_test.py                # Test scripts and experiments
│
├── shared/                      # Shared configs/utilities
├── venv/                        # Python virtual environment
├── .env                         # Environment variables (API keys, etc.)
├── .gitignore                   # Git ignore rules
├── Readme.md                    # Project overview & guide
└── requirements.txt             # Python dependencies
```



## Setup Instructions

1. **Clone the Repository**

```bash
 
git clone https://github.com/Akul-Kaushal/CAP_astra.git
cd CAP_astra
Create and Activate Virtual Environment
```

```bash
 
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
 
pip install -r requirements.txt
```

3. **Set Environment Variables**

Create a .env file:

```env
 
GEMINI_API_KEY=your_api_key_here
```

## Contributing to ASTRA
Here's how to do it right:

✅ Fork & Commit Instructions
Fork this repository using the GitHub "Fork" button.

1. **Clone your forked repo locally:**

```bash
 
git clone https://github.com/YOUR_USERNAME/PROJECT_ASTRA.git
cd PROJECT_ASTRA
```

2. **Create a new branch for your feature or fix:**

```bash
 
git checkout -b your-feature-name
```

3. **Make your changes only in your fork.**

```bash
 
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

