"""
Tela de Configuração.
"""

import flet as ft
from workout import gerar_etapas, stats_treino
from components.exercise_row import ExerciseRow
from components.controls_bar import BotaoPrincipal
from store import store


def ConfigScreen(page: ft.Page, on_iniciar, num_ciclos_inicial=3, on_navegar_editor=None):
    estado = {"ciclos": num_ciclos_inicial}

    txt_ciclos_valor = ft.Text(str(estado["ciclos"]), size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY)
    txt_footer = ft.Text("", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER)
    lv_etapas = ft.ListView(spacing=0, padding=ft.Padding(0, 0, 0, 100))
    chips_container = ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND)

    def rebuild():
        nc = estado["ciclos"]
        etapas = gerar_etapas(store.config, nc)
        stats = stats_treino(store.config, nc)
        txt_ciclos_valor.value = str(nc)
        txt_footer.value = f"Repetir x{nc} \u2022 {len(store.config.exercicios)} exerc\u00edcios"
        chips_container.controls = [
            _StatChip("CICLOS", str(nc), ft.Colors.PRIMARY),
            _StatChip("TEMPO", stats["tempo_total_fmt"], ft.Colors.SECONDARY),
            _StatChip("ETAPAS", str(stats["total_etapas"]), ft.Colors.TERTIARY),
        ]
        lv_etapas.controls = [ExerciseRow(etapa=ep) for ep in etapas]
        page.update()

    def ao_mudar_ciclos(e):
        estado["ciclos"] = int(e.control.value)
        rebuild()

    def ao_clicar_iniciar():
        on_iniciar(estado["ciclos"])

    def ao_clicar_editor():
        if on_navegar_editor:
            on_navegar_editor()

    rebuild()

    return ft.View(
        route="/config",
        appbar=ft.AppBar(
            title=ft.Text("Meu Treino HIIT", weight=ft.FontWeight.BOLD),
            center_title=True, bgcolor=ft.Colors.SURFACE,
            actions=[ft.IconButton(icon=ft.Icons.EDIT, tooltip="Personalizar", on_click=lambda _: ao_clicar_editor())],
        ),
        bgcolor=ft.Colors.SURFACE,
        controls=[
            ft.Container(padding=ft.Padding(16, 12, 16, 12), content=chips_container),
            ft.Container(padding=ft.Padding(16, 8, 16, 8), content=ft.Column(spacing=8, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("N\u00daMERO DE CICLOS", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT),
                    txt_ciclos_valor,
                ]),
                ft.Slider(value=estado["ciclos"], min=1, max=10, divisions=9, label="{value}",
                    on_change=ao_mudar_ciclos, active_color=ft.Colors.PRIMARY, inactive_color=ft.Colors.OUTLINE_VARIANT),
            ])),
            ft.Container(padding=ft.Padding(8, 0, 8, 0), expand=True, content=lv_etapas),
            ft.Container(padding=ft.Padding(16, 16, 16, 16), bgcolor=ft.Colors.SURFACE,
                border=ft.border.Border(
                    top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                    right=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                    bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                    left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
                ),
                content=ft.Column(spacing=8, controls=[
                    txt_footer,
                    BotaoPrincipal(texto="INICIAR", icone=ft.Icons.PLAY_ARROW, on_click=ao_clicar_iniciar, expandir=True, cor_fundo=ft.Colors.SECONDARY_CONTAINER),
                ])),
        ],
    )


def _StatChip(label, value, color):
    return ft.Container(
        padding=ft.padding.Padding.symmetric(horizontal=16, vertical=8), border_radius=20,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border=ft.border.Border(
            left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            right=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
        ),
        content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2, controls=[
            ft.Text(label, size=10, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT, ),
            ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=color, font_family="RobotoMono"),
        ]),
    )