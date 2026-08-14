# 🛡️ Rede Consciente — Jogo contra o Cyberbullying

App educativo em Streamlit para conscientizar adolescentes sobre cyberbullying,
através de um quiz narrativo ramificado com sistema de reputação/gamificação.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abra o link local que aparecer no terminal (normalmente `http://localhost:8501`).

## Estrutura do projeto

| Arquivo | O que faz |
|---|---|
| `app.py` | App principal: máquina de estados, CSS, telas, roteamento e persistência |
| `scoac_scale.py` | Escala **SCOAC** (real, validada) — perfil de exposição ao cyberbullying |
| `icc_scale.py` | **ICC** — instrumento autoral pré/pós para medir consciência (conhecimento, atitude, intenção) |
| `story.py` | Quiz narrativo ramificado: nós, escolhas, pontuação de reputação e finais |
| `resources.py` | Canais de apoio reais (SaferNet, Disque 100, CVV) e frases de impacto |

## Decisão importante sobre a "Escala ECOAC"

Não existe, na literatura, um instrumento validado chamado exatamente "ECOAC".
O mais próximo é a **SCOAC (Scale of Cyberbullying and Online Aggressive Conduct)**,
publicada em 2026 por Ramos et al. na *Frontiers in Psychiatry*, validada com
adolescentes brasileiros (17 itens, 3 fatores: Ameaça, Difamação/Exposição,
Problemas Emocionais; ponto de corte ≥ 8).

Só que a SCOAC mede **exposição/vitimização recente** ao cyberbullying — não
"grau de consciência". Usá-la como pré/pós-teste de consciência seria um uso
inadequado do instrumento e enfraqueceria a validade do projeto.

Por isso o app usa **duas ferramentas com papéis diferentes**:

1. **SCOAC** — aplicada **uma única vez**, no início, como perfil de exposição/triagem
   (com aviso claro de que não é diagnóstico).
2. **ICC (Índice de Consciência sobre Cyberbullying)** — instrumento **autoral**,
   criado especificamente para este projeto, aplicado **antes e depois** do quiz,
   com 15 itens em 3 dimensões (Conhecimento, Atitude protetora, Intenção de agir).
   É esse instrumento que efetivamente mede se o jogo aumentou a consciência —
   deixe isso explícito no relatório/TCC como "instrumento de avaliação de
   programa, não validado psicometricamente", o que é uma prática comum e aceita
   em estudos de intervenção educacional.

Se seu professor/orientador exigir especificamente uma escala com o nome "ECOAC",
vale confirmar a referência exata com ele — pode ser um apelido local para a SCOAC
ou outro instrumento não indexado nas bases que consultei.

## Persistência de dados (memória do navegador)

Os dados de cada usuário (histórico de jogadas, pontuações ICC pré/pós, reputação,
conquistas) são salvos via `localStorage` do navegador, usando o pacote
`streamlit-local-storage`. Isso significa:

- Cada navegador/dispositivo tem seu próprio histórico, sem precisar de login ou banco de dados.
- Os dados **não** são enviados a um servidor — ficam só no navegador do usuário.
- Se o usuário limpar o cache do navegador, o histórico se perde (isso é esperado
  e deve ser mencionado como limitação no relatório, especialmente se pretende
  fazer coleta de dados agregada para pesquisa).

⚠️ Para uma coleta de dados real (planilha consolidada de todos os participantes
para análise estatística do projeto), você vai precisar complementar isso com um
banco de dados de verdade (Google Sheets via API, Firebase, Supabase etc.), já
que `localStorage` é local por definição — não centraliza nada. Posso te ajudar a
montar essa camada de coleta se for necessário para a etapa de "Análise e coleta
de dados" do projeto.

## Gamificação implementada

- **Reputação**: pontos ganhos/perdidos a cada escolha na história, com 4 níveis
  (Herói Digital, Aliado em Formação, Espectador Silencioso, Perfil de Risco).
- **Finais múltiplos**: 4 finais narrativos diferentes, alcançados por caminhos
  distintos dentro da árvore de decisões (`story.py`).
- **Conquistas**: desbloqueadas a partir do histórico salvo no navegador
  (ex: "Primeira Jornada", "Coração de Herói", "Consciência em Alta").

## Próximos passos sugeridos

- Adicionar mais cenas/ramificações à história (hoje são 8 nós + 4 finais).
- Trocar o armazenamento local por um banco real se for preciso consolidar dados
  de vários participantes para análise estatística do TCC/projeto.
- Validar os itens do ICC com um pequeno grupo de juízes especialistas (como foi
  feito com a SCOAC), se quiser reforçar a robustez metodológica do instrumento.
