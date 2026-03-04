from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class Esquivar(State):
    
    def __init__(self, id):
        super().__init__(id)
        self.action = AgentConsts.NO_MOVE

    def Start(self, agent):
        print("No queda tiempo, esquivando bala...")

    def Update(self, perception, map, agent):
        
        obstaculos = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.BRICK,
            AgentConsts.COMMAND_CENTER,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.SEMI_BREKABLE
        ]

        movimientos_seguros = []

        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL:

            if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_LEFT)

            if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_RIGHT)

        elif perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL:

            if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_UP)

            if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_DOWN)


        if not movimientos_seguros:
            if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_UP] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_UP)

            if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_DOWN] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_DOWN)

            if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_RIGHT] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_RIGHT)

            if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_LEFT] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_LEFT)

        if movimientos_seguros:
            self.action = random.choice(movimientos_seguros)
        else:
            self.action = AgentConsts.NO_MOVE

        return self.action, False
    
    def Transit(self, perception, map):
        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X] < 0:
            return "BuscarSalida"
        
        entorno = [
            perception[AgentConsts.NEIGHBORHOOD_UP],
            perception[AgentConsts.NEIGHBORHOOD_DOWN],
            perception[AgentConsts.NEIGHBORHOOD_RIGHT],
            perception[AgentConsts.NEIGHBORHOOD_LEFT]
        ]

        if AgentConsts.SHELL in entorno:
            if perception[AgentConsts.CAN_FIRE] == 1:
                return "Disparar"
            else:
                return self.id
        
        if AgentConsts.PLAYER in entorno or AgentConsts.COMMAND_CENTER in entorno:
            return "Disparar"
        
        return "Explorar"