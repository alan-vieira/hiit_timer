# ⏱️ HIIT Timer

Cronômetro para treinos HIIT (High-Intensity Interval Training) desenvolvido em **Python 3.12 + Flet** e compilado nativamente para **Android**.

> **Versão:** 2.0.0 · **Autor:** Alan Vieira · **Licença:** MIT

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
pip install flet
```

### Executar (desenvolvimento)

```bash
python main.py
```

### Build do APK (Android)

```bash
flet build apk --org com.alanvieira --product "HIITTimer"
```

O APK será gerado em `build/apk/hiit_timer.apk`.

---

## 📁 Estrutura do Projeto

```
hiit_timer/
├── main.py          # App completo (~460 linhas)
├── dados.json       # Configuração persistida (criado automaticamente)
├── pyproject.toml   # Config: Pylint, Black, Ruff, isort
├── _legacy/         # Arquitetura modular v1.x (referência histórica)
└── build/           # Artefatos de build (APK, etc.)
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

| Métrica | v1.x (modular) | v2.0 (monolítico) |
|---------|----------------|-------------------|
| Arquivos de código | 8+ | 1 |
| Linhas totais | ~1500 | ~460 |
| Complexidade | Alta (store reativo, dataclasses frozen, 149 testes) | Baixa |
| Bugs de navegação | Tela preta, seta de voltar quebrada | Resolvidos |
| Build Android | Funcional | Funcional |

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

*Documento de referência. Última atualização: Setembro 2026 (v2.0.0).*