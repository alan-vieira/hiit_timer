"""
Stats no topo da tela do timer.
"""

import flet as ft


def _StatColumn(label, value, accent_color):
    return ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2, controls=[
        ft.Text(label, size=11, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT, ),
        ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=accent_color, font_family="RobotoMono"),
    ])


def TopStats(tempo_total_fmt, ciclo_atual, total_ciclos, etapa_atual, total_etapas, tempo_restante_fmt):
    return ft.Container(
        padding=ft.Padding(16, 12, 16, 12),
        margin=ft.Margin(0, 0, 0, 8),
        border_radius=12,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border=ft.border.Border(
            left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            right=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
        ),
        content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
            _StatColumn("TEMPO TOTAL", tempo_total_fmt, ft.Colors.PRIMARY),
            _StatColumn("CICLO", f"{ciclo_atual} / {total_ciclos}", ft.Colors.SECONDARY),
            _StatColumn("RESTANTE", tempo_restante_fmt, ft.Colors.TERTIARY),
        ]),
    )


def ProximoExercicioBanner(proximo_nome, proximo_emoji, proximo_tipo):
    tipo_cores = {"exercicio": ft.Colors.PRIMARY, "descanso": ft.Colors.OUTLINE, "descanso_ciclo": ft.Colors.SECONDARY}
    cor = tipo_cores.get(proximo_tipo, ft.Colors.ON_SURFACE_VARIANT)
    return ft.Container(
        padding=ft.Padding(16, 8, 16, 8),
        margin=ft.Margin(0, 0, 0, 16),
        border_radius=8,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border=ft.border.Border(
            left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            right=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
        ),
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
            ft.Icon(ft.Icons.ARROW_FORWARD, size=18, color=cor),
            ft.Text("PRÓXIMO:", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT, ),
            ft.Text(f"{proximo_emoji} {proximo_nome}", size=16, weight=ft.FontWeight.BOLD, color=cor),
        ]),
    )