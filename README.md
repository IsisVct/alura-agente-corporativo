# 🏢 Agente Corporativo de Inteligência Artificial — Neo Bank

Bem-vindo ao repositório do **Agente Corporativo de IA**, desenvolvido como parte do desafio técnico da Alura em parceria com a Oracle Next Education (ONE)!

## 📖 Sobre o Projeto
Este projeto consiste em um assistente virtual conversacional inteligente voltado para o ambiente corporativo de uma fintech hipotética (**Neo Bank**). O agente atua como uma base de conhecimento centralizada baseada em **RAG (Retrieval-Augmented Generation)**, capaz de responder dúvidas de colaboradores consultando documentos internos de diferentes domínios organizacionais (como RH, TI, Compliance, Operações e Jurídico) com controle estrito contra alucinações e fallback estruturado para e-mails de suporte.

---

## 🚀 Funcionalidades
* **Recuperação Contextual (RAG):** Busca semântica precisa em documentos internos (PDFs, planilhas e relatórios).
* **Processamento de Linguagem Natural Avançado:** Respostas estruturadas geradas via modelos de altíssima velocidade integrados pela API da **Groq**.
* **Controle de Alucinação & Fallback:** O agente é instruído a responder estritamente com base no contexto recuperado e direciona para e-mails de setores específicos (RH, TI, Jurídico) caso não encontre a informação.
* **Interface Moderna em React:** Chat interativo responsivo integrado via API REST com FastAPI.
* **Deploy em Nuvem:** Totalmente funcional, hospedado em produção no **Render**.

---

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **Inteligência Artificial & Orquestração:** LangChain, LangChain-Groq, HuggingFace Embeddings (`all-MiniLM-L6-v2`)
* **Banco de Dados Vetorial:** ChromaDB
* **Processamento de Dados:** Pandas, OpenPyXL, PyPDF, LangChain Community
* **Frontend:** React, Vite, JavaScript / CSS moderno
* **Deploy & Hospedagem:** Render (Web Service)

---
## 🎥 Demonstração em Nuvem
<img width="1018" height="948" alt="image" src="https://github.com/user-attachments/assets/5c2fe7ab-cf30-4bb2-98fa-60b4b51153e0" />


---


## 📁 Estrutura do Projeto
```text
/
├── data/                 # Base de conhecimento (documentos fictícios da fintech)
├── frontend/             # Aplicação front-end em React + Vite
├── src/                  # Código fonte principal da API e do Agente RAG
│   ├── agente_rag.py     # Configuração da cadeia LangChain, retriever e prompt
│   ├── main.py           # Endpoints do FastAPI e montagem do front-end estático
│   └── processador_docs.py # Script de leitura e indexação dos documentos no ChromaDB
├── requirements.txt      # Dependências do projeto Python
├── render.yaml           # Configuração de build e deploy automatizado para o Render
└── README.md             # Documentação oficial do projeto
