import os 
import streamlit as st
import time 
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not google_api_key:
    raise RuntimeError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file.")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    google_api_key=google_api_key,
)

st.title("ResearchPioneer")
st.write("Welcome to ResearchPioneer! Not only read. Understand the paper")

st.sidebar.title("URLs")
st.sidebar.write("Enter your paper's URLs below")
process_url_clicked = st.sidebar.button("Process URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

main_placeholder = st.empty()
index_path = os.path.join(os.path.dirname(__file__), "faiss_store_gemini")

model = "openai/gpt-oss-120b"

llm = ChatGroq(
    model = model,
    temperature = 0
)

if process_url_clicked :
    if not urls:
        st.sidebar.error("please enter atleast one URL")
    else:
        loader = UnstructuredURLLoader(urls = urls)
        main_placeholder.text("Data Loading...Started...✅✅✅")
        data = loader.load()

        spliter = RecursiveCharacterTextSplitter(
            separators = ["\n\n", "\n", " ", "."],
            chunk_size = 1000,
            chunk_overlap = 200,
        )
        main_placeholder.text("Text Splitter...Started...✅✅✅")
        docs = spliter.split_documents(data)

        vectors = FAISS.from_documents(docs, embeddings)
        main_placeholder.text("Embedding Vector Started Building...✅✅✅")
        time.sleep(2)
        main_placeholder.text("Done... Now enter your query ✅✅✅")

        vectors.save_local(index_path)


query = st.text_input("Enter your query here")
if query:
    index_files = (
        os.path.join(index_path, "index.faiss"),
        os.path.join(index_path, "index.pkl"),
    )
    if all(os.path.isfile(path) for path in index_files):
        # Only load the index saved locally by this app; do not load untrusted pickle files.
        vectors = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        retriever = vectors.as_retriever(search_kwargs={"k": 8})
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            retriever=retriever,
        )
        result = chain({"question": query}, return_only_outputs = True)
        st.header("Answer")
        st.write(result["answer"])

        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")  # Split the sources by newline
            for source in sources_list:
                st.write(source)
    else:
        st.info("Process URLs first to create the Gemini embeddings index.")
