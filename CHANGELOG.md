# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [2.2.1] - 2026-09-12

### ✨ Adicionado
- **Botão "🚪 SAIR DO APP"** na tela de configuração — encerra o processo completamente (`sys.exit(0)`) no Android
- **Handler `on_view_pop`** — intercepta o botão físico "Voltar" do Android nas rotas `/timer`, `/editor`, `/finish`, para o timer ativo antes de navegar de volta para a configuração
- **Handler `on_route_change`** — detecta retorno programático à tela de configuração (`/config`) e para timer ativo se estiver rodando

### 🐛 Corrigido
- **Áudio funcionando no Android** — caminhos dos arquivos de áudio corrigidos (removido prefixo `assets/` que causava falha no Android); serviços de áudio (`flet_audio.Audio`) registrados via `page.services.extend()` **ANTES** da primeira view ser montada; arquivos convertidos de `.wav` para `.mp3` para compatibilidade total com Android
- **Fechamento correto do app** — wake lock liberado corretamente no método `TimerController.stop()`; task assíncrona do timer cancelada explicitamente ao sair; processo não fica mais rodando em background após fechar o app

### 🔧 Alterado
- Arquivos de áudio renomeados: `.wav` → `.mp3` (`som_inicio.mp3`, `som_intervalo.mp3`, `som_countdown.mp3`, `som_fim.mp3`)
- Registro dos serviços de áudio movido para o topo da função `main()` (linhas 909-919), garantindo inicialização antes de qualquer navegação
- `ft.run(main, assets_dir="assets")` mantido para servir os assets corretamente no build Android

---

## [2.2.0] - 2026-09-11

### ✨ Adicionado
- **TimerController** — classe que encapsula toda a lógica do cronômetro (separação UI/estado/ciclo de vida assíncrono)
- Type Safety completa com `TypedDict` para `Config`, `Estado` e `Etapa`
- Pausa eficiente com `asyncio.Event` (zero CPU quando pausado)
- Tratamento de erros específico (sem `except Exception` genérico)
- Flag `_running` para controle explícito do ciclo de vida
- Limpeza automática de tasks ao navegar entre telas

### 🐛 Corrigido
- `TypeError: handler must be a coroutine function` — sintaxe correta de `page.run_task(func, arg1, arg2)`
- `Future can't be used in await` — `stop()` agora é síncrono
- `AttributeError: no attribute 'retroceder'` — método restaurado
- `ListView Control must be added to the page first` — população direta antes do `return`
- `AttributeError: module 'flet.controls.padding' has no attribute 'only'` — substituído por `ft.Padding(0,0,0,16)`
- Rolagem quebrada no editor — `ft.Column(scroll=AUTO)` em vez de `ft.ListView` aninhado
- Exclusão de exercícios falha — padrão robusto com `list comprehension`
- Wake lock com `__enter__()` quebrado — gerenciamento explícito no ciclo de vida
- Task do timer continuava em background — cancelamento explícito ao navegar

### 🔧 Alterado
- Arquitetura do timer migrada para classe `TimerController`
- Editor simplificado com `ft.Column` + scroll
- Áudio não-bloqueante com `page.run_task`
- Score Pylint de 8.75/10 para ~9.5/10
- Compatibilidade Flet 0.86.5 (uso correto de `page.dialog`, `page.snack_bar`)

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

*Documento de referência. Última atualização: Setembro 2026 (v2.2.1).*