# ⏱️ HIIT Timer

Cronômetro para treinos HIIT (High-Intensity Interval Training) desenvolvido em **Python 3.12 + Flet** e compilado nativamente para **Android**.

> **Versão:** 2.2.1 · **Autor:** Alan Vieira · **Licença:** MIT

---

## ✨ Sobre o Projeto

Aplicativo simples e direto para gerenciar treinos intervalados. Configure exercícios, durações e ciclos de descanso, inicie o treino e acompanhe o cronômetro com feedback visual (ring animado), sonoro (4 efeitos distintos) e háptico (vibração) nas transições.

**Filosofia:** simplicidade sobre complexidade. Um cronômetro não precisa de arquitetura enterprise — precisa funcionar.

---

## 🚀 Funcionalidades

- **Tela de Configuração** — Resumo do treino (ciclos, exercícios, etapas, tempo total) + preview das etapas
- **Editor de Treino** — Personalize exercícios (nome, emoji, duração), intervalos curtos/longos e número de ciclos (1–20)
- **Cronômetro Ativo** — Ring visual animado, badge de fase (EXERCÍCIO/DESCANSO), stats em tempo real, controles de pausar/pular/retroceder
- **Tela de Conclusão** — Resumo do treino com opções de repetir ou reconfigurar
- **Persistência Local** — Configurações salvas automaticamente em JSON (sobrevivem a reinicialização)
- **Tema Escuro Material 3** — Paleta violeta/roxo consistente (seed `#9C27B0`)
- **Navegação Android** — Botão físico "Voltar" interceptado corretamente em todas as telas
- **Build Nativo Android** — APK pronto para instalação via `flet build apk`
- **🔊 Sistema de Áudio** — 4 efeitos sonoros distintos em MP3:
  - `som_inicio.mp3` — início de exercício
  - `som_intervalo.mp3` — intervalo/descanso
  - `som_countdown.mp3` — contagem regressiva (3, 2, 1 nos últimos 3s)
  - `som_fim.mp3` — fim do treino
- **🔋 Wake Lock** — Mantém tela ligada durante treino no Android (via `wakepy`)
- **📜 Editor com Scroll** — Lista de exercícios expansível com scroll interno automático
- **🏃 Emoji Padrão** — Novo exercício já vem com emoji 🏃
- **🚪 Fechamento Correto** — Botão "SAIR DO APP" encerra o processo completamente; handler `on_view_pop` para timer ao voltar; wake lock e task cancelados corretamente

---

## 📋 Últimas Mudanças (v2.2.1 - 2026-09-12)

### ✨ Adicionado
- **Botão "🚪 SAIR DO APP"** na tela de configuração — encerra o processo completamente no Android
- **Handler `on_view_pop`** — intercepta botão "Voltar" do Android e para o timer antes de navegar
- **Handler `on_route_change`** — detecta retorno à tela de configuração e para timer ativo

### 🐛 Corrigido
- **Áudio funcionando no Android** — caminhos dos arquivos corrigidos (removido prefixo `assets/`), serviços registrados ANTES da primeira view, arquivos convertidos de `.wav` para `.mp3`
- **Fechamento correto do app** — wake lock liberado no `stop()`, task do timer cancelada ao sair, processo não fica mais rodando em background

### 🔧 Alterado
- Arquivos de áudio: `.wav` → `.mp3` (compatibilidade Android)
- Registro de serviços de áudio movido para o início do `main()` (antes de qualquer view)

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
├── main.py              # App completo (~950 linhas)
├── dados.json           # Configuração persistida (criado automaticamente)
├── pyproject.toml       # Config: Pylint, Black, Ruff, isort + metadados PEP 621
├── requirements.txt     # Dependências de produção
├── CHANGELOG.md         # Histórico de versões detalhado
├── roadmap.md           # Roteiro do projeto e próximas features
├── assets/              # Arquivos de áudio (som_inicio.mp3, som_intervalo.mp3, som_countdown.mp3, som_fim.mp3)
├── _legacy/             # Arquitetura modular v1.x (referência histórica)
├── build/               # Artefatos de build (APK, etc.)
├── docs/                # Documentação adicional
│   ├── instalacao.md
│   ├── uso.md
│   ├── arquitetura.md
│   └── personalizacao.md
├── .gitignore
└── venv/                # Ignorado pelo git
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

O arquivo é criado automaticamente na primeira execução com valores padrão (5 exercícios de 60s, descanso curto 30s, descanso longo 60s, 3 ciclos).

---

## 🔄 Fluxo de Uso

1. **Configuração** (tela inicial) → revise o treino e toque em **INICIAR TREINO**
2. **Cronômetro** → acompanhe as etapas, pause, pule ou retroceda conforme necessário
3. **Conclusão** → veja o resumo e escolha repetir ou reconfigurar
4. **Editor** (via botão "PERSONALIZAR TREINO") → ajuste exercícios, durações e ciclos
5. **Sair** (via botão "🚪 SAIR DO APP") → encerra o aplicativo completamente

---

## 📊 Comparativo de Versões

| Métrica | v1.x (modular) | v2.0 (monolítico) | v2.1 | v2.2 | v2.2.1 (atual) |
|---------|----------------|-------------------|------|------|----------------|
| Arquivos de código | 8+ | 1 | 1 | 1 | 1 |
| Linhas totais | ~1500 | ~460 | ~550 | ~600 | ~950 |
| Complexidade | Alta | Baixa | Baixa | Baixa | Baixa |
| Bugs de navegação | Tela preta, seta de voltar quebrada | Resolvidos | Resolvidos | Resolvidos | Resolvidos |
| Build Android | Funcional | Funcional | Funcional | Funcional | Funcional |
| Áudio | ❌ | ❌ | ✅ 4 sons + countdown | ✅ 4 sons + countdown | ✅ 4 sons MP3 (Android OK) |
| Wake Lock | ❌ | ❌ | ✅ wakepy | ✅ wakepy | ✅ wakepy |
| Editor Scroll | ❌ | ❌ | ✅ Auto-expansível | ✅ Auto-expansível | ✅ Auto-expansível |
| Type Safety | ❌ | ❌ | ❌ | ✅ TypedDict completo | ✅ TypedDict completo |
| Pausa eficiente | ❌ | ❌ | ❌ | ✅ asyncio.Event (zero CPU) | ✅ asyncio.Event (zero CPU) |
| Fechamento app | ❌ | ❌ | ❌ | ❌ | ✅ Botão + handlers |
| Score Pylint | N/A | N/A | 8.75/10 | ~9.5/10 | ~9.5/10 |

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

## 📚 Documentação Adicional

- [Changelog completo](CHANGELOG.md)
- [Roadmap do projeto](roadmap.md)
- [Guia de instalação](docs/instalacao.md)
- [Como usar o app](docs/uso.md)
- [Arquitetura do código](docs/arquitetura.md)
- [Personalização avançada](docs/personalizacao.md)

---

*Documento de referência. Última atualização: Setembro 2026 (v2.2.1).*