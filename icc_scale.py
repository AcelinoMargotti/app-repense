"""
ICC - Índice de Consciência sobre Cyberbullying
Instrumento autoral, criado para este projeto, aplicado em formato pré/pós-teste
para medir mudança em conhecimento, atitudes e intenção comportamental frente
ao cyberbullying. NÃO é uma escala clinicamente validada — é um instrumento de
avaliação de programa (pre/post), prática comum em estudos de intervenção
educacional. Isso deve ficar declarado no relatório final do projeto.

Estrutura (3 dimensões, 5 itens cada = 15 itens):
  - Conhecimento (CONH): o que a pessoa sabe sobre o que conta como cyberbullying
  - Atitude (ATIT): quão aceitável/normalizado a pessoa julga certos comportamentos
    (itens invertidos: concordar = menos consciência)
  - Intenção comportamental (INT): o quanto a pessoa diz que agiria de forma protetora

Escala de resposta: 1 a 5 (Discordo totalmente -> Concordo totalmente)
Itens de ATIT são revertidos na hora de pontuar (score = 6 - resposta).
Score final: soma 0-75, convertido em % de 0 a 100 para exibição amigável.
"""

ICC_ITEMS = [
    # ---- Conhecimento (CONH) ----
    {
        "id": "conh_1",
        "dim": "CONH",
        "text": "Enviar memes ou montagens debochando de uma pessoa, mesmo sem xingar, pode ser considerado cyberbullying.",
        "reverse": False,
    },
    {
        "id": "conh_2",
        "dim": "CONH",
        "text": "Excluir alguém de um grupo do WhatsApp de propósito, repetidamente, é uma forma de cyberbullying.",
        "reverse": False,
    },
    {
        "id": "conh_3",
        "dim": "CONH",
        "text": "Compartilhar print de conversa privada de alguém sem autorização pode causar dano real, mesmo que 'seja só brincadeira'.",
        "reverse": False,
    },
    {
        "id": "conh_4",
        "dim": "CONH",
        "text": "Cyberbullying só conta se a pessoa que sofreu ficar sabendo quem foi o autor.",
        "reverse": True,
    },
    {
        "id": "conh_5",
        "dim": "CONH",
        "text": "Curtir ou repostar um conteúdo que ataca alguém também faz parte da corrente de cyberbullying, mesmo sem ter criado o conteúdo original.",
        "reverse": False,
    },
    # ---- Atitude (ATIT) - itens revertidos ----
    {
        "id": "atit_1",
        "dim": "ATIT",
        "text": "Se a pessoa 'exagerou' e ficou chateada com uma zoeira online, o problema é dela, não de quem postou.",
        "reverse": True,
    },
    {
        "id": "atit_2",
        "dim": "ATIT",
        "text": "Ficar só observando um ataque online sem participar não tem nada de errado.",
        "reverse": True,
    },
    {
        "id": "atit_3",
        "dim": "ATIT",
        "text": "Denunciar um perfil ou conteúdo é 'dedurar' e por isso eu evitaria fazer isso.",
        "reverse": True,
    },
    {
        "id": "atit_4",
        "dim": "ATIT",
        "text": "É normal rir de piadas que expõem um colega, contanto que todo mundo no grupo esteja rindo também.",
        "reverse": True,
    },
    {
        "id": "atit_5",
        "dim": "ATIT",
        "text": "Se eu falar sobre cyberbullying com um adulto, isso vai piorar a situação, então é melhor não falar.",
        "reverse": True,
    },
    # ---- Intenção comportamental (INT) ----
    {
        "id": "int_1",
        "dim": "INT",
        "text": "Se eu visse um colega sendo atacado online, eu chamaria essa pessoa em particular para saber se está tudo bem.",
        "reverse": False,
    },
    {
        "id": "int_2",
        "dim": "INT",
        "text": "Eu me sentiria confiante para denunciar um conteúdo ofensivo dentro do próprio aplicativo/rede social.",
        "reverse": False,
    },
    {
        "id": "int_3",
        "dim": "INT",
        "text": "Eu procuraria um adulto de confiança (familiar, professor, orientador) se soubesse de um caso de cyberbullying.",
        "reverse": False,
    },
    {
        "id": "int_4",
        "dim": "INT",
        "text": "Eu me recusaria a repostar ou encaminhar um conteúdo que expõe ou ridiculariza alguém.",
        "reverse": False,
    },
    {
        "id": "int_5",
        "dim": "INT",
        "text": "Eu guardaria prints/provas para ajudar a vítima caso ela precise denunciar o caso depois.",
        "reverse": False,
    },
]

LIKERT_LABELS = {
    1: "Discordo totalmente",
    2: "Discordo",
    3: "Neutro",
    4: "Concordo",
    5: "Concordo totalmente",
}

DIM_LABELS = {
    "CONH": "Conhecimento",
    "ATIT": "Atitude protetora",
    "INT": "Intenção de agir",
}


def score_icc(responses: dict) -> dict:
    """
    responses: dict {item_id: int 1-5}
    Retorna dict com score bruto total, % total, e % por dimensão.
    """
    dim_raw = {"CONH": 0, "ATIT": 0, "INT": 0}
    dim_max = {"CONH": 0, "ATIT": 0, "INT": 0}

    for item in ICC_ITEMS:
        val = responses.get(item["id"])
        if val is None:
            continue
        scored = (6 - val) if item["reverse"] else val
        dim_raw[item["dim"]] += scored
        dim_max[item["dim"]] += 5

    total_raw = sum(dim_raw.values())
    total_max = sum(dim_max.values())

    result = {
        "total_raw": total_raw,
        "total_max": total_max,
        "total_pct": round(100 * total_raw / total_max, 1) if total_max else 0,
        "dimensions": {},
    }
    for dim in dim_raw:
        pct = round(100 * dim_raw[dim] / dim_max[dim], 1) if dim_max[dim] else 0
        result["dimensions"][dim] = {
            "raw": dim_raw[dim],
            "max": dim_max[dim],
            "pct": pct,
            "label": DIM_LABELS[dim],
        }
    return result


def awareness_tier(pct: float) -> dict:
    """Classificação amigável do nível de consciência para exibir ao usuário."""
    if pct >= 85:
        return {"label": "Consciência Avançada", "emoji": "🟢", "color": "#22C55E"}
    if pct >= 65:
        return {"label": "Consciência em Desenvolvimento", "emoji": "🟡", "color": "#EAB308"}
    if pct >= 40:
        return {"label": "Consciência Inicial", "emoji": "🟠", "color": "#F97316"}
    return {"label": "Consciência Baixa — vamos evoluir isso!", "emoji": "🔴", "color": "#EF4444"}
