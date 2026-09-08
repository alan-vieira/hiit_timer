"""
Ring timer circular gigante.
"""

import flet as ft


def RingTimer(progresso, cor_ring, cor_fundo_ring, tamanho=280, espessura=12, texto_centro="", subtexto_centro=""):
    progresso = max(0.0, min(1.0, progresso))
    ring_stack = ft.Stack(width=tamanho, height=tamanho, controls=[
        ft.ProgressRing(value=1.0, width=tamanho, height=tamanho, stroke_width=espessura, color=cor_fundo_ring, bgcolor=ft.Colors.TRANSPARENT),
        ft.ProgressRing(value=progresso, width=tamanho, height=tamanho, stroke_width=espessura, color=cor_ring, bgcolor=ft.Colors.TRANSPARENT),
    ])
    centro = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
        ft.Text(texto_centro, size=22, weight=ft.FontWeight.W_600, color=ft.Colors.ON_SURFACE,
            text_align=ft.TextAlign.CENTER, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
        ft.Text(subtexto_centro, size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE,
            font_family="RobotoMono") if subtexto_centro else ft.Container(),
    ])
    return ft.Container(
        content=ft.Stack(width=tamanho, height=tamanho, controls=[
            ring_stack,
            ft.Container(content=centro, alignment=ft.Alignment(0, 0), width=tamanho, height=tamanho),
        ]),
        alignment=ft.Alignment(0, 0),
    )