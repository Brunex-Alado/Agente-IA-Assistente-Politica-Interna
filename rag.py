import pathlib, re
from pathlib import Path
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

def carregar_pdfs(caminho: Path):
    docs = []
    for n in caminho.glob("*.pdf"):
        try:
            loader = PyMuPDFLoader(str(n))
            docs.extend(loader.load())
            print(f"Carregado com sucesso: {n.name}")
        except Exception as e:
            print(f"Erro ao carregar {n.name}: {e}")
    print(f"Total de documentos: {len(docs)}")
    return docs

def criar_rag(docs, api_key: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 4}
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
    prompt_rag = ChatPromptTemplate.from_messages([
        ("system",
         "Você é um Assistente de Políticas Internas (RH/IT) da empresa Carraro Desenvolvimento. "
         "Responda SOMENTE com base no contexto fornecido. "
         "Se não houver base suficiente, responda apenas 'Não sei'."),
        ("human", "Pergunta: {input}\n\nContexto:\n{context}")
    ])
    document_chain = create_stuff_documents_chain(llm, prompt_rag)

    return retriever, document_chain

# --- utilidades ---
def _clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def extrair_trecho(texto: str, query: str, janela: int = 240) -> str:
    txt = _clean_text(texto)
    termos = [t.lower() for t in re.findall(r"\w+", query or "") if len(t) >= 4]
    pos = -1
    for t in termos:
        pos = txt.lower().find(t)
        if pos != -1: break
    if pos == -1: pos = 0
    ini, fim = max(0, pos - janela//2), min(len(txt), pos + janela//2)
    return txt[ini:fim]

def formatar_citacoes(docs_rel: List, query: str) -> List[Dict]:
    cites, seen = [], set()
    for d in docs_rel:
        src = pathlib.Path(d.metadata.get("source", "")).name
        page = int(d.metadata.get("page", 0)) + 1
        key = (src, page)
        if key in seen: continue
        seen.add(key)
        cites.append({"documento": src, "pagina": page, "trecho": extrair_trecho(d.page_content, query)})
    return cites[:3]
