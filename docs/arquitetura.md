# 🏗️ Arquitetura do Código — HIIT Timer

> **Versão:** v2.2.1 · **Arquitetura:** Monolítica (single-file) · **Linguagem:** Python 3.12 + Flet 0.86.5

---

## 📐 Visão Geral

```
main.py (~950 linhas)
│
├── 📦 Imports & Config
├── 🏷️ Tipos (TypedDict)
├── 💾 Persistência (JSON)
├── 🛠️ Helpers
├── 🎮 TimerController (classe principal)
├── 🖥️ Telas (4 Views Flet)
└── 🚀 Entry Point (main async)
```

**Princípio:** Um único arquivo, zero dependências internas, fácil de ler, modificar e buildar.

---

## 🏷️ Tipos (TypedDict) — Type Safety Completa

```python
class Etapa(TypedDict):
    indice: int       # 1-based index da etapa
    nome: str         # "Polichinelo", "Descanso", etc.
    emoji: str        # "🤸", "☕", etc.
    duracao: int      # Segundos
    tipo: str         # "exercicio" | "descanso" | "descanso_ciclo"
    ciclo: int        # Número do ciclo (1-based)

class Config(TypedDict):
    exercicios: list[dict[str, Any]]  # [{nome, emoji, duracao}, ...]
    descanso_curto: int                # Segundos entre exercícios
    descanso_ciclo: int                # Segundos entre ciclos
    num_ciclos: int                    # 1-20

class Estado(TypedDict):
    idx: int              # Etapa atual (0-based)
    tempo: int            # Segundos restantes na etapa
    pausado: bool         # True se pausado
    finalizado: bool      # True se treino acabou
    ultimo_segundo_tocado: int  # Para countdown (evita tocar 2x)
    som_final_tocado: bool      # Evita tocar som_fim 2x
```

> ✅ **Benefício:** IDE autocomplete, mypy/pylint detectam erros, refactoring seguro.

---

## 💾 Persistência — `dados.json`

### `carregar() -> Config`
```python
def carregar() -> Config:
    try:
        with get_path().open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return CONFIG_PADRAO.copy()
```

### `salvar(dados: Config) -> bool`
```python
def salvar(dados: Config) -> bool:
    try:
        with get_path().open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False
```

- **Atomicidade:** Escrita direta (arquivo pequeno, risco baixo)
- **Fallback:** Config padrão se arquivo corrompido/ausente
- **Encoding:** UTF-8 com `ensure_ascii=False` (emojis preservados)

---

## 🛠️ Helters Principais

| Função | Descrição |
|--------|-----------|
| `fmt(segundos: int) -> str` | Formata `MM:SS` (ex: `125` → `"02:05"`) |
| `gerar_etapas(config, num_ciclos) -> list[Etapa]` | Gera lista plana de todas as etapas do treino |
| `tempo_total(config, num_ciclos) -> int` | Soma duração de todas as etapas |
| `navegar(page, tela_func, *args)` | `page.views.clear()` + `append()` + `update()` — navegação limpa sem histórico fantasma |

### Lógica de `gerar_etapas()`
```
Para cada ciclo (1..num_ciclos):
  Para cada exercício:
    Adiciona etapa "exercicio"
    Se último exercício do ciclo:
      Se não for último ciclo: adiciona "descanso_ciclo"
    Senão:
      Adiciona "descanso" (curto)
```

---

## 🎮 TimerController — Cérebro do Cronômetro

### Responsabilidades
- Estado do timer (`Estado`)
- Loop assíncrono de contagem (1Hz)
- Controle de pausa eficiente (`asyncio.Event`)
- Reprodução de áudio não-bloqueante
- Wake lock lifecycle
- Binding UI ↔ Estado

### Atributos Principais
```python
class TimerController:
    def __init__(self, page: ft.Page, config: Config, num_ciclos: int):
        self.page = page
        self.config = config
        self.num_ciclos = num_ciclos
        self.etapas = gerar_etapas(config, num_ciclos)
        self.estado: Estado = {...}  # idx=0, tempo=duracao_1, pausado=False...
        self._running = False        # Flag explícita de ciclo de vida
        self._pause_event = asyncio.Event()  # Pausa eficiente
        self._pause_event.set()      # Inicia "despausado"
        self._task: asyncio.Task | None = None
        self._wake_lock = None       # wakepy keep object
```

### Métodos Públicos

| Método | Descrição |
|--------|-----------|
| `start()` | Inicia task assíncrona `_run_loop()`, adquire wake lock |
| `stop()` | Para tudo: `_running=False`, `_pause_event.set()`, cancela task, libera wake lock |
| `alternar_pausa()` | Toggle `_pause_event` (clear/set) |
| `pular()` | Avança `idx`, reseta `tempo` para próxima etapa |
| `retroceder()` | Volta `idx` (se > 0), reseta `tempo` |
| `parar_e_voltar()` | `stop()` + `navegar(page, tela_config)` |
| `bind_ui(...)` | Conecta controles Flet para updates granulares |

### Loop Principal — `_run_loop()`
```python
async def _run_loop(self) -> None:
    self._running = True
    self._acquire_wake_lock()
    
    while self._running and self.estado["idx"] < len(self.etapas):
        await self._pause_event.wait()  # Bloqueia se pausado (zero CPU)
        
        if not self._running:
            break
            
        # Toca áudio da fase (início/intervalo) uma vez por etapa
        # Toca countdown nos últimos 3s
        # Decrementa tempo
        # Atualiza UI via _refresh_ui()
        # Se tempo == 0: avança etapa
        
        await asyncio.sleep(1.0)
    
    if self._running:  # Terminou naturalmente
        self._play_som_fim()
        self.page.run_task(lambda: navegar(page, tela_finish, ...))
    
    self._release_wake_lock()
```

### Pausa Eficiente — `asyncio.Event`
```python
# Pausar
self._pause_event.clear()  # _run_loop() bloqueia no wait()

# Continuar
self._pause_event.set()    # _run_loop() desenfileira imediatamente
```
> ✅ **Zero CPU** quando pausado — sem busy loop, sem `sleep` curto.

### Áudio Não-Bloqueante
```python
async def _play_audio(self, audio: fta.Audio) -> None:
    try:
        await asyncio.wait_for(audio.play_async(), timeout=3.0)
    except (asyncio.TimeoutError, Exception):
        pass  # Silencioso — nunca trava o timer
```
Chamado via `self.page.run_task(self._play_audio, audio)` — fire-and-forget.

### Wake Lock
```python
def _acquire_wake_lock(self) -> None:
    try:
        self._wake_lock = keep.presenting()
        self._wake_lock.__enter__()
    except Exception:
        self._wake_lock = None

def _release_wake_lock(self) -> None:
    if self._wake_lock:
        try:
            self._wake_lock.__exit__(None, None, None)
        except Exception:
            pass
        self._wake_lock = None
```

---

## 🖥️ Telas (Views Flet) — 4 Rotas

| Rota | Função | Descrição |
|------|--------|-----------|
| `/config` | `tela_config(page)` | Tela inicial — stats, preview, 3 botões |
| `/editor` | `tela_editor(page)` | Editor com Column+scroll, formulário inline |
| `/timer` | `tela_timer(page, config, num_ciclos)` | Cronômetro ativo com TimerController |
| `/finish` | `tela_finish(page, tempo_total, num_ciclos)` | Conclusão com botões repetir/configurar |

### Padrão de Navegação
```python
def navegar(page: ft.Page, tela_func: Any, *args: Any, **kwargs: Any) -> None:
    page.views.clear()
    page.views.append(tela_func(page, *args, **kwargs))
    page.update()
```
- **Sempre** `clear()` → `append()` → `update()`
- **Sem** `page.go()` ou `page.views.append()` solto
- **Elimina** "tela preta fantasma" do histórico

### Navegação Android — Handlers Globais (v2.2.1)

```python
# main() — registrado ANTES da primeira view
def on_view_pop(e: ft.ViewPopEvent) -> None:
    if page.route in ["/timer", "/editor", "/finish"]:
        if hasattr(page, "timer_controller") and page.timer_controller:
            page.timer_controller.stop()
        navegar(page, tela_config)
        e.prevent_default = True

def on_route_change(e: ft.RouteChangeEvent) -> None:
    if e.route == "/config" and hasattr(page, "timer_controller") and page.timer_controller:
        if page.timer_controller._running:
            page.timer_controller.stop()

page.on_view_pop = on_view_pop
page.on_route_change = on_route_change
```

---

## 🎨 Tema & Estilo

```python
page.theme_mode = ft.ThemeMode.DARK
page.theme = ft.Theme(
    color_scheme_seed="#9C27B0",  # Roxo Material 3
    use_material3=True
)
```

**Cores por Fase (CORES dict):**
| Tipo | Primária | Container | Label |
|------|----------|-----------|-------|
| exercicio | `#9C27B0` | PRIMARY_CONTAINER | EXERCÍCIO |
| descanso | `#FF9800` | SECONDARY_CONTAINER | DESCANSO |
| descanso_ciclo | `#FF9800` | SECONDARY_CONTAINER | DESCANSO LONGO |

---

## 🔊 Sistema de Áudio (v2.2.1)

### Inicialização (main() — linhas 909-919)
```python
som_inicio = fta.Audio(src="som_inicio.mp3", autoplay=False, volume=0.8)
som_intervalo = fta.Audio(src="som_intervalo.mp3", autoplay=False, volume=0.8)
som_countdown = fta.Audio(src="som_countdown.mp3", autoplay=False, volume=0.6)
som_fim = fta.Audio(src="som_fim.mp3", autoplay=False, volume=1.0)

page.services.extend([som_inicio, som_intervalo, som_countdown, som_fim])
page.som_inicio = som_inicio
# ... (referências para TimerController acessar)
```

**Pontos Críticos:**
1. **Registrado ANTES** de `navegar(page, tela_config)` — `page.services` deve ter os audios antes de qualquer view
2. **Sem prefixo `assets/`** no `src` — Flet serve via `assets_dir="assets"` no `ft.run()`
3. **Formato MP3** — Compatibilidade Android (`.wav` falhava)

### Uso no TimerController
```python
# Início de exercício
await self.page.run_task(self._play_audio, self.page.som_inicio)

# Início de descanso
await self.page.run_task(self._play_audio, self.page.som_intervalo)

# Countdown (últimos 3s)
if tempo in (3, 2, 1) and tempo != self.estado["ultimo_segundo_tocado"]:
    await self.page.run_task(self._play_audio, self.page.som_countdown)

# Fim do treino
await self.page.run_task(self._play_audio, self.page.som_fim)
```

---

## 📦 Build Android

```bash
flet build apk --release
```

**Configuração implícita via `ft.run(main, assets_dir="assets")`:**
- Assets copiados para APK automaticamente
- `flet_audio` serviços registrados funcionam no Android
- `wakepy` usa `PowerManager.WAKE_LOCK` nativo

**Estrutura de saída:**
```
build/
└── app/outputs/flutter-apk/
    └── app-release.apk  # ~15-20 MB
```

---

## 📊 Métricas de Código (v2.2.1)

| Métrica | Valor |
|---------|-------|
| Linhas totais | ~950 |
| Funções | ~25 |
| Classes | 1 (`TimerController`) |
| TypedDicts | 3 |
| Complexidade ciclomática | Baixa |
| Pylint score | ~9.5/10 |
| Type hints | 100% API pública |

---

## 🔄 Fluxo de Dados

```
[main.py load]
       │
       ▼
carregar() → Config (dados.json ou padrão)
       │
       ▼
tela_config() → View com stats calculados (gerar_etapas, tempo_total)
       │
       ├── INICIAR → tela_timer() → TimerController.start() → _run_loop()
       │                    │
       │                    ├── asyncio.Event (pausa)
       │                    ├── page.run_task(audio) (sons)
       │                    ├── wakepy (tela ligada)
       │                    └── bind_ui() → updates granulares
       │
       ├── EDITAR → tela_editor() → salva → tela_config()
       │
       └── SAIR → sys.exit(0)
```

---

## 🎯 Decisões de Design

| Decisão | Justificativa |
|---------|---------------|
| **Single-file** | Simplicidade, build rápido, fácil debug, zero imports internos quebrados |
| **TypedDict vs dataclass** | Leve, serializável JSON nativo, sem `__post_init__` ou frozen |
| **asyncio.Event para pausa** | Zero CPU, wakeup instantâneo, padrão Python idiomático |
| **page.views.clear()** | Elimina bugs de navegação Flet (tela preta, histórico sujo) |
| **Serviços de áudio no main()** | Requerido pelo Flet Android — services devem existir antes da view |
| **MP3 não WAV** | `flet_audio` + Android MediaPlayer: MP3 = suporte universal |
| **sys.exit(0) para sair** | Garante finalização de processo no Android (não fica em background) |

---

## 🧪 Testabilidade

- **TimerController** isolado — pode ser instanciado com `page` mockado
- **Helpers** (`gerar_etapas`, `tempo_total`, `fmt`) — funções puras, testáveis unitariamente
- **Persistência** — `carregar/salvar` usam `Path` injetável (pode mockar `get_path`)

---

*Atualizado: Setembro 2026 (v2.2.1)*