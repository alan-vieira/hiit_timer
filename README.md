# ⏱️ HIIT Timer

Cronômetro para treinos HIIT (High-Intensity Interval Training) desenvolvido em **Python 3.12 + Flet** e compilado nativamente para **Android**.

> **Versão:** 2.2.0 · **Autor:** Alan Vieira · **Licença:** MIT

---

## ✨ Sobre o Projeto

Aplicativo simples e direto para gerenciar treinos intervalados. Configure exercícios, durações e ciclos de descanso, inicie o treino e acompanhe o cronômetro com feedback visual (ring animado) e háptico (vibração) nas transições.

**Filosofia:** simplicidade sobre complexidade. Um cronômetro não precisa de arquitetura enterprise — precisa funcionar.

---

## 🚀 Funcionalidades

- **Tela de Configuração** — Resumo do treino (ciclos, exercícios, etapas, tempo total) + preview das etapas
- **Editor de Treino** — Personalize exercícios (nome, emoji, duração), intervalos curtos/longos e número de ciclos (1–20)
- **Cronômetro Ativo** — Ring visual animado, badge de fase (EXERCÍCIO/DESCANSO), stats em tempo real, controles de pausar/pular/retroceder
- **Tela de Conclusão** — Resumo do treino com opções de repetir ou reconfigurar
- **Persistência Local** — Configurações salvas automaticamente em JSON (sobrevivem a reinicialização)
- **Tema Escuro Material 3** — Paleta violeta/roxo consistente
- **Navegação Android** — Botão físico "Voltar" interceptado corretamente em todas as telas
- **Build Nativo Android** — APK pronto para instalação
- **🔊 Sistema de Áudio** — 4 efeitos sonoros: início, intervalo, countdown 3-2-1, finalização (via `flet-audio`)
- **🔋 Wake Lock** — Mantém tela ligada durante treino no Android (via `wakepy`)
- **📜 Editor com Scroll** — Lista de exercícios expansível com scroll interno automático
- **🏃 Emoji Padrão** — Novo exercício já vem com emoji 🏃

---

## 📋 Últimas Mudanças (v2.2.0 - 2026-09-11)

### ✨ Adicionado
- **TimerController** — arquitetura limpa separando UI, estado e ciclo de vida assíncrono
- Type Safety completa com `TypedDict` (Config, Estado, Etapa)
- Pausa eficiente com `asyncio.Event` (zero CPU quando pausado)
- Tratamento de erros específico (sem `except Exception` genérico)
- Limpeza automática de tasks ao navegar entre telas

### 🐛 Corrigido
- `TypeError: handler must be a coroutine function`
- `Future can't be used in await`
- `ListView Control must be added to the page first`
- Rolagem quebrada no editor
- Exclusão de exercícios falha
- Task do timer continuava em background
- Wake lock lifecycle management

### 🔧 Alterado
- Arquitetura do timer migrada para classe `TimerController`
- Editor simplificado com `ft.Column` + scroll
- Pylint score: 8.75/10 → ~9.5/10

---

## 🚀 Como Executar

### Requisitos

- Python 3.12+
- Flet 0.86+

### Instalação

```bash
git clone https://github.com/alan-vieira/hiit_timer.git
cd hiit_timer
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### Executar (desenvolvimento)

```bash
python main.py
```

### Build do APK (Android)

```bash
flet build apk --release
```

O APK será gerado em `build/app/outputs/flutter-apk/app-release.apk`.

---

## 📁 Estrutura do Projeto

```
hiit_timer/
├── main.py              # App completo (~550 linhas)
├── dados.json           # Configuração persistida (criado automaticamente)
├── pyproject.toml       # Config: Pylint, Black, Ruff, isort + metadados PEP 621
├── requirements.txt     # Dependências de produção
├── CHANGELOG.md         # Histórico de versões
├── assets/              # Arquivos de áudio (som_inicio.wav, som_intervalo.wav, som_countdown.wav, som_fim.wav)
├── _legacy/             # Arquitetura modular v1.x (referência histórica)
└── build/               # Artefatos de build (APK, etc.)
```

**Decisão de arquitetura:** a partir da v2.0.0, o projeto adotou uma estrutura **monolítica (single-file)** para priorizar simplicidade e manutenibilidade. A arquitetura modular anterior (v1.x) está preservada em `_legacy/` para referência.

---

## 💾 Formato dos Dados

**dados.json**

```json
{
  "exercicios": [
    {"nome": "Polichinelo", "emoji": "🤸", "duracao": 60},
    {"nome": "Elevação de joelhos", "emoji": "🦵", "duracao": 60}
  ],
  "descanso_curto": 30,
  "descanso_ciclo": 60,
  "num_ciclos": 3
}
```

O arquivo é criado automaticamente na primeira execução com valores padrão.

---

## 🔄 Fluxo de Uso

1. **Configuração** (tela inicial) → revise o treino e toque em **INICIAR TREINO**
2. **Cronômetro** → acompanhe as etapas, pause, pule ou retroceda conforme necessário
3. **Conclusão** → veja o resumo e escolha repetir ou reconfigurar
4. **Editor** (via botão "PERSONALIZAR TREINO") → ajuste exercícios, durações e ciclos

---

## 📊 Comparativo de Versões

| Métrica | v1.x (modular) | v2.0 (monolítico) | v2.1 | v2.2 (atual) |
|---------|----------------|-------------------|--------------|--------------|
| Arquivos de código | 8+ | 1 | 1 | 1 |
| Linhas totais | ~1500 | ~460 | ~550 | ~600 |
| Complexidade | Alta (store reativo, dataclasses frozen, 149 testes) | Baixa | Baixa | Baixa |
| Bugs de navegação | Tela preta, seta de voltar quebrada | Resolvidos | Resolvidos | Resolvidos |
| Build Android | Funcional | Funcional | Funcional | Funcional |
| Áudio | ❌ | ❌ | ✅ 4 sons + countdown | ✅ 4 sons + countdown |
| Wake Lock | ❌ | ❌ | ✅ wakepy | ✅ wakepy |
| Editor Scroll | ❌ | ❌ | ✅ Auto-expansível | ✅ Auto-expansível |
| Type Safety | ❌ | ❌ | ❌ | ✅ TypedDict completo |
| Pausa eficiente | ❌ | ❌ | ❌ | ✅ asyncio.Event (zero CPU) |
| Score Pylint | N/A | N/A | 8.75/10 | ~9.5/10 |

---

## 🛠️ Desenvolvimento

### Convenções

- Indentação: 4 espaços
- Line length: 120 caracteres
- Docstrings: uma linha, imperativo, em todas as funções públicas
- Type hints: em API pública
- Linting: `python -m pylint main.py` (config em `pyproject.toml`)

### Comandos úteis

```bash
# Lint
python -m pylint main.py

# Formatar
black main.py

# Ordenar imports
isort main.py
```

---

## 📄 Licença

Copyright © 2026 Alan Vieira. Distribuído sob licença MIT.

---

*Documento de referência. Última atualização: Setembro 2026 (v2.2.0).*