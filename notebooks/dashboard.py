"""
Churn Analytics Dashboard - Avec filtres dynamiques
Pour lancer : streamlit run dashboard_grid.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ===========================================================
# CONFIGURATION & STYLE
# ===========================================================
st.set_page_config(page_title="Churn Analytics Dashboard", layout="wide", page_icon="📡")

CRIMSON = "#D6294F"
NAVY = "#1B2A4A"
GOLD = "#F4B93B"
TEAL = "#4FC3DC"
GRAY_BG = "#F2F3F5"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {GRAY_BG}; }}
    .card {{
        background-color: white;
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }}
    .card-title {{ font-size: 15px; font-weight: 700; color: {NAVY}; margin-bottom: 2px; }}
    .card-subtitle {{ font-size: 11.5px; color: #8a8f98; margin-bottom: 8px; }}
    h1 {{ color: {NAVY}; font-weight: 800; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{ background-color: white; }}
    </style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    margin=dict(l=10, r=10, t=10, b=10), height=190,
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(size=11, color=NAVY), showlegend=False,
)

def card_wrapper(title, subtitle, fig):
    st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# DONNÉES
# ===========================================================
@st.cache_data
def load_data():
    df_raw = pd.read_csv('../Data/raw/telco_churn_raw.csv')
    df_raw['TotalCharges'] = pd.to_numeric(df_raw['TotalCharges'], errors='coerce').fillna(0)
    return df_raw

df_full = load_data()

# ===========================================================
# BARRE LATÉRALE : FILTRES DYNAMIQUES
# ===========================================================
st.sidebar.title("🎛️ Filtres")
st.sidebar.markdown("Ajustez les filtres pour mettre à jour le dashboard en temps réel.")
st.sidebar.markdown("---")

contract_filter = st.sidebar.multiselect(
    "Type de contrat",
    options=df_full['Contract'].unique(),
    default=df_full['Contract'].unique()
)

internet_filter = st.sidebar.multiselect(
    "Service internet",
    options=df_full['InternetService'].unique(),
    default=df_full['InternetService'].unique()
)

gender_filter = st.sidebar.multiselect(
    "Genre",
    options=df_full['gender'].unique(),
    default=df_full['gender'].unique()
)

senior_filter = st.sidebar.radio(
    "Senior Citizen",
    options=["Tous", "Senior uniquement", "Non-senior uniquement"],
    index=0
)

tenure_range = st.sidebar.slider(
    "Ancienneté (mois)",
    min_value=int(df_full['tenure'].min()),
    max_value=int(df_full['tenure'].max()),
    value=(int(df_full['tenure'].min()), int(df_full['tenure'].max()))
)

charges_range = st.sidebar.slider(
    "Charges mensuelles (€)",
    min_value=float(df_full['MonthlyCharges'].min()),
    max_value=float(df_full['MonthlyCharges'].max()),
    value=(float(df_full['MonthlyCharges'].min()), float(df_full['MonthlyCharges'].max()))
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Réinitialiser les filtres"):
    st.rerun()

# ===========================================================
# APPLICATION DES FILTRES
# ===========================================================
df = df_full[
    (df_full['Contract'].isin(contract_filter)) &
    (df_full['InternetService'].isin(internet_filter)) &
    (df_full['gender'].isin(gender_filter)) &
    (df_full['tenure'].between(tenure_range[0], tenure_range[1])) &
    (df_full['MonthlyCharges'].between(charges_range[0], charges_range[1]))
]

if senior_filter == "Senior uniquement":
    df = df[df['SeniorCitizen'] == 1]
elif senior_filter == "Non-senior uniquement":
    df = df[df['SeniorCitizen'] == 0]

# Message si le filtre ne retourne rien
if len(df) == 0:
    st.error("⚠️ Aucun client ne correspond aux filtres sélectionnés. Élargissez vos critères.")
    st.stop()

churn_yes = (df['Churn'] == 'Yes').sum()
churn_no = (df['Churn'] == 'No').sum()
churn_rate = churn_yes / len(df) * 100 if len(df) > 0 else 0

# ===========================================================
# EN-TÊTE
# ===========================================================
st.markdown("# Churn Analytics Dashboard")
st.markdown(f"<p style='color:#8a8f98; margin-top:-10px;'>{len(df):,} clients affichés sur {len(df_full):,} au total (après filtres)</p>", unsafe_allow_html=True)
st.write("")

# ===========================================================
# RANGÉE 1
# ===========================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig = go.Figure(data=[go.Pie(
        values=[churn_no, churn_yes], hole=0.55,
        marker_colors=[TEAL, CRIMSON], textinfo='none'
    )])
    fig.update_layout(**PLOTLY_LAYOUT)
    st.markdown(f"""
        <div class="card">
            <div class="card-title">Churn vs Not Churn</div>
            <div class="card-subtitle">Taux de churn : {churn_rate:.0f}%</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='text-align:center'><b style='color:{CRIMSON}'>{churn_yes:,}</b><br><span style='font-size:11px;color:#8a8f98'>Churn</span></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center'><b style='color:{TEAL}'>{churn_no:,}</b><br><span style='font-size:11px;color:#8a8f98'>Retenus</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    gender_churn = df[df['Churn'] == 'Yes']['gender'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=['Femmes', 'Hommes'],
        y=[gender_churn.get('Female', 0), gender_churn.get('Male', 0)],
        marker_color=[CRIMSON, NAVY],
        text=[gender_churn.get('Female', 0), gender_churn.get('Male', 0)], textposition='outside'
    )])
    fig.update_layout(**PLOTLY_LAYOUT)
    card_wrapper("Répartition par genre", "Parmi les clients ayant churné", fig)

with col3:
    senior_churn = df[df['Churn'] == 'Yes']['SeniorCitizen'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=['Non senior', 'Senior'],
        y=[senior_churn.get(0, 0), senior_churn.get(1, 0)],
        marker_color=[GOLD, CRIMSON],
        text=[senior_churn.get(0, 0), senior_churn.get(1, 0)], textposition='outside'
    )])
    fig.update_layout(**PLOTLY_LAYOUT)
    card_wrapper("Churn par âge (Senior)", "Répartition sur la sélection actuelle", fig)

with col4:
    partner_churn = df[df['Churn'] == 'Yes']['Partner'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=['Sans partenaire', 'Avec partenaire'],
        y=[partner_churn.get('No', 0), partner_churn.get('Yes', 0)],
        marker_color=[CRIMSON, GOLD],
        text=[partner_churn.get('No', 0), partner_churn.get('Yes', 0)], textposition='outside'
    )])
    fig.update_layout(**PLOTLY_LAYOUT)
    card_wrapper("Churn par statut de couple", "Répartition sur la sélection actuelle", fig)

# ===========================================================
# RANGÉE 2
# ===========================================================
col5, col6, col7 = st.columns([1, 2, 1])

with col5:
    internet_churn = df[df['Churn'] == 'Yes']['InternetService'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=internet_churn.index, y=internet_churn.values,
        marker_color=[CRIMSON, NAVY, TEAL][:len(internet_churn)],
        text=internet_churn.values, textposition='outside'
    )])
    fig.update_layout(**PLOTLY_LAYOUT)
    card_wrapper("Churn par service internet", "Sur la sélection filtrée", fig)

with col6:
    contract_churn = df[df['Churn'] == 'Yes']['Contract'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=contract_churn.index, y=contract_churn.values,
        marker_color=[CRIMSON, GOLD, TEAL][:len(contract_churn)],
        text=contract_churn.values, textposition='outside'
    )])
    fig.update_layout(**{**PLOTLY_LAYOUT, 'height': 190})
    card_wrapper("Churn par type de contrat", "Sur la sélection filtrée", fig)

with col7:
    payment_churn = df[df['Churn'] == 'Yes']['PaymentMethod'].value_counts()
    fig = go.Figure(data=[go.Bar(
        y=payment_churn.index, x=payment_churn.values, orientation='h',
        marker_color=CRIMSON, text=payment_churn.values, textposition='outside'
    )])
    fig.update_layout(**{**PLOTLY_LAYOUT, 'height': 190})
    card_wrapper("Churn par moyen de paiement", "Sur la sélection filtrée", fig)

# ===========================================================
# RANGÉE 3
# ===========================================================
col8, col9, col10 = st.columns(3)

with col8:
    df_bucket = df.copy()
    df_bucket['tenure_bucket'] = pd.cut(df_bucket['tenure'], bins=[0, 12, 24, 36, 48, 60, 72],
                                          labels=['0-12', '12-24', '24-36', '36-48', '48-60', '60-72'])
    tenure_churn = df_bucket[df_bucket['Churn'] == 'Yes']['tenure_bucket'].value_counts().sort_index()
    fig = go.Figure(data=[go.Bar(
        x=tenure_churn.index.astype(str), y=tenure_churn.values,
        marker_color=CRIMSON, text=tenure_churn.values, textposition='outside'
    )])
    fig.update_layout(**PLOTLY_LAYOUT)
    card_wrapper("Ancienneté vs Churn", "Sur la sélection filtrée", fig)

with col9:
    if len(df) > 5:
        df_bucket['charges_bucket'] = pd.cut(df_bucket['MonthlyCharges'], bins=5)
        charges_churn = df_bucket[df_bucket['Churn'] == 'Yes']['charges_bucket'].value_counts().sort_index()
        fig = go.Figure(data=[go.Bar(
            x=[f"{int(i.left)}-{int(i.right)}" for i in charges_churn.index], y=charges_churn.values,
            marker_color=GOLD, text=charges_churn.values, textposition='outside'
        )])
        fig.update_layout(**PLOTLY_LAYOUT)
        card_wrapper("Charges mensuelles vs Churn", "Sur la sélection filtrée", fig)

with col10:
    resultats_auc = {
        'Rég. Logistique': 0.842, 'KNN': 0.793, 'Naive Bayes': 0.809,
        'Arbre Décision': 0.825, 'RF base': 0.828, 'RF optimisé': 0.841
    }
    fig = go.Figure(data=[go.Bar(
        y=list(resultats_auc.keys()), x=list(resultats_auc.values()), orientation='h',
        marker_color=NAVY, text=[f"{v:.3f}" for v in resultats_auc.values()], textposition='outside'
    )])
    fig.update_layout(**{**PLOTLY_LAYOUT, 'xaxis': dict(range=[0.6, 0.9])})
    card_wrapper("Comparaison des modèles (AUC)", "Résultats fixes (indépendants des filtres)", fig)

# ===========================================================
# PIED DE PAGE
# ===========================================================
st.markdown("---")
st.caption("Projet #3 - Prédiction du Churn Client - L'École Multimédia")