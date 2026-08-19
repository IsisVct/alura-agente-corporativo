import os
import shutil
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def carregar_e_processar_documentos(diretorio_dados="data"):
    documentos_processados = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    print(f"Iniciando varredura no diretório: {diretorio_dados}...")

    for arquivo in os.listdir(diretorio_dados):
        caminho_completo = os.path.join(diretorio_dados, arquivo)
        if not os.path.isfile(caminho_completo): continue

        docs_extraidos = []
        try:
            if arquivo.endswith(".pdf"):
                print(f"Processando PDF: {arquivo}")
                loader = PyPDFLoader(caminho_completo)
                docs_extraidos = loader.load()
                
            elif arquivo.endswith(".csv"):
                print(f"Processando CSV: {arquivo}")
                loader = CSVLoader(file_path=caminho_completo, encoding="utf-8")
                docs_extraidos = loader.load()
                
            elif arquivo.endswith(".xlsx"):
                print(f"Processando Excel: {arquivo}")
                df = pd.read_excel(caminho_completo)
                for index, row in df.iterrows():
                    conteudo_linha = " | ".join([f"{col}: {val}" for col, val in row.items()])
                    docs_extraidos.append(Document(page_content=conteudo_linha, metadata={"source": caminho_completo}))
            else:
                continue
            
            chunks = text_splitter.split_documents(docs_extraidos)
            
            for i, chunk in enumerate(chunks):
                chunk.metadata["categoria"] = "NeoBank_Docs"
                chunk.metadata["nome_arquivo"] = arquivo
                documentos_processados.append(chunk)
                
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    print(f"\nTotal de chunks gerados: {len(documentos_processados)}")
    return documentos_processados

def criar_banco_vetorial(chunks_de_texto):
    pasta_db = "./chroma_db"
    
    if os.path.exists(pasta_db):
        print("Apagando banco vetorial antigo...")
        shutil.rmtree(pasta_db)

    print("\nInicializando o modelo de Embeddings...")
    modelo_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Vetorizando os documentos e salvando no ChromaDB...")
    Chroma.from_documents(
        documents=chunks_de_texto,
        embedding=modelo_embedding,
        persist_directory=pasta_db
    )
    print(f"Indexação concluída! Banco atualizado na pasta: {pasta_db}")

if __name__ == "__main__":
    meus_chunks = carregar_e_processar_documentos()
    if meus_chunks:
        criar_banco_vetorial(meus_chunks)