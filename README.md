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
| `sheets.py` | Envio de cada resultado final para uma planilha do Google Sheets via API |
| `secrets.toml.example` | Modelo de configuração das credenciais do Google Sheets |

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

## Coleta centralizada de dados (Google Sheets)

Além do `localStorage`, cada jogada finalizada é enviada automaticamente para
uma planilha do Google Sheets, via API com uma **Conta de Serviço**. É a forma
mais simples de centralizar dados de vários participantes sem precisar de
Supabase, Firebase, ou banco de dados próprio.

### Passo a passo (leva ~10 minutos, só precisa fazer uma vez)

**1. Criar a planilha**
- Crie uma planilha nova no Google Sheets (pode ficar vazia — o app cria o
  cabeçalho sozinho na primeira resposta).
- Copie o ID dela na URL: `https://docs.google.com/spreadsheets/d/ESTE_TRECHO/edit`

**2. Criar a Conta de Serviço no Google Cloud**
- Acesse [console.cloud.google.com](https://console.cloud.google.com/) e crie
  um projeto (ou use um existente).
- Vá em **APIs e Serviços > Biblioteca** e ative:
  - `Google Sheets API`
  - `Google Drive API`
- Vá em **APIs e Serviços > Credenciais > Criar Credenciais > Conta de Serviço**.
- Dê um nome (ex: `rede-consciente-app`) e crie.
- Na conta de serviço criada, vá em **Chaves > Adicionar Chave > Criar nova
  chave > JSON**. Isso baixa um arquivo `.json` — guarde-o com cuidado, ele é
  uma credencial sensível.

**3. Compartilhar a planilha com a conta de serviço**
- Abra o arquivo `.json` baixado e copie o valor de `client_email`
  (algo como `rede-consciente-app@seu-projeto.iam.gserviceaccount.com`).
- Na planilha do Google Sheets, clique em **Compartilhar** e adicione esse
  e-mail como **Editor**.

**4. Configurar o app**
- Copie `secrets.toml.example` para `.streamlit/secrets.toml`.
- Preencha a seção `[gcp_service_account]` com os campos do `.json` baixado
  (`project_id`, `private_key_id`, `private_key`, `client_email`, `client_id`, etc.).
- Preencha `[gsheet]` com o `sheet_id` copiado no passo 1.
- **Nunca** suba `.streamlit/secrets.toml` para um repositório público —
  adicione ao `.gitignore`.

**5. Se for publicar no Streamlit Community Cloud**
- Não é preciso subir o `secrets.toml` junto com o código.
- No painel do app, vá em **Settings > Secrets** e cole lá o mesmo conteúdo
  do `secrets.toml` preenchido.

### O que é salvo em cada linha da planilha

`timestamp_iso`, `user_id`, `nickname`, `icc_pre_pct`, `icc_post_pct`,
`icc_delta_pct`, `icc_pre/post_conhecimento/atitude/intencao`, `scoac_total`,
`scoac_at_risk`, `scoac_ameaca`, `scoac_difamacao_exposicao`,
`scoac_problemas_emocionais`, `reputation`, `reputation_tier`, `ending_title`,
`story_path_json` (o caminho de escolhas feito na história, como JSON).

Isso já vem pronto para análise: dá para abrir a planilha, filtrar/agrupar por
`ending_title` ou `reputation_tier`, calcular médias de `icc_delta_pct` (o
quanto a consciência aumentou), correlacionar `scoac_at_risk` com o
comportamento no jogo, etc. — sem precisar programar nada extra.

### Se o Sheets não estiver configurado

O app **não quebra**: ele detecta que os secrets não existem, não tenta
enviar, e mostra um aviso discreto na tela de resultado ("Coleta central não
configurada — dados salvos só neste navegador"). Isso é útil para testar o
app localmente antes de configurar tudo.

## Persistência de dados (memória do navegador)

Os dados de cada usuário (histórico de jogadas, pontuações ICC pré/pós, reputação,
conquistas) são salvos via `localStorage` do navegador, usando o pacote
`streamlit-local-storage`. Isso significa:

- Cada navegador/dispositivo tem seu próprio histórico, sem precisar de login ou banco de dados.
- Os dados **não** são enviados a um servidor — ficam só no navegador do usuário.
- Se o usuário limpar o cache do navegador, o histórico se perde (isso é esperado
  e deve ser mencionado como limitação no relatório, especialmente se pretende
  fazer coleta de dados agregada para pesquisa).

⚠️ `localStorage` é local por definição — não centraliza nada entre usuários.
Por isso, a coleta consolidada para análise (etapa "Análise e coleta de dados"
do projeto) agora é feita via **Google Sheets** (ver seção acima). O
`localStorage` continua sendo usado só para as conquistas/histórico pessoal
de cada usuário dentro do próprio navegador.

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
