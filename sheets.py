"""
Integração com Google Sheets para coleta centralizada de dados do jogo.

Como funciona:
- Usa uma Conta de Serviço (Service Account) do Google Cloud, autenticada via
  st.secrets (arquivo .streamlit/secrets.toml localmente, ou "Secrets" no
  painel do Streamlit Community Cloud quando publicado).
- Cada resposta final do jogo vira UMA LINHA na planilha configurada.
- Se as credenciais não estiverem configuradas, o app não quebra: ele
  simplesmente não envia para o Sheets (fica só no localStorage do navegador),
  e informa isso na tela de resultado.

Configuração necessária em st.secrets (ver .streamlit/secrets.toml.example):

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "...@....iam.gserviceaccount.com"
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"

[gsheet]
sheet_id = "ID_DA_PLANILHA_NA_URL"
worksheet_name = "respostas"
"""

import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Ordem das colunas na planilha. A primeira linha (cabeçalho) é criada
# automaticamente na primeira gravação, caso a planilha esteja vazia.
HEADER = [
    "timestamp_iso",
    "user_id",
    "nickname",
    "icc_pre_pct",
    "icc_post_pct",
    "icc_delta_pct",
    "icc_pre_conhecimento",
    "icc_pre_atitude",
    "icc_pre_intencao",
    "icc_post_conhecimento",
    "icc_post_atitude",
    "icc_post_intencao",
    "scoac_total",
    "scoac_at_risk",
    "scoac_ameaca",
    "scoac_difamacao_exposicao",
    "scoac_problemas_emocionais",
    "reputation",
    "reputation_tier",
    "ending_title",
    "story_path_json",
]


def is_configured() -> bool:
    """Verifica se as credenciais e a planilha estão configuradas em st.secrets."""
    if not GSPREAD_AVAILABLE:
        return False
    try:
        return "gcp_service_account" in st.secrets and "gsheet" in st.secrets
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def _get_client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    client = _get_client()
    gs_conf = st.secrets["gsheet"]
    sheet_id = gs_conf.get("sheet_id")
    sheet_title = gs_conf.get("sheet_title")
    worksheet_name = gs_conf.get("worksheet_name", "respostas")

    if sheet_id:
        sh = client.open_by_key(sheet_id)
    elif sheet_title:
        sh = client.open(sheet_title)
    else:
        raise ValueError("Configure 'sheet_id' ou 'sheet_title' em st.secrets['gsheet'].")

    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows=2000, cols=len(HEADER) + 2)

    existing = ws.get_all_values()
    if not existing:
        ws.append_row(HEADER, value_input_option="USER_ENTERED")

    return ws


def append_record(record: dict) -> tuple[bool, str]:
    """
    Envia um registro (uma jogada finalizada) para o Google Sheets.
    Retorna (sucesso: bool, mensagem: str).
    """
    if not is_configured():
        return False, "Google Sheets não configurado — dados salvos apenas no navegador."
    try:
        ws = _get_worksheet()
        row = [record.get(col, "") for col in HEADER]
        ws.append_row(row, value_input_option="USER_ENTERED")
        return True, "Dados enviados para a planilha com sucesso."
    except Exception as e:
        return False, f"Falha ao enviar para o Google Sheets: {e}"
