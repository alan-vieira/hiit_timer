# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [2.1.0] - 2026-09-10

### ✨ Adicionado
- 🔊 **Sistema de áudio completo** com 4 efeitos sonoros via `flet-audio`:
  - Som de início de exercício
  - Som de intervalo/descanso
  - Countdown 3-2-1 (último 3s de cada fase)
  - Som de finalização do treino
- 🔋 **Wake lock** via `wakepy` — mantém tela ligada durante treino (Android)
- 📜 **Scroll automático** no Editor de Treino — lista de exercícios expande com scroll interno
- 🎯 **Emoji padrão** (🏃) ao adicionar novo exercício no editor

### 🐛 Corrigido
- ❌ **Descanso longo não adicionado após último ciclo** — lógica ajustada em `gerar_etapas()`
- 🎵 **Execução de áudio não-bloqueante** — timeouts e error handling para não travar o timer

### 🔧 Alterado
- 📦 `requirements.txt` atualizado com `flet-audio>=0.1.0` e `wakepy>=0.7.0`
- 📦 `pyproject.toml` convertido para formato PEP 621 com metadados do projeto
- 🚀 `ft.run(main, assets_dir="assets")` — assets servidos corretamente no build Android

---

## [2.0.0] - 2026-09-09

### 🎯 Refatoração Radical: Arquitetura Monolítica

**Motivação:** a arquitetura modular anterior (v1.x) introduzia complexidade desnecessária para um app pessoal de cronômetro — 8+ arquivos, ~1500 linhas, store reativo, dataclasses frozen, 149 testes — e ainda assim apresentava bugs críticos (tela preta na inicialização, seta de voltar quebrada).

A v2.0.0 adota uma estrutura **monolítica (single-file)** priorizando simplicidade, manutenibilidade e funcionalidade.

### Adicionado
- ✅ **Tela de Configuração** com estatísticas (ciclos, exercícios, etapas, tempo total) e preview das primeiras 10 etapas
- ✅ **Editor de Treino** completo: exercícios (emoji/nome/duração), intervalos curtos/longos, número de ciclos (1–20)
- ✅ **Cronômetro Ativo** com ring visual animado, badge de fase, stats em tempo real, controles de pausar/pular/retroceder
- ✅ **Tela de Conclusão** com resumo do treino e opções de repetir/reconfigurar
- ✅ **Navegação centralizada** com `page.views.clear()` — elimina "tela preta fantasma" do histórico
- ✅ **Handler do botão físico "Voltar"** do Android funcionando em todas as telas
- ✅ **Setas de voltar** (`leading` no `AppBar`) nas telas Timer e Editor
- ✅ **Persistência em JSON** (`dados.json`) com fallback para configuração padrão
- ✅ **Updates granulares** no timer (`control.update()` apenas nos controles que mudam)
- ✅ **Tema Material 3** com seed violeta (#9C27B0)
- ✅ **Build Android** funcional (`flet build apk`)
- ✅ **pyproject.toml** com configuração de Pylint, Black, Ruff e isort

### Removido
- ❌ Arquitetura modular (`screens/`, `components/`, `utils/`, `tests/`)
- ❌ `store.py` com `@ft.observable` e persistência via `client_storage`
- ❌ `workout.py` com dataclasses frozen e validações `__post_init__`
- ❌ 149 testes automatizados (pytest)
- ❌ `flet_build.yaml`, `requirements.txt`, `requirements-dev.txt`
- ❌ Over-engineering (injeção de dependência, reatividade, type hints excessivos)

### Corrigido
- 🐛 **Tela preta na inicialização** — causada por `if name == "main":` (faltavam underscores) e pilha de views acumulada
- 🐛 **Seta de voltar quebrada** — agora presente e funcional nas telas Timer e Editor
- 🐛 **Strings com espaços fantasmas** (`"exercicio "`, `"Polichinelo "`) — removidas
- 🐛 **APIs depreciadas do Flet** (`page.open()`, `page.window.vibrate()`, `ft.padding.Padding`) — substituídas por equivalentes válidos
- 🐛 **Indentação quebrada** em múltiplos arquivos — corrigida

### Migrado
- 📦 Arquitetura modular v1.x preservada em `_legacy/` para referência histórica
- 📦 Configurações de linting movidas para `pyproject.toml` na raiz

---

## [1.1.1] - 2026-09-07

### Corrigido
- Tela preta/branca no Android: removido splash screen intermediário que conflitava com sistema `page.views`
- Back button handler: definido antes da primeira navegação para interceptação correta no Android

---

## [1.1.0] - 2026-09-07

### Adicionado
- Back button handler nativo Android
- Persistência de configurações via `page.client_storage` (SharedPreferences)

### Melhorado
- Performance do timer: updates granulares (`control.update()`) no loop de 1s
- Editor de exercícios: handlers `on_change` só mutam estado local
- Navegação simplificada com `page.views.clear()/append()`
- APIs Flet 0.86.5 padronizadas (`ft.Padding`, `ft.Margin`, `ft.Alignment`)

### Corrigido
- `flet_build.yaml`: removido `compile_sdk_version` inválido
- Importação inútil: removido `RingTimer` não utilizado
- Compatibilidade Android: window operations protegidas com try/except

---

## [1.0.1] - 2026-09-07

### Corrigido
- Bug crítico: parâmetro incorreto `suffix_text` → `suffix` no `TextField` da tela de edição
- Validação: parâmetros válidos do Flet 0.86+ são `prefix`, `suffix`, `prefix_icon`, `suffix_icon`

---

## [1.0.0] - 2026-09-07

### Adicionado
- Configuração de exercícios e intervalos personalizáveis via editor
- Cronômetro HIIT com ring visual gigante e mudança de cor por fase
- Build nativo para Android (APK) via Flet
- Arquitetura modular: `screens/`, `components/`, `utils/`, `store`
- Timer assíncrono preciso com `asyncio`
- Vibração e beep sonoro nas transições de fase
- Controles de Pausar, Pular, Voltar
- Prevenção de sono da tela durante treino
- Tema escuro Material Design 3
- Suporte a 1–20 ciclos configuráveis

### Corrigido
- Compatibilidade Android: window operations envolvidas em try/except

---

## [Unreleased]

### Planejado
- Histórico de treinos realizados
- Notificações locais para próximos treinos
- Suporte a iOS
- Testes automatizados (reintrodução estratégica)
- Toggle tema claro/escuro
- Som nas transições de fase
- Salvamento do estado do timer (se fechar o app no meio do treino)