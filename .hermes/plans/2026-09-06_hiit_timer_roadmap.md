# HIIT Timer — Roadmap de Melhorias Arquiteturais (v1.1.0+)

> **Análise baseada em inspeção completa do codebase** (655 LOC Python, 12 arquivos, Flet 0.86.5, Android target)

---

## 1. Resumo da Análise Atual

O projeto **HIIT Timer** apresenta uma arquitetura **modular e bem organizada** para o escopo atual (timer assíncrono, 4 telas, store reativo com `@ft.observable`, componentes funcionais). Pontos fortes: separação clara `workout.py` (negócio) vs `screens/` (UI), uso correto do paradigma declarativo Flet 0.86+ (sem `UserControl`), tema MD3 configurado, build Android funcional com permissões de wake lock/vibração.

**Gaps críticos identificados:**
- **Performance no TimerScreen**: `page.update()` a cada segundo reconstrói múltiplos containers (ring, stats, banner, controls) — custo O(n) desnecessário.
- **Persistência zero**: Configuração de exercícios/ciclos perdida ao fechar o app.
- **Testes inexistentes**: Nenhuma infraestrutura de teste (unit/integration).
- **DX tooling ausente**: Sem lint (Ruff), formatação (Black), pre-commit, CI/CD.
- **Recursos Android parciais**: Wake lock OK, mas sem notificações locais nem execução em background.

---

## 2. Roadmap de Melhorias (Priorizado)

| # | Categoria | Melhoria | Impacto | Esforço | Dica Técnica |
|---|-----------|----------|---------|---------|--------------|
| 1 | **Arquitetura/Persistência** | **Persistência de config via `ft.storage` (SharedPreferences)** | **Alto** | **Baixo** | `page.client_storage.set("config", json.dumps(config_dict))` no `ExerciseEditorScreen.handle_save()`; ler no `main()` antes de montar `ConfigScreen`. |
| 2 | **Performance/Flet** | **TimerScreen: atualização granular (sem `page.update()` full)** | **Alto** | **Médio** | Extrair `txt_tempo`, `ring_progress`, `txt_badge`, `top_stats_container`, `banner_container`, `controls_container` como `ft.Ref` ou variáveis de closure; chamar `.update()` **apenas nos controles mutados** (ex: `txt_tempo.update()`). Evita rebuild de `SafeArea`/`Column`/`Stack` pai. |
| 3 | **Android/Nativo** | **Notificações locais (flutter_local_notifications via Flet)** | **Médio** | **Médio** | `page.run_js("flutterLocalNotificationsPlugin.show(...)")` ou plugin Flet nativo quando disponível; disparar no `finalizar_treino()` e agendar lembrete diário via `WorkManager` (futuro). |
| 4 | **DX/Qualidade** | **Lint/Format + Pre-commit (Ruff + Black)** | **Médio** | **Baixo** | `ruff check . && ruff format .`; `pre-commit install` com `.pre-commit-config.yaml` (ruff, black, check-yaml). |
| 5 | **DX/Qualidade** | **Testes unitários (pytest + flet.testing)** | **Médio** | **Médio** | Testar `workout.py` (puro Python) primeiro: `gerar_etapas`, `tempo_total_estimado`, `stats_treino`. Mockar `store` para telas. |
| 6 | **Android/Nativo** | **Wake Lock robusto (manter tela acesa em background)** | **Médio** | **Baixo** | Já tem permissão; garantir `page.window.prevent_close = True` + `page.window.full_screen = True` no `TimerScreen`; avaliar `flet.plugins.android.wake_lock` se existir. |
| 7 | **Arquitetura/Persistência** | **Histórico de treinos (SQLite/JSON local)** | **Baixo** | **Médio** | `page.client_storage` para lista de sessões (`{data, ciclos, tempo_total, exercicios}`); tela `HistoryScreen` nova. |
| 8 | **DX/Qualidade** | **CI/CD GitHub Actions (build APK + lint + test)** | **Baixo** | **Médio** | Workflow `build-apk.yml`: `setup-python`, `pip install flet`, `flet build apk --release`, upload artifact. |
| 9 | **Performance/Flet** | **Transições suaves entre telas (`ft.AnimatedSwitcher` / `page.views` animate)** | **Baixo** | **Baixo** | `page.views.clear()` → `page.views.append(View(...))` + `page.animate_route()` (Flet 0.86+ suporta transições nativas). |
| 10 | **Arquitetura** | **Roteamento declarativo com `ft.Router`** | **Baixo** | **Médio** | Substituir `page.views` manual por `ft.Router(routes=[Route("/config", ConfigScreen), ...])` — ganha deep-link, back-stack nativo Android. |

---

## 3. Próximo Passo Recomendado (Maior Valor / Menor Esforço)

### ✅ **[Arquitetura/Persistência] Persistência de config via `ft.storage` (SharedPreferences)**

**Por que:** Resolve a principal dor do usuário (reconfigurar treino a cada abertura), impacto imediato na UX, esforço mínimo (~30 linhas), zero breaking changes, alinhado ao CHANGELOG "Planejado".

---

### Implementação (Snippets Prontos)

#### A) `main.py` — Carregar config ao iniciar
```python
# main.py — linhas 88-105 (substituir bloco async def main)
async def main(page: ft.Page):
    # ... window settings, theme setup ...

    # 1. Carregar config salva (SharedPreferences via ft.storage)
    saved = page.client_storage.get("workout_config")
    if saved:
        try:
            import json
            from workout import WorkoutConfig, ExercicioConfig
            data = json.loads(saved)
            store.config = WorkoutConfig(
                exercicios=[ExercicioConfig(**ex) for ex in data["exercicios"]],
                descanso_curto=data["descanso_curto"],
                descanso_ciclo=data["descanso_ciclo"],
            )
            store.atualizar_etapas()
        except Exception:
            pass  # Fallback para defaults se JSON corrompido

    # 2. Carregar num_ciclos salvo
    saved_ciclos = page.client_storage.get("num_ciclos")
    if saved_ciclos:
        try:
            store.num_ciclos = int(saved_ciclos)
        except Exception:
            pass

    # 3. Montar tela inicial
    page.views.append(ConfigScreen(page=page, on_iniciar=lambda nc: iniciar_treino(page, nc),
        num_ciclos_inicial=store.num_ciclos, on_navegar_editor=lambda: navegar_editor(page)))
    page.update()
```

#### B) `screens/exercise_editor_screen.py` — Salvar config ao confirmar
```python
# exercise_editor_screen.py — função handle_save (linhas 76-83)
def handle_save():
    store.config = WorkoutConfig(
        exercicios=local["exercicios"],
        descanso_curto=local["descanso_curto"],
        descanso_ciclo=local["descanso_ciclo"],
    )
    store.atualizar_etapas()

    # >>> NOVO: persistir no client_storage (SharedPreferences)
    import json
    data = {
        "exercicios": [{"nome": ex.nome, "emoji": ex.emoji, "duracao": ex.duracao} for ex in store.config.exercicios],
        "descanso_curto": store.config.descanso_curto,
        "descanso_ciclo": store.config.descanso_ciclo,
    }
    page.client_storage.set("workout_config", json.dumps(data))

    on_save()
```

#### C) `main.py` — Persistir `num_ciclos` ao iniciar treino
```python
# main.py — função iniciar_treino (linhas 49-54)
def iniciar_treino(page, num_ciclos):
    store.reiniciar_treino(num_ciclos)
    page.client_storage.set("num_ciclos", str(num_ciclos))  # >>> NOVO
    page.views.clear()
    page.views.append(TimerScreen(page=page, etapas=store.etapas, indice_inicial=0,
        on_finalizar=lambda: finalizar_treino(page), on_voltar_config=lambda: voltar_config(page)))
    page.update()
```

---

### Validação Rápida
```bash
# 1. Rodar app, configurar exercícios/ciclos, fechar, reabrir → config mantida
# 2. Verificar no Android: adb shell cmd appops get com.hiit GET_PREFERENCES (deve permitir)
# 3. Smoke test: python main.py (desktop) → funcionalidade idêntica
```

---

## Próximos Passos Sugeridos (após persistência)

1. **TimerScreen granular update** (Item #2) — ganho real de performance no Android (menos GC, 60fps estável).
2. **Ruff + Black + pre-commit** (Item #4) — base de qualidade para contribuições futuras.
3. **Testes `workout.py`** (Item #5) — lógica pura, fácil de testar, previne regressões em `gerar_etapas`.

---

*Documento gerado em 2026-09-06 — Análise arquitetural HIIT Timer v1.0.0 → v1.1.0+*