# HIIT Timer

Aplicativo de cronômetro HIIT (High-Intensity Interval Training) desenvolvido com Python 3.12, Flet 0.86.5 e Material Design 3. Build nativo para Android.

## Funcionalidades

- Timer preciso com asyncio
- 4 telas: Configuração, Editor de Exercícios, Cronômetro Ativo, Fim do Treino
- Ring visual gigante com mudança de cor (exercício/descanso)
- Vibração ao trocar de fase
- Beep sonoro nos últimos 3 segundos
- Controles: Pausar, Pular, Voltar
- Tela cheia durante o treino
- Prevenção de sono da tela
- Slider para ajustar ciclos (1-20)
- Tema escuro Material Design 3
- Editor de exercícios personalizáveis

## Instalação

### Pré-requisitos
- Python 3.12+
- Git

### Passos

```bash
# Clonar/entrar no projeto
cd hiit_timer

# Criar e ativar ambiente virtual (Python 3.12)
py -3.12 -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

## Build para Android

```bash
# Com a venv ativada
flet build apk --release
```

O APK será gerado em:
```
build/app/outputs/flutter-apk/app-release.apk
```

### Instalar no dispositivo Android

```bash
# Via ADB (dispositivo conectado via USB)
adb install build/app/outputs/flutter-apk/app-release.apk
```

Ou transfira o APK para o celular e instale manualmente.

## Estrutura do Projeto

```
hiit_timer/
├── main.py                 # Aplicação principal
├── flet_build.yaml         # Configuração de build Android
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
├── workout.py              # Dados do treino e helpers
├── store.py                # Estado global (store)
├── utils/
│   └── helpers.py          # Funções utilitárias
├── components/
│   ├── ring_timer.py       # Ring gigante do cronômetro
│   ├── exercise_row.py     # Linha da lista de exercícios
│   ├── top_stats.py        # Stats no topo (ciclo, tempo, etc)
│   └── controls_bar.py     # Barra de controles (pause, skip)
└── screens/
    ├── config_screen.py    # Tela de configuração/inicial
    ├── timer_screen.py     # Tela do cronômetro ativo
    ├── finish_screen.py    # Tela de fim de treino
    └── exercise_editor_screen.py  # Editor de exercícios
```

## Tecnologias

- Python 3.12
- Flet 0.86.5 (Flutter wrapper)
- Material Design 3
- asyncio para timer assíncrono

## Como Usar

1. Abra o app na tela de **Configuração**
2. Ajuste o número de ciclos (1-20) no slider
3. Opcional: clique em "Editar Exercícios" para personalizar nomes, emojis e durações
4. Clique em **Iniciar Treino**
5. Na tela do **Cronômetro**: use Pausar, Pular ou Voltar conforme necessário
6. Ao finalizar, a tela de **Fim de Treino** mostra o resumo

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

## Licença

MIT License - Sinta-se livre para usar e modificar.