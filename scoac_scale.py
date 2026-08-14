"""
SCOAC - Scale of Cyberbullying and Online Aggressive Conduct
(Escala de Conduta Online Agressiva e Cyberbullying)

Fonte: Ramos, R.F.S., de Oliveira, W.A., Romualdo, C., Baptista, M.N., et al. (2026).
Development and validation of a scale of cyberbullying and online aggressive conduct
in Brazilian adolescents. Frontiers in Psychiatry, 17, 1759871.
https://doi.org/10.3389/fpsyt.2026.1759871

17 itens, 3 fatores: Ameaça (6), Difamação/Exposição (6), Problemas Emocionais (5).
Escala de resposta original: frequência (0 = Nunca ... 3 = Frequentemente/sempre).
Ponto de corte validado: escore total >= 8 sinaliza perfil de risco para cyberbullying.

IMPORTANTE: este instrumento mede EXPOSIÇÃO/VITIMIZAÇÃO recente, não consciência.
No app ele é usado como perfil inicial (triagem), aplicado uma única vez, e os
itens foram traduzidos/adaptados livremente do inglês para linguagem de app --
não configura a versão oficialmente validada em português, servindo aqui para
fins educativos e de sensibilização, não diagnósticos.
"""

FREQ_LABELS = {
    0: "Nunca",
    1: "Raramente",
    2: "Às vezes",
    3: "Frequentemente",
}

SCOAC_ITEMS = [
    # ---- Ameaça (Threat) ----
    {"id": "s1", "factor": "Ameaça", "text": "Alguém debochou de mim, me xingou ou me chamou de apelidos ofensivos online."},
    {"id": "s2", "factor": "Ameaça", "text": "Eu me senti ameaçado(a) ou inseguro(a) por causa de algo que aconteceu online."},
    {"id": "s3", "factor": "Ameaça", "text": "Alguém me ameaçou de me machucar fisicamente pela internet."},
    {"id": "s4", "factor": "Ameaça", "text": "Alguém ameaçou espalhar mentiras sobre mim online."},
    {"id": "s5", "factor": "Ameaça", "text": "Alguém ameaçou me excluir de algo (grupo, jogo, turma) online."},
    {"id": "s6", "factor": "Ameaça", "text": "Alguém disse que ia 'se vingar' ou 'pegar' de mim pela internet."},
    # ---- Difamação / Exposição ----
    {"id": "s7", "factor": "Difamação/Exposição", "text": "Compartilharam uma foto ou vídeo meu sem a minha permissão."},
    {"id": "s8", "factor": "Difamação/Exposição", "text": "Me deram um apelido maldoso ou humilhante online."},
    {"id": "s9", "factor": "Difamação/Exposição", "text": "Fizeram um meme ou editaram uma imagem sobre mim para zoar."},
    {"id": "s10", "factor": "Difamação/Exposição", "text": "Postaram print de uma conversa privada minha sem me avisar."},
    {"id": "s11", "factor": "Difamação/Exposição", "text": "Compartilharam meus dados pessoais (endereço, telefone) sem minha permissão."},
    {"id": "s12", "factor": "Difamação/Exposição", "text": "Contaram um segredo meu ou algo privado que eu disse em mensagens/redes."},
    # ---- Problemas Emocionais ----
    {"id": "s13", "factor": "Problemas Emocionais", "text": "Ser atacado(a) online está mexendo com minha saúde mental e emocional."},
    {"id": "s14", "factor": "Problemas Emocionais", "text": "Tenho tido dificuldade de concentração desde que comecei a receber mensagens/comentários maldosos online."},
    {"id": "s15", "factor": "Problemas Emocionais", "text": "Tenho tido dificuldade para dormir desde que comecei a receber mensagens/comentários maldosos online."},
    {"id": "s16", "factor": "Problemas Emocionais", "text": "Tenho tido dificuldade para fazer coisas do dia a dia desde que comecei a receber mensagens/comentários maldosos online."},
    {"id": "s17", "factor": "Problemas Emocionais", "text": "Notei mudanças no meu humor ou comportamento desde que comecei a receber mensagens/comentários maldosos online."},
]

CUTOFF = 8


def score_scoac(responses: dict) -> dict:
    """responses: dict {item_id: int 0-3}. Retorna score total, por fator e classificação de risco."""
    factors = {}
    total = 0
    for item in SCOAC_ITEMS:
        val = responses.get(item["id"], 0)
        total += val
        factors.setdefault(item["factor"], 0)
        factors[item["factor"]] += val

    at_risk = total >= CUTOFF
    return {
        "total": total,
        "factors": factors,
        "at_risk": at_risk,
        "max_possible": len(SCOAC_ITEMS) * 3,
    }
