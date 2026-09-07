"""Store global - Estado compartilhado com persistência"""

import json
import flet as ft
from dataclasses import dataclass, field, asdict
from typing import Optional
from workout import gerar_etapas, tempo_total_estimado, WorkoutConfig, ExercicioConfig


@ft.observable
@dataclass
class HIITStore:
    config: WorkoutConfig = field(default_factory=WorkoutConfig)
    num_ciclos: int = 3
    etapas: list = field(default_factory=list)
    indice_etapa_atual: int = 0
    treino_em_andamento: bool = False
    treino_finalizado: bool = False
    _page: Optional[ft.Page] = field(default=None, repr=False)
    
    def __post_init__(self):
        self.atualizar_etapas()
    
    def attach_page(self, page: ft.Page):
        """Deve ser chamado ANTES de criar telas — carrega do storage"""
        self._page = page
        self._carregar_do_storage()
    
    def _carregar_do_storage(self):
        if not self._page:
            return
        try:
            # Config de treino
            saved_config = self._page.client_storage.get("workout_config")
            if saved_config:
                data = json.loads(saved_config)
                self.config = WorkoutConfig(
                    exercicios=[ExercicioConfig(**ex) for ex in data.get("exercicios", [])],
                    descanso_curto=data.get("descanso_curto", 30),
                    descanso_ciclo=data.get("descanso_ciclo", 60),
                )
            # Número de ciclos
            saved_ciclos = self._page.client_storage.get("num_ciclos")
            if saved_ciclos:
                self.num_ciclos = int(saved_ciclos)
            self.atualizar_etapas()
        except (json.JSONDecodeError, ValueError, TypeError, KeyError, AttributeError):
            # Qualquer erro → defaults seguros (já definidos no dataclass)
            pass
    
    def _salvar_no_storage(self):
        if not self._page:
            return
        try:
            self._page.client_storage.set("workout_config", json.dumps({
                "exercicios": [asdict(ex) for ex in self.config.exercicios],
                "descanso_curto": self.config.descanso_curto,
                "descanso_ciclo": self.config.descanso_ciclo,
            }, ensure_ascii=False))
            self._page.client_storage.set("num_ciclos", str(self.num_ciclos))
        except (OSError, TypeError, AttributeError):
            # Falha silenciosa — não quebra app
            pass
    
    def atualizar_etapas(self):
        self.etapas = gerar_etapas(self.config, self.num_ciclos)
        self.indice_etapa_atual = 0
        self.treino_finalizado = False
        self._salvar_no_storage()
    
    def reiniciar_treino(self, num_ciclos=None):
        if num_ciclos is not None:
            self.num_ciclos = num_ciclos
            self._salvar_no_storage()
        self.atualizar_etapas()
        self.treino_em_andamento = True
    
    def finalizar_treino(self):
        self.treino_em_andamento = False
        self.treino_finalizado = True
    
    def voltar_config(self):
        self.treino_em_andamento = False
        self.treino_finalizado = False
        self.indice_etapa_atual = 0
    
    @property
    def tempo_total_seg(self) -> int:
        return tempo_total_estimado(self.config, self.num_ciclos)


store = HIITStore()