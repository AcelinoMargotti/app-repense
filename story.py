"""
Quiz narrativo ramificado sobre cyberbullying.
Cada escolha altera a Reputação (pontuação de gamificação) e leva a nós
diferentes da história, resultando em finais distintos.
"""

STORY = {
    "start": {
        "scene": "🏫 Grupo da Turma",
        "text": (
            "Você está no grupo da turma no celular. Alguém posta uma montagem "
            "zoando o Enzo, um colega mais quieto, chamando ele de apelidos e "
            "marcando várias pessoas para verem. Várias figurinhas de risada "
            "já apareceram no chat."
        ),
        "choices": [
            {"label": "😂 Comentar apoiando a 'brincadeira'", "points": -10, "next": "path_neg1"},
            {"label": "👀 Ficar só olhando, sem fazer nada", "points": -3, "next": "path_neutral1"},
            {"label": "💬 Chamar o Enzo no privado para saber se ele está bem", "points": 10, "next": "path_pos1"},
        ],
    },
    "path_pos1": {
        "scene": "📩 Conversa Privada",
        "text": (
            "Você chama o Enzo no privado. Ele responde que está péssimo e pede "
            "para você não contar a ninguém que ele desabafou. Enquanto isso, no "
            "grupo, mais pessoas continuam comentando e cobram que você também "
            "'entre na piada' para não ficar de fora."
        ),
        "choices": [
            {"label": "🚩 Denunciar a publicação dentro do próprio app", "points": 10, "next": "path_pos2"},
            {"label": "🗣️ Pedir no grupo para todo mundo parar, sem denunciar", "points": 5, "next": "path_pos2"},
            {"label": "😬 Ceder à pressão e mandar uma piadinha 'só pra não ser excluído'", "points": -8, "next": "path_neutral2"},
        ],
    },
    "path_neutral1": {
        "scene": "📸 O Print Vaza",
        "text": (
            "A '' piada '' cresce. Alguém tira print da conversa e começa a "
            "espalhar em outros grupos da escola. O Enzo para de responder "
            "mensagens de qualquer pessoa."
        ),
        "choices": [
            {"label": "💬 Decidir agora chamar o Enzo e oferecer ajuda", "points": 8, "next": "path_pos2"},
            {"label": "🤷 Continuar sem se envolver", "points": -5, "next": "path_neutral2"},
            {"label": "📤 Repassar o print para outro grupo 'só pra mostrar'", "points": -12, "next": "path_neg2"},
        ],
    },
    "path_neg1": {
        "scene": "👀 Seu Nome Aparece",
        "text": (
            "Seu comentário engraçadinho virou um dos mais curtidos. O Enzo "
            "viu seu nome nos comentários e você percebe que ele te removeu "
            "das redes sociais dele."
        ),
        "choices": [
            {"label": "🙏 Pedir desculpas publicamente e apagar o comentário", "points": 6, "next": "path_neutral2"},
            {"label": "🤐 Ignorar e seguir a vida", "points": -6, "next": "path_neg2"},
            {"label": "😏 Mandar mais uma piada para 'manter o clima'", "points": -12, "next": "path_neg2"},
        ],
    },
    "path_pos2": {
        "scene": "🧑‍🏫 A Escola Descobre",
        "text": (
            "A orientadora da escola ficou sabendo do caso e chamou a turma "
            "para conversar. Ela pergunta abertamente se alguém sabe de algo "
            "e quem pode ajudar a esclarecer a situação."
        ),
        "choices": [
            {"label": "🦸 Contar a verdade e oferecer apoio ao Enzo na frente de todos", "points": 12, "next": "end_hero"},
            {"label": "🤫 Confirmar os fatos, mas sem se expor muito", "points": 3, "next": "end_ally"},
        ],
    },
    "path_neutral2": {
        "scene": "🧑‍🏫 Reunião com a Direção",
        "text": (
            "O grupo inteiro é chamado à direção por causa das denúncias. "
            "Todo mundo está tentando se explicar ao mesmo tempo."
        ),
        "choices": [
            {"label": "🙋 Assumir sua parte e se desculpar de verdade com o Enzo", "points": 8, "next": "end_ally"},
            {"label": "👉 Botar a culpa nos outros pra não se dar mal", "points": -10, "next": "end_bystander"},
        ],
    },
    "path_neg2": {
        "scene": "📵 O Enzo Some",
        "text": (
            "Depois de dias sendo o assunto da escola, o Enzo para de ir às "
            "aulas por uma semana e desativa as redes sociais."
        ),
        "choices": [
            {"label": "💌 Procurar o Enzo depois e pedir desculpas de verdade", "points": 10, "next": "end_bystander"},
            {"label": "🙈 Fingir que nada disso aconteceu", "points": -10, "next": "end_risk"},
        ],
    },
    # ---------------- FINAIS ----------------
    "end_hero": {
        "ending": True,
        "title": "🦸 Final: Herói Digital",
        "text": (
            "Você escolheu se posicionar, apoiar quem precisava e assumir a "
            "responsabilidade das suas ações mesmo quando isso não era fácil. "
            "O Enzo se sentiu apoiado, e a turma começou a rever como trata os "
            "colegas online."
        ),
    },
    "end_ally": {
        "ending": True,
        "title": "🤝 Final: Aliado em Formação",
        "text": (
            "Você não foi perfeito o tempo todo, mas quando precisou se "
            "posicionar, escolheu o caminho certo. Reconhecer erros e mudar de "
            "atitude também é uma forma real de cuidar de quem está ao seu redor."
        ),
    },
    "end_bystander": {
        "ending": True,
        "title": "🙇 Final: Espectador que Acordou Tarde",
        "text": (
            "Por um bom tempo você preferiu não se envolver, e isso teve um "
            "custo para o Enzo. No fim, você tentou consertar — e isso importa —, "
            "mas o dano já tinha acontecido. Silêncio também é uma escolha."
        ),
    },
    "end_risk": {
        "ending": True,
        "title": "⚠️ Final: Perfil de Risco",
        "text": (
            "Suas escolhas alimentaram o ataque ao Enzo, direta ou "
            "indiretamente, e mesmo diante das consequências você optou por "
            "não encarar isso. Esse tipo de comportamento tem nome — e tem "
            "impacto real na vida de quem sofre."
        ),
    },
}

REPUTATION_TIERS = [
    (28, {"label": "Herói Digital", "emoji": "🦸", "color": "#22C55E"}),
    (10, {"label": "Aliado em Formação", "emoji": "🤝", "color": "#3B82F6"}),
    (-5, {"label": "Espectador Silencioso", "emoji": "🙇", "color": "#EAB308"}),
    (-999, {"label": "Perfil de Risco", "emoji": "⚠️", "color": "#EF4444"}),
]


def get_reputation_tier(score: int) -> dict:
    for threshold, info in REPUTATION_TIERS:
        if score >= threshold:
            return info
    return REPUTATION_TIERS[-1][1]
