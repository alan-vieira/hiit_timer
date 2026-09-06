"""
HIIT Timer - Aplicação Principal
"""

import flet as ft
import asyncio

from screens.config_screen import ConfigScreen
from screens.timer_screen import TimerScreen
from screens.finish_screen import FinishScreen
from screens.exercise_editor_screen import ExerciseEditorScreen
from store import store


def build_theme():
    return ft.Theme(color_scheme_seed=ft.Colors.INDIGO, use_material3=True,
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD),
            headline_medium=ft.TextStyle(size=24, weight=ft.FontWeight.W_600),
            title_large=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
            body_large=ft.TextStyle(size=16), body_medium=ft.TextStyle(size=14), label_small=ft.TextStyle(size=12)))


def build_dark_theme():
    return ft.Theme(color_scheme_seed=ft.Colors.INDIGO, use_material3=True,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.INDIGO, on_primary=ft.Colors.WHITE,
            primary_container=ft.Colors.INDIGO_100, on_primary_container=ft.Colors.INDIGO_900,
            secondary=ft.Colors.ORANGE, on_secondary=ft.Colors.WHITE,
            secondary_container=ft.Colors.ORANGE_100, on_secondary_container=ft.Colors.ORANGE_900,
            tertiary=ft.Colors.PURPLE, on_tertiary=ft.Colors.WHITE,
            tertiary_container=ft.Colors.PURPLE_100, on_tertiary_container=ft.Colors.PURPLE_900,
            surface=ft.Colors.GREY_900, on_surface=ft.Colors.WHITE,
            surface_container=ft.Colors.GREY_800, surface_container_high=ft.Colors.GREY_800,
            surface_container_highest=ft.Colors.GREY_700, surface_container_low=ft.Colors.GREY_800,
            surface_container_lowest=ft.Colors.GREY_900,
            outline=ft.Colors.GREY_600, outline_variant=ft.Colors.GREY_700,
            error=ft.Colors.RED_400, on_error=ft.Colors.WHITE,
            error_container=ft.Colors.RED_900, on_error_container=ft.Colors.RED_100),
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            headline_medium=ft.TextStyle(size=24, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            title_large=ft.TextStyle(size=20, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
            body_large=ft.TextStyle(size=16, color=ft.Colors.WHITE),
            body_medium=ft.TextStyle(size=14, color=ft.Colors.GREY_300),
            label_small=ft.TextStyle(size=12, color=ft.Colors.GREY_400)))


def iniciar_treino(page, num_ciclos):
    store.reiniciar_treino(num_ciclos)
    page.views.clear()
    page.views.append(TimerScreen(page=page, etapas=store.etapas, indice_inicial=0,
        on_finalizar=lambda: finalizar_treino(page), on_voltar_config=lambda: voltar_config(page)))
    page.update()


def finalizar_treino(page):
    store.finalizar_treino()
    page.views.clear()
    page.views.append(FinishScreen(page=page, tempo_total_seg=store.tempo_total_seg,
        num_ciclos=store.num_ciclos, on_repetir=lambda: repetir_treino(page),
        on_configurar=lambda: voltar_config(page)))
    page.update()


def voltar_config(page):
    store.voltar_config()
    page.views.clear()
    page.views.append(ConfigScreen(page=page, on_iniciar=lambda nc: iniciar_treino(page, nc),
        num_ciclos_inicial=store.num_ciclos, on_navegar_editor=lambda: navegar_editor(page)))
    page.update()


def repetir_treino(page):
    store.reiniciar_treino()
    page.views.clear()
    page.views.append(TimerScreen(page=page, etapas=store.etapas, indice_inicial=0,
        on_finalizar=lambda: finalizar_treino(page), on_voltar_config=lambda: voltar_config(page)))
    page.update()


def navegar_editor(page):
    page.views.append(ExerciseEditorScreen(page=page,
        on_save=lambda: voltar_config(page), on_cancel=lambda: voltar_config(page)))
    page.update()


async def main(page: ft.Page):
    # Window settings only work on desktop; wrap in try/except for Android compatibility
    try:
        page.window.width = 400
        page.window.height = 850
        page.window.min_width = 360
        page.window.min_height = 700
        await page.window.center()
    except Exception:
        pass  # Ignored on mobile/Android where window operations are not supported
    page.theme = build_theme()
    page.dark_theme = build_dark_theme()
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "HIIT Timer"

    page.views.append(ConfigScreen(page=page, on_iniciar=lambda nc: iniciar_treino(page, nc),
        num_ciclos_inicial=store.num_ciclos, on_navegar_editor=lambda: navegar_editor(page)))
    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")