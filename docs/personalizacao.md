# 🎨 Personalização Avançada — HIIT Timer

> **Versão:** v2.2.1

---

## 🎵 Adicionando/Substituindo Sons

### Arquivos Necessários
Coloque na pasta `assets/` (mesmo nível do `main.py`):

| Arquivo | Uso | Volume Padrão | Duração Sugerida |
|---------|-----|---------------|------------------|
| `som_inicio.mp3` | Início de exercício | 0.8 | 0.5–2s |
| `som_intervalo.mp3` | Início de descanso | 0.8 | 0.5–2s |
| `som_countdown.mp3` | Countdown 3-2-1 | 0.6 | 0.3–1s (tocado 3x) |
| `som_fim.mp3` | Fim do treino | 1.0 | 1–3s |

### Requisitos Técnicos
- **Formato:** MP3 (obrigatório para Android)
- **Sample rate:** 44.1 kHz ou 48 kHz
- **Canais:** Mono ou Estéreo
- **Bitrate:** 128–320 kbps

### Como Substituir
1. Gere/baixe seus arquivos `.mp3`
2. Renomeie exatamente como acima
3. Substitua os arquivos em `assets/`
4. Rebuild: `flet build apk --release`

> ⚠️ **Importante:** Nomes **devem ser exatos** (case-sensitive). O código referencia `src="som_inicio.mp3"` etc.

### Volume Personalizado
Edite no `main()` (linhas 910-913):
```python
som_inicio = fta.Audio(src="som_inicio.mp3", autoplay=False, volume=0.8)  # 0.0 a 1.0
som_intervalo = fta.Audio(src="som_intervalo.mp3", autoplay=False, volume=0.8)
som_countdown = fta.Audio(src="som_countdown.mp3", autoplay=False, volume=0.6)
som_fim = fta.Audio(src="som_fim.mp3", autoplay=False, volume=1.0)
```

### Adicionar Mais Sons (Ex: Som de "Pausa")
1. Adicione `som_pausa.mp3` em `assets/`
2. No `main()`:
```python
som_pausa = fta.Audio(src="som_pausa.mp3", autoplay=False, volume=0.7)
page.services.extend([som_inicio, som_intervalo, som_countdown, som_fim, som_pausa])
page.som_pausa = som_pausa
```
3. No `TimerController.alternar_pausa()`:
```python
def alternar_pausa(self) -> None:
    self.estado["pausado"] = not self.estado["pausado"]
    if self.estado["pausado"]:
        self._pause_event.clear()
        self.page.run_task(self._play_audio, self.page.som_pausa)  # NOVO
    else:
        self._pause_event.set()
    self._update_controls()
```

---

## 🎨 Mudando o Tema (Cores)

### Seed Color Principal
Edite no `main()` (linha 907):
```python
page.theme = ft.Theme(color_scheme_seed="#9C27B0", use_material3=True)
```

**Seeds Populares:**
| Cor | Hex | Vibe |
|-----|-----|------|
| Roxo (atual) | `#9C27B0` | Elegante, foco |
| Azul | `#2196F3` | Calmo, profissional |
| Verde | `#4CAF50` | Natureza, saúde |
| Laranja | `#FF9800` | Energia, ação |
| Vermelho | `#F44336` | Intensidade, urgência |
| Teal | `#009688` | Equilíbrio, moderno |
| Índigo | `#3F51B5` | Profundo, tech |
| Rosa | `#E91E63` | Vibrante, divertido |

### Modo Claro/Escuro
Forçar modo (linha 906):
```python
page.theme_mode = ft.ThemeMode.DARK   # Escuro (padrão)
# page.theme_mode = ft.ThemeMode.LIGHT  # Claro
# page.theme_mode = ft.ThemeMode.SYSTEM  # Segue OS
```

### Cores por Fase (Exercício/Descanso)
Edite o dict `CORES` (linhas 55-65):
```python
CORES = {
    "exercicio": (
        "#9C27B0",           # Cor do ring (progresso)
        "#4A148C",           # Cor do track (fundo)
        ft.Colors.PRIMARY_CONTAINER,    # Badge bg
        ft.Colors.ON_PRIMARY_CONTAINER, # Badge texto
        "EXERCÍCIO"          # Label
    ),
    "descanso": (
        "#FF9800",
        "#E65100",
        ft.Colors.SECONDARY_CONTAINER,
        ft.Colors.ON_SECONDARY_CONTAINER,
        "DESCANSO"
    ),
    "descanso_ciclo": (
        "#FF9800",
        "#E65100",
        ft.Colors.SECONDARY_CONTAINER,
        ft.Colors.ON_SECONDARY_CONTAINER,
        "DESCANSO LONGO"
    ),
}
```

**Estrutura da tupla:** `(ring_color, track_color, badge_bg, badge_text, label)`

### Tema Customizado Completo (Material 3)
```python
page.theme = ft.Theme(
    color_scheme_seed="#9C27B0",
    use_material3=True,
    # Overrides opcionais:
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.PURPLE,
        on_primary=ft.Colors.WHITE,
        primary_container=ft.Colors.PURPLE_100,
        on_primary_container=ft.Colors.PURPLE_900,
        secondary=ft.Colors.ORANGE,
        on_secondary=ft.Colors.WHITE,
        surface=ft.Colors.GREY_900,
        on_surface=ft.Colors.WHITE,
        # ... etc
    ),
    # Tipografia
    text_theme=ft.TextTheme(
        headline_large=ft.TextStyle(font_family="Roboto", size=32, weight=ft.FontWeight.BOLD),
        body_medium=ft.TextStyle(font_family="Roboto", size=14),
        # ...
    ),
)
```

---

## ⚙️ Configurações Padrão (CONFIG_PADRAO)

Edite no topo do `main.py` (linhas 42-53):
```python
CONFIG_PADRAO: Config = {
    "exercicios": [
        {"nome": "Polichinelo", "emoji": "🤸", "duracao": 60},
        {"nome": "Elevação de joelhos", "emoji": "🦵", "duracao": 60},
        {"nome": "Crucifixo", "emoji": "🦋", "duracao": 60},
        {"nome": "Extensão de braços", "emoji": "💪", "duracao": 60},
        {"nome": "Agachamento", "emoji": "🏋️", "duracao": 60},
    ],
    "descanso_curto": 30,
    "descanso_ciclo": 60,
    "num_ciclos": 3,
}
```

### Exemplos de Presets

#### Tabata (4 min)
```python
CONFIG_PADRAO = {
    "exercicios": [{"nome": "Sprint", "emoji": "🏃", "duracao": 20}],
    "descanso_curto": 10,
    "descanso_ciclo": 0,
    "num_ciclos": 8,
}
```

#### EMOM 10 min
```python
CONFIG_PADRAO = {
    "exercicios": [
        {"nome": "Burpees", "emoji": "🤸", "duracao": 40},
        {"nome": "Push-ups", "emoji": "💪", "duracao": 40},
    ],
    "descanso_curto": 20,
    "descanso_ciclo": 60,
    "num_ciclos": 5,
}
```

#### Treino Força (3×5)
```python
CONFIG_PADRAO = {
    "exercicios": [
        {"nome": "Agachamento", "emoji": "🏋️", "duracao": 45},
        {"nome": "Flexão", "emoji": "💪", "duracao": 45},
        {"nome": "Prancha", "emoji": "🧘", "duracao": 60},
        {"nome": "Afundo", "emoji": "🦵", "duracao": 45},
        {"nome": "Prancha lateral", "emoji": "🧘", "duracao": 30},
    ],
    "descanso_curto": 30,
    "descanso_ciclo": 90,
    "num_ciclos": 3,
}
```

---

## 📱 Comportamento Android

### Ícone do App
Substitua `assets/icon.png` (512x512) e rebuild.

### Splash Screen
Crie `assets/splash.png` e configure no `pyproject.toml` (se usar `flet_build.yaml`):
```yaml
# flet_build.yaml (criar na raiz se não existir)
flutter:
  assets:
    - assets/splash.png
```

### Permissões (AndroidManifest.xml)
O Flet injeta automaticamente baseadas no código. Para customizar, crie `android/app/src/main/AndroidManifest.xml`:
```xml
<manifest>
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <!-- Para notificações futuras -->
</manifest>
```

---

## 🔧 Ajustes de Performance

### Intervalo do Timer (Atual: 1Hz)
No `TimerController._run_loop()`:
```python
await asyncio.sleep(1.0)  # Mude para 0.5 para updates mais suaves (mais CPU)
```

### Timeout de Áudio (Atual: 3s)
No `TimerController._play_audio()`:
```python
await asyncio.wait_for(audio.play_async(), timeout=3.0)  # Aumente se sons longos
```

### Wake Lock Strategy
Atual: `keep.presenting()` (tela ligada). Alternativas do `wakepy`:
```python
# keep.running()  # CPU ativa, tela pode apagar
# keep.presenting()  # Tela ligada (atual)
```

---

## 🌐 Internacionalização (i18n) — Preparação

### Textos Hardcoded para Extrair
Procure por strings em português no código:
- Labels: `"EXERCÍCIO"`, `"DESCANSO"`, `"DESCANSO LONGO"`
- Botões: `"INICIAR TREINO"`, `"PERSONALIZAR TREINO"`, `"SAIR DO APP"`
- Mensagens: `"Treino Concluído! 🎉"`, `"Erro ao salvar!"`
- Tooltips: `"Voltar"`, `"Remover exercício"`

### Estrutura Sugerida
```python
# i18n.py (novo arquivo)
TRANSLATIONS = {
    "pt_BR": {
        "exercicio": "EXERCÍCIO",
        "descanso": "DESCANSO",
        "iniciar_treino": "INICIAR TREINO",
        # ...
    },
    "en_US": {
        "exercicio": "EXERCISE",
        "descanso": "REST",
        "iniciar_treino": "START WORKOUT",
        # ...
    },
}

def t(key: str, lang: str = "pt_BR") -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["pt_BR"]).get(key, key)
```

---

## 🧪 Testando Mudanças Localmente

### Hot Reload (Desenvolvimento)
```bash
# Terminal 1: Roda o app
python main.py

# Terminal 2: Edita main.py → salva → app recarrega (Flet suporta hot reload)
```

### Lint & Format
```bash
python -m pylint main.py      # Meta: ≥ 9.0/10
black main.py                 # Formatação
isort main.py                 # Imports
```

### Build Test Android
```bash
flet build apk --release
# Teste no device físico (emulador não tem áudio/wake lock confiável)
```

---

## 📦 Estrutura de Assets Personalizada

```
hiit_timer/
├── assets/
│   ├── som_inicio.mp3
│   ├── som_intervalo.mp3
│   ├── som_countdown.mp3
│   ├── som_fim.mp3
│   ├── icon.png           # 512x512 - ícone do app
│   ├── splash.png         # Opcional - splash screen
│   └── fonts/             # Opcional - fontes customizadas
│       └── MinhaFonte.ttf
├── main.py
└── ...
```

### Usar Fonte Customizada
```python
# main()
page.fonts = {"MinhaFonte": "fonts/MinhaFonte.ttf"}
page.theme = ft.Theme(font_family="MinhaFonte", ...)
```

---

## 🔗 Integrações Futuras

### Exportar Treino (JSON Shareable)
```python
def exportar_treino(config: Config) -> str:
    import json, base64
    data = json.dumps(config, ensure_ascii=False).encode("utf-8")
    return base64.urlsafe_b64encode(data).decode("ascii")

def importar_treino(encoded: str) -> Config:
    import json, base64
    data = base64.urlsafe_b64decode(encoded.encode("ascii"))
    return json.loads(data.decode("utf-8"))
```

### Compartilhamento via Share Sheet (Android)
```python
# Requer plugin flet-share ou intent nativo
async def compartilhar(page: ft.Page, config: Config):
    encoded = exportar_treino(config)
    url = f"hiittimer://import?data={encoded}"
    # page.launch_url(url)  # Ou usar share nativo
```

---

## 📋 Checklist de Personalização

- [ ] Sons: 4 arquivos MP3 em `assets/` com nomes corretos
- [ ] Tema: `color_scheme_seed` definido
- [ ] Cores por fase: `CORES` dict ajustado
- [ ] Config padrão: `CONFIG_PADRAO` para seu público
- [ ] Ícone: `assets/icon.png` (512x512)
- [ ] Build: `flet build apk --release` testado no device
- [ ] Lint: `pylint main.py` ≥ 9.0/10

---

*Atualizado: Setembro 2026 (v2.2.1)*