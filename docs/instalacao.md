# 📥 Guia de Instalação — HIIT Timer

> **Versão:** v2.2.1 · **Requisitos:** Python 3.12+, Flet 0.86+

---

## 🖥️ Windows

### 1. Pré-requisitos
- **Python 3.12+** — [Download](https://www.python.org/downloads/) (marque "Add Python to PATH")
- **Git** — [Download](https://git-scm.com/download/win) (opcional, para clonar o repo)

### 2. Clonar e configurar
```bash
# Abra o PowerShell ou CMD
git clone https://github.com/alan-vieira/hiit_timer.git
cd hiit_timer

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Executar
```bash
python main.py
```

### 4. Build APK (Android)
```bash
# Requer: JDK 17+, Android SDK (via Android Studio)
flet build apk --release
# APK em: build/app/outputs/flutter-apk/app-release.apk
```

---

## 🐧 Linux (Ubuntu/Debian/Fedora/Arch)

### 1. Pré-requisitos
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3.12 python3.12-venv git

# Fedora
sudo dnf install python3.12 python3.12-venv git

# Arch
sudo pacman -S python python-virtualenv git
```

### 2. Clonar e configurar
```bash
git clone https://github.com/alan-vieira/hiit_timer.git
cd hiit_timer

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Executar
```bash
python main.py
```

### 4. Build APK
```bash
# Instalar Android Studio + SDK + JDK 17
# Configurar ANDROID_HOME no ~/.bashrc:
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

flet build apk --release
```

---

## 🍎 macOS

### 1. Pré-requisitos
```bash
# Via Homebrew (recomendado)
brew install python@3.12 git

# Ou baixe do python.org
```

### 2. Clonar e configurar
```bash
git clone https://github.com/alan-vieira/hiit_timer.git
cd hiit_timer

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Executar
```bash
python main.py
```

### 4. Build APK
```bash
# Instalar Android Studio + SDK + JDK 17
# Configurar ANDROID_HOME no ~/.zshrc:
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

flet build apk --release
```

> ⚠️ **Nota:** Build para iOS (`flet build ipa`) requer macOS + Xcode + conta Apple Developer. Ainda não testado neste projeto.

---

## 📱 Android (Instalação do APK)

### Opção 1: Build Local (Desenvolvedor)
```bash
# No seu PC (Windows/Linux/macOS)
flet build apk --release
# Copie o APK para o celular via USB/ADB/Cloud
# Instale no Android (habilite "Fontes desconhecidas")
```

### Opção 2: Download Direto (Usuário Final)
1. Acesse a página de **Releases** no GitHub
2. Baixe `app-release.apk` da versão mais recente
3. Transfira para o celular e instale

### Permissões Necessárias
O app solicita automaticamente:
- **WAKE_LOCK** — Manter tela ligada durante treino
- **INTERNET** — Necessário para o Flet (mesmo offline)
- **VIBRATE** — Feedback háptico nas transições

---

## 🐳 Docker (Opcional)

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
docker build -t hiit-timer .
docker run --rm -it hiit-timer
```

---

## ✅ Verificação Pós-Instalação

Ao executar `python main.py`, você deve ver:
1. Janela aberta com tema escuro roxo
2. Tela "HIIT Timer" com estatísticas do treino padrão
3. Botões: **INICIAR TREINO**, **PERSONALIZAR TREINO**, **🚪 SAIR DO APP**
4. Console sem erros de áudio (`flet_audio` carregado)

### Problemas Comuns

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError: flet` | `pip install -r requirements.txt` no venv ativo |
| `flet_audio` não carrega | Verifique se `assets/` tem os 4 arquivos `.mp3` |
| Build APK falha | Instale Android Studio, aceite licenças SDK, configure `ANDROID_HOME` |
| Tela preta no Android | Use `flet build apk --release` (não debug) |

---

## 🔗 Links Úteis

- [Flet Documentation](https://flet.dev/docs/)
- [Flet Build Android](https://flet.dev/docs/publish/android/)
- [Python venv Guide](https://docs.python.org/3/library/venv.html)
- [Android SDK Setup](https://developer.android.com/studio)

---

*Atualizado: Setembro 2026 (v2.2.1)*