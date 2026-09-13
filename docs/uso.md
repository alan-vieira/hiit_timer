# 📖 Como Usar — HIIT Timer

> **Versão:** v2.2.1

---

## 🎬 Visão Rápida

O HIIT Timer tem **4 telas principais** navegadas de forma linear:

```
[Configuração] → [Cronômetro] → [Conclusão]
      ↑              ↓
      └──── [Editor] ←┘
```

---

## 1️⃣ Tela de Configuração (Inicial)

É a tela que abre ao iniciar o app. Mostra um **resumo completo** do treino atual.

### O que você vê:
- **Estatísticas** (cards coloridos):
  - 🔴 **CICLOS** — Número de repetições do circuito (1–20)
  - 🟣 **EXERCÍCIOS** — Quantidade de exercícios por ciclo
  - 🟢 **ETAPAS** — Total de passos (exercícios + intervalos)
  - 🔵 **TEMPO** — Duração total estimada do treino
- **Preview do Treino** — Lista das primeiras 10 etapas com emoji, nome e duração
- **3 Botões de Ação**:

| Botão | Ação |
|-------|------|
| **▶ INICIAR TREINO** | Vai para o cronômetro e começa a contagem |
| **⚙ PERSONALIZAR TREINO** | Abre o editor para mudar exercícios, intervalos, ciclos |
| **🚪 SAIR DO APP** | Encerra o aplicativo completamente (processo finalizado) |

---

## 2️⃣ Editor de Treino

Personalize **tudo** do seu treino. Acesse via "PERSONALIZAR TREINO".

### Seção: INTERVALOS E CICLOS
| Campo | Padrão | Intervalo | Descrição |
|-------|--------|-----------|-----------|
| **Curto (s)** | 30 | 1–300 | Descanso entre exercícios do mesmo ciclo |
| **Longo (s)** | 60 | 1–600 | Descanso entre ciclos (após último exercício) |
| **Ciclos** | 3 | 1–20 | Quantas vezes repetir o circuito completo |

### Seção: EXERCÍCIOS
Lista expansível com **scroll automático**. Cada exercício tem:
- **Emoji** — Ícone visual (ex: 🤸, 🦵, 💪)
- **Nome** — Texto livre (ex: "Polichinelo", "Agachamento")
- **Duração (s)** — Tempo do exercício (1–600)

**Ações por exercício:**
- ✏️ Edite direto nos campos (salva automaticamente ao sair)
- ➕ **ADICIONAR** — Insere novo exercício com emoji 🏃 e 45s
- 🗑️ **DELETE** — Remove exercício (mínimo 1 exercício)

### Botões de Rodapé
| Botão | Ação |
|-------|------|
| **CANCELAR** | Volta à configuração **sem salvar** |
| **SALVAR** | Grava em `dados.json` e volta à configuração |

> 💡 **Dica:** As alterações só persistem após clicar em **SALVAR**. "CANCELAR" descarta tudo.

---

## 3️⃣ Cronômetro Ativo (Timer)

O coração do app. Inicia ao clicar **INICIAR TREINO**.

### Interface
```
┌─────────────────────────────┐
│  Treino em Andamento   ← ───┤  (seta volta cancela treino)
├─────────────────────────────┤
│   ESTATÍSTICAS EM TEMPO REAL │
│  Etapa 3/12  •  Ciclo 1/3   │
├─────────────────────────────┤
│      🤸 POLICHINELO          │
│        00:45                 │
│    ●●●●●○○○○○○○○○○○○        │  (ring animado roxo)
│        EXERCÍCIO             │  (badge colorido)
├─────────────────────────────┤
│  Próximo: 🦵 Elevação...     │
├─────────────────────────────┤
│  ⏮️  RETROCEDER             │
│  ⏸️  PAUSAR   ▶️ CONTINUAR  │
│  ⏭️  PULAR                  │
└─────────────────────────────┘
```

### Controles

| Botão | Função | Atalho |
|-------|--------|--------|
| **⏸️ PAUSAR** | Para a contagem (zero CPU via `asyncio.Event`) | — |
| **▶️ CONTINUAR** | Retoma de onde parou | — |
| **⏭️ PULAR** | Avança para próxima etapa imediatamente | — |
| **⏮️ RETROCEDER** | Volta para etapa anterior (se não for a primeira) | — |
| **Seta "Voltar" (Android)** | Cancela treino e volta à configuração | Botão físico |

### Feedback Multissensorial
- 🎨 **Visual:** Ring animado muda de cor (roxo=exercício, laranja=descanso)
- 🔊 **Áudio:** 4 sons distintos (início, intervalo, countdown 3-2-1, fim)
- 📳 **Háptico:** Vibração nas transições de fase

### Navegação Android
- Botão físico **"Voltar"** → Cancela treino, para timer, volta à configuração
- Seta no AppBar (←) → Mesmo comportamento

---

## 4️⃣ Tela de Conclusão

Aparece automaticamente ao terminar todas as etapas.

### Mostra:
- 🏆 Ícone de conquista
- "Treino Concluído! 🎉"
- Resumo: "Você completou **X ciclos** em **MM:SS**"
- Cards: TEMPO, CICLOS, STATUS ✅

### Opções:
| Botão | Ação |
|-------|------|
| **🔁 REPETIR TREINO** | Reinicia o mesmo treino (mesma config) |
| **⚙ VOLTAR À CONFIGURAÇÃO** | Volta à tela inicial para ajustar |

---

## ⚙️ Configuração Padrão (Primeira Execução)

Ao rodar pela primeira vez, `dados.json` é criado com:

```json
{
  "exercicios": [
    {"nome": "Polichinelo", "emoji": "🤸", "duracao": 60},
    {"nome": "Elevação de joelhos", "emoji": "🦵", "duracao": 60},
    {"nome": "Crucifixo", "emoji": "🦋", "duracao": 60},
    {"nome": "Extensão de braços", "emoji": "💪", "duracao": 60},
    {"nome": "Agachamento", "emoji": "🏋️", "duracao": 60}
  ],
  "descanso_curto": 30,
  "descanso_ciclo": 60,
  "num_ciclos": 3
}
```

**Total:** 5 exercícios × 3 ciclos = 15 exercícios + 12 intervalos curtos + 2 intervalos longos = **29 etapas** ≈ **22 min 30s**

---

## 🔊 Sistema de Áudio (v2.2.1+)

| Arquivo | Momento | Volume |
|---------|---------|--------|
| `som_inicio.mp3` | Início de cada exercício | 80% |
| `som_intervalo.mp3` | Início de cada descanso | 80% |
| `som_countdown.mp3` | Últimos 3s de cada fase (3, 2, 1) | 60% |
| `som_fim.mp3` | Fim do treino completo | 100% |

> 📱 **Android:** Áudio funciona nativamente no APK. Arquivos em `assets/` servidos via `ft.run(main, assets_dir="assets")`.

---

## 🔋 Wake Lock

- **Ativo** durante todo o cronômetro (tela não apaga)
- **Liberado** automaticamente ao: pausar, concluir, pular pro fim, sair do app
- **Android:** Requer permissão `WAKE_LOCK` (concedida no build)

---

## 🚪 Saindo do App (v2.2.1+)

### No Android:
1. Na tela de **Configuração**, toque em **🚪 SAIR DO APP**
2. App encerra **completamente** (processo morto)
3. Timer parado, wake lock liberado, sem background

### No Desktop (Windows/Linux/macOS):
- Use o **X** da janela ou `Ctrl+C` no terminal
- `sys.exit(0)` garante limpeza correta

---

## 💾 Persistência

- Arquivo: `dados.json` (na raiz do projeto)
- Salvo **automaticamente** ao clicar **SALVAR** no editor
- Carregado **automaticamente** ao abrir o app
- Sobrevive a reinicialização, update de versão, rebuild APK

---

## 🎯 Exemplos de Treinos Populares

### Tabata Clássico (4 min)
```json
{
  "exercicios": [{"nome": "Sprint/Exercício", "emoji": "🏃", "duracao": 20}],
  "descanso_curto": 10,
  "descanso_ciclo": 0,
  "num_ciclos": 8
}
```

### EMOM 10 min (Every Minute On the Minute)
```json
{
  "exercicios": [
    {"nome": "Burpees", "emoji": "🤸", "duracao": 40},
    {"nome": "Push-ups", "emoji": "💪", "duracao": 40}
  ],
  "descanso_curto": 20,
  "descanso_ciclo": 60,
  "num_ciclos": 5
}
```

### Treino de Força (3 séries × 5 exercícios)
```json
{
  "exercicios": [
    {"nome": "Agachamento", "emoji": "🏋️", "duracao": 45},
    {"nome": "Flexão", "emoji": "💪", "duracao": 45},
    {"nome": "Prancha", "emoji": "🧘", "duracao": 60},
    {"nome": "Afundo", "emoji": "🦵", "duracao": 45},
    {"nome": "Prancha lateral", "emoji": "🧘", "duracao": 30}
  ],
  "descanso_curto": 30,
  "descanso_ciclo": 90,
  "num_ciclos": 3
}
```

---

## ❓ FAQ Rápido

| Pergunta | Resposta |
|----------|----------|
| **Posso editar durante o treino?** | Não. Pause → Voltar à configuração → Editar → Iniciar novamente |
| **O countdown toca no descanso?** | Sim, nos últimos 3s de **qualquer** fase (exercício ou descanso) |
| **Como resetar para o padrão?** | Apague `dados.json` e reinicie o app |
| **Funciona offline?** | Sim, 100% offline após instalado |
| **Consome bateria?** | Mínimo. Wake lock só durante treino; pausa = zero CPU |

---

*Atualizado: Setembro 2026 (v2.2.1)*