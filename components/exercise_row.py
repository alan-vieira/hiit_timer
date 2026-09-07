"""
Linha da lista de exercícios.
"""

import flet as ft
from workout import Etapa, fmt


def ExerciseRow(etapa: Etapa, indice_atual=None):
    is_atual = indice_atual is not None and etapa.indice == indice_atual
    badge_colors = {
        "exercicio": ft.Colors.PRIMARY_CONTAINER,
        "descanso": ft.Colors.OUTLINE_VARIANT,
        "descanso_ciclo": ft.Colors.SECONDARY_CONTAINER,
    }
    badge_text_colors = {
        "exercicio": ft.Colors.ON_PRIMARY_CONTAINER,
        "descanso": ft.Colors.ON_SURFACE_VARIANT,
        "descanso_ciclo": ft.Colors.ON_SECONDARY_CONTAINER,
    }
    badge_labels = {
        "exercicio": "EXERCÍCIO",
        "descanso": "DESCANSO",
        "descanso_ciclo": "DESCANSO CICLO",
    }
    bg_color = ft.Colors.SURFACE_CONTAINER_HIGHEST if is_atual else ft.Colors.SURFACE
    border_color = ft.Colors.PRIMARY if is_atual else ft.Colors.OUTLINE_VARIANT
    return ft.Container(
        padding=ft.Padding(16, 12, 16, 12),
        margin=ft.Margin(0, 0, 0, 8),
        border_radius=12,
        bgcolor=bg_color,
        border=ft.border.Border(
            left=ft.BorderSide(1, border_color),
            right=ft.BorderSide(1, border_color),
            top=ft.BorderSide(1, border_color),
            bottom=ft.BorderSide(1, border_color)
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Container(content=ft.Text(str(etapa.indice), size=14, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE_VARIANT if not is_atual else ft.Colors.PRIMARY), width=28, alignment=ft.Alignment(0, 0)),
                    ft.Text(etapa.emoji, size=24),
                    ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.START, controls=[
                        ft.Text(etapa.nome, size=16, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                        ft.Text(f"Ciclo {etapa.ciclo}", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                    ]),
                ]),
                ft.Row(spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Container(padding=ft.Padding(10, 4, 10, 4), border_radius=20,
                        bgcolor=badge_colors[etapa.tipo],
                        content=ft.Text(badge_labels[etapa.tipo], size=10, weight=ft.FontWeight.BOLD,
                            color=badge_text_colors[etapa.tipo])),
                    ft.Text(fmt(etapa.duracao), size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE if not is_atual else ft.Colors.PRIMARY, font_family="RobotoMono"),
                ]),
            ],
        ),
    )