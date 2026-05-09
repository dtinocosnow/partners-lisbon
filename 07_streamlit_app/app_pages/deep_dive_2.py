import streamlit as st

st.markdown("""
<div style="border-left: 5px solid #7D44CF; padding-left: 1.2rem; margin-bottom: 1.5rem;">
    <h1 style="color: #7D44CF !important; margin: 0;">Aprofundamento II</h1>
    <p style="color: #8A999E; margin: 0.3rem 0 0 0; font-size: 1.05rem;">IA e Aplicacoes &bull; David Tinoco &bull; 30 min + Demo</p>
</div>
""", unsafe_allow_html=True)

tab_cortex, tab_llm, tab_analyst, tab_search, tab_agents, tab_ml, tab_apps, tab_quiz = st.tabs(
    ["Cortex AI", "LLM Functions", "Analyst", "Search", "Agents", "ML Functions", "Apps & Marketplace", "Quiz"]
)

with tab_cortex:
    st.markdown("### Snowflake Cortex AI")

    st.markdown("""
<p class="sf-big-text">
Capacidades de IA integradas nativamente no Snowflake.<br>
Sem infraestrutura adicional, sem mover dados.
</p>
""", unsafe_allow_html=True)

    cols = st.columns(5)
    capabilities = [
        ("LLM Functions", "SENTIMENT, TRANSLATE, SUMMARIZE, CLASSIFY, EXTRACT", "#29B5E8"),
        ("Cortex Analyst", "Linguagem natural para SQL", "#11567F"),
        ("Cortex Search", "Pesquisa semantica em documentos", "#7D44CF"),
        ("Cortex Agents", "Orquestracao multi-ferramenta", "#FF9F36"),
        ("ML Functions", "FORECAST, ANOMALY_DETECTION", "#71D3DC"),
    ]

    for col, (title, desc, color) in zip(cols, capabilities):
        with col:
            st.markdown(f"""
<div class="sf-card" style="border-top: 3px solid {color}; text-align: center; min-height: 130px;">
<strong style="color: {color};">{title}</strong><br>
<span style="color: #8A999E; font-size: 0.85rem;">{desc}</span>
</div>
""", unsafe_allow_html=True)

    st.success("**Mensagem-chave:** A IA vem aos dados, nao o contrario. Os dados nunca saem do Snowflake.")

with tab_llm:
    st.markdown("### Funcoes LLM - IA em SQL")
    st.markdown("Executar IA diretamente em SQL, sem APIs externas, sem Python:")

    llm1, llm2, llm3, llm4, llm5 = st.tabs(["Sentiment", "Translate", "Summarize", "Classify", "Extract"])

    with llm1:
        st.code("""SELECT review_text,
       SNOWFLAKE.CORTEX.SENTIMENT(review_text) as score
FROM product_reviews;
-- score: -1.0 (negativo) a 1.0 (positivo)""", language="sql")

    with llm2:
        st.code("""SELECT SNOWFLAKE.CORTEX.TRANSLATE(
  'Hello, how are you?', 'en', 'pt'
);
-- Resultado: 'Ola, como esta?'""", language="sql")

    with llm3:
        st.code("""SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
  document_text
) as resumo
FROM contracts;""", language="sql")

    with llm4:
        st.code("""SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'O produto chegou danificado e com atraso',
  ['positivo', 'negativo', 'neutro']
);
-- Resultado: 'negativo'""", language="sql")

    with llm5:
        st.code("""SELECT SNOWFLAKE.CORTEX.EXTRACT(
  documento_texto,
  ['nome_cliente', 'valor_total', 'data_fatura']
) FROM faturas;""", language="sql")

with tab_analyst:
    st.markdown("### Cortex Analyst - Linguagem Natural para SQL")

    st.markdown("""
<p class="sf-big-text">
Utilizadores fazem perguntas em linguagem natural e recebem respostas SQL executadas automaticamente.
</p>
""", unsafe_allow_html=True)

    st.markdown("#### Fluxo em 5 passos")

    steps = [
        ("1", "Utilizador pergunta em linguagem natural"),
        ("2", "Cortex Analyst interpreta a pergunta"),
        ("3", "Semantic View fornece contexto de negocio"),
        ("4", "SQL gerado automaticamente"),
        ("5", "Resultado apresentado ao utilizador"),
    ]

    for num, desc in steps:
        st.markdown(f"""
<div style="display: flex; align-items: center; margin: 4px 0;">
<span style="background: #29B5E8; color: white; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-right: 12px; flex-shrink: 0;">{num}</span>
<span style="font-size: 1rem;">{desc}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Componentes")
        st.markdown("""
- **Semantic View** - Metricas, dimensoes e relacoes
- **Verified Queries** - Queries validadas como referencia
- **Custom Instructions** - Regras de negocio
""")

    with col2:
        st.markdown("#### Exemplo")
        st.code("""CREATE SEMANTIC VIEW sv_sales_analytics
  COMMENT = 'Sales analytics model'
  TABLES (
    o AS DB.SCHEMA.ORDERS
      PRIMARY KEY (ORDER_ID)
  )
  METRICS (
    total_revenue AS SUM(o.TOTAL_AMOUNT)
      COMMENT 'Total sales revenue'
  )
  DIMENSIONS (
    order_date AS o.ORDER_DATE
      COMMENT 'Date of the order'
  );""", language="sql")

with tab_search:
    st.markdown("### Cortex Search - Pesquisa Semantica")

    st.markdown("""
<p class="sf-big-text">
Pesquisa semantica sobre documentos, contratos, emails - qualquer texto no Snowflake.
</p>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Como funciona")
        st.markdown("""
1. Criar um **Cortex Search Service** sobre uma tabela com texto
2. O servico indexa e cria embeddings automaticamente
3. Queries em linguagem natural retornam resultados relevantes
""")

    with col2:
        st.markdown("#### Casos de uso para partners")
        st.markdown("""
- Pesquisa inteligente em bases de conhecimento
- Chatbots sobre documentacao tecnica
- Analise de contratos e compliance
- FAQ automatico sobre manuais
""")

    st.code("""CREATE CORTEX SEARCH SERVICE reviews_search
  ON review_text
  ATTRIBUTES product_name, rating
  WAREHOUSE = partners_wh
  TARGET_LAG = '1 hour'
AS (
  SELECT review_text, product_name, rating
  FROM product_reviews
);""", language="sql")

with tab_agents:
    st.markdown("### Cortex Agents - Orquestracao Inteligente")

    st.markdown("""
<p class="sf-big-text">
Agents combinam <strong>Cortex Analyst</strong> + <strong>Cortex Search</strong> + ferramentas custom
para responder a perguntas complexas de forma autonoma.
</p>
""", unsafe_allow_html=True)

    st.markdown("""
**Exemplo:** *"Compara o desempenho do melhor cliente com os termos do contrato"*

O Agent automaticamente:
- Usa **Cortex Analyst** para dados de vendas (estruturados)
- Usa **Cortex Search** para encontrar o contrato (documentos)
- Combina ambos numa resposta integrada
""")

    st.code("""CREATE OR REPLACE AGENT sales_assistant
FROM SPECIFICATION $$
models:
  - mistral-large2
orchestration: cortex_default
instructions: |
  You are a sales analytics assistant.
  Answer questions about sales and product reviews.
tools:
  - tool_type: cortex_analyst_text_to_sql
    tool_spec:
      semantic_view: sv_sales_analytics
  - tool_type: cortex_search
    tool_spec:
      search_service: reviews_search
      max_results: 5
$$;""", language="sql")

    st.markdown("#### Ferramentas disponiveis")
    st.markdown("""
| Ferramenta | Descricao |
|---|---|
| `cortex_analyst_text_to_sql` | Queries sobre dados estruturados |
| `cortex_search` | Pesquisa em documentos |
| `data_to_chart` | Gerar visualizacoes |
| `web_search` | Informacao externa |
| `generic` | Stored procedures custom |
""")

with tab_ml:
    st.markdown("### ML Functions - Machine Learning Sem Codigo")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Previsao (Forecast)")
        st.code("""-- Criar modelo de previsao
CREATE SNOWFLAKE.ML.FORECAST sales_forecast (
  INPUT_DATA => TABLE(training_view),
  TIMESTAMP_COLNAME => 'ORDER_DATE',
  TARGET_COLNAME => 'DAILY_REVENUE'
);

-- Gerar previsoes para 30 dias
CALL sales_forecast!FORECAST(30);""", language="sql")

    with col2:
        st.markdown("#### Detecao de Anomalias")
        st.code("""-- Criar detector
CREATE SNOWFLAKE.ML.ANOMALY_DETECTION detector (
  INPUT_DATA => TABLE(training_data),
  TIMESTAMP_COLNAME => 'DATA',
  TARGET_COLNAME => 'VALOR'
);

-- Detetar anomalias
CALL detector!DETECT_ANOMALIES(
  INPUT_DATA => TABLE(new_data)
);""", language="sql")

    st.info("**Zero infraestrutura:** Nao e necessario configurar clusters ML, instalar bibliotecas ou gerir modelos. Tudo corre nativamente dentro do Snowflake.")

with tab_apps:
    st.markdown("### Streamlit & Native Apps")

    apps1, apps2 = st.tabs(["Streamlit in Snowflake", "Native Apps & Marketplace"])

    with apps1:
        st.markdown("""
<p class="sf-big-text">
Construir aplicacoes web interativas diretamente no Snowflake, usando Python e Streamlit.
</p>
""", unsafe_allow_html=True)

        st.code("""import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()
st.title("Dashboard de Vendas")

df = session.sql("SELECT * FROM analytics.vendas_mensal").to_pandas()
st.bar_chart(df, x="MES", y="TOTAL_VENDAS")""", language="python")

        st.markdown("""
**Vantagens:**
- Sem infraestrutura para gerir
- Dados nunca saem do Snowflake
- Governanca integrada (acesso app = acesso dados)
""")

    with apps2:
        st.markdown("""
<p class="sf-big-text">
Partners podem empacotar solucoes como Native Apps e distribui-las no Marketplace.
</p>
""", unsafe_allow_html=True)

        st.markdown("""
**Fluxo:**
1. Partner desenvolve solucao (logica + UI + dados)
2. Empacota como Native App
3. Publica no Marketplace (listing publica ou privada)
4. Cliente instala e utiliza (dados nunca saem)
""")
        st.success("**Oportunidade GTM:** Escalar as vossas solucoes para toda a base global de clientes Snowflake com monetizacao integrada.")

with tab_quiz:
    st.markdown("### Validacao de Conhecimentos")
    st.markdown("Teste o que aprendeu nesta secao.")

    st.markdown("---")

    st.markdown("#### Pergunta 1")
    st.markdown("**Qual e a principal vantagem de usar funcoes LLM diretamente no Snowflake?**")
    options_q1 = [
        "",
        "A) Sao mais baratas que qualquer outro servico de IA",
        "B) Os dados nunca saem do Snowflake - a IA vem aos dados, sem APIs externas",
        "C) Substituem completamente modelos custom treinados",
        "D) Funcionam apenas com texto em ingles",
    ]
    q1 = st.selectbox("Selecione:", options_q1, index=0, key="q1_dd2")
    if q1:
        if "B)" in q1:
            st.success("Correto! As funcoes Cortex AI executam dentro do Snowflake, eliminando a necessidade de mover dados para servicos externos.")
        else:
            st.error("Incorreto. A resposta correta e **B)** - a IA executa onde os dados estao, sem copias nem APIs externas.")

    st.markdown("---")

    st.markdown("#### Pergunta 2")
    st.markdown("**O que e necessario para o Cortex Analyst converter linguagem natural em SQL?**")
    options_q2 = [
        "",
        "A) Um modelo de ML treinado com os dados do cliente",
        "B) Uma Semantic View que define metricas, dimensoes e relacoes",
        "C) Um ficheiro CSV com exemplos de perguntas e respostas",
        "D) Acesso direto a API da OpenAI",
    ]
    q2 = st.selectbox("Selecione:", options_q2, index=0, key="q2_dd2")
    if q2:
        if "B)" in q2:
            st.success("Correto! A Semantic View fornece o contexto de negocio para o Cortex Analyst gerar SQL preciso.")
        else:
            st.error("Incorreto. A resposta correta e **B)** - Semantic Views sao a fonte de verdade para o Analyst.")

    st.markdown("---")

    st.markdown("#### Pergunta 3")
    st.markdown("**O que diferencia um Cortex Agent das funcoes LLM individuais?**")
    options_q3 = [
        "",
        "A) Agents sao mais rapidos que funcoes individuais",
        "B) Agents apenas funcionam com dados nao estruturados",
        "C) Agents orquestram multiplas ferramentas de forma autonoma para perguntas complexas",
        "D) Agents substituem a necessidade de ter tabelas",
    ]
    q3 = st.selectbox("Selecione:", options_q3, index=0, key="q3_dd2")
    if q3:
        if "C)" in q3:
            st.success("Correto! Cortex Agents combinam Analyst + Search + ferramentas custom para resolver perguntas multi-dominio.")
        else:
            st.error("Incorreto. A resposta correta e **C)** - orquestracao inteligente de multiplas ferramentas.")
