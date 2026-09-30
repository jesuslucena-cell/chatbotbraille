import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Crear carpeta 'documentos' si no existe
DOCS_DIR = "documentos"
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)
    print(f"Carpeta '{DOCS_DIR}' creada. Mete ahí tus archivos PDF o TXT y vuelve a ejecutar este script.")
    exit()

# 2. Cargar documentos
print("Cargando documentos desde la carpeta 'documentos'...")
loader_pdf = PyPDFDirectoryLoader(DOCS_DIR)
docs_pdf = loader_pdf.load()

loader_txt = DirectoryLoader(DOCS_DIR, glob="*.txt", loader_cls=TextLoader)
docs_txt = loader_txt.load()

todos_los_docs = docs_pdf + docs_txt

if not todos_los_docs:
    print("No se encontraron archivos en la carpeta 'documentos'. Añade PDFs o TXT y vuelve a probar.")
    exit()

print(f"Se cargaron {len(todos_los_docs)} archivo(s).")

# 3. Dividir el texto en fragmentos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
textos_divididos = text_splitter.split_documents(todos_los_docs)

# 4. Generar la base de datos de embeddings
print("Generando el índice de búsqueda (FAISS)...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

vectorstore = FAISS.from_documents(textos_divididos, embeddings)

# 5. Guardar el índice
vectorstore.save_local("faiss_index")
print("¡Éxito! Se ha creado/actualizado la carpeta 'faiss_index'.")
