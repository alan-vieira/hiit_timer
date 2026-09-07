# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-09-07

### Adicionado
- **Back button handler nativo Android**: Intercepta botão voltar físico/gesto, previne fechamento acidental durante treino
- **Splash screen imediato**: ProgressRing renderizado antes de qualquer setup pesado (<500ms cold start)
- **Persistência de configurações**: `page.client_storage` (SharedPreferences) salva/restaura treino e ciclos automaticamente

### Melhorado
- **Performance do timer**: Updates granulares (`control.update()`) no loop de 1s — elimina jank, reduz CPU/bateria
- **Editor de exercícios**: Handlers `on_change` só mutam estado local — rebuild da lista só em add/remove
- **Navegação centralizada**: Funções `_navegar_*` + `route_change`/`view_pop` para stack consistente
- **APIs Flet 0.86.5 padronizadas**: `ft.Padding`, `ft.Margin`, `ft.Alignment` em vez de helpers deprecated

### Corrigido
- **`flet_build.yaml`**: Removido `compile_sdk_version` inválido (não existe no schema Flet)
- **Importação inútil**: Removido `RingTimer` não utilizado em `timer_screen.py`
- **Compatibilidade Android**: Window operations já protegidas com try/except (mantido)

## [1.0.1] - 2026-09-07

### Corrigido
- **Bug crítico**: Parâmetro incorreto `suffix_text` → `suffix` no `TextField` da tela de edição de exercícios (causava crash ao editar/voltar)
- Validação: parâmetros válidos do Flet 0.86+ são `prefix`, `suffix`, `prefix_icon`, `suffix_icon`

## [1.0.0] - 2026-09-07

### Adicionado
- Configuração de exercícios e intervalos personalizáveis via editor
- Cronômetro HIIT com ring visual gigante e mudança de cor por fase
- Build nativo para Android (APK) via Flet
- Arquitetura modular: screens, components, utils, store
- Timer assíncrono preciso com asyncio
- Vibração e beep sonoro nas transições de fase
- Controles de Pausar, Pular, Voltar
- Prevenção de sono da tela durante treino
- Tema escuro Material Design 3
- Suporte a 1-20 ciclos configuráveis

### Corrigido
- Compatibilidade Android: window operations envolvidas em try/except

## [Unreleased]

### Planejado
- Histórico de treinos realizados
- Notificações locais para próximos treinos
- Suporte a iOS
- Testes automatizados