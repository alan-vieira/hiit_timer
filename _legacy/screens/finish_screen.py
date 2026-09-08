"""Tela de Fim de Treino."""
import flet as ft
from workout import fmt

def FinishScreen(page: ft.Page, tempo_total_seg: int, num_ciclos: int, on_repetir, on_configurar):
    tempo_fmt = fmt(tempo_total_seg)
    
    # Liberar wake lock ao finalizar o treino
    try:
        if hasattr(page, 'keep_screen_on'):
            page.keep_screen_on = False
    except Exception:
        pass

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
                                border=ft.Border(
                                    left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                                    right=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                                    top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                                    bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                                ),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        _FS("TEMPO TOTAL", tempo_fmt, ft.Colors.PRIMARY),
                                        _FS("CICLOS", str(num_ciclos), ft.Colors.SECONDARY),
                                        _FS("STATUS", "✅ CONCLUÍDO", ft.Colors.TERTIARY),
                                    ],
                                ),
                            ),
                            ft.Column(
                                spacing=12,
                                width=300,
                                controls=[
                                    ft.FilledButton(
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=8,
                                            controls=[
                                                ft.Icon(ft.Icons.REPLAY, size=20),
                                                ft.Text("REPETIR TREINO", size=16, weight=ft.FontWeight.BOLD),
                                            ],
                                        ),
                                        on_click=lambda _: on_repetir(),
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 16, 0, 16),
                                            shape=ft.RoundedRectangleBorder(radius=16),
                                            bgcolor=ft.Colors.SECONDARY_CONTAINER,
                                            color=ft.Colors.ON_SECONDARY_CONTAINER,
                                        ),
                                    ),
                                    ft.OutlinedButton(
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=8,
                                            controls=[
                                                ft.Icon(ft.Icons.SETTINGS, size=20),
                                                ft.Text("CONFIGURAR", size=16, weight=ft.FontWeight.W_500),
                                            ],
                                        ),
                                        on_click=lambda _: on_configurar(),
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 16, 0, 16),
                                            shape=ft.RoundedRectangleBorder(radius=16),
                                            side=ft.BorderSide(2, ft.Colors.OUTLINE),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        ],
    )

def _FS(label: str, value: str, color: str):
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2,
        controls=[
            ft.Text(label, size=10, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=color, font_family="RobotoMono"),
        ],
    )