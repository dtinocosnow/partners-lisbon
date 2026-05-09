/*
=============================================================================
  SUPERNOVA SUPERMERCADOS - LABORATORIO PRATICO
  Script: Setup da Camada Bronze
  
  Cenario: SuperNova e uma cadeia de supermercados portuguesa com 12 lojas.
  Este script cria o ambiente completo e carrega dados na camada Bronze.
  
  Duracao: ~3 minutos para executar
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;

-- =============================================================================
-- PARTE 1: Criar o ambiente
-- =============================================================================

CREATE OR REPLACE DATABASE SUPERNOVA_LAB;

CREATE SCHEMA SUPERNOVA_LAB.BRONZE;
CREATE SCHEMA SUPERNOVA_LAB.SILVER;
CREATE SCHEMA SUPERNOVA_LAB.GOLD;
CREATE SCHEMA SUPERNOVA_LAB.APPS;

CREATE OR REPLACE WAREHOUSE SUPERNOVA_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse para laboratorio SuperNova';

USE WAREHOUSE SUPERNOVA_WH;
USE DATABASE SUPERNOVA_LAB;
USE SCHEMA BRONZE;

-- =============================================================================
-- PARTE 2: Tabela LOJAS (12 lojas em Portugal)
-- =============================================================================

CREATE OR REPLACE TABLE LOJAS (
    LOJA_ID         INTEGER,
    NOME_LOJA       VARCHAR(50),
    CIDADE          VARCHAR(30),
    DISTRITO        VARCHAR(30),
    REGIAO          VARCHAR(20),
    AREA_M2         INTEGER,
    DATA_ABERTURA   DATE
);

INSERT INTO LOJAS VALUES
(1,  'SuperNova Lisboa Centro',     'Lisboa',   'Lisboa',       'Sul',   2200, '2018-03-15'),
(2,  'SuperNova Parque Nacoes',     'Lisboa',   'Lisboa',       'Sul',   3100, '2019-06-20'),
(3,  'SuperNova Belem',             'Lisboa',   'Lisboa',       'Sul',   1800, '2021-01-10'),
(4,  'SuperNova Porto Boavista',    'Porto',    'Porto',        'Norte', 2500, '2018-09-01'),
(5,  'SuperNova Porto Gaia',        'Vila Nova de Gaia', 'Porto', 'Norte', 2800, '2020-04-15'),
(6,  'SuperNova Braga',             'Braga',    'Braga',        'Norte', 2000, '2019-11-20'),
(7,  'SuperNova Coimbra',           'Coimbra',  'Coimbra',      'Centro', 1900, '2020-08-05'),
(8,  'SuperNova Faro',              'Faro',     'Faro',         'Sul',   1600, '2021-05-12'),
(9,  'SuperNova Aveiro',            'Aveiro',   'Aveiro',       'Centro', 1700, '2022-02-28'),
(10, 'SuperNova Setubal',           'Setubal',  'Setubal',      'Sul',   1500, '2022-07-15'),
(11, 'SuperNova Funchal',           'Funchal',  'Madeira',      'Ilhas', 1400, '2023-01-20'),
(12, 'SuperNova Evora',             'Evora',    'Evora',        'Sul',   1300, '2023-09-10');

-- =============================================================================
-- PARTE 3: Tabela PRODUTOS (~50 SKUs em 6 categorias)
-- =============================================================================

CREATE OR REPLACE TABLE PRODUTOS (
    PRODUTO_ID      INTEGER,
    NOME_PRODUTO    VARCHAR(100),
    CATEGORIA       VARCHAR(30),
    SUBCATEGORIA    VARCHAR(30),
    PRECO_VENDA     DECIMAL(8,2),
    PRECO_CUSTO     DECIMAL(8,2),
    UNIDADE         VARCHAR(10),
    FORNECEDOR      VARCHAR(50)
);

INSERT INTO PRODUTOS VALUES
-- Frescos
(1,  'Maca Royal Gala 1kg',         'Frescos',      'Frutas',       2.49, 1.20, 'kg',   'Frutas do Ribatejo'),
(2,  'Banana Madeira',              'Frescos',      'Frutas',       1.99, 0.95, 'kg',   'Cooperativa Madeira'),
(3,  'Laranja Algarve',             'Frescos',      'Frutas',       2.29, 1.10, 'kg',   'Citrinos do Sul'),
(4,  'Tomate Cherry',               'Frescos',      'Legumes',      3.49, 1.80, 'kg',   'Hortas do Oeste'),
(5,  'Alface Iceberg',              'Frescos',      'Legumes',      0.99, 0.45, 'un',   'Hortas do Oeste'),
(6,  'Cenoura Bio',                 'Frescos',      'Legumes',      1.79, 0.85, 'kg',   'Bio Portugal'),
(7,  'Frango Inteiro',              'Frescos',      'Carne',        4.99, 3.20, 'kg',   'Avicula do Centro'),
(8,  'Bife Novilho',                'Frescos',      'Carne',       12.99, 8.50, 'kg',   'Carnes Premium PT'),
(9,  'Salmao Fresco',               'Frescos',      'Peixe',       14.99, 9.80, 'kg',   'Mar Atlantico'),
(10, 'Bacalhau Demolhado',          'Frescos',      'Peixe',       11.99, 7.50, 'kg',   'Bacalhau Tradicional'),
-- Mercearia
(11, 'Arroz Carolino 1kg',          'Mercearia',    'Basicos',      1.59, 0.80, 'un',   'Arrozes do Mondego'),
(12, 'Massa Esparguete 500g',       'Mercearia',    'Basicos',      0.89, 0.40, 'un',   'Nacional'),
(13, 'Azeite Extra Virgem 750ml',   'Mercearia',    'Basicos',      5.99, 3.50, 'un',   'Olivais do Alentejo'),
(14, 'Atum em Conserva 120g',       'Mercearia',    'Conservas',    1.49, 0.70, 'un',   'Ramirez'),
(15, 'Feijao Encarnado 500g',       'Mercearia',    'Leguminosas',  1.29, 0.60, 'un',   'Leguminosas PT'),
(16, 'Cafe Torrado 250g',           'Mercearia',    'Cafe',         3.99, 2.10, 'un',   'Delta Cafes'),
(17, 'Acar Branco 1kg',            'Mercearia',    'Basicos',      0.99, 0.50, 'un',   'RAR'),
(18, 'Farinha Trigo 1kg',           'Mercearia',    'Basicos',      0.79, 0.35, 'un',   'Nacional'),
-- Bebidas
(19, 'Agua Luso 1.5L',              'Bebidas',      'Agua',         0.49, 0.20, 'un',   'Sociedade da Agua de Luso'),
(20, 'Sumo Laranja Natural 1L',     'Bebidas',      'Sumos',        2.99, 1.50, 'un',   'Compal'),
(21, 'Cerveja Super Bock 6x33cl',   'Bebidas',      'Cerveja',      4.99, 2.80, 'un',   'Super Bock Group'),
(22, 'Vinho Tinto Alentejo 750ml',  'Bebidas',      'Vinho',        5.49, 2.80, 'un',   'Monte da Ravasqueira'),
(23, 'Coca-Cola 1.5L',              'Bebidas',      'Refrigerantes', 1.89, 0.90, 'un',  'CCEP Portugal'),
(24, 'Vinho Verde 750ml',           'Bebidas',      'Vinho',        3.99, 1.90, 'un',   'Aveleda'),
-- Lacticinios
(25, 'Leite Meio-Gordo 1L',         'Lacticinios',  'Leite',        0.89, 0.50, 'un',   'Mimosa'),
(26, 'Iogurte Natural 4x125g',      'Lacticinios',  'Iogurte',      1.49, 0.75, 'un',   'Danone'),
(27, 'Queijo Flamengo Fatias 200g', 'Lacticinios',  'Queijo',       2.29, 1.20, 'un',   'Terra Nostra'),
(28, 'Manteiga com Sal 250g',       'Lacticinios',  'Manteiga',     2.49, 1.40, 'un',   'Milhafre'),
(29, 'Natas 200ml',                  'Lacticinios',  'Natas',        0.99, 0.50, 'un',   'Mimosa'),
(30, 'Queijo Serra Estrela',        'Lacticinios',  'Queijo',       8.99, 5.50, 'un',   'Queijaria da Serra'),
-- Higiene
(31, 'Detergente Roupa 40 doses',   'Higiene',      'Limpeza',      8.99, 4.50, 'un',   'Henkel'),
(32, 'Papel Higienico 12 rolos',    'Higiene',      'Papel',        4.99, 2.50, 'un',   'Renova'),
(33, 'Champô Anti-Caspa 400ml',    'Higiene',      'Pessoal',      3.99, 1.80, 'un',   'Head & Shoulders'),
(34, 'Pasta Dentes 75ml',           'Higiene',      'Pessoal',      2.49, 1.10, 'un',   'Colgate'),
(35, 'Detergente Loica 1L',         'Higiene',      'Limpeza',      2.29, 1.00, 'un',   'Fairy'),
(36, 'Desodorizante Roll-On',       'Higiene',      'Pessoal',      2.99, 1.30, 'un',   'Nivea'),
-- Congelados
(37, 'Pizza Margherita 350g',        'Congelados',   'Refeicoes',    3.49, 1.70, 'un',   'Dr. Oetker'),
(38, 'Gelado Baunilha 1L',          'Congelados',   'Gelados',      3.99, 2.00, 'un',   'Olá'),
(39, 'Ervilhas Congeladas 1kg',     'Congelados',   'Legumes',      1.99, 0.90, 'un',   'Iglo'),
(40, 'Filetes Pescada 400g',        'Congelados',   'Peixe',        4.49, 2.50, 'un',   'Pescanova'),
(41, 'Batata Pre-Frita 1kg',        'Congelados',   'Acompanhamentos', 2.49, 1.10, 'un', 'McCain'),
(42, 'Lasanha Bolonhesa 1kg',       'Congelados',   'Refeicoes',    5.99, 3.20, 'un',   'Iglo');

-- =============================================================================
-- PARTE 4: Tabela CLIENTES (programa fidelidade)
-- =============================================================================

CREATE OR REPLACE TABLE CLIENTES (
    CLIENTE_ID      INTEGER,
    NOME            VARCHAR(80),
    EMAIL           VARCHAR(100),
    TELEFONE        VARCHAR(20),
    CIDADE          VARCHAR(30),
    DATA_REGISTO    DATE,
    SEGMENTO        VARCHAR(20)
);

INSERT INTO CLIENTES VALUES
(1,  'Maria da Graca Santos',    'maria.santos@email.pt',      '+351 912 345 678', 'Lisboa',   '2020-01-15', 'Premium'),
(2,  'Joao Pedro Almeida',      'joao.almeida@email.pt',      '+351 923 456 789', 'Lisboa',   '2020-03-20', 'Standard'),
(3,  'Ana Beatriz Ferreira',     'ana.ferreira@email.pt',      '+351 934 567 890', 'Porto',    '2020-06-10', 'Premium'),
(4,  'Carlos Manuel Costa',      'carlos.costa@email.pt',      '+351 945 678 901', 'Braga',    '2020-08-25', 'Standard'),
(5,  'Sofia Isabel Rodrigues',   'sofia.rodrigues@email.pt',   '+351 956 789 012', 'Coimbra',  '2021-01-05', 'Premium'),
(6,  'Pedro Miguel Sousa',       'pedro.sousa@email.pt',       '+351 967 890 123', 'Faro',     '2021-03-18', 'Standard'),
(7,  'Ines Margarida Lopes',     'ines.lopes@email.pt',        '+351 978 901 234', 'Aveiro',   '2021-05-30', 'Standard'),
(8,  'Ricardo Jorge Martins',    'ricardo.martins@email.pt',   '+351 989 012 345', 'Setubal',  '2021-08-12', 'Premium'),
(9,  'Catarina Sofia Pereira',   'catarina.pereira@email.pt',  '+351 910 123 456', 'Lisboa',   '2021-11-20', 'Standard'),
(10, 'Miguel Angelo Oliveira',   'miguel.oliveira@email.pt',   '+351 921 234 567', 'Porto',    '2022-02-14', 'Premium'),
(11, 'Teresa Maria Gonçalves',   'teresa.goncalves@email.pt',  '+351 932 345 678', 'Evora',    '2022-04-28', 'Standard'),
(12, 'Antonio Jose Ribeiro',     'antonio.ribeiro@email.pt',   '+351 943 456 789', 'Funchal',  '2022-07-10', 'Standard'),
(13, 'Mariana Cruz Silva',       'mariana.silva@email.pt',     '+351 954 567 890', 'Lisboa',   '2022-09-22', 'Premium'),
(14, 'Diogo Rafael Carvalho',    'diogo.carvalho@email.pt',    '+351 965 678 901', 'Porto',    '2023-01-08', 'Standard'),
(15, 'Leonor Beatriz Moreira',   'leonor.moreira@email.pt',    '+351 976 789 012', 'Braga',    '2023-03-30', 'Standard'),
(16, 'Francisco Jose Teixeira',  'francisco.teixeira@email.pt', '+351 987 890 123', 'Coimbra', '2023-06-15', 'Premium'),
(17, 'Beatriz Helena Nunes',     'beatriz.nunes@email.pt',     '+351 918 901 234', 'Lisboa',   '2023-09-01', 'Standard'),
(18, 'Tiago Manuel Fernandes',   'tiago.fernandes@email.pt',   '+351 929 012 345', 'Faro',     '2023-11-20', 'Standard'),
(19, 'Matilde Sara Correia',     'matilde.correia@email.pt',   '+351 940 123 456', 'Aveiro',   '2024-02-10', 'Premium'),
(20, 'Guilherme Pedro Pinto',    'guilherme.pinto@email.pt',   '+351 951 234 567', 'Setubal',  '2024-05-05', 'Standard');

-- =============================================================================
-- PARTE 5: Tabela VENDAS (transacoes POS, Jan-Jun 2025)
-- =============================================================================

CREATE OR REPLACE TABLE VENDAS (
    VENDA_ID        INTEGER AUTOINCREMENT,
    LOJA_ID         INTEGER,
    CLIENTE_ID      INTEGER,
    PRODUTO_ID      INTEGER,
    DATA_VENDA      DATE,
    HORA_VENDA      TIME,
    QUANTIDADE      INTEGER,
    VALOR_TOTAL     DECIMAL(10,2),
    METODO_PAGAMENTO VARCHAR(20)
);

INSERT INTO VENDAS (LOJA_ID, CLIENTE_ID, PRODUTO_ID, DATA_VENDA, HORA_VENDA, QUANTIDADE, VALOR_TOTAL, METODO_PAGAMENTO)
SELECT
    UNIFORM(1, 12, RANDOM()) AS LOJA_ID,
    CASE WHEN UNIFORM(1, 100, RANDOM()) <= 70 THEN UNIFORM(1, 20, RANDOM()) ELSE NULL END AS CLIENTE_ID,
    UNIFORM(1, 42, RANDOM()) AS PRODUTO_ID,
    DATEADD('day', SEQ4() % 181, '2025-01-01'::DATE) AS DATA_VENDA,
    TIMEADD('minute', UNIFORM(480, 1320, RANDOM()), '00:00:00'::TIME) AS HORA_VENDA,
    UNIFORM(1, 5, RANDOM()) AS QUANTIDADE,
    ROUND(UNIFORM(1, 42, RANDOM()) * UNIFORM(1, 5, RANDOM()) * 2.5, 2) AS VALOR_TOTAL,
    CASE UNIFORM(1, 4, RANDOM())
        WHEN 1 THEN 'Multibanco'
        WHEN 2 THEN 'MBWay'
        WHEN 3 THEN 'Dinheiro'
        ELSE 'Cartao Credito'
    END AS METODO_PAGAMENTO
FROM TABLE(GENERATOR(ROWCOUNT => 3000));

UPDATE VENDAS v
SET VALOR_TOTAL = v.QUANTIDADE * p.PRECO_VENDA
FROM PRODUTOS p
WHERE v.PRODUTO_ID = p.PRODUTO_ID;

-- =============================================================================
-- PARTE 6: Tabela REVIEWS (feedback de clientes em portugues)
-- =============================================================================

CREATE OR REPLACE TABLE REVIEWS_PRODUTOS (
    REVIEW_ID       INTEGER,
    PRODUTO_ID      INTEGER,
    CLIENTE_ID      INTEGER,
    DATA_REVIEW     DATE,
    RATING          INTEGER,
    COMENTARIO      VARCHAR(500)
);

INSERT INTO REVIEWS_PRODUTOS VALUES
(1,  1,  1,  '2026-01-20', 5, 'Macas sempre frescas e crocantes. A qualidade do SuperNova e consistente.'),
(2,  9,  3,  '2026-01-25', 5, 'Salmao fresco de excelente qualidade. Muito melhor que na concorrencia.'),
(3,  13, 5,  '2026-02-01', 4, 'Azeite muito bom, sabor intenso. Preco justo para a qualidade.'),
(4,  7,  2,  '2026-02-10', 3, 'Frango aceitavel mas ja comprei melhor. Podiam melhorar a frescura.'),
(5,  21, 4,  '2026-02-15', 5, 'Super Bock sempre ao melhor preco. Promocoes frequentes.'),
(6,  32, 6,  '2026-02-20', 4, 'Papel higienico Renova, boa qualidade. Pacote grande dura bastante.'),
(7,  10, 8,  '2026-03-01', 5, 'Melhor bacalhau demolhado que ja encontrei em supermercado. Muito pratico.'),
(8,  37, 9,  '2026-03-05', 2, 'Pizza congelada dececionante. Massa fina demais e pouco recheio.'),
(9,  16, 1,  '2026-03-10', 5, 'Cafe Delta e o melhor. Aroma incrivel todas as manhas.'),
(10, 4,  10, '2026-03-15', 4, 'Tomate cherry sabor otimo mas o preco subiu bastante ultimamente.'),
(11, 22, 13, '2026-03-20', 5, 'Vinho do Alentejo fantastico para o preco. Otima relacao qualidade-preco.'),
(12, 38, 7,  '2026-03-25', 3, 'Gelado razoavel. Esperava mais cremosidade para um gelado de marca.'),
(13, 30, 5,  '2026-04-01', 5, 'Queijo Serra da Estrela autentico. Textura perfeita e sabor intenso. Vale cada centimo.'),
(14, 8,  3,  '2026-04-05', 4, 'Bife de novilho macio e saboroso. So nao dou 5 porque o corte podia ser mais uniforme.'),
(15, 25, 17, '2026-04-10', 1, 'Leite com sabor estranho no ultimo pacote. Data de validade OK mas qualidade duvidosa.'),
(16, 19, 11, '2026-04-15', 5, 'Agua Luso e a minha agua preferida. Preco imbativel no SuperNova.'),
(17, 31, 14, '2026-04-20', 4, 'Detergente eficaz e bom preco. Roupa fica limpa e com bom aroma.'),
(18, 2,  19, '2026-05-01', 5, 'Banana da Madeira e incomparavel. Doce, saborosa, sempre no ponto certo.'),
(19, 40, 12, '2026-05-10', 2, 'Filetes de pescada com demasiado gelo. Peso real muito inferior ao indicado.'),
(20, 6,  16, '2026-05-15', 4, 'Cenoura bio otima para sumos. Sabe-se a diferenca do biologico.');

-- =============================================================================
-- VERIFICACAO FINAL
-- =============================================================================

SELECT 
    (SELECT COUNT(*) FROM LOJAS) AS LOJAS,
    (SELECT COUNT(*) FROM PRODUTOS) AS PRODUTOS,
    (SELECT COUNT(*) FROM CLIENTES) AS CLIENTES,
    (SELECT COUNT(*) FROM VENDAS) AS VENDAS,
    (SELECT COUNT(*) FROM REVIEWS_PRODUTOS) AS REVIEWS;

-- =============================================================================
-- NOTA: Os dados de inflacao (CPI) vem diretamente do Marketplace!
-- A base FINANCE__ECONOMICS.CYBERSYN ja esta disponivel na conta.
-- No Passo 2, o dbt vai consumir esses dados diretamente - sem copias!
-- =============================================================================
