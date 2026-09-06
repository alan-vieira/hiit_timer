# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
- Persistência de configurações (SharedPreferences / JSON)
- Histórico de treinos realizados
- Notificações locais para próximos treinos
- Suporte a iOS
- Testes automatizados