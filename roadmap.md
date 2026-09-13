# 🗺️ Roadmap — HIIT Timer

> **Status atual:** ✅ **v2.2.1 — Estável e funcional** (Setembro 2026)

---

## 📜 Histórico de Versões

| Versão | Data | Status | Principais Mudanças |
|--------|------|--------|---------------------|
| **v2.2.1** | 2026-09-12 | ✅ Estável | Áudio Android corrigido, botão SAIR, handlers de navegação, fechamento correto |
| **v2.2.0** | 2026-09-11 | ✅ Estável | TimerController, TypedDict, pausa eficiente, error handling específico |
| **v2.1.0** | 2026-09-10 | ✅ Estável | Áudio (4 sons), wake lock, scroll editor, emoji padrão |
| **v2.0.0** | 2026-09-09 | ✅ Estável | Refatoração monolítica, navegação corrigida, build Android |
| **v1.x** | 2026-09-07 | 📦 Legacy | Arquitetura modular (preservada em `_legacy/`) |

---

## 🎯 Próximas Features Sugeridas

### 🔥 Prioridade Alta (Qualidade de Vida)

- [ ] **Modo Escuro/Claro** — Toggle no editor ou config para alternar tema
- [ ] **Exportar/Importar Treino** — JSON shareable (WhatsApp, email, arquivo)
- [ ] **Notificações Locais** — Alerta sonoro/vibração quando app em background (Android)
- [ ] **Histórico de Treinos** — Log local com data, duração, exercícios completados

### 🎨 Prioridade Média (UX)

- [ ] **Presets de Treino** — Templates prontos (Tabata, EMOM, AMRAP, Custom)
- [ ] **Contagem Regressiva por Voz** — TTS "3, 2, 1, comece" (opcional)
- [ ] **Vibração Personalizada** — Padrões diferentes para exercício/descanso/fim
- [ ] **Tela de Estatísticas** — Total de treinos, tempo total, streak de dias

### 🔧 Prioridade Baixa (Nice to Have)

- [ ] **Suporte a iOS** — Testes e ajustes via `flet build ipa`
- [ ] **Web Build** — `flet build web` para versão PWA
- [ ] **Internacionalização (i18n)** — PT-BR / EN / ES
- [ ] **Temas de Cor** — Múltiplas seeds Material 3 (verde, azul, laranja)
- [ ] **Widget Android** — Iniciar treino rápido da home screen

---

## 🐛 Issues Conhecidas (v2.2.1)

| Issue | Severidade | Status | Notas |
|-------|------------|--------|-------|
| Áudio pode falhar em alguns dispositivos Android antigos (API < 29) | Baixa | 🔍 Investigando | `flet-audio` depende de `MediaPlayer` nativo |
| Wake lock não funciona em modo "Picture-in-Picture" | Baixa | 📋 Documentado | Limitação do `wakepy` no Android |
| Scroll do editor pode travar com 20+ exercícios | Muito baixa | ✅ Aceitável | Uso real raramente passa de 10 exercícios |
| Botão "SAIR" não aparece no desktop (Linux/macOS) | Muito baixa | 📋 Documentado | `sys.exit(0)` funciona, mas UX melhoraria com `page.window.destroy()` |

---

## 💡 Ideias Futuras (Backlog)

- **Modo "Treino Livre"** — Sem ciclos fixos, cronômetro simples start/stop/lap
- **Integração Health/Google Fit** — Sincronizar treinos concluídos
- **Compartilhamento Social** — Card de conclusão para Instagram Stories
- **Modo "Treino em Dupla"** — Dois timers sincronizados (ex: casal, personal + aluno)
- **Planejamento Semanal** — Calendário com treinos agendados e lembretes

---

## 📋 Checklist de Release (para próximas versões)

- [ ] Atualizar versão em `pyproject.toml`, `README.md`, `CHANGELOG.md`
- [ ] Testar `flet build apk --release` em device físico
- [ ] Verificar áudio, wake lock, navegação "Voltar", botão SAIR
- [ ] Rodar `python -m pylint main.py` (meta: ≥ 9.0/10)
- [ ] Tag git: `git tag vX.Y.Z && git push origin vX.Y.Z`
- [ ] Atualizar documentação em `docs/` se houver mudanças de arquitetura

---

*Última atualização: Setembro 2026 (v2.2.1).*