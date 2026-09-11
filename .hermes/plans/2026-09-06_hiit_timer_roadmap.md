# HIIT Timer — Roadmap e Histórico Arquitetural (Atualizado para v2.2.0)

> **Status Atual:** v2.2.0 (Estável)  
> **Última Atualização:** 2026-09-11  
> **Arquitetura:** Monolítica (Single-file) com `TimerController`, Type Safety e ciclo de vida assíncrono robusto.

---

## 1. Resumo da Evolução Arquitetural

O projeto evoluiu de uma arquitetura modular complexa (v1.x) para uma estrutura monolítica altamente otimizada (v2.x), priorizando **simplicidade, estabilidade e performance**.

### ✅ Gaps Críticos da v1.x (RESOLVIDOS na v2.x)
- **Performance no Timer:** Resolvido. Atualizações granulares (`control.update()`) e pausa com zero CPU via `asyncio.Event`.
- **Persistência:** Resolvido. Configurações salvas automaticamente em `dados.json` com fallback seguro.
- **DX Tooling:** Resolvido. `pyproject.toml` configurado com Pylint, Black, Ruff e isort.
- **Bugs de Navegação:** Resolvidos. Handler do botão "Voltar" do Android e `page.views.clear()` eliminam a "tela preta fantasma".
- **Wake Lock:** Resolvido. Gerenciamento explícito via `wakepy` integrado ao ciclo de vida do `TimerController`.

### 🏆 Conquistas da v2.2.0
- **`TimerController`:** Desacoplamento total da lógica de negócio da UI, garantindo código testável e livre de efeitos colaterais.
- **Type Safety Completa:** `TypedDict` para `Config`, `Estado` e `Etapa`, prevenindo bugs silenciosos.
- **Tratamento de Erros Robusto:** Fim dos `except Exception:` genéricos; capturas específicas de `asyncio.CancelledError`, `TimeoutError`, etc.
- **Editor 100% Funcional:** Rolagem fluida (`ft.Column` + scroll) e exclusão de exercícios confiável via `list comprehension`.

---

## 2. Roadmap de Melhorias Futuras (v2.3.0+)

| # | Categoria | Melhoria | Impacto | Esforço | Status / Dica Técnica |
|---|-----------|----------|---------|---------|-----------------------|
| 1 | **Android/Nativo** | **Notificações Locais** | Médio | Médio | *Pendente*. Usar `page.run_js` ou plugin nativo para notificar fim do treino. |
| 2 | **Arquitetura** | **Histórico de Treinos** | Médio | Médio | *Pendente*. Salvar sessões concluídas em `dados.json` e criar `tela_historico`. |
| 3 | **DX/Qualidade** | **CI/CD GitHub Actions** | Baixo | Baixo | *Pendente*. Workflow `build-apk.yml` para lint e build automático do APK. |
| 4 | **DX/Qualidade** | **Testes Unitários Estratégicos** | Baixo | Médio | *Pendente*. Reintroduzir `pytest` focado apenas em funções puras (`gerar_etapas`, `tempo_total`). |
| 5 | **UX/UI** | **Toggle Tema Claro/Escuro** | Baixo | Baixo | *Pendente*. Adicionar botão nas configurações para alternar `page.theme_mode`. |
| 6 | **Android/Nativo** | **Execução em Background** | Baixo | Alto | *Pendente*. Avaliar plugins para manter o timer rodando com a tela bloqueada. |

---

## 3. Histórico de Decisões Arquiteturais

### v2.0.0: A Grande Simplificação (Set/2026)
- **Decisão:** Abandonar a arquitetura modular (8+ arquivos, store reativo, 149 testes) em favor de um arquivo único (`main.py`).
- **Motivo:** A complexidade não trazia benefícios para um app pessoal e introduzia bugs de navegação.
- **Resultado:** Código reduzido de ~1500 para ~460 linhas, com manutenção drasticamente simplificada.

### v2.1.0: Polimento e Recursos Nativos (Set/2026)
- **Decisão:** Adicionar `flet-audio` e `wakepy` sem complicar o loop principal.
- **Resultado:** Feedback sonoro (countdown 3-2-1) e tela sempre ligada durante o treino.

### v2.2.0: Robustez e Type Safety (Set/2026)
- **Decisão:** Refatorar o loop do timer para uma classe `TimerController` com gerenciamento explícito de estado e tarefas.
- **Resultado:** Eliminação de vazamentos de memória, pausa com zero CPU e score Pylint elevado para ~9.5/10.

---

*Documento mantido pelo Hermes Agent. Última revisão: 2026-09-11.*