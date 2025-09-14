# 🤖 Agente de IA - Assistente de Políticas Internas (Triagem + RAG)

<br>

## 🚀 Tecnologias Utilizadas
<div>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Google_Gemini_API-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-0066CC?style=for-the-badge&logo=airflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/FAISS-005571?style=for-the-badge&logo=codesignal&logoColor=white" />
  <img src="https://img.shields.io/badge/Pydantic-0A66C2?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PyMuPDF-CC0000?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" />
  <img src="https://img.shields.io/badge/Requests-478778?style=for-the-badge&logo=requests&logoColor=white">
</div>

<br>

## 🎯 Objetivo

Este projeto foi desenvolvido durante a **Imersão Dev - Agentes de IA (Google & Alura)** com o objetivo de aplicar inteligência artificial na automação do atendimento interno empresarial.

A aplicação é um Assistente Inteligente de Políticas Internas, voltado para o suporte a colaboradores em dúvidas sobre processos de RH e TI. Ele combina:

- 🧠 Triagem com LLM (via LangGraph):
Utiliza um modelo de linguagem para classificar a intenção da mensagem do usuário em três categorias:

   - AUTO_RESOLVER → pergunta objetiva, pode ser respondida com base nas políticas existentes.

   - PEDIR_INFO → a pergunta está vaga ou faltam dados para avançar.

   - ABRIR_CHAMADO → situações que requerem encaminhamento humano.

A tomada de decisão é gerenciada por um grafo de execução com nós distintos, criado com a biblioteca LangGraph.

- 📚 RAG (Retrieval-Augmented Generation):
Quando a triagem decide por AUTO_RESOLVER, o sistema ativa um pipeline RAG que:

   - Busca trechos relevantes em documentos PDF internos (com FAISS + embeddings do Gemini).

   - Gera uma resposta contextualizada com base nesses trechos, utilizando o modelo Gemini.

- 💻 Interface Web com Streamlit:
Melhoria criada à parte da imersão, afim de fornecer uma interface amigável e acessível via navegador, permitindo que qualquer colaborador consulte o assistente de forma intuitiva.

<br/>

## 🔁 Visão Geral do Fluxo de Triagem

| ![image](https://raw.githubusercontent.com/Brunex-Alado/Agente-IA-Assistente-Politica-Interna/refs/heads/main/img/fluxo_de_triagem.png) | 

<br/>

## 💻 Interface Web (Streamlit)

O projeto oferece uma interface intuitiva e interativa via **Streamlit**, permitindo que qualquer pessoa da empresa utilize o agente diretamente no navegador.

| ![image](https://raw.githubusercontent.com/Brunex-Alado/Agente-IA-Assistente-Politica-Interna/refs/heads/main/img/assistente_politcas_internas.png) |

<br/>

## ▶️ Como Executar o Agente de IA Localmente

1. **Clone o repositório*:
git clone https://github.com/Brunex-Alado/Agente-IA-Assistente-Politica-Interna

2. Instale as dependências: pip install -r requirements.txt

3. Configure as variáveis de ambiente:
Copie o arquivo de exemplo ".env.example" para .env com o comando:
cp .env.example .env

4. Obtenha uma chave de API do Gemini: https://aistudio.google.com/app/apikey

5. Abra o arquivo .env e cole sua chave da API Gemini: GEMINI_API_KEY=COLE_SUA_CHAVE_GERADA_AQUI

6. Configure o ".gitignore" para proteger seus dados sensíveis:
   "# Secrets"
   .env

   "# Virtual env"
   venv/
   __pycache__/

7. Execute o Agente no terminal: streamlit run app.py

8. Acesse pelo navegador:

O Streamlit abrirá automaticamente em:
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501"

Se for a primeira vez utilizando o Streamlit, apenas pressione ENTER quando solicitado um e-mail.
 
<br/>

