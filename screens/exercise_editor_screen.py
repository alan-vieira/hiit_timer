"""Tela de Edição de Exercícios e Intervalos (Otimizada)."""

import flet as ft
from workout import ExercicioConfig, WorkoutConfig
from store import store


def ExerciseEditorScreen(page: ft.Page, on_save, on_cancel):
    # Cópia local para edição
    local = {
        "exercicios": [ExercicioConfig(ex.nome, ex.emoji, ex.duracao) for ex in store.config.exercicios],
        "descanso_curto": store.config.descanso_curto,
        "descanso_ciclo": store.config.descanso_ciclo,
    }

    tf_curto = ft.TextField(value=str(local["descanso_curto"]), keyboard_type=ft.KeyboardType.NUMBER, width=100, text_align=ft.TextAlign.CENTER)
    tf_ciclo = ft.TextField(value=str(local["descanso_ciclo"]), keyboard_type=ft.KeyboardType.NUMBER, width=100, text_align=ft.TextAlign.CENTER)
    lv_exercicios = ft.ListView(spacing=8)

    def rebuild_list():
        lv_exercicios.controls = []
        for idx, ex in enumerate(local["exercicios"]):
            i = idx
            tf_emoji = ft.TextField(value=ex.emoji, width=60, text_align=ft.TextAlign.CENTER)
            tf_nome = ft.TextField(value=ex.nome, dense=True, expand=True)
            tf_dur = ft.TextField(value=str(ex.duracao), width=70, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER, suffix="s")
            btn_del = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.ERROR, disabled=len(local["exercicios"]) <= 1)

            # Handlers que APENAS mutam o estado, SEM chamar rebuild_list()
            def on_emoji_change(e, idx=i):
                local["exercicios"][idx].emoji = e.control.value or "🏃"
            
            def on_nome_change(e, idx=i):
                local["exercicios"][idx].nome = e.control.value or "Exercício"
            
            def on_dur_change(e, idx=i):
                try:
                    v = int(e.control.value) if e.control.value else 30
                except ValueError:
                    v = 30
                local["exercicios"][idx].duracao = v

            def on_del(_, idx=i):
                if len(local["exercicios"]) > 1:
                    local["exercicios"].pop(idx)
                    rebuild_list()  # Só rebuilda ao adicionar/remover, NÃO ao digitar
                    page.update()

            tf_emoji.on_change = on_emoji_change
            tf_nome.on_change = on_nome_change
            tf_dur.on_change = on_dur_change
            btn_del.on_click = on_del

            lv_exercicios.controls.append(ft.Card(content=ft.Container(padding=12, content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[tf_emoji, tf_nome, tf_dur, btn_del]))))
        page.update()

    def on_curto_change(e):
        try:
            local["descanso_curto"] = int(e.control.value) if e.control.value else 30
        except ValueError:
            local["descanso_curto"] = 30

    def on_ciclo_change(e):
        try:
            local["descanso_ciclo"] = int(e.control.value) if e.control.value else 30
        except ValueError:
            local["descanso_ciclo"] = 30

    tf_curto.on_change = on_curto_change
    tf_ciclo.on_change = on_ciclo_change

    def add_exercicio():
        local["exercicios"].append(ExercicioConfig("Novo Exercício", "🏃", 45))
        rebuild_list()

    def handle_save():
        store.config = WorkoutConfig(
            exercicios=local["exercicios"],
            descanso_curto=local["descanso_curto"],
            descanso_ciclo=local["descanso_ciclo"],
        )
        store.atualizar_etapas()
        on_save()

    rebuild_list()

    return ft.View(route="/editor", bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(title=ft.Text("Personalizar Treino", weight=ft.FontWeight.BOLD), center_title=True, bgcolor=ft.Colors.SURFACE),
        controls=[ft.SafeArea(content=ft.Column(expand=True, controls=[
            ft.Container(padding=16, margin=ft.Margin(16, 16, 16, 16), border_radius=12, bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(spacing=12, controls=[
                    ft.Text("DURAÇÃO DOS INTERVALOS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Row([
                        ft.Column([ft.Text("Descanso Curto (s)", size=12), tf_curto]),
                        ft.Column([ft.Text("Descanso Longo (s)", size=12), tf_ciclo]),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ])),
            ft.Container(padding=ft.Padding(16, 0, 16, 0),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("EXERCÍCIOS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.TextButton("ADICIONAR", icon=ft.Icons.ADD, on_click=lambda _: add_exercicio()),
                ])),
            ft.Container(expand=True, padding=ft.Padding(16, 0, 16, 0), content=lv_exercicios),
            ft.Container(padding=16, bgcolor=ft.Colors.SURFACE,
                content=ft.Row(alignment=ft.MainAxisAlignment.END, spacing=12, controls=[
                    ft.TextButton("CANCELAR", on_click=lambda _: on_cancel()),
                    ft.FilledButton("SALVAR TREINO", icon=ft.Icons.CHECK, on_click=lambda _: handle_save()),
                ])),
        ]))],
    )