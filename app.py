import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from triagem import criar_chain_triagem
from rag import carregar_pdfs, criar_rag
from langgraph_workflow import criar_fluxo_langgraph

# --- Carregar variáveis ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    st.error("❌ GEMINI_API_KEY não encontrada. Verifique seu .env.")
    st.stop()

# --- Inicializar Triagem e RAG ---
@st.cache_resource
def setup():
    chain_triagem = criar_chain_triagem(GOOGLE_API_KEY)
    caminho_pdfs = Path("./pdfs")
    docs = carregar_pdfs(caminho_pdfs)
    retriever, document_chain = criar_rag(docs, GOOGLE_API_KEY)
    graph = criar_fluxo_langgraph(chain_triagem, retriever, document_chain)
    return graph

graph = setup()

# --- Interface Web ---
st.set_page_config(page_title="Assistente Carraro", page_icon="🤖")
st.title("🤖 Assistente de Políticas Internas")
st.caption("Carraro Desenvolvimento — RH / TI")

st.markdown("Digite sua dúvida relacionada às políticas internas da empresa. Ex: `Como solicitar férias?`")

mensagem = st.text_input("📩 Sua pergunta:")

if mensagem:
    with st.spinner("Analisando..."):
        final_state = graph.invoke({"mensagem": mensagem})
        triagem = final_state["triagem"]
        resposta = final_state["resposta"]

    st.markdown("---")
    st.subheader("📌 Triagem")
    st.json(triagem)

    st.subheader("🤖 Resposta")
    st.markdown(resposta["answer"])

    citacoes = resposta.get("citacoes", [])
    if citacoes:
        st.subheader("🔍 Citações de contexto")
        for c in citacoes:
            st.markdown(f"**📄 Documento:** `{c['documento']}` — Página {c['pagina']}")
            st.code(c["trecho"])
