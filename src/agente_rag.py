import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

@lru_cache(maxsize=1)
def obter_agente_rag():
    """Cria a cadeia RAG somente quando ela for necessária, evitando carga pesada no startup."""
    return criar_cadeia_rag()


def obter_retriever(caminho_db="./chroma_db", top_k=4):
    """
    Carrega o banco ChromaDB existente e instancia o Retriever 
    com o mesmo modelo de embedding da indexação.
    """
    modelo_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    banco_vetorial = Chroma(
        persist_directory=caminho_db,
        embedding_function=modelo_embedding
    )
    
    retriever = banco_vetorial.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    return retriever

def formatar_contexto(documentos):
    """
    Montagem do contexto:
    Une os trechos selecionados preservando metadados de origem para citação.
    """
    blocos = []
    for doc in documentos:
        origem = doc.metadata.get("nome_arquivo", "Documento desconhecido")
        pagina = doc.metadata.get("page", None)
        cabecalho = f"[Fonte: {origem}" + (f" | Página: {pagina+1}]" if pagina is not None else "]")
        blocos.append(f"{cabecalho}\n{doc.page_content}")
        
    return "\n\n---\n\n".join(blocos)

def criar_cadeia_rag():
    """
    Monta a cadeia completa: Pergunta -> Recuperação -> Contexto + Prompt -> LLM -> Resposta
    """
    retriever = obter_retriever()

    llm = ChatGroq(
        model="qwen/qwen3.6-27b", 
        temperature=0.2
    )

    template_prompt = """Você é o Assistente Virtual Corporativo da nossa Fintech.
Seu objetivo é responder dúvidas de colaboradores baseando-se ESTRITAMENTE no contexto fornecido abaixo.

Diretrizes Operacionais:
1. Geração: Responda de forma clara, profissional e estruturada (use tópicos se facilitar a leitura).
2. Controle de Alucinação: Baseie sua resposta APENAS nas informações contidas no "Contexto Recuperado". Sob nenhuma circunstância utilize conhecimento prévio ou externo para preencher lacunas.
3. Citação de Fonte: Ao final de toda resposta, você DEVE citar o documento de origem no formato: 
   > 📄 Fontes consultadas: [nome_do_arquivo] (Página [X] ou Seção aplicável).

Diretriz de Fallback (MUITO IMPORTANTE):
Se o Contexto Recuperado não contiver informações suficientes ou exatas para responder à pergunta, NÃO INVENTE uma resposta. Informe claramente que não possui os dados e direcione o colaborador para os seguintes contatos internos, dependendo do tema:
- Dúvidas de RH, Férias e Benefícios: rh@fintech.com.br
- Dúvidas de TI, Acessos e Sistemas: suporte.ti@fintech.com.br
- Dúvidas de Compliance, Segurança e Jurídico: juridico@fintech.com.br
- Operações de Clientes e Tarifas: operacoes@fintech.com.br

Contexto Recuperado:
{context}

Pergunta do Colaborador:
{question}

Resposta Final:"""

    prompt = PromptTemplate.from_template(template_prompt)
    
    cadeia_rag = (
        {
            "context": retriever | formatar_contexto,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return cadeia_rag

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("Erro: A variável GROQ_API_KEY não foi encontrada no arquivo .env.")
    else:
        print("Inicializando o agente...")
        agente = criar_cadeia_rag()
        
        pergunta_teste = "Quais são os limites de transação via PIX no período noturno?"
        print(f"\nPergunta: {pergunta_teste}\n")
        
        resposta = agente.invoke(pergunta_teste)
        print("Resposta do Agente:")
        print(resposta)