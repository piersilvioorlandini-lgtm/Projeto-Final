import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sqlalchemy import create_engine, text
import os

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mercado de TI no Brasil",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0ea5e9;
        margin-bottom: 4px;
    }
    .sub-title {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    .kpi-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #38bdf8;
        border-left: 4px solid #0ea5e9;
        padding-left: 10px;
        margin: 24px 0 14px 0;
    }
    .interpret-box {
        background: #1e293b;
        border-left: 4px solid #0ea5e9;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.7;
        margin-top: 8px;
    }
    .footer-box {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: #475569;
        font-size: 0.85rem;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BANCO DE DADOS SQLite (Funcionalidade Avançada)
# ─────────────────────────────────────────────
DB_PATH = "database/mercado_ti.db"
CSV_PATH = "dados/simulacao_mercado_ti_brasil.csv"

@st.cache_resource
def init_db():
    os.makedirs("database", exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df_raw = pd.read_csv(CSV_PATH)
    df_raw.to_sql("mercado_ti", engine, if_exists="replace", index=False)
    return engine

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, parse_dates=["data"])
    df["data"] = pd.to_datetime(df["data"])
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)
    return df

engine = init_db()
df_full = load_data()

# ─────────────────────────────────────────────
# NAVEGAÇÃO MULTIPÁGINA (Funcionalidade Avançada)
# ─────────────────────────────────────────────
st.sidebar.markdown("## 💻 Mercado de TI Brasil")
st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "📌 Navegação",
    ["🏠 Visão Geral", "📈 Análise Temporal", "🗺️ Análise Regional",
     "⚙️ Tecnologias e Cargos", "💰 Análise Salarial", "🔍 Explorador de Dados"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎚️ Filtros Globais")

# ─── FILTROS (Funcionalidade Intermediária) ───
anos = sorted(df_full["ano"].unique())
sel_anos = st.sidebar.select_slider("Período (Ano)", options=anos, value=(anos[0], anos[-1]))

regioes = ["Todas"] + sorted(df_full["regiao"].unique().tolist())
sel_regiao = st.sidebar.selectbox("Região", regioes)

ufs = ["Todas"] + sorted(df_full["uf"].unique().tolist())
sel_uf = st.sidebar.selectbox("Estado (UF)", ufs)

cargos = ["Todos"] + sorted(df_full["cargo"].unique().tolist())
sel_cargo = st.sidebar.selectbox("Cargo", cargos)

tecnologias = ["Todas"] + sorted(df_full["tecnologia"].unique().tolist())
sel_tec = st.sidebar.selectbox("Tecnologia", tecnologias)

senioridades = ["Todas"] + sorted(df_full["senioridade"].unique().tolist())
sel_sen = st.sidebar.selectbox("Senioridade", senioridades)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.78rem;color:#475569;text-align:center;'>Piersilvio de Carvalho Orlandini<br>Avaliação G2 · Tema 25</div>",
    unsafe_allow_html=True
)

# ─── APLICAR FILTROS ───
df = df_full[
    (df_full["ano"] >= sel_anos[0]) &
    (df_full["ano"] <= sel_anos[1])
].copy()

if sel_regiao != "Todas":
    df = df[df["regiao"] == sel_regiao]
if sel_uf != "Todas":
    df = df[df["uf"] == sel_uf]
if sel_cargo != "Todos":
    df = df[df["cargo"] == sel_cargo]
if sel_tec != "Todas":
    df = df[df["tecnologia"] == sel_tec]
if sel_sen != "Todas":
    df = df[df["senioridade"] == sel_sen]

# ─────────────────────────────────────────────
# KPIs DINÂMICOS
# ─────────────────────────────────────────────
def render_kpis(df):
    total_vagas = int(df["quantidade_vagas"].sum())
    cargo_top = df.groupby("cargo")["quantidade_vagas"].sum().idxmax() if not df.empty else "—"
    tec_top = df.groupby("tecnologia")["quantidade_vagas"].sum().idxmax() if not df.empty else "—"
    salario_med = df["salario_medio"].mean()
    regiao_top = df.groupby("regiao")["quantidade_vagas"].sum().idxmax() if not df.empty else "—"
    modal_top = df.groupby("modalidade")["quantidade_vagas"].sum().idxmax() if not df.empty else "—"

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpis = [
        (c1, f"{total_vagas:,}".replace(",", "."), "Total de Vagas"),
        (c2, cargo_top, "Cargo + Demandado"),
        (c3, tec_top, "Tecnologia + Requisitada"),
        (c4, f"R$ {salario_med:,.0f}".replace(",", "."), "Salário Médio Nacional"),
        (c5, regiao_top, "Região c/ Mais Vagas"),
        (c6, modal_top, "Modalidade Predominante"),
    ]
    for col, val, lbl in kpis:
        with col:
            st.markdown(
                f'<div class="kpi-box"><div class="kpi-value">{val}</div>'
                f'<div class="kpi-label">{lbl}</div></div>',
                unsafe_allow_html=True
            )

# ═══════════════════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ═══════════════════════════════════════════════════════════
if pagina == "🏠 Visão Geral":
    st.markdown('<div class="main-title">📊 Mercado de TI no Brasil</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Análise de Tendências do Mercado de Trabalho em Tecnologia da Informação · 2015–2024</div>',
        unsafe_allow_html=True
    )
    st.markdown("""
    > Este dashboard analisa o mercado de trabalho em TI no Brasil entre **2015 e 2024**,
    > investigando cargos, tecnologias, salários e distribuição regional.
    > Use os **filtros na barra lateral** para explorar os dados interativamente.
    """)

    st.markdown('<div class="section-header">📌 Indicadores-Chave (KPIs)</div>', unsafe_allow_html=True)
    render_kpis(df)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">📅 Evolução Anual de Vagas</div>', unsafe_allow_html=True)
        ev = df.groupby("ano")["quantidade_vagas"].sum().reset_index()
        fig = px.bar(ev, x="ano", y="quantidade_vagas",
                     text_auto=True, color="quantidade_vagas",
                     color_continuous_scale="Blues",
                     labels={"ano": "Ano", "quantidade_vagas": "Total de Vagas"})
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">🌍 Vagas por Região</div>', unsafe_allow_html=True)
        reg = df.groupby("regiao")["quantidade_vagas"].sum().reset_index()
        fig2 = px.pie(reg, names="regiao", values="quantidade_vagas",
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      hole=0.4)
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#e2e8f0")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">💼 Vagas por Cargo</div>', unsafe_allow_html=True)
        cargo_df = df.groupby("cargo")["quantidade_vagas"].sum().sort_values().reset_index()
        fig3 = px.bar(cargo_df, x="quantidade_vagas", y="cargo", orientation="h",
                      color="quantidade_vagas", color_continuous_scale="Blues",
                      labels={"cargo": "Cargo", "quantidade_vagas": "Vagas"})
        fig3.update_layout(showlegend=False, coloraxis_showscale=False,
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#e2e8f0")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">⚙️ Vagas por Tecnologia</div>', unsafe_allow_html=True)
        tec_df = df.groupby("tecnologia")["quantidade_vagas"].sum().sort_values().reset_index()
        fig4 = px.bar(tec_df, x="quantidade_vagas", y="tecnologia", orientation="h",
                      color="quantidade_vagas", color_continuous_scale="Teal",
                      labels={"tecnologia": "Tecnologia", "quantidade_vagas": "Vagas"})
        fig4.update_layout(showlegend=False, coloraxis_showscale=False,
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#e2e8f0")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="interpret-box">🔎 <strong>Interpretação:</strong> A visão geral demonstra que o mercado de TI apresenta crescimento consistente ao longo do período analisado. A região Sudeste concentra a maior parte das oportunidades, enquanto Python e SQL lideram as tecnologias mais requisitadas. Os cargos de Dev Backend e Cientista de Dados se destacam em volume de vagas.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 2 — ANÁLISE TEMPORAL
# ═══════════════════════════════════════════════════════════
elif pagina == "📈 Análise Temporal":
    st.markdown('<div class="main-title">📈 Análise Temporal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evolução das vagas e salários ao longo do tempo</div>', unsafe_allow_html=True)

    render_kpis(df)
    st.markdown("---")

    # Linha temporal mensal
    st.markdown('<div class="section-header">📅 Evolução Mensal de Vagas</div>', unsafe_allow_html=True)
    mensal = df.groupby("ano_mes")["quantidade_vagas"].sum().reset_index()
    mensal.columns = ["Período", "Vagas"]
    fig_line = px.line(mensal, x="Período", y="Vagas", markers=True,
                       color_discrete_sequence=["#0ea5e9"])
    fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#e2e8f0", xaxis_tickangle=-45)
    st.plotly_chart(fig_line, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">💰 Evolução Salarial por Ano</div>', unsafe_allow_html=True)
        sal_ano = df.groupby("ano")["salario_medio"].mean().reset_index()
        fig_sal = px.area(sal_ano, x="ano", y="salario_medio",
                          color_discrete_sequence=["#10b981"],
                          labels={"ano": "Ano", "salario_medio": "Salário Médio (R$)"})
        fig_sal.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e2e8f0")
        st.plotly_chart(fig_sal, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">🏠 Modalidade ao Longo do Tempo</div>', unsafe_allow_html=True)
        modal_tempo = df.groupby(["ano", "modalidade"])["quantidade_vagas"].sum().reset_index()
        fig_mod = px.line(modal_tempo, x="ano", y="quantidade_vagas",
                          color="modalidade", markers=True,
                          color_discrete_sequence=["#0ea5e9", "#f59e0b", "#10b981"],
                          labels={"ano": "Ano", "quantidade_vagas": "Vagas", "modalidade": "Modalidade"})
        fig_mod.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e2e8f0")
        st.plotly_chart(fig_mod, use_container_width=True)

    st.markdown('<div class="section-header">📊 Crescimento por Cargo ao Longo dos Anos</div>', unsafe_allow_html=True)
    cargo_tempo = df.groupby(["ano", "cargo"])["quantidade_vagas"].sum().reset_index()
    fig_ct = px.bar(cargo_tempo, x="ano", y="quantidade_vagas", color="cargo",
                    barmode="group",
                    labels={"ano": "Ano", "quantidade_vagas": "Vagas", "cargo": "Cargo"})
    fig_ct.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0")
    st.plotly_chart(fig_ct, use_container_width=True)

    st.markdown('<div class="interpret-box">🔎 <strong>Interpretação:</strong> A série temporal revela crescimento contínuo das vagas em TI, com aceleração notável a partir de 2020 — período que coincide com a digitalização acelerada pós-pandemia. O trabalho remoto passou de modalidade residual para competir com o presencial a partir de 2021. Salários também apresentam tendência de alta, principalmente para cargos de Cientista de Dados e DevOps.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 3 — ANÁLISE REGIONAL
# ═══════════════════════════════════════════════════════════
elif pagina == "🗺️ Análise Regional":
    st.markdown('<div class="main-title">🗺️ Análise Regional</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Distribuição geográfica de vagas e salários no Brasil</div>', unsafe_allow_html=True)

    render_kpis(df)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">🌍 Vagas Totais por Região</div>', unsafe_allow_html=True)
        reg_df = df.groupby("regiao")["quantidade_vagas"].sum().sort_values(ascending=False).reset_index()
        fig_r = px.bar(reg_df, x="regiao", y="quantidade_vagas",
                       text_auto=True, color="quantidade_vagas",
                       color_continuous_scale="Blues",
                       labels={"regiao": "Região", "quantidade_vagas": "Total de Vagas"})
        fig_r.update_layout(showlegend=False, coloraxis_showscale=False,
                             plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                             font_color="#e2e8f0")
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">💰 Salário Médio por Região</div>', unsafe_allow_html=True)
        sal_reg = df.groupby("regiao")["salario_medio"].mean().sort_values(ascending=False).reset_index()
        fig_sr = px.bar(sal_reg, x="regiao", y="salario_medio",
                        text_auto=".2f", color="salario_medio",
                        color_continuous_scale="Greens",
                        labels={"regiao": "Região", "salario_medio": "Salário Médio (R$)"})
        fig_sr.update_layout(showlegend=False, coloraxis_showscale=False,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font_color="#e2e8f0")
        st.plotly_chart(fig_sr, use_container_width=True)

    # Heatmap Regional
    st.markdown('<div class="section-header">🔥 Heatmap — Vagas por Região e Cargo</div>', unsafe_allow_html=True)
    heatmap_df = df.pivot_table(index="regiao", columns="cargo",
                                 values="quantidade_vagas", aggfunc="sum", fill_value=0)
    fig_heat = px.imshow(heatmap_df, text_auto=True, aspect="auto",
                          color_continuous_scale="Blues",
                          labels={"color": "Vagas"})
    fig_heat.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#e2e8f0")
    st.plotly_chart(fig_heat, use_container_width=True)

    # Por Estado
    st.markdown('<div class="section-header">🏛️ Top 10 Estados com Mais Vagas</div>', unsafe_allow_html=True)
    uf_df = df.groupby("uf")["quantidade_vagas"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_uf = px.bar(uf_df, x="uf", y="quantidade_vagas",
                    text_auto=True, color="quantidade_vagas",
                    color_continuous_scale="Purples",
                    labels={"uf": "Estado", "quantidade_vagas": "Total de Vagas"})
    fig_uf.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0")
    st.plotly_chart(fig_uf, use_container_width=True)

    st.markdown('<div class="interpret-box">🔎 <strong>Interpretação:</strong> O Sudeste, especialmente SP e RJ, concentra a maior parte das vagas em TI, reflexo da densidade econômica e dos grandes polos tecnológicos. Ainda assim, o Sul tem apresentado crescimento acelerado, com SC e PR como destaques. O trabalho remoto tende a redistribuir oportunidades para regiões historicamente sub-representadas como Norte e Nordeste.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 4 — TECNOLOGIAS E CARGOS
# ═══════════════════════════════════════════════════════════
elif pagina == "⚙️ Tecnologias e Cargos":
    st.markdown('<div class="main-title">⚙️ Tecnologias e Cargos</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Ranking de tecnologias e comparativo entre cargos</div>', unsafe_allow_html=True)

    render_kpis(df)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">🏆 Ranking de Tecnologias</div>', unsafe_allow_html=True)
        tec_rank = df.groupby("tecnologia")["quantidade_vagas"].sum().sort_values(ascending=False).reset_index()
        fig_tec = px.bar(tec_rank, x="tecnologia", y="quantidade_vagas",
                         text_auto=True, color="quantidade_vagas",
                         color_continuous_scale="Teal",
                         labels={"tecnologia": "Tecnologia", "quantidade_vagas": "Total de Vagas"})
        fig_tec.update_layout(showlegend=False, coloraxis_showscale=False,
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e2e8f0")
        st.plotly_chart(fig_tec, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">👔 Distribuição por Senioridade</div>', unsafe_allow_html=True)
        sen_df = df.groupby("senioridade")["quantidade_vagas"].sum().reset_index()
        fig_sen = px.pie(sen_df, names="senioridade", values="quantidade_vagas",
                         color_discrete_sequence=["#0ea5e9", "#06b6d4", "#38bdf8"],
                         hole=0.35)
        fig_sen.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e2e8f0")
        st.plotly_chart(fig_sen, use_container_width=True)

    # Heatmap Cargo x Tecnologia
    st.markdown('<div class="section-header">🔥 Heatmap — Cargo vs Tecnologia</div>', unsafe_allow_html=True)
    ct_heat = df.pivot_table(index="cargo", columns="tecnologia",
                              values="quantidade_vagas", aggfunc="sum", fill_value=0)
    fig_cth = px.imshow(ct_heat, text_auto=True, aspect="auto",
                         color_continuous_scale="Teal",
                         labels={"color": "Vagas"})
    fig_cth.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0")
    st.plotly_chart(fig_cth, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">🏢 Vagas por Setor Empresarial</div>', unsafe_allow_html=True)
        setor_df = df.groupby("empresa_setor")["quantidade_vagas"].sum().sort_values(ascending=False).reset_index()
        fig_setor = px.bar(setor_df, x="empresa_setor", y="quantidade_vagas",
                           text_auto=True, color="quantidade_vagas",
                           color_continuous_scale="Oranges",
                           labels={"empresa_setor": "Setor", "quantidade_vagas": "Vagas"})
        fig_setor.update_layout(showlegend=False, coloraxis_showscale=False,
                                 plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                 font_color="#e2e8f0")
        st.plotly_chart(fig_setor, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">⚠️ Nível de Demanda</div>', unsafe_allow_html=True)
        dem_df = df.groupby("nivel_demanda")["quantidade_vagas"].sum().reset_index()
        dem_order = ["Baixo", "Médio", "Alto", "Crítico"]
        dem_df["nivel_demanda"] = pd.Categorical(dem_df["nivel_demanda"], categories=dem_order, ordered=True)
        dem_df = dem_df.sort_values("nivel_demanda")
        fig_dem = px.bar(dem_df, x="nivel_demanda", y="quantidade_vagas",
                         text_auto=True, color="nivel_demanda",
                         color_discrete_map={"Baixo": "#22c55e", "Médio": "#f59e0b",
                                             "Alto": "#ef4444", "Crítico": "#7c3aed"},
                         labels={"nivel_demanda": "Nível", "quantidade_vagas": "Vagas"})
        fig_dem.update_layout(showlegend=False,
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e2e8f0")
        st.plotly_chart(fig_dem, use_container_width=True)

    st.markdown('<div class="interpret-box">🔎 <strong>Interpretação:</strong> Python e SQL dominam as exigências técnicas do mercado, refletindo a alta demanda por profissionais de dados. Java e JavaScript mantêm relevância no desenvolvimento backend e frontend, respectivamente. O setor de Fintech lidera a contratação de profissionais de TI, seguido por Saúde e Governo — indicando digitalização crescente além do setor privado tradicional.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 5 — ANÁLISE SALARIAL
# ═══════════════════════════════════════════════════════════
elif pagina == "💰 Análise Salarial":
    st.markdown('<div class="main-title">💰 Análise Salarial</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Correlação entre salários, vagas e perfil profissional</div>', unsafe_allow_html=True)

    render_kpis(df)
    st.markdown("---")

    # Dispersão salário x vagas (Correlação Estatística — Funcionalidade Avançada)
    st.markdown('<div class="section-header">📉 Dispersão: Salário Médio vs Quantidade de Vagas</div>', unsafe_allow_html=True)
    fig_disp = px.scatter(
        df, x="salario_medio", y="quantidade_vagas",
        color="cargo", size="quantidade_vagas",
        hover_data=["regiao", "tecnologia", "senioridade"],
        opacity=0.7,
        labels={"salario_medio": "Salário Médio (R$)",
                "quantidade_vagas": "Quantidade de Vagas",
                "cargo": "Cargo"},
        title="Correlação: Salário Médio x Quantidade de Vagas"
    )
    fig_disp.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#e2e8f0")
    st.plotly_chart(fig_disp, use_container_width=True)

    # Correlação numérica
    corr = df[["salario_medio", "quantidade_vagas"]].corr().iloc[0, 1]
    st.info(f"📊 **Coeficiente de Correlação (Pearson):** `{corr:.4f}` — {'correlação positiva fraca' if abs(corr) < 0.3 else 'correlação moderada' if abs(corr) < 0.6 else 'correlação forte'} entre salário e volume de vagas.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">💼 Salário Médio por Cargo</div>', unsafe_allow_html=True)
        sal_cargo = df.groupby("cargo")["salario_medio"].mean().sort_values(ascending=False).reset_index()
        fig_sc = px.bar(sal_cargo, x="cargo", y="salario_medio",
                        text_auto=".0f", color="salario_medio",
                        color_continuous_scale="Greens",
                        labels={"cargo": "Cargo", "salario_medio": "Salário Médio (R$)"})
        fig_sc.update_layout(showlegend=False, coloraxis_showscale=False,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font_color="#e2e8f0")
        st.plotly_chart(fig_sc, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">🎓 Salário Médio por Senioridade</div>', unsafe_allow_html=True)
        sal_sen = df.groupby("senioridade")["salario_medio"].mean().reset_index()
        ordem = {"Júnior": 1, "Pleno": 2, "Sênior": 3}
        sal_sen["ordem"] = sal_sen["senioridade"].map(ordem)
        sal_sen = sal_sen.sort_values("ordem")
        fig_ss = px.bar(sal_sen, x="senioridade", y="salario_medio",
                        text_auto=".0f", color="senioridade",
                        color_discrete_map={"Júnior": "#38bdf8", "Pleno": "#06b6d4", "Sênior": "#0369a1"},
                        labels={"senioridade": "Senioridade", "salario_medio": "Salário Médio (R$)"})
        fig_ss.update_layout(showlegend=False,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font_color="#e2e8f0")
        st.plotly_chart(fig_ss, use_container_width=True)

    # Box plot salário por cargo
    st.markdown('<div class="section-header">📦 Distribuição Salarial por Cargo (Box Plot)</div>', unsafe_allow_html=True)
    fig_box = px.box(df, x="cargo", y="salario_medio", color="cargo",
                     labels={"cargo": "Cargo", "salario_medio": "Salário Médio (R$)"},
                     color_discrete_sequence=px.colors.qualitative.Set2)
    fig_box.update_layout(showlegend=False,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0")
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="interpret-box">🔎 <strong>Interpretação:</strong> A análise salarial evidencia diferença significativa entre os níveis de senioridade — profissionais Sênior chegam a receber mais do que o dobro de um Júnior na mesma área. Cargos como DevOps e Cientista de Dados possuem os maiores salários medianos. A correlação entre salário e volume de vagas revela que cargos bem remunerados não são necessariamente os mais numerosos, apontando para escassez de profissionais qualificados.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 6 — EXPLORADOR DE DADOS (SQLAlchemy)
# ═══════════════════════════════════════════════════════════
elif pagina == "🔍 Explorador de Dados":
    st.markdown('<div class="main-title">🔍 Explorador de Dados</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Tabela dinâmica e consulta ao banco SQLite</div>', unsafe_allow_html=True)

    render_kpis(df)
    st.markdown("---")

    # Upload de arquivo CSV (Funcionalidade Intermediária)
    st.markdown('<div class="section-header">📂 Upload de Novo Dataset (CSV)</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Faça upload de um arquivo CSV para análise temporária", type=["csv"])
    if uploaded:
        df_upload = pd.read_csv(uploaded)
        st.success(f"✅ Arquivo carregado com sucesso! {df_upload.shape[0]} linhas × {df_upload.shape[1]} colunas.")
        st.dataframe(df_upload.head(20), use_container_width=True)
    else:
        st.markdown('<div class="section-header">📋 Tabela Dinâmica — Dados Filtrados</div>', unsafe_allow_html=True)
        st.dataframe(df.head(200), use_container_width=True, height=350)

    st.markdown("---")

    # Consulta SQL via SQLAlchemy (Funcionalidade Avançada)
    st.markdown('<div class="section-header">🗄️ Consulta SQL ao Banco de Dados (SQLite)</div>', unsafe_allow_html=True)
    st.markdown("Execute consultas diretamente na tabela `mercado_ti` persistida em SQLite:")

    default_query = "SELECT cargo, AVG(salario_medio) as salario_medio, SUM(quantidade_vagas) as total_vagas FROM mercado_ti GROUP BY cargo ORDER BY salario_medio DESC"
    query = st.text_area("Consulta SQL", value=default_query, height=80)

    if st.button("▶️ Executar Consulta"):
        try:
            with engine.connect() as conn:
                result = pd.read_sql(text(query), conn)
            st.success(f"✅ Consulta executada! {len(result)} registros retornados.")
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erro na consulta: {e}")

    st.markdown("---")
    st.markdown('<div class="section-header">📊 Estatísticas Descritivas</div>', unsafe_allow_html=True)
    st.dataframe(df[["salario_medio", "quantidade_vagas"]].describe().round(2), use_container_width=True)

    st.markdown('<div class="interpret-box">🔎 <strong>Interpretação:</strong> O explorador de dados permite análise ad hoc via SQL diretamente sobre o banco SQLite, possibilitando consultas customizadas sem necessidade de reprocessamento. O upload de CSV permite analisar datasets externos para comparação com o mercado de TI nacional.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONCLUSÃO EXECUTIVA (rodapé em todas as páginas)
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">✅ Conclusão Executiva</div>', unsafe_allow_html=True)
st.markdown("""
<div class="interpret-box">
<strong>📌 Principais conclusões do projeto:</strong><br><br>
• O mercado de TI brasileiro cresceu de forma consistente entre 2015 e 2024, com aceleração após 2020.<br>
• Python e SQL são as tecnologias mais demandadas, seguidas por JavaScript e AWS.<br>
• O Sudeste concentra o maior volume de vagas, mas o trabalho remoto está redistribuindo oportunidades geograficamente.<br>
• Profissionais Sênior recebem em média 2–3× mais que Júniores na mesma área.<br>
• DevOps e Cientista de Dados lideram em remuneração, enquanto Dev Frontend e Analista de Dados têm maior volume de vagas.<br>
• O setor de Fintech é o maior contratante de profissionais de TI no período analisado.
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="footer-box">Desenvolvido por <strong>Piersilvio de Carvalho Orlandini</strong> · Avaliação G2 · Tema 25 · Análise e Visualização de Dados com Python</div>',
    unsafe_allow_html=True
)
