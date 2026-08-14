import json
import uuid
from datetime import datetime

import streamlit as st
from streamlit_local_storage import LocalStorage

from icc_scale import ICC_ITEMS, LIKERT_LABELS, score_icc, awareness_tier
from scoac_scale import SCOAC_ITEMS, FREQ_LABELS, score_scoac
from story import STORY, get_reputation_tier
from resources import HELP_RESOURCES, IMPACT_PHRASES

# ----------------------------------------------------------------------------
# CONFIG & ESTILO
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Rede Consciente — Jogo contra o Cyberbullying",
    page_icon="🛡️",
    layout="centered",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, .story-title {
    font-family: 'Baloo 2', sans-serif !important;
}

.stApp {
    background: radial-gradient(circle at top left, #1e1b4b 0%, #0f0c29 45%, #0a0818 100%);
    color: #F1F5F9;
}

section.main > div { padding-top: 1.5rem; }

.hero-card {
    background: linear-gradient(135deg, #7C3AED 0%, #DB2777 100%);
    border-radius: 22px;
    padding: 28px 26px;
    box-shadow: 0 10px 40px rgba(124, 58, 237, 0.35);
    margin-bottom: 18px;
}
.hero-card h1 { color: white; margin: 0 0 8px 0; font-size: 2rem;}
.hero-card p { color: #EDE9FE; margin: 0; font-size: 1.02rem; }

.scene-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 22px 22px;
    margin-bottom: 16px;
    backdrop-filter: blur(6px);
}
.scene-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 8px; }
.scene-text { font-size: 1.02rem; line-height: 1.55; color: #E2E8F0; }

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    margin: 3px 4px 3px 0;
}
.rep-bar-bg {
    background: rgba(255,255,255,0.12);
    border-radius: 999px;
    height: 14px;
    width: 100%;
    overflow: hidden;
    margin: 6px 0 14px 0;
}
.rep-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease;
}
.impact-phrase {
    font-family: 'Baloo 2', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    padding: 22px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
    color: white;
    margin: 18px 0;
}
.resource-card {
    background: rgba(255,255,255,0.06);
    border-left: 4px solid #22C55E;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.footer-note {
    font-size: 0.78rem;
    color: #94A3B8;
    text-align: center;
    margin-top: 30px;
}
div.stButton > button {
    border-radius: 14px !important;
    border: none !important;
    padding: 0.7rem 1rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #7C3AED, #DB2777) !important;
    color: white !important;
    width: 100%;
}
div.stButton > button:hover { filter: brightness(1.1); }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

localS = LocalStorage()

# ----------------------------------------------------------------------------
# ESTADO / PERSISTÊNCIA (browser localStorage)
# ----------------------------------------------------------------------------
def init_state():
    defaults = {
        "stage": "welcome",
        "nickname": "",
        "user_id": None,
        "scoac_responses": {},
        "icc_pre_responses": {},
        "icc_post_responses": {},
        "story_node": "start",
        "story_path": [],
        "reputation": 0,
        "history_loaded": False,
        "history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# Carrega (uma vez) o histórico salvo no navegador do usuário
if not st.session_state.history_loaded:
    raw_uid = localS.getItem("cyberapp_user_id")
    raw_hist = localS.getItem("cyberapp_history")
    if raw_uid:
        st.session_state.user_id = raw_uid
    if raw_hist:
        try:
            st.session_state.history = json.loads(raw_hist) if isinstance(raw_hist, str) else raw_hist
        except Exception:
            st.session_state.history = []
    st.session_state.history_loaded = True


def persist_history():
    """Salva o histórico do usuário na memória local do navegador (localStorage)."""
    if not st.session_state.user_id:
        st.session_state.user_id = str(uuid.uuid4())
        localS.setItem("cyberapp_user_id", st.session_state.user_id, key="set_uid")
    localS.setItem(
        "cyberapp_history",
        json.dumps(st.session_state.history),
        key=f"set_hist_{len(st.session_state.history)}",
    )


def goto(stage):
    st.session_state.stage = stage
    st.rerun()


# ----------------------------------------------------------------------------
# CONQUISTAS (gamificação, calculadas a partir do histórico salvo)
# ----------------------------------------------------------------------------
def compute_achievements(history):
    ach = []
    if len(history) >= 1:
        ach.append(("🏁", "Primeira Jornada", "Completou o jogo pela primeira vez."))
    if len(history) >= 3:
        ach.append(("🔁", "Sempre Presente", "Jogou 3 vezes ou mais."))
    if history and any(h.get("ending_title", "").startswith("🦸") for h in history):
        ach.append(("🦸", "Coração de Herói", "Alcançou o final Herói Digital."))
    if history and any(h["icc_post_pct"] - h["icc_pre_pct"] >= 15 for h in history):
        ach.append(("📈", "Consciência em Alta", "Aumentou 15+ pontos percentuais no ICC em uma jogada."))
    if history and any(h["reputation"] >= 28 for h in history):
        ach.append(("⭐", "Reputação Máxima", "Terminou uma jogada com reputação de destaque."))
    return ach


# ----------------------------------------------------------------------------
# TELAS
# ----------------------------------------------------------------------------
def screen_welcome():
    st.markdown(
        """
        <div class="hero-card">
            <h1>🛡️ Rede Consciente</h1>
            <p>Um jogo de escolhas sobre cyberbullying — suas decisões constroem
            sua reputação e revelam quanto você já sabe sobre como agir online.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.history:
        with st.expander(f"🏆 Suas conquistas ({len(st.session_state.history)} jogada(s) salvas neste navegador)"):
            achievements = compute_achievements(st.session_state.history)
            if achievements:
                for emoji, title, desc in achievements:
                    st.markdown(f"**{emoji} {title}** — {desc}")
            else:
                st.write("Continue jogando para desbloquear conquistas!")

    st.markdown("### Como funciona:")
    st.markdown(
        "1. 📋 Um perfil rápido sobre suas vivências online (**escala SCOAC**)\n"
        "2. 🧠 Um teste inicial de consciência sobre cyberbullying\n"
        "3. 🎮 Um quiz narrativo com escolhas reais — cada decisão muda sua reputação e o rumo da história\n"
        "4. 🧠 Um teste final de consciência, para comparar sua evolução\n"
        "5. 💙 Frase de impacto + canais de apoio reais"
    )

    nickname = st.text_input("Como podemos te chamar? (pode ser um apelido)", value=st.session_state.nickname)
    consent = st.checkbox("Entendo que este jogo aborda o tema cyberbullying e que meus dados de resposta ficam salvos apenas no meu próprio navegador.")

    if st.button("🚀 Começar minha jornada", disabled=not consent):
        st.session_state.nickname = nickname.strip() or "Jogador(a)"
        goto("scoac")


def screen_scoac():
    st.markdown("### 📋 Perfil de Vivências Online")
    st.caption(
        "Baseado na escala científica **SCOAC** (Ramos et al., 2026, *Frontiers in "
        "Psychiatry*), adaptada para este app. Responda com base nos **últimos 30 dias**."
    )
    with st.form("scoac_form"):
        responses = {}
        for item in SCOAC_ITEMS:
            val = st.radio(
                item["text"],
                options=list(FREQ_LABELS.keys()),
                format_func=lambda x: FREQ_LABELS[x],
                horizontal=True,
                key=f"scoac_{item['id']}",
                index=st.session_state.scoac_responses.get(item["id"], 0),
            )
            responses[item["id"]] = val
        submitted = st.form_submit_button("Continuar ➡️")
        if submitted:
            st.session_state.scoac_responses = responses
            goto("icc_pre")


def render_icc_form(stage_key, title, subtitle, next_stage):
    st.markdown(f"### 🧠 {title}")
    st.caption(subtitle)
    saved = st.session_state[stage_key]
    with st.form(f"form_{stage_key}"):
        responses = {}
        for item in ICC_ITEMS:
            val = st.slider(
                item["text"],
                min_value=1,
                max_value=5,
                value=saved.get(item["id"], 3),
                key=f"{stage_key}_{item['id']}",
                help="1 = Discordo totalmente · 5 = Concordo totalmente",
            )
            responses[item["id"]] = val
        submitted = st.form_submit_button("Continuar ➡️")
        if submitted:
            st.session_state[stage_key] = responses
            goto(next_stage)


def screen_icc_pre():
    render_icc_form(
        "icc_pre_responses",
        "Teste Inicial de Consciência (ICC)",
        "Não existe resposta certa ou errada — seja sincero(a). Isso é só o ponto de partida da sua jornada.",
        "story",
    )


def screen_story():
    node = STORY[st.session_state.story_node]

    if node.get("ending"):
        screen_story_ending(node)
        return

    rep = st.session_state.reputation
    tier = get_reputation_tier(rep)
    bar_pct = max(5, min(100, int(50 + rep)))  # visual apenas

    st.markdown(
        f"""
        <div class="badge" style="background:{tier['color']}22; color:{tier['color']}; border:1px solid {tier['color']}66;">
            {tier['emoji']} Reputação atual: {tier['label']} ({rep} pts)
        </div>
        <div class="rep-bar-bg">
            <div class="rep-bar-fill" style="width:{bar_pct}%; background:{tier['color']};"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="scene-card">
            <div class="scene-title">{node['scene']}</div>
            <div class="scene-text">{node['text']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i, choice in enumerate(node["choices"]):
        if st.button(choice["label"], key=f"choice_{st.session_state.story_node}_{i}"):
            st.session_state.reputation += choice["points"]
            st.session_state.story_path.append(
                {"scene": st.session_state.story_node, "choice": choice["label"], "points": choice["points"]}
            )
            st.session_state.story_node = choice["next"]
            st.rerun()


def screen_story_ending(node):
    tier = get_reputation_tier(st.session_state.reputation)
    st.markdown(
        f"""
        <div class="scene-card" style="border:2px solid {tier['color']}88;">
            <div class="scene-title">{node['title']}</div>
            <div class="scene-text">{node['text']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="badge" style="background:{tier['color']}22; color:{tier['color']}; border:1px solid {tier['color']}66;">
            {tier['emoji']} Reputação final: {tier['label']} ({st.session_state.reputation} pts)
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state._ending_title = node["title"]
    if st.button("🧠 Ir para o teste final de consciência ➡️"):
        goto("icc_post")


def screen_icc_post():
    render_icc_form(
        "icc_post_responses",
        "Teste Final de Consciência (ICC)",
        "Agora que você passou pela história, responda de novo às mesmas afirmações.",
        "results",
    )


def screen_results():
    pre = score_icc(st.session_state.icc_pre_responses)
    post = score_icc(st.session_state.icc_post_responses)
    scoac = score_scoac(st.session_state.scoac_responses)
    delta = round(post["total_pct"] - pre["total_pct"], 1)
    tier_pre = awareness_tier(pre["total_pct"])
    tier_post = awareness_tier(post["total_pct"])
    rep_tier = get_reputation_tier(st.session_state.reputation)
    ending_title = getattr(st.session_state, "_ending_title", STORY[st.session_state.story_node].get("title", ""))

    st.markdown("## 📊 Seu Resultado")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Consciência ANTES", f"{pre['total_pct']}%", help=tier_pre["label"])
    with col2:
        st.metric("Consciência DEPOIS", f"{post['total_pct']}%", delta=f"{delta} p.p.")

    st.markdown(
        f"""
        <div class="badge" style="background:{tier_post['color']}22; color:{tier_post['color']}; border:1px solid {tier_post['color']}66;">
            {tier_post['emoji']} Nível final: {tier_post['label']}
        </div>
        <div class="badge" style="background:{rep_tier['color']}22; color:{rep_tier['color']}; border:1px solid {rep_tier['color']}66;">
            {rep_tier['emoji']} Reputação no jogo: {rep_tier['label']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Ver detalhes por dimensão (Conhecimento / Atitude / Intenção)"):
        for dim, d in post["dimensions"].items():
            pre_pct = pre["dimensions"][dim]["pct"]
            st.write(f"**{d['label']}**: {pre_pct}% ➜ {d['pct']}%")
            st.progress(min(100, int(d["pct"])) / 100)

    with st.expander("Ver seu perfil de vivências online (SCOAC)"):
        st.write(f"Pontuação total: **{scoac['total']} / {scoac['max_possible']}** (ponto de corte de referência: 8)")
        if scoac["at_risk"]:
            st.warning(
                "Suas respostas indicam sinais de exposição a comportamentos de "
                "cyberbullying recentemente. Isso não é um diagnóstico, mas vale muito "
                "conversar com um adulto de confiança ou usar os canais de apoio abaixo."
            )
        for factor, val in scoac["factors"].items():
            st.write(f"- {factor}: {val} pts")

    import random
    phrase = random.choice(IMPACT_PHRASES)
    st.markdown(f'<div class="impact-phrase">💬 "{phrase}"</div>', unsafe_allow_html=True)

    st.markdown("### 💙 Canais de apoio")
    for r in HELP_RESOURCES:
        st.markdown(
            f"""
            <div class="resource-card">
                <b>{r['name']}</b> — {r['contact']}<br>
                <span style="color:#CBD5E1;">{r['desc']}</span><br>
                <a href="{r['url']}" target="_blank" style="color:#38BDF8;">{r['url']}</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Salva no histórico local do navegador
    if "saved_this_run" not in st.session_state:
        record = {
            "timestamp": datetime.now().isoformat(),
            "nickname": st.session_state.nickname,
            "icc_pre_pct": pre["total_pct"],
            "icc_post_pct": post["total_pct"],
            "scoac_total": scoac["total"],
            "scoac_at_risk": scoac["at_risk"],
            "reputation": st.session_state.reputation,
            "ending_title": ending_title,
            "story_path": st.session_state.story_path,
        }
        st.session_state.history.append(record)
        persist_history()
        st.session_state.saved_this_run = True

    st.divider()
    if st.button("🔄 Jogar novamente"):
        for k in [
            "stage", "scoac_responses", "icc_pre_responses", "icc_post_responses",
            "story_node", "story_path", "reputation", "saved_this_run",
        ]:
            if k in st.session_state:
                del st.session_state[k]
        goto("welcome")

    st.markdown(
        """
        <div class="footer-note">
        Este app é uma ferramenta educativa e não substitui avaliação psicológica
        profissional. Escala SCOAC: Ramos et al. (2026), Frontiers in Psychiatry —
        adaptada aqui para fins de sensibilização. Índice de Consciência (ICC) é um
        instrumento autoral criado para este projeto.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# ROTEAMENTO
# ----------------------------------------------------------------------------
ROUTES = {
    "welcome": screen_welcome,
    "scoac": screen_scoac,
    "icc_pre": screen_icc_pre,
    "story": screen_story,
    "icc_post": screen_icc_post,
    "results": screen_results,
}

ROUTES.get(st.session_state.stage, screen_welcome)()
