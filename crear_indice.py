import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

DOCS_DIR = "documentos"
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)
    print("Carpeta 'documentos' creada. Mete ahí tus PDF/TXT y vuelve a ejecutar.")
    exit()

docs = PyPDFDirectoryLoader(DOCS_DIR).load()
docs += DirectoryLoader(DOCS_DIR, glob="*.txt", loader_cls=TextLoader,
                        loader_kwargs={"encoding": "utf-8"}).load()

if not docs:
    print("No hay archivos en 'documentos'.")
    exit()

# Cada trozo empieza con el nombre del documento para dar contexto
for d in docs:
    nombre = os.path.basename(d.metadata.get("source", "documento"))
    d.page_content = f"[Documento: {nombre}]\n{d.page_content}"

splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=120)
trozos = splitter.split_documents(docs)
print(f"{len(docs)} páginas -> {len(trozos)} fragmentos")

embeddings = FastEmbedEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vectorstore = FAISS.from_documents(trozos, embeddings)
vectorstore.save_local("faiss_index")
print("Índice creado en 'faiss_index'.")
