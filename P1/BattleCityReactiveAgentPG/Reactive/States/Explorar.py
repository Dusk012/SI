from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class Explorar(State):

    def __init__(self, id):
        super().__init__(id)
        self.action = AgentConsts.NO_MOVE

    def Start(self, agent):
        print(f"[{self.id}] Iniciando exploracion...")

    def Update(self, perception, map, agent):
        obstaculos = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.BRICK,
            AgentConsts.COMMAND_CENTER,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.SEMI_BREKABLE
        ]

        movimientos_validos = []

        if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos:
            movimientos_validos.append(AgentConsts.MOVE_UP)

        if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos:
            movimientos_validos.append(AgentConsts.MOVE_DOWN)

        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos:
            movimientos_validos.append(AgentConsts.MOVE_RIGHT)

        if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos:
            movimientos_validos.append(AgentConsts.MOVE_LEFT)

        if movimientos_validos:
            if self.action in movimientos_validos and random.random() < 0.85:
                pass
            else:
                self.action = random.choice(movimientos_validos)
        else:
            self.action = AgentConsts.NO_MOVE

        return self.action, False
    
    def Transit(self,perception, map):

        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X < 0] < 0:
            return "BuscarSalida"
        
        entorno = [
            perception[AgentConsts.NEIGHBORHOOD_UP],
            perception[AgentConsts.NEIGHBORHOOD_DOWN],
            perception[AgentConsts.NEIGHBORHOOD_RIGHT],
            perception[AgentConsts.NEIGHBORHOOD_LEFT]
        ]

        if AgentConsts.SHELL in entorno:
            return "Esquivar"
        
        if AgentConsts.PLAYER in entorno or AgentConsts.COMMAND_CENTER in entorno:
            return "Disparar"

        return self.id
    
    def Reset(self):
        self.action = random.randint(1,4)
        self.updateTime = 0