Overview
ResearchPioneer is an AI-assisted document question-answering
project designed to help users explore research material and web-based
documents without having to manually read every page.

The interface provides fields for submitting up to three URLs and a
query box for asking questions about the supplied material. The
underlying notebook prototype demonstrates a Retrieval-Augmented
Generation (RAG) workflow: documents are loaded from URLs, divided
into smaller chunks, converted into vector embeddings, indexed for
similarity search, and passed to a language model to generate a
context-grounded response with source references.

The repository is named Equity-Research-Analysis-Tool. The current
implementation also demonstrates the broader document-research workflow
that powers the ResearchPioneer interface.
Key capabilities
- URL-based document ingestion --- provide web-page URLs as source
  material.
- Document processing --- extract text from loaded pages and split
  it into manageable chunks.
- Semantic retrieval --- represent document chunks as embeddings
  and retrieve relevant content for a query.
- Vector indexing --- use FAISS for similarity-based retrieval.
- Question answering --- ask natural-language questions about the
  indexed material.
- Source-aware responses --- use LangChain's retrieval QA chain
  with source support.
- Simple research interface --- a dark-themed interface with URL
  inputs and a central query field.
Current scope: The repository contains notebook-based RAG
experiments and a UI screenshot. Treat this as an evolving
project/prototype; the exact production deployment entry point and
complete application wiring are not yet documented in the repository.

<img width="1200" height="600" alt="ChatGPT Image Nov 25, 2026 at 12_22_23 AM" src="https://github.com/user-attachments/assets/5fcac4a5-e7c1-4fdd-bdb3-f4ad4cfb04d2" />


How it works
      User supplies source URLs
                 |
                 v
       URL document loader
       (UnstructuredURLLoader)
                 |
                 v
        Extracted page content
                 |
                 v
       Recursive text splitting
       (chunk size: 1000
        overlap: 200)
                 |
                 v
       Embedding generation
       (Google Gemini Embeddings)
                 |
                 v
          FAISS vector index
                 |
                 v
        User submits a query
                 |
                 v
       Relevant chunks retrieved
                 |
                 v
       Groq-hosted language model
                 |
                 v
      Answer with source references

      RAG pipeline
1. Load: UnstructuredURLLoader retrieves and extracts content
   from the supplied URLs.
2. Split: RecursiveCharacterTextSplitter divides the documents
   into chunks. The notebook prototype uses a chunk size of 1000 and
   an overlap of 200.
3. Embed: GoogleGenerativeAIEmbeddings converts the chunks into
   vector representations.
4. Index: LangChain's FAISS vector store builds a searchable index
   from the document embeddings.
5. Retrieve: The user's question is used to retrieve relevant
   chunks from the vector store.
6. Generate: RetrievalQAWithSourcesChain sends the retrieved
   context and question to a Groq-hosted chat model and produces an
   answer with source information.
Technology stack
  Component               Technology                         Purpose
  Language                Python                             Core implementation

  LLM orchestration       LangChain                          Document and retrieval
pipeline

  URL ingestion           Unstructured /                     Load and extract
UnstructuredURLLoader            web-page content

  Text splitting          RecursiveCharacterTextSplitter   Chunk long documents

  Embeddings              Google Gemini Embeddings           Convert text into
vectors

  Vector database         FAISS                              Similarity search over
document chunks

  LLM inference           Groq API via ChatGroq            Generate answers from
retrieved context

  Notebook environment    Jupyter / Google Colab             Experimentation and
development
UI                      Streamlit-based interface (as      User interaction
represented by the project UI)
The notebook currently configures the Groq model as
openai/gpt-oss-120b. Model availability and API support depend on the
provider and may change.


Repository structure
Equity-Research-Analysis-Tool/
│
├── Equity_research_tool.ipynb   # Main notebook: URL ingestion and RAG workflow
├── retrieval.ipynb              # Retrieval-related experiments
├── gemini_api_use.ipynb         # Gemini API experiments
├── requirements.txt             # Python dependency list
├── langchain_2/                 # Additional LangChain-related project material
├── notebook/                    # Notebook/project resources
└── README.md

The folder contents may evolve as development continues. Open the
notebooks to inspect the latest implementation details.
Getting started


1. Clone the repository
git clone https://github.com/Sayak-coder/Equity-Research-Analysis-Tool.git
cd Equity-Research-Analysis-Tool

2. Create and activate a virtual environment
python -m venv .venv

macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\activate
3. Install dependencies
The project uses the packages below across its notebooks. Install them
in the active environment:
python -m pip install --upgrade pip
python -m pip install \
  langchain \
  langchain-classic \
  langchain-community \
  langchain-text-splitters \
  langchain-groq \
  langchain-google-genai \
  unstructured \
  sentence-transformers \
  faiss-cpu \
  streamlit \
  pandas \
  numpy
If you prefer pip install -r requirements.txt, first ensure the
version specifiers in that file use valid pip syntax (for example,
package==version or package>=version). The dependency file in the
repository may need normalisation before it can be installed reliably.
4. Configure API keys
The RAG notebook uses Google Gemini for embeddings and Groq for
language-model inference. Create API keys with the respective providers
and keep them private.

For a local Python environment, set the keys as environment variables:

macOS / Linux
export GEMINI_API_KEY="your_gemini_api_key"
export GROQ_API_KEY="your_groq_api_key"
Windows PowerShell
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:GROQ_API_KEY="your_groq_api_key"
In Google Colab, use Secrets (the key icon in the left sidebar)
rather than hard-coding credentials in notebook cells. The notebook's
current examples read secrets named gen_ai and groq; update the
variable names in the notebook if your Colab secret names differ.

Never commit API keys, .env files containing secrets, or provider
credentials to GitHub.
5. Run the notebook prototype
Open the repository in Jupyter Notebook or Google Colab and run:
Equity_research_tool.ipynb
Run the cells in order. The notebook demonstrates the document-loading,
chunking, embedding, FAISS indexing, retrieval, and question-answering
stages.
The repository does not currently document a definitive Streamlit
application filename or launch command. Once the UI entry-point script
is added or identified, document its exact command here (for example,
streamlit run <app-file>.py). Do not assume the notebook itself
launches the web interface.

Using the interface
The ResearchPioneer interface is designed around a straightforward
workflow:
1. Enter a research-paper or document URL in the URL fields on the
   left.
2. Add additional URLs if you want to work across multiple sources (up
   to the three fields currently shown in the interface).
3. Select Process URLs to begin source processing.
4. Enter a question in the main query field.
5. Submit the query using the application's query interaction and
   review the generated response.
The exact processing and submission controls may differ as the interface
implementation develops.

Configuration notes
  Setting                  Current notebook example
  Text chunk size          1000 characters
Chunk overlap            200 characters
Embedding integration    Google Gemini
Vector store             FAISS
Chat model integration   Groq
Chat model identifier    openai/gpt-oss-120b
Temperature              0.6
Maximum output tokens    500

These are prototype settings from the notebook, not universal
recommendations. Tune them based on document length, retrieval quality,
latency, and the capabilities of the selected model.

Limitations and responsible use
- The quality of answers depends on whether the supplied URLs are
  reachable and their content can be extracted correctly.
- Some websites block automated retrieval, require authentication, or
  render content dynamically. Such pages may not load as expected.
- Retrieval can miss relevant passages if the source text is noisy,
  chunking is unsuitable, or the query is ambiguous.
- Language-model output can be incomplete or incorrect. Verify
  important claims against the original source documents.
- Source references help with traceability, but they do not replace
  checking the cited material.
- Do not use generated output as a substitute for professional
  financial, legal, medical, or investment advice.
  
Roadmap
Potential next steps for the project include:
- [ ] Complete and document the web application entry point.
- [ ] Connect the URL-processing interface to the RAG pipeline.
- [ ] Add URL validation and clearer processing/error states.
- [ ] Display retrieved passages and source links alongside answers.
- [ ] Support persistent vector indexes to avoid reprocessing the same
  sources.
- [ ] Add document-level summaries and structured research notes.
- [ ] Improve dependency pinning and add a reproducible environment
  configuration.
- [ ] Add automated tests for ingestion, retrieval, and response
  generation.
- [ ] Add deployment instructions and a public demo when the app is
  deployment-ready.

Contributing
Contributions, suggestions, and bug reports are welcome.
1. Fork the repository.
2. Create a feature branch:
   git checkout -b feature/your-feature-name
3. Commit your changes:
   git commit -m "Add: your feature"
4. Push the branch and open a Pull Request.
For major changes, open an issue first to discuss the proposed update.

Author
Sayak Biswas
- GitHub: @Sayak-coder
- Repository:
  Equity-Research-Analysis-Tool
  
License
No license is currently specified in the repository. Unless a license is
added, the project should not be assumed to be available for
unrestricted reuse, modification, or redistribution.
