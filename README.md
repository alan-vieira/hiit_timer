# HIIT Timer

Aplicativo de cronômetro para treinos HIIT (High-Intensity Interval Training) desenvolvido em Python 3.12 com Flet (Material Design 3) e compilado nativamente para Android.

## Visão Geral
Ferramenta personalizada para gerenciamento de treinos intervalados, permitindo configuração granular de exercícios, durações e ciclos de descanso. O aplicativo prioriza precisão no timing, feedback sensorial (vibração/áudio) e prevenção de suspensão da tela durante a execução.

## Funcionalidades Técnicas
- **Motor de Tempo**: Cronômetro assíncrono (`asyncio`) com precisão de segundo a segundo.
- **Gerenciamento de Estado**: Store centralizado para controle de ciclos, fases (exercício/intervalo) e configurações.
- **Feedback do Sistema**: Vibração (haptic feedback) nas transições de fase e alerta sonoro (beep) nos últimos 3 segundos.
- **UX/Otimização**: Modo tela cheia (fullscreen), prevenção de bloqueio de tela (wake lock) e interface adaptativa com tema escuro Material Design 3.
- **Configuração**: Editor integrado para personalizar até 20 ciclos, com durações independentes.

## Estrutura do Projeto
```text
hiit_timer/
├── screens/ # Camada de apresentação (UI)
│ ├── config_screen.py # Tela de configuração inicial
│ ├── exercise_editor_screen.py # Editor de parâmetros do treino
│ ├── timer_screen.py # Tela principal do cronômetro (ring visual)
│ └── finish_screen.py # Tela de resumo/fim do treino
├── components/ # Componentes de UI reutilizáveis
├── utils/ # Funções auxiliares (helpers de formatação e async)
├── main.py # Ponto de entrada e inicialização do app Flet
├── workout.py # Lógica de negócio e orquestração do treino
├── store.py # Gerenciamento de estado global
├── flet_build.yaml # Configurações de build para Android
└── requirements.txt # Dependências do projeto
```

## Setup e Execução Local

### Pré-requisitos
- Python 3.12+
- Git

### Instalação

```bash
cd hiit_timer
python -m venv venv
venv\Scripts\activate # Windows (use 'source venv/bin/activate' no Linux/macOS)
pip install -r requirements.txt
python main.py
```

## Build para Android
Para gerar o pacote de instalação (.apk):

```bash
flet build apk --release
```

Saída: O arquivo será gerado em `build/app/outputs/flutter-apk/app-release.apk`.

---

*Documento de referência técnica. Última atualização: Setembro 2026.*