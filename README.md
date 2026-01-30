# Terminal de Inteligência de Mercado - B3

Este projeto automatiza o ciclo completo de dados financeiros de ativos listados na B3: desde a extração de cotações e indicadores fundamentalistas via Python, passando pela modelagem em SQL, até a visualização analítica avançada no Power BI.

## Visão Geral
O objetivo desta ferramenta é fornecer suporte à decisão para investidores, permitindo o cruzamento de preços históricos com a saúde contábil real das empresas (DRE e Balanço Patrimonial) de forma automática e escalável.

## Tecnologias Utilizadas
* **Python**: Extração de dados com a biblioteca `yfinance`.
* **Pandas**: Manipulação, limpeza e tratamento de grandes volumes de dados.
* **SQL (SQLite)**: Armazenamento e persistência dos dados estruturados em banco de dados local.
* **Power BI**: Dashboards analíticos com DAX avançado e visuais customizados via integração HTML/CSS.

---

## Estrutura do Projeto
* `invest_extractor.py`: Script mestre que centraliza o pipeline de extração de metadados, contabilidade trimestral e histórico de preços.

* `dados_investimentos.db`: Banco de dados SQLite.

* `projeto_carteira.pbip`: Relatório final com análises de performance, volume e fundamentos econômicos.

---

## Principais Funcionalidades

### 1. Engenharia de Dados e Extração
* **Automação Completa**: Captura de preços ajustados (corrigidos automaticamente por dividendos e *splits*) diretamente da B3 via Yahoo Finance.
* **Pipeline Fundamentalista**: Extração de indicadores críticos como EBITDA, Lucro Líquido, Dívida Total e Patrimônio Líquido.

### 2. Modelagem e Performance
* **Modelagem Star Schema**: Dados organizados para garantir alta performance e facilidade na criação de novas métricas em DAX.
* **Persistência Estruturada**: Uso de SQL para garantir que o histórico de cotações seja preservado e consultado de forma eficiente.

### 3. Visualização e UX (User Experience)
* **Design Premium**: Interface desenvolvida com foco em usabilidade (Dark Mode).
* **Visuais Dinâmicos**: Integração de logos de empresas via HTML/CSS, eliminando barras de rolagem e garantindo transparência nos visuais.

---

## Como Executar
1. Instale as dependências necessárias:
   ```bash
   pip install yfinance pandas

2. Executar script de extração:  
   ```bash
   py invest_extractor.py