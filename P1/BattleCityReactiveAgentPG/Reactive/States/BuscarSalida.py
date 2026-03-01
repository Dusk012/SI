from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class BuscarSalida(State):

    def __init__(self, id):
        super().__init__(id)
        self.action = AgentConsts.NO_MOVE

    def Start(self, agent):
        print("Objetivo cumplido, nos largamos")

    def Update(self, perception, map, agent):
        mi_x = perception[AgentConsts.AGENT_X]
        mi_y = perception[AgentConsts.AGENT_Y]
        salida_x = perception[AgentConsts.EXIT_X]
        salida_y = perception[AgentConsts.EXIT_Y]

        obstaculos = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.BRICK,
            AgentConsts.COMMAND_CENTER,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.SEMI_BREKABLE
        ]

        accion_anterior = self.action
        movimiento_ideal = AgentConsts.NO_MOVE

        distancia_x = abs(salida_x - mi_x)
        distancia_y = abs(salida_y - mi_y)

        if distancia_x > distancia_y:
            if mi_x > salida_x:
                movimiento_ideal = AgentConsts.MOVE_LEFT
            else:
                movimiento_ideal = AgentConsts.MOVE_RIGHT
        else:
            if mi_y > salida_y:
                movimiento_ideal = AgentConsts.MOVE_UP
            else:
                movimiento_ideal = AgentConsts.MOVE_DOWN

        es_seguro = False
        if movimiento_ideal == AgentConsts.MOVE_UP and perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos: es_seguro = True
        elif movimiento_ideal == AgentConsts.MOVE_DOWN and perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos: es_seguro = True
        elif movimiento_ideal == AgentConsts.MOVE_RIGHT and perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos: es_seguro = True
        elif movimiento_ideal == AgentConsts.MOVE_LEFT and perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos: es_seguro = True

        if es_seguro:
            self.action = movimiento_ideal
        else:
            movimientos_validos = []
            if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos: movimientos_validos.append(AgentConsts.MOVE_UP)
            if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos: movimientos_validos.append(AgentConsts.MOVE_DOWN)
            if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos: movimientos_validos.append(AgentConsts.MOVE_RIGHT)
            if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos: movimientos_validos.append(AgentConsts.MOVE_LEFT)

            if movimientos_validos: 
                if accion_anterior in movimientos_validos and random.random() < 0.90:
                    self.action = accion_anterior
                else:
                    self.action = random.choice(movimientos_validos)
            else:
                self.action = AgentConsts.NO_MOVE

        return self.action, False
    
    def Transit(self, perception, map):
        return self.id