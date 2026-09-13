"""HIIT Timer - Cronômetro HIIT simples e funcional (Editor Simplificado)."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, TypedDict

import flet as ft
import flet_audio as fta
from wakepy import keep


# ==================== TIPOS ====================
class Etapa(TypedDict):
    indice: int
    nome: str
    emoji: str
    duracao: int
    tipo: str
    ciclo: int


class Config(TypedDict):
    exercicios: list[dict[str, Any]]
    descanso_curto: int
    descanso_ciclo: int
    num_ciclos: int


class Estado(TypedDict):
    idx: int
    tempo: int
    pausado: bool
    finalizado: bool
    ultimo_segundo_tocado: int
    som_final_tocado: bool


# ==================== CONFIGURAÇÃO ====================
ARQUIVO_DADOS = "dados.json"
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

CORES = {
    "exercicio": ("#9C27B0", "#4A148C", ft.Colors.PRIMARY_CONTAINER, ft.Colors.ON_PRIMARY_CONTAINER, "EXERCÍCIO"),
    "descanso": ("#FF9800", "#E65100", ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SECONDARY_CONTAINER, "DESCANSO"),
    "descanso_ciclo": (
        "#FF9800",
        "#E65100",
        ft.Colors.SECONDARY_CONTAINER,
        ft.Colors.ON_SECONDARY_CONTAINER,
        "DESCANSO LONGO",
    ),
}


# ==================== PERSISTÊNCIA ====================
def get_path() -> Path:
    return Path(__file__).parent.resolve() / ARQUIVO_DADOS


def carregar() -> Config:
    try:
        with get_path().open("r", encoding="utf-8") as f:
            return json.load(f)  # type: ignore
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return CONFIG_PADRAO.copy()


def salvar(dados: Config) -> bool:
    try:
        with get_path().open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


# ==================== HELPERS ====================
def fmt(segundos: int) -> str:
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


def gerar_etapas(config: Config, num_ciclos: int) -> list[Etapa]:
    etapas: list[Etapa] = []
    idx = 0
    for ciclo in range(1, num_ciclos + 1):
        for i, ex in enumerate(config["exercicios"]):
            idx += 1
            etapas.append(
                {
                    "indice": idx,
                    "nome": ex["nome"],
                    "emoji": ex["emoji"],
                    "duracao": ex["duracao"],
                    "tipo": "exercicio",
                    "ciclo": ciclo,
                }
            )
            idx += 1
            if i == len(config["exercicios"]) - 1:
                if ciclo < num_ciclos:
                    etapas.append(
                        {
                            "indice": idx,
                            "nome": "Descanso de ciclo",
                            "emoji": "☕",
                            "duracao": config["descanso_ciclo"],
                            "tipo": "descanso_ciclo",
                            "ciclo": ciclo,
                        }
                    )
            else:
                etapas.append(
                    {
                        "indice": idx,
                        "nome": "Descanso",
                        "emoji": "⏸️",
                        "duracao": config["descanso_curto"],
                        "tipo": "descanso",
                        "ciclo": ciclo,
                    }
                )
    return etapas


def tempo_total(config: Config, num_ciclos: int) -> int:
    return sum(e["duracao"] for e in gerar_etapas(config, num_ciclos))


def navegar(page: ft.Page, tela_func: Any, *args: Any, **kwargs: Any) -> None:
    page.views.clear()
    page.views.append(tela_func(page, *args, **kwargs))
    page.update()


def _stat(label: str, value: str, color: str) -> ft.Column:
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
        controls=[
            ft.Text(label, size=10, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=color),
        ],
    )


def _controls_bar(retroceder: Any, alternar_pausa: Any, pular: Any, pausado: bool) -> ft.Container:
    return ft.Container(
        padding=ft.Padding(16, 16, 16, 16),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.SKIP_PREVIOUS, icon_size=32, tooltip="Anterior", on_click=lambda _: retroceder()
                ),
                ft.FilledButton(
                    "⏸ PAUSAR" if not pausado else "▶ CONTINUAR",
                    icon=ft.Icons.PAUSE if not pausado else ft.Icons.PLAY_ARROW,
                    on_click=lambda _: alternar_pausa(),
                    style=ft.ButtonStyle(
                        padding=ft.Padding(24, 12, 24, 12), shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                ),
                ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_size=32, tooltip="Pular", on_click=lambda _: pular()),
            ],
        ),
    )


# ==================== TIMER CONTROLLER ====================
class TimerController:
    def __init__(self, page: ft.Page, config: Config, num_ciclos: int):
        self.page = page
        self.config = config
        self.num_ciclos = num_ciclos
        self.etapas = gerar_etapas(config, num_ciclos)

        self.estado: Estado = {
            "idx": 0,
            "tempo": self.etapas[0]["duracao"] if self.etapas else 0,
            "pausado": False,
            "finalizado": False,
            "ultimo_segundo_tocado": -1,
            "som_final_tocado": False,
        }

        self._task: Any = None
        self._pause_event = asyncio.Event()
        self._pause_event.set()
        self._wake_lock: Any = None
        self._running = False

        self.txt_nome: ft.Text | None = None
        self.txt_tempo: ft.Text | None = None
        self.ring_progress: ft.ProgressRing | None = None
        self.ring_track: ft.ProgressRing | None = None
        self.txt_badge: ft.Text | None = None
        self.badge_container: ft.Container | None = None
        self.txt_stats: ft.Text | None = None
        self.txt_proximo: ft.Text | None = None
        self._controls_container: ft.Container | None = None

    def bind_ui(
        self,
        txt_nome: ft.Text,
        txt_tempo: ft.Text,
        ring_progress: ft.ProgressRing,
        ring_track: ft.ProgressRing,
        txt_badge: ft.Text,
        badge_container: ft.Container,
        txt_stats: ft.Text,
        txt_proximo: ft.Text,
        controls_container: ft.Container,
    ) -> None:
        self.txt_nome = txt_nome
        self.txt_tempo = txt_tempo
        self.ring_progress = ring_progress
        self.ring_track = ring_track
        self.txt_badge = txt_badge
        self.badge_container = badge_container
        self.txt_stats = txt_stats
        self.txt_proximo = txt_proximo
        self._controls_container = controls_container

    async def start(self) -> None:
        if not self.etapas:
            navegar(self.page, tela_config)
            return

        try:
            self._wake_lock = keep.presenting()
            self._wake_lock.__enter__()
        except Exception as e:
            print(f"⚠️ Wake lock não disponível: {e}")

        self._running = True
        self._task = self.page.run_task(self._timer_loop)

    def stop(self) -> None:
        print("⏹️ Parando timer e limpando recursos...")
        self._running = False
        self._pause_event.set()

        # ✅ Cancela a task do timer
        if self._task is not None:
            try:
                self._task.cancel()
                print("✅ Task do timer cancelada")
            except Exception as e:
                print(f"⚠️ Erro ao cancelar task: {e}")
            self._task = None

        # ✅ Libera o wake lock
        if self._wake_lock is not None:
            try:
                self._wake_lock.__exit__(None, None, None)
                print("✅ Wake lock liberado")
            except Exception as e:
                print(f"⚠️ Erro ao liberar wake lock: {e}")
            self._wake_lock = None

    async def _timer_loop(self) -> None:
        self._update_static_ui()
        self._refresh_ui()

        while self._running and self.estado["idx"] < len(self.etapas) and not self.estado["finalizado"]:
            await self._pause_event.wait()
            if not self._running:
                break

            await asyncio.sleep(1)
            if not self._running:
                break

            self.estado["tempo"] -= 1
            tempo_atual = self.estado["tempo"]

            if tempo_atual in [3, 2, 1] and self.estado["ultimo_segundo_tocado"] != tempo_atual:
                self.estado["ultimo_segundo_tocado"] = tempo_atual
                self.page.run_task(self._tocar_som_com_timeout, self.page.som_countdown, 1.0)

            if tempo_atual <= 0:
                await self._avancar()
            else:
                self._refresh_ui()

        if self._running and self.estado["idx"] >= len(self.etapas) and not self.estado["finalizado"]:
            self.estado["finalizado"] = True
            await self._on_finalizar()

    async def _avancar(self) -> None:
        try:
            self.page.haptic_feedback()
        except Exception:
            pass

        self.estado["ultimo_segundo_tocado"] = -1
        if self.estado["idx"] + 1 < len(self.etapas):
            self.estado["idx"] += 1
            self.estado["tempo"] = self.etapas[self.estado["idx"]]["duracao"]
            self.page.run_task(self._tocar_som, self.etapas[self.estado["idx"]]["tipo"])
            self._update_static_ui()
            self._refresh_ui()
        else:
            self.estado["finalizado"] = True
            await self._on_finalizar()

    def retroceder(self) -> None:
        self.estado["ultimo_segundo_tocado"] = -1
        if self.estado["idx"] > 0:
            self.estado["idx"] -= 1
            self.estado["tempo"] = self.etapas[self.estado["idx"]]["duracao"]
            self._update_static_ui()
            self._refresh_ui()
        else:
            self.parar_e_voltar()

    def pular(self) -> None:
        self.estado["ultimo_segundo_tocado"] = -1
        if self.estado["idx"] + 1 < len(self.etapas):
            self.estado["idx"] += 1
            self.estado["tempo"] = self.etapas[self.estado["idx"]]["duracao"]
            self.page.run_task(self._tocar_som, self.etapas[self.estado["idx"]]["tipo"])
            self._update_static_ui()
            self._refresh_ui()

    def alternar_pausa(self) -> None:
        self.estado["pausado"] = not self.estado["pausado"]
        if self.estado["pausado"]:
            self._pause_event.clear()
        else:
            self._pause_event.set()
        self._update_static_ui()

    def parar_e_voltar(self, e: Any = None) -> None:
        self.stop()
        navegar(self.page, tela_config)

    async def _on_finalizar(self) -> None:
        if self.estado["som_final_tocado"]:
            return
        self.estado["som_final_tocado"] = True
        await self._tocar_som_com_timeout(self.page.som_fim, 2.0)
        self.stop()
        navegar(self.page, tela_finish, tempo_total(self.config, self.num_ciclos), self.num_ciclos)

    async def _tocar_som(self, tipo_etapa: str) -> None:
        try:
            if tipo_etapa == "exercicio":
                await self._tocar_som_com_timeout(self.page.som_inicio)
            elif tipo_etapa in ["descanso", "descanso_ciclo"]:
                await self._tocar_som_com_timeout(self.page.som_intervalo)
        except Exception as e:
            print(f"Erro ao tocar som: {e}")

    async def _tocar_som_com_timeout(self, audio_obj: Any, timeout: float = 2.0) -> None:
        try:
            await asyncio.wait_for(audio_obj.play(), timeout=timeout)
        except TimeoutError:
            print("⚠️ Timeout ao tocar som (ignorado)")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"⚠️ Erro ao tocar som: {e}")

    def _update_static_ui(self) -> None:
        if not self.txt_badge or not self._controls_container:
            return
        idx = self.estado["idx"]
        if idx >= len(self.etapas):
            return
        ep = self.etapas[idx]
        prox = self.etapas[idx + 1] if idx + 1 < len(self.etapas) else None
        _, _, badge_bg, badge_fg, badge_label = CORES.get(ep["tipo"], CORES["exercicio"])

        self.txt_badge.value = badge_label
        self.txt_badge.color = badge_fg
        self.badge_container.bgcolor = badge_bg

        ciclo_atual = ep["ciclo"]
        total_ciclos = max((e["ciclo"] for e in self.etapas), default=1)
        self.txt_stats.value = f"Ciclo {ciclo_atual}/{total_ciclos} • Etapa {idx + 1}/{len(self.etapas)}"
        self.txt_proximo.value = f"Próximo: {prox['emoji']} {prox['nome']}" if prox else "Última etapa!"

        self._controls_container.content = _controls_bar(
            self.retroceder, self.alternar_pausa, self.pular, self.estado["pausado"]
        )

        self.txt_badge.update()
        self.badge_container.update()
        self.txt_stats.update()
        self.txt_proximo.update()
        self._controls_container.update()

    def _refresh_ui(self) -> None:
        if not self.txt_tempo or not self.ring_progress:
            return
        idx = self.estado["idx"]
        tempo = self.estado["tempo"]
        if idx >= len(self.etapas):
            return
        ep = self.etapas[idx]
        cr, cf, _, _, _ = CORES.get(ep["tipo"], CORES["exercicio"])

        self.ring_progress.color = cr
        self.ring_track.color = cf
        progresso = max(0.0, min(1.0, 1.0 - (tempo / ep["duracao"]))) if ep["duracao"] > 0 else 0.0
        self.ring_progress.value = progresso

        self.txt_nome.value = f"{ep['emoji']} {ep['nome']}"
        self.txt_tempo.value = fmt(tempo)

        self.txt_tempo.update()
        self.ring_progress.update()


# ==================== TELAS ====================
def tela_config(page: ft.Page) -> ft.View:
    config = carregar()
    num_ciclos = config["num_ciclos"]
    etapas = gerar_etapas(config, num_ciclos)
    tempo = tempo_total(config, num_ciclos)

    def iniciar_treino(_: Any) -> None:
        navegar(page, tela_timer, config, num_ciclos)

    def abrir_editor(_: Any) -> None:
        navegar(page, tela_editor)

    # ✅ NOVO: Botão para sair do app (Android)
    def sair_do_app(_: Any) -> None:
        print("🚪 Usuário clicou em sair")
        # Para qualquer timer ativo
        if hasattr(page, "timer_controller") and page.timer_controller:
            page.timer_controller.stop()

        # Força o fechamento
        sys.exit(0)

    linhas_etapas = []
    for ep in etapas[:10]:
        cor = ft.Colors.PRIMARY if ep["tipo"] == "exercicio" else ft.Colors.ON_SURFACE_VARIANT
        linhas_etapas.append(
            ft.Row(
                [
                    ft.Text(ep["emoji"], size=18),
                    ft.Text(ep["nome"], size=14, color=cor, expand=True),
                    ft.Text(fmt(ep["duracao"]), size=14, weight=ft.FontWeight.BOLD, color=cor),
                ]
            )
        )
    if len(etapas) > 10:
        linhas_etapas.append(
            ft.Text(
                f"... e mais {len(etapas) - 10} etapas",
                size=12,
                color=ft.Colors.ON_SURFACE_VARIANT,
                italic=True,
            )
        )

    return ft.View(
        route="/config",
        bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(
            title=ft.Text("HIIT Timer", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.PRIMARY,
        ),
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=24,
                            margin=ft.Margin(16, 16, 16, 8),
                            border_radius=16,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            content=ft.Column(
                                spacing=16,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            _stat("CICLOS", str(num_ciclos), ft.Colors.PRIMARY),
                                            _stat("EXERCÍCIOS", str(len(config["exercicios"])), ft.Colors.SECONDARY),
                                            _stat("ETAPAS", str(len(etapas)), ft.Colors.TERTIARY),
                                            _stat("TEMPO", fmt(tempo), ft.Colors.PRIMARY),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=16,
                            margin=ft.Margin(16, 8, 16, 8),
                            border_radius=16,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        "PREVIEW DO TREINO",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.ON_SURFACE_VARIANT,
                                    ),
                                    ft.Column(linhas_etapas, spacing=4),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=ft.Padding(16, 16, 16, 16),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.FilledButton(
                                        "▶ INICIAR TREINO",
                                        icon=ft.Icons.PLAY_ARROW,
                                        on_click=iniciar_treino,
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)
                                        ),
                                        expand=True,
                                    ),
                                    ft.OutlinedButton(
                                        "⚙ PERSONALIZAR TREINO",
                                        icon=ft.Icons.EDIT,
                                        on_click=abrir_editor,
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)
                                        ),
                                        expand=True,
                                    ),
                                    # ✅ NOVO: Botão de sair adicionado aqui
                                    ft.TextButton(
                                        "🚪 SAIR DO APP",
                                        on_click=sair_do_app,
                                        style=ft.ButtonStyle(color=ft.Colors.ERROR),
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            )
        ],
    )


def tela_editor(page: ft.Page) -> ft.View:
    """Editor simplificado usando Column com scroll."""
    config = carregar()

    exercicios = [ex.copy() for ex in config["exercicios"]]

    tf_curto = ft.TextField(
        value=str(config["descanso_curto"]),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=100,
        text_align=ft.TextAlign.CENTER,
    )
    tf_ciclo = ft.TextField(
        value=str(config["descanso_ciclo"]),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=100,
        text_align=ft.TextAlign.CENTER,
    )
    tf_ciclos = ft.TextField(
        value=str(config["num_ciclos"]), keyboard_type=ft.KeyboardType.NUMBER, width=100, text_align=ft.TextAlign.CENTER
    )

    lista_column = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)

    def build_item(idx: int) -> ft.Card:
        """Constrói um card de exercício."""
        ex = exercicios[idx]

        tf_emoji = ft.TextField(value=ex["emoji"], width=60, text_align=ft.TextAlign.CENTER)
        tf_nome = ft.TextField(value=ex["nome"], dense=True, expand=True)
        tf_dur = ft.TextField(
            value=str(ex["duracao"]), width=80, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER
        )

        btn_del = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.ERROR,
            disabled=len(exercicios) <= 1,
            tooltip="Remover exercício",
        )

        def on_emoji(e):
            exercicios[idx]["emoji"] = e.control.value or "🏃"

        def on_nome(e):
            exercicios[idx]["nome"] = e.control.value or "Exercício"

        def on_dur(e):
            try:
                exercicios[idx]["duracao"] = max(1, int(e.control.value) if e.control.value else 30)
            except ValueError:
                exercicios[idx]["duracao"] = 30

        # ✅ EXCLUSÃO DIRETA SEM DIÁLOGO (mais simples e confiável)
        def on_del(e):
            exercicios.pop(idx)
            rebuild()

        tf_emoji.on_change = on_emoji
        tf_nome.on_change = on_nome
        tf_dur.on_change = on_dur
        btn_del.on_click = on_del

        return ft.Card(
            content=ft.Container(
                padding=12,
                content=ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[tf_emoji, tf_nome, tf_dur, btn_del]
                ),
            )
        )

    def rebuild():
        """Reconstrói toda a lista."""
        lista_column.controls.clear()
        for i in range(len(exercicios)):
            lista_column.controls.append(build_item(i))
        page.update()

    def add_exercicio(e):
        exercicios.append({"nome": "Novo Exercício", "emoji": "🏃", "duracao": 45})
        rebuild()

    def salvar_tudo(e):
        try:
            novo_config: Config = {
                "exercicios": exercicios,
                "descanso_curto": max(1, int(tf_curto.value) if tf_curto.value else 30),
                "descanso_ciclo": max(1, int(tf_ciclo.value) if tf_ciclo.value else 60),
                "num_ciclos": max(1, min(20, int(tf_ciclos.value) if tf_ciclos.value else 3)),
            }
            if salvar(novo_config):
                navegar(page, tela_config)
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("Erro ao salvar!"), bgcolor=ft.Colors.ERROR)
                page.snack_bar.open = True
                page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Valores inválidos!"), bgcolor=ft.Colors.ERROR)
            page.snack_bar.open = True
            page.update()

    def cancelar(e):
        navegar(page, tela_config)

    # Popula a lista inicialmente
    for i in range(len(exercicios)):
        lista_column.controls.append(build_item(i))

    return ft.View(
        route="/editor",
        bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(
            title=ft.Text("Personalizar Treino", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.SURFACE,
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=cancelar),
        ),
        controls=[
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=16,
                        margin=ft.Margin(16, 16, 16, 8),
                        border_radius=12,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        content=ft.Column(
                            spacing=12,
                            controls=[
                                ft.Text(
                                    "INTERVALOS E CICLOS",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        ft.Column([ft.Text("Curto (s)", size=12), tf_curto]),
                                        ft.Column([ft.Text("Longo (s)", size=12), tf_ciclo]),
                                        ft.Column([ft.Text("Ciclos", size=12), tf_ciclos]),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.Padding(16, 0, 16, 0),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "EXERCÍCIOS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT
                                ),
                                ft.TextButton("ADICIONAR", icon=ft.Icons.ADD, on_click=add_exercicio),
                            ],
                        ),
                    ),
                    ft.Container(expand=True, padding=ft.Padding(16, 0, 16, 0), content=lista_column),
                    ft.Container(
                        padding=16,
                        bgcolor=ft.Colors.SURFACE,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            spacing=12,
                            controls=[
                                ft.TextButton("CANCELAR", on_click=cancelar),
                                ft.FilledButton("SALVAR", icon=ft.Icons.CHECK, on_click=salvar_tudo),
                            ],
                        ),
                    ),
                ],
            )
        ],
    )


def tela_timer(page: ft.Page, config: Config, num_ciclos: int) -> ft.View:
    controller = TimerController(page, config, num_ciclos)
    page.timer_controller = controller

    txt_nome = ft.Text(
        "", size=22, weight=ft.FontWeight.W_600, color=ft.Colors.ON_SURFACE, text_align=ft.TextAlign.CENTER, max_lines=2
    )
    txt_tempo = ft.Text("", size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, font_family="RobotoMono")
    ring_progress = ft.ProgressRing(value=0.0, width=260, height=260, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    ring_track = ft.ProgressRing(value=1.0, width=260, height=260, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    txt_badge = ft.Text("", size=12, weight=ft.FontWeight.BOLD)
    badge_container = ft.Container(
        padding=ft.Padding(16, 6, 16, 6), margin=ft.Margin(0, 0, 0, 16), border_radius=20, content=txt_badge
    )
    txt_stats = ft.Text("", size=12, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER)
    txt_proximo = ft.Text("", size=14, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER)
    controls_container = ft.Container()

    ring_stack = ft.Stack(
        width=260,
        height=260,
        controls=[
            ring_track,
            ring_progress,
            ft.Container(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[txt_nome, txt_tempo]
                ),
                alignment=ft.Alignment(0, 0),
                width=260,
                height=260,
            ),
        ],
    )
    ring_area = ft.Container(
        content=ring_stack, alignment=ft.Alignment(0, 0), expand=True, padding=ft.Padding(24, 16, 24, 16)
    )

    controller.bind_ui(
        txt_nome,
        txt_tempo,
        ring_progress,
        ring_track,
        txt_badge,
        badge_container,
        txt_stats,
        txt_proximo,
        controls_container,
    )

    page.run_task(controller.start)

    return ft.View(
        route="/timer",
        bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(
            title=ft.Text("Treino em Andamento", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.SURFACE,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK, tooltip="Cancelar treino", on_click=controller.parar_e_voltar
            ),
        ),
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[txt_stats, badge_container, ring_area, txt_proximo, controls_container],
                )
            )
        ],
    )


def tela_finish(page: ft.Page, tempo_total_seg: int, num_ciclos: int) -> ft.View:
    tempo_fmt = fmt(tempo_total_seg)

    def repetir(_: Any) -> None:
        config = carregar()
        navegar(page, tela_timer, config, config["num_ciclos"])

    def configurar(_: Any) -> None:
        navegar(page, tela_config)

    return ft.View(
        route="/finish",
        bgcolor=ft.Colors.SURFACE,
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    padding=32,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=24,
                        controls=[
                            ft.Container(
                                padding=24,
                                border_radius=60,
                                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                                content=ft.Icon(ft.Icons.EMOJI_EVENTS, size=64, color=ft.Colors.ON_SECONDARY_CONTAINER),
                            ),
                            ft.Text(
                                "Treino Concluído! 🎉",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ON_SURFACE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                f"Você completou {num_ciclos} ciclo{'s' if num_ciclos > 1 else ''} em {tempo_fmt}",
                                size=16,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(
                                padding=ft.Padding(16, 16, 16, 16),
                                border_radius=16,
                                bgcolor=ft.Colors.SURFACE_CONTAINER,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        _stat("TEMPO", tempo_fmt, ft.Colors.PRIMARY),
                                        _stat("CICLOS", str(num_ciclos), ft.Colors.SECONDARY),
                                        _stat("STATUS", "✅ OK", ft.Colors.TERTIARY),
                                    ],
                                ),
                            ),
                            ft.Column(
                                spacing=12,
                                width=300,
                                controls=[
                                    ft.FilledButton(
                                        "🔁 REPETIR TREINO",
                                        on_click=repetir,
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)
                                        ),
                                        expand=True,
                                    ),
                                    ft.OutlinedButton(
                                        "⚙ VOLTAR À CONFIGURAÇÃO",
                                        on_click=configurar,
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)
                                        ),
                                        expand=True,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        ],
    )


# ==================== ENTRY POINT ====================
async def main(page: ft.Page) -> None:
    page.title = "HIIT Timer"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="#9C27B0", use_material3=True)

    # ✅ 1. Registrar os audios ANTES de qualquer view
    som_inicio = fta.Audio(src="som_inicio.mp3", autoplay=False, volume=0.8)
    som_intervalo = fta.Audio(src="som_intervalo.mp3", autoplay=False, volume=0.8)
    som_countdown = fta.Audio(src="som_countdown.mp3", autoplay=False, volume=0.6)
    som_fim = fta.Audio(src="som_fim.mp3", autoplay=False, volume=1.0)

    page.services.extend([som_inicio, som_intervalo, som_countdown, som_fim])
    page.som_inicio = som_inicio
    page.som_intervalo = som_intervalo
    page.som_countdown = som_countdown
    page.som_fim = som_fim

    # ✅ 2. Handler do back button (único evento confiável no Android)
    def on_view_pop(e: ft.ViewPopEvent) -> None:
        print(f"🔙 Back button pressionado na rota: {page.route}")
        if page.route in ["/timer", "/editor", "/finish"]:
            if hasattr(page, "timer_controller") and page.timer_controller:
                print("⏹️ Parando timer antes de voltar...")
                page.timer_controller.stop()
            navegar(page, tela_config)
            e.prevent_default = True
        else:
            e.prevent_default = False

    page.on_view_pop = on_view_pop

    # ✅ 3. Handler para quando a rota muda (detecta fechamento indireto)
    def on_route_change(e: ft.RouteChangeEvent) -> None:
        print(f"🔄 Rota mudou para: {e.route}")
        # Se voltar para a raiz e o timer estava rodando, para ele
        if e.route == "/config" and hasattr(page, "timer_controller") and page.timer_controller:
            if page.timer_controller._running:
                print("⏹️ Timer estava rodando, parando...")
                page.timer_controller.stop()

    page.on_route_change = on_route_change

    # ✅ 4. Só agora monta a primeira view
    navegar(page, tela_config)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
