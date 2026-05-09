import streamlit as st

st.markdown("""
<div style="border-left: 5px solid #11567F; padding-left: 1.2rem; margin-bottom: 1.5rem;">
    <h1 style="color: #11567F !important; margin: 0;">Aprofundamento I</h1>
    <p style="color: #8A999E; margin: 0.3rem 0 0 0; font-size: 1.05rem;">Fundamentos da Plataforma &bull; David Tinoco &bull; 35 min + Demo</p>
</div>
""", unsafe_allow_html=True)

tab_arq, tab_seg, tab_perf, tab_ing, tab_dt, tab_quiz = st.tabs(
    ["Arquitetura", "Seguranca", "Desempenho", "Ingestao", "Dynamic Tables", "Quiz"]
)

with tab_arq:
    st.markdown("### Arquitetura Multi-Cluster de Dados Partilhados")

    st.markdown("""
<p class="sf-big-text">
Snowflake separa <strong>armazenamento</strong>, <strong>computacao</strong> e <strong>servicos cloud</strong>
em tres camadas independentes. Cada camada escala de forma autonoma.
</p>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
<div class="sf-card sf-card-accent" style="border-left-color: #29B5E8;">
<h4 style="margin-top:0;">Servicos Cloud</h4>
<ul>
<li>Otimizacao automatica de queries</li>
<li>Gestao de transacoes ACID</li>
<li>Seguranca e encriptacao E2E</li>
<li>Gestao de metadados</li>
<li>Cache inteligente</li>
</ul>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="sf-card sf-card-accent" style="border-left-color: #7D44CF;">
<h4 style="margin-top:0;">Computacao</h4>
<ul>
<li>Virtual Warehouses (XS a 6XL)</li>
<li>Multi-cluster para concorrencia</li>
<li>Isolamento total de workloads</li>
<li>Auto-suspend / Auto-resume</li>
<li>Pagar apenas quando em uso</li>
</ul>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
<div class="sf-card sf-card-accent" style="border-left-color: #FF9F36;">
<h4 style="margin-top:0;">Armazenamento</h4>
<ul>
<li>Formato colunar (micro-particoes)</li>
<li>Compressao automatica</li>
<li>Centralizado e partilhado</li>
<li>Sem gerir indices</li>
<li>Suporte: JSON, Avro, Parquet, ORC</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.info("**Conceito-chave:** Os dados sao armazenados uma unica vez e acedidos por multiplos warehouses simultaneamente - sem duplicacao, sem contencao.")

    with st.expander("Zero-Copy Cloning"):
        st.markdown("Clonar bases de dados, schemas ou tabelas **em segundos** sem copiar dados fisicamente.")
        st.code("""CREATE DATABASE dev_environment CLONE production;
-- Instantaneo, sem custo adicional de armazenamento (ate haver alteracoes)""", language="sql")
        st.markdown("**Casos de uso:** Ambientes de dev/test instantaneos | Snapshots para auditoria | Experimentacao sem risco")

    with st.expander("Secure Data Sharing"):
        st.markdown("""
Partilhar dados **ao vivo** entre contas Snowflake sem copiar, mover ou transferir.

- Dados sempre atualizados (nao e uma copia)
- Governanca mantida pelo fornecedor
- Sem custos de transferencia
- Cross-cloud e cross-region
""")

    with st.expander("Multi-Cloud e Multi-Regiao"):
        st.markdown("""
- Disponivel em **AWS, Azure e GCP**
- Mais de 30 regioes globais
- Replicacao cross-cloud e cross-region
- Failover automatico e Business Continuity
""")

with tab_seg:
    st.markdown("### Seguranca e Governanca Nativa")

    seg1, seg2, seg3, seg4 = st.tabs(["RBAC", "Masking Policies", "Row Access", "Horizon Catalog"])

    with seg1:
        st.markdown("#### Role-Based Access Control")
        st.code("""ACCOUNTADMIN
  +-- SYSADMIN
  |    +-- DB_ADMIN
  |    |    +-- ANALYST_ROLE
  |    |    +-- ENGINEER_ROLE
  |    +-- CUSTOM_ROLES...
  +-- SECURITYADMIN
       +-- Gestao de roles e grants""", language="text")

        st.dataframe(
            [
                {"Role": "ACCOUNTADMIN", "Responsabilidade": "Administracao total da conta"},
                {"Role": "SYSADMIN", "Responsabilidade": "Criar e gerir objetos (databases, schemas, warehouses)"},
                {"Role": "SECURITYADMIN", "Responsabilidade": "Gerir roles, utilizadores e grants"},
                {"Role": "USERADMIN", "Responsabilidade": "Criar e gerir utilizadores e roles"},
                {"Role": "PUBLIC", "Responsabilidade": "Role base - privilegios minimos"},
            ],
            use_container_width=True,
        )

        st.markdown("""
**Principios:**
- Hierarquia de roles com heranca de privilegios
- Principio do minimo privilegio
- Criar **roles custom** por equipa (ANALYST_ROLE, ENGINEER_ROLE)
""")

    with seg2:
        st.markdown("#### Masking Policies - Seguranca ao Nivel da Coluna")
        st.markdown("Diferentes roles veem diferentes niveis de detalhe na **mesma tabela**:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**ADMIN ve:**")
            st.dataframe(
                [{"EMAIL": "joao@empresa.pt", "TELEFONE": "+351 912 345 678"}],
                use_container_width=True,
            )
        with col2:
            st.markdown("**ANALYST ve:**")
            st.dataframe(
                [{"EMAIL": "j***@***.pt", "TELEFONE": "***-***-678"}],
                use_container_width=True,
            )

        st.code("""CREATE MASKING POLICY mask_email AS (val STRING)
  RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ADMIN') THEN val
    ELSE REGEXP_REPLACE(val, '.+@', '***@')
  END;

ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY mask_email;""", language="sql")

    with seg3:
        st.markdown("#### Row Access Policies - Seguranca ao Nivel da Linha")
        st.markdown("Diferentes utilizadores veem **diferentes linhas** da mesma tabela.")
        st.code("""CREATE ROW ACCESS POLICY region_policy AS (region STRING)
  RETURNS BOOLEAN ->
  CURRENT_ROLE() = 'GLOBAL_ANALYST'
  OR region = 'EMEA';

ALTER TABLE orders ADD ROW ACCESS POLICY region_policy ON (region);""", language="sql")

    with seg4:
        st.markdown("#### Snowflake Horizon - Governanca Unificada")
        cols = st.columns(5)
        items = [
            ("Descoberta", "Catalogo universal"),
            ("Seguranca", "Masking, RLS"),
            ("Conformidade", "Classificacao, auditoria"),
            ("Privacidade", "Clean rooms"),
            ("Acesso", "RBAC, policies"),
        ]
        for col, (title, desc) in zip(cols, items):
            with col:
                st.markdown(f"""
<div class="sf-card" style="text-align:center; padding: 1rem;">
<strong>{title}</strong><br><span style="color:#8A999E; font-size:0.85rem;">{desc}</span>
</div>
""", unsafe_allow_html=True)

with tab_perf:
    st.markdown("### Desempenho e Gestao de Custos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Dimensionamento de Warehouses")
        st.dataframe(
            [
                {"Tamanho": "XS", "Creditos/Hora": 1, "Caso de Uso": "Queries ad-hoc, dev"},
                {"Tamanho": "S", "Creditos/Hora": 2, "Caso de Uso": "BI dashboards"},
                {"Tamanho": "M", "Creditos/Hora": 4, "Caso de Uso": "ETL medio, analytics"},
                {"Tamanho": "L", "Creditos/Hora": 8, "Caso de Uso": "Grandes transformacoes"},
                {"Tamanho": "XL+", "Creditos/Hora": 16, "Caso de Uso": "Workloads massivos"},
            ],
            use_container_width=True,
        )

    with col2:
        st.markdown("#### Camadas de Cache")
        st.markdown("""
<div class="sf-card">
<strong>1. Result Cache</strong> — Gratis, 24h, mesma query exata<br>
<strong>2. Local Disk Cache</strong> — No warehouse, dados "quentes"<br>
<strong>3. Remote Disk Cache</strong> — Storage layer, micro-particoes
</div>
""", unsafe_allow_html=True)
        st.info("**Dica:** \"A primeira execucao demora X seg, a segunda e quase instantanea\" - Result Cache em acao.")

    st.markdown("#### Boas praticas")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
- Comecar pequeno (XS) e escalar conforme necessidade
- Multi-cluster warehouses para concorrencia
""")
    with col_b:
        st.markdown("""
- Auto-suspend apos 1-5 min de inatividade
- Resource Monitors para controlar custos
""")

with tab_ing:
    st.markdown("### Opcoes de Ingestao de Dados")

    st.dataframe(
        [
            {"Metodo": "COPY INTO", "Latencia": "Minutos", "Caso de Uso": "Cargas batch de ficheiros", "Complexidade": "Baixa"},
            {"Metodo": "Snowpipe", "Latencia": "~1 minuto", "Caso de Uso": "Ingestao continua automatizada", "Complexidade": "Media"},
            {"Metodo": "Snowpipe Streaming", "Latencia": "Segundos", "Caso de Uso": "Streaming em tempo real", "Complexidade": "Media-Alta"},
            {"Metodo": "Connectors/OpenFlow", "Latencia": "Variavel", "Caso de Uso": "Kafka, Spark, CDC", "Complexidade": "Variavel"},
        ],
        use_container_width=True,
    )

    with st.expander("Exemplo: Snowpipe"):
        st.code("""-- Criar stage externo
CREATE STAGE my_s3_stage URL = 's3://my-bucket/data/'
  CREDENTIALS = (AWS_KEY_ID='...' AWS_SECRET_KEY='...');

-- Criar pipe para ingestao automatica
CREATE PIPE my_pipe AUTO_INGEST = TRUE AS
  COPY INTO raw.events FROM @my_s3_stage
  FILE_FORMAT = (TYPE = 'JSON');

-- Verificar status
SELECT SYSTEM$PIPE_STATUS('my_pipe');""", language="sql")

with tab_dt:
    st.markdown("### Dynamic Tables - ETL Declarativo")

    st.markdown("""
<p class="sf-big-text">
Em vez de pipelines ETL complexos, definimos <strong>o resultado desejado</strong>
e o Snowflake trata da atualizacao incremental automaticamente.
</p>
""", unsafe_allow_html=True)

    st.code("""CREATE DYNAMIC TABLE analytics_orders
  TARGET_LAG = '1 hour'
  WAREHOUSE = wh_etl
AS
  SELECT
    o.order_date,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) as total_amount
  FROM raw.orders o
  JOIN raw.customers c ON o.customer_id = c.customer_id
  JOIN raw.order_items oi ON o.order_id = oi.order_id
  GROUP BY 1, 2;""", language="sql")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Orquestracao", "Zero")
    with col2:
        st.metric("Refresh", "Incremental")
    with col3:
        st.metric("Custo", "Menor")

    st.markdown("""
**Vantagens:**
- Sem orquestracao manual (sem Airflow, sem cron)
- Refresh incremental automatico
- Menor custo vs. full refresh repetido
- Encadeamento declarativo de dependencias
""")

with tab_quiz:
    st.markdown("### Validacao de Conhecimentos")
    st.markdown("Teste o que aprendeu nesta secao.")

    st.markdown("---")

    st.markdown("#### Pergunta 1")
    st.markdown("**Qual e a principal vantagem da separacao de armazenamento e computacao no Snowflake?**")
    options_q1 = [
        "",
        "A) Reduz o numero de tabelas no sistema",
        "B) Permite escalar computacao e armazenamento de forma independente, pagando apenas pelo que se utiliza",
        "C) Obriga a usar apenas um warehouse por base de dados",
        "D) Elimina a necessidade de SQL",
    ]
    q1 = st.selectbox("Selecione:", options_q1, index=0, key="q1_dd1")
    if q1:
        if "B)" in q1:
            st.success("Correto! A separacao permite que cada camada escale de forma autonoma. Multiplos warehouses acedem aos mesmos dados sem contencao.")
        else:
            st.error("Incorreto. A resposta correta e **B)** - computacao e armazenamento escalem independentemente.")

    st.markdown("---")

    st.markdown("#### Pergunta 2")
    st.markdown("**O que e uma Dynamic Table no Snowflake?**")
    options_q2 = [
        "",
        "A) Uma tabela que muda de tamanho automaticamente",
        "B) Uma tabela que define o resultado desejado em SQL e o Snowflake gere o refresh incremental",
        "C) Uma tabela temporaria que se apaga apos cada sessao",
        "D) Uma tabela que so permite INSERT",
    ]
    q2 = st.selectbox("Selecione:", options_q2, index=0, key="q2_dd1")
    if q2:
        if "B)" in q2:
            st.success("Correto! Dynamic Tables sao ETL declarativo - definimos o SELECT e o Snowflake trata do refresh incremental.")
        else:
            st.error("Incorreto. A resposta correta e **B)** - ETL declarativo com refresh incremental automatico.")

    st.markdown("---")

    st.markdown("#### Pergunta 3")
    st.markdown("**O que permite uma Masking Policy?**")
    options_q3 = [
        "",
        "A) Encriptar toda a base de dados",
        "B) Impedir acesso a determinada tabela",
        "C) Mostrar diferentes niveis de detalhe na mesma coluna conforme o role do utilizador",
        "D) Eliminar dados sensiveis permanentemente",
    ]
    q3 = st.selectbox("Selecione:", options_q3, index=0, key="q3_dd1")
    if q3:
        if "C)" in q3:
            st.success("Correto! Masking Policies permitem que diferentes roles vejam diferentes representacoes do mesmo dado.")
        else:
            st.error("Incorreto. A resposta correta e **C)** - valores diferentes conforme o CURRENT_ROLE().")
