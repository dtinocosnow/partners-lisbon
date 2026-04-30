# Guia Interno: Informacao Partilhavel vs. Confidencial
## Referencia para Pedro e David - Sessao Partners Lisboa

> **DOCUMENTO INTERNO SNOWFLAKE - NAO PARTILHAR COM PARTNERS**

---

## PODE PARTILHAR (Informacao Publica)

### Arquitetura e Produto
- Arquitetura de 3 camadas (storage, compute, services)
- Separacao de storage e compute
- Funcionalidades disponveis em GA (General Availability)
- Funcionalidades em Public Preview (indicando que sao preview)
- Documentacao publica (docs.snowflake.com)
- Edicoes disponiveis (Standard, Enterprise, Business Critical, VPS)
- Regioes e clouds suportados (AWS, Azure, GCP)
- Credit consumption table (publica)
- Funcoes Cortex AI (as que estao em GA ou Public Preview)

### Precos (informacao publica)
- Modelo de precos baseado em consumo (pay-as-you-go)
- Creditos por hora por tamanho de warehouse (tabela publica)
- Custo de armazenamento por TB/mes (informacao publica)
- Diferencas entre edicoes a nivel de funcionalidades
- Pagina de precos: https://www.snowflake.com/pricing

### Recursos e Formacao
- Quickstart guides (quickstarts.snowflake.com)
- Snowflake University (learn.snowflake.com)
- Documentacao (docs.snowflake.com)
- Comunidade (community.snowflake.com)
- GitHub Snowflake-Labs
- Certificacoes SnowPro (precos, formato, topicos)
- Partner Portal e cursos para partners
- Brand guidelines e templates para partners

### Casos de Uso
- Casos de uso publicos publicados no site Snowflake
- Historias de clientes publicadas em snowflake.com/customers
- Benchmarks publicos (TPC-DS results se publicados)
- Demos com dados sinteticos ou de amostra

### Integracao e Ecossistema
- Lista de conectores e integradores suportados
- Compatibilidade com ferramentas de BI (Tableau, Power BI, Looker, etc.)
- Integracao com dbt, Spark, Kafka, etc.
- Apache Iceberg support (informacao publica)
- Marketplace (listings publicas)

---

## NAO PODE PARTILHAR (Informacao Confidencial/Interna)

### Roadmap e Funcionalidades Futuras
- Roadmap de produto (dates, features planeadas)
- Funcionalidades em Private Preview (exceto se o partner tem acesso)
- Datas de lancamento de funcionalidades futuras
- Informacao sobre aquisicoes ou parcerias nao anunciadas

### Precos e Comercial
- Tabelas de descontos internas
- Pricing agreements com outros clientes ou partners
- Estrutura de margens ou comissoes
- Deal terms ou deal structures internas
- Informacao sobre revenue, ARR, ou metricas financeiras internas
- Estrategia de precos competitiva

### Clientes e Dados
- Nomes de clientes sem permissao explicita
- Detalhes de implementacao de clientes especificos
- Volumes de dados ou consumo de clientes especificos
- Arquitecturas de clientes especificos

### Competitivo
- Battle cards ou comparativos internos
- Analise competitiva interna
- Benchmark results nao publicados
- Estrategias de win/loss contra competidores
- Fraquezas conhecidas da plataforma (documentadas internamente)

### Interno
- Processos internos Snowflake (como trabalhamos, ferramentas internas)
- Estrutura organizacional detalhada
- Informacao de Slack, email, ou comunicacoes internas
- Ferramentas internas (Salesforce, Seismic, Highspot - apenas links publicos)
- Informacao sobre colaboradores (exceto contactos partilhados voluntariamente)

---

## ZONA CINZENTA - Usar Bom Senso

| Topico | Orientacao |
|--------|-----------|
| Funcionalidades em Public Preview | Mencionar que existe e e preview. Nao prometer datas de GA |
| Limitacoes conhecidas | Ser honesto sobre limitacoes documentadas publicamente |
| Comparacao com concorrentes | Focar nos diferenciais Snowflake, sem atacar concorrentes |
| Precos "ballpark" | Usar apenas a tabela publica de creditos. Nunca dar estimativas de custos para workloads especificos |
| Clientes em Portugal | Apenas mencionar se ha caso publico. Caso contrario, dizer "temos clientes na regiao" sem nomes |
| Performance claims | Usar apenas benchmarks publicos. Dizer "tipicamente vemos X" em vez de "garantimos X" |

---

## Frases Uteis para Redirecionar

Quando pedirem informacao que nao podem partilhar:

- **Roadmap:** "Nao posso partilhar detalhes do roadmap, mas posso dizer que a Snowflake investe fortemente em [area]. Recomendo seguir os anuncios publicos no blog e no Snowflake Summit."

- **Precos especificos:** "O modelo de precos esta disponivel publicamente em snowflake.com/pricing. Para uma estimativa especifica para o vosso caso de uso, podemos envolver a equipa comercial."

- **Clientes:** "Temos uma presenca crescente no mercado portugues. Para casos de uso publicos, recomendo visitar snowflake.com/customers."

- **Comparacao direta:** "Prefiro focar no que o Snowflake faz bem. Cada plataforma tem os seus pontos fortes. O melhor e testar com um POC no vosso contexto especifico."

---

## Contactos Internos para Duvidas

Se durante a sessao surgirem questoes que nao podem responder:

- Anotar a pergunta e o contacto de quem perguntou
- Comprometer-se a dar follow-up em 48 horas
- Escalar para o manager ou equipa relevante internamente

---

*Documento interno Snowflake - Atualizado Abril 2026*
