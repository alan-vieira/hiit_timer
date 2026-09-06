"""
Barra de controles e botão principal.
"""

import flet as ft


def ControlsBar(on_voltar, on_pausar, on_pular, esta_pausado=False, desabilitado=False):
    return ft.Container(
        padding=ft.padding.Padding.symmetric(horizontal=24, vertical=16),
        content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, controls=[
            ft.IconButton(icon=ft.Icons.REPLAY_10, icon_size=28, tooltip="Voltar",
                on_click=lambda _: on_voltar() if not desabilitado else None, disabled=desabilitado,
                style=ft.ButtonStyle(
                    color={ft.ControlState.DISABLED: ft.Colors.ON_SURFACE_VARIANT, ft.ControlState.DEFAULT: ft.Colors.ON_SURFACE},
                    bgcolor={ft.ControlState.DISABLED: ft.Colors.SURFACE_CONTAINER_HIGHEST, ft.ControlState.DEFAULT: ft.Colors.SURFACE_CONTAINER},
                    shape=ft.CircleBorder(), padding=16)),
            ft.IconButton(
                icon=ft.Icons.PLAY_ARROW if esta_pausado else ft.Icons.PAUSE, icon_size=32,
                tooltip="Continuar" if esta_pausado else "Pausar",
                on_click=lambda _: on_pausar() if not desabilitado else None, disabled=desabilitado,
                style=ft.ButtonStyle(
                    color=ft.Colors.ON_SECONDARY_CONTAINER,
                    bgcolor={ft.ControlState.DISABLED: ft.Colors.OUTLINE_VARIANT, ft.ControlState.DEFAULT: ft.Colors.SECONDARY_CONTAINER},
                    shape=ft.CircleBorder(), padding=20)),
            ft.IconButton(icon=ft.Icons.FORWARD_10, icon_size=28, tooltip="Pular",
                on_click=lambda _: on_pular() if not desabilitado else None, disabled=desabilitado,
                style=ft.ButtonStyle(
                    color={ft.ControlState.DISABLED: ft.Colors.ON_SURFACE_VARIANT, ft.ControlState.DEFAULT: ft.Colors.ON_SURFACE},
                    bgcolor={ft.ControlState.DISABLED: ft.Colors.SURFACE_CONTAINER_HIGHEST, ft.ControlState.DEFAULT: ft.Colors.SURFACE_CONTAINER},
                    shape=ft.CircleBorder(), padding=16)),
        ]),
    )


def BotaoPrincipal(texto, on_click, icone=None, desabilitado=False, expandir=False, cor_fundo=None):
    return ft.Container(
        expand=expandir,
        content=ft.FilledButton(
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
                ft.Icon(icone, size=20) if icone else ft.Container(),
                ft.Text(texto, size=16, weight=ft.FontWeight.BOLD),
            ]),
            on_click=lambda _: on_click() if not desabilitado else None,
            disabled=desabilitado,
            style=ft.ButtonStyle(
                padding=ft.padding.Padding.symmetric(horizontal=32, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=16),
                bgcolor=cor_fundo or ft.Colors.SECONDARY_CONTAINER,
                color=ft.Colors.ON_SECONDARY_CONTAINER),
        ),
    )