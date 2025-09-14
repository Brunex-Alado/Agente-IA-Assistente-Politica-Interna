from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict

from triagem import executar_triagem
from rag import formatar_citacoes

class AgentState(TypedDict):
    mensagem: str
    triagem: Dict
    resposta: Dict

def node_triagem(state: AgentState, chain_triagem, **kwargs):
    state["triagem"] = executar_triagem(chain_triagem, state["mensagem"])
    return state

def node_resposta_auto(state: AgentState, retriever, document_chain, **kwargs):
    pergunta = state["mensagem"]
    docs_rel = retriever.invoke(pergunta)

    if not docs_rel:
        state["resposta"] = {"answer": "Não sei.", "citacoes": []}
        return state

    resposta = document_chain.invoke({"input": pergunta, "context": docs_rel}).strip()
    if resposta.rstrip(".!?") == "Não sei":
        state["resposta"] = {"answer": "Não sei.", "citacoes": []}
        return state

    citacoes = formatar_citacoes(docs_rel, pergunta)
    state["resposta"] = {"answer": resposta, "citacoes": citacoes}
    return state

def node_pedir_info(state: AgentState):
    state["resposta"] = {"answer": "Preciso de mais informações.", "citacoes": []}
    return state

def node_abrir_chamado(state: AgentState):
    state["resposta"] = {"answer": "Será aberto um chamado para sua solicitação.", "citacoes": []}
    return state

def criar_fluxo_langgraph(chain_triagem, retriever, document_chain):
    builder = StateGraph(AgentState)

    builder.add_node("triagem", lambda s: node_triagem(s, chain_triagem))
    builder.add_node("resposta_auto", lambda s: node_resposta_auto(s, retriever, document_chain))
    builder.add_node("pedir_info", node_pedir_info)
    builder.add_node("abrir_chamado", node_abrir_chamado)
    builder.add_node("fim", lambda s: s)

    builder.set_entry_point("triagem")

    def roteador(state: AgentState):
        decisao = state["triagem"]["decisao"]
        if decisao == "AUTO_RESOLVER":
            return "resposta_auto"
        elif decisao == "PEDIR_INFO":
            return "pedir_info"
        elif decisao == "ABRIR_CHAMADO":
            return "abrir_chamado"
        return "fim"

    builder.add_conditional_edges("triagem", roteador)
    builder.add_edge("resposta_auto", "fim")
    builder.add_edge("pedir_info", "fim")
    builder.add_edge("abrir_chamado", "fim")

    return builder.compile()
