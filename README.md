# 📊 Análise do Mercado de Trabalho em Tecnologia da Informação

**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Aluno:** Piersilvio de Carvalho Orlandini  
**Tema:** 25 — Mercado de Trabalho em TI no Brasil (2015–2024)

---

## 🎯 Objetivo

Este projeto analisa tendências do mercado de trabalho em Tecnologia da Informação no Brasil entre 2015 e 2024, investigando:

- Cargos mais demandados
- Tecnologias mais requisitadas
- Evolução salarial ao longo do tempo
- Distribuição regional de vagas
- Comparativo entre modalidades de trabalho
- Análise por senioridade

---

## 🗂️ Estrutura do Projeto

```
Projeto-Final/
│
├── app.py                  # Dashboard Streamlit principal
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação
├── index.html              # Página GitHub Pages
├── dados/
│   └── simulacao_mercado_ti_brasil.csv
├── notebooks/
│   └── analise_mercado_ti.ipynb
├── database/
│   └── mercado_ti.db       # Banco SQLite (gerado ao executar app.py)
└── imagens/
```

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/Projeto-Final.git
cd Projeto-Final
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o dashboard

```bash
streamlit run app.py
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.11+ | Linguagem principal |
| Pandas | Manipulação e análise de dados |
| Plotly | Gráficos interativos |
| Streamlit | Dashboard web |
| SQLAlchemy + SQLite | Persistência em banco de dados |
| NumPy | Cálculos estatísticos |
| Seaborn / Matplotlib | Visualizações no notebook |
| GitHub Pages | Publicação da página do projeto |
| Streamlit Cloud | Publicação do dashboard |

---

## 📈 KPIs e Análises

- **Total de Vagas** no período selecionado
- **Cargo mais demandado** no mercado
- **Tecnologia mais requisitada**
- **Salário médio nacional**
- **Região com mais oportunidades**
- **Modalidade predominante** (Remoto / Híbrido / Presencial)

---

## 🌐 Links

- 🔗 **GitHub:** [github.com/SEU_USUARIO/Projeto-Final](https://github.com/SEU_USUARIO/Projeto-Final)
- 🌍 **GitHub Pages:** [SEU_USUARIO.github.io/Projeto-Final](https://SEU_USUARIO.github.io/Projeto-Final)
- 📊 **Dashboard Streamlit:** [seu-app.streamlit.app](https://seu-app.streamlit.app)

---

## 👤 Autor

**Piersilvio de Carvalho Orlandini**  
Projeto de Avaliação G2 — Análise e Visualização de Dados com Python
