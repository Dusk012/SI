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
        # Miro hacia arriba y abajo si hay una bala
        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL:
            # Hay bala en el eje vertical, me muevo a la izquierda o derecha si puedp
            if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_LEFT)

            if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_RIGHT)

        # Exatamente la misma logica pero al reves
        elif perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL:

            if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_UP)

            if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos:
                movimientos_seguros.append(AgentConsts.MOVE_DOWN)

        # Estamos es un pasillo estrecho sin poder movernos a los lados, busco algun hueco como sea
        if not movimientos_seguros:
            if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_UP] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_UP)

            if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_DOWN] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_DOWN)

            if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_RIGHT] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_RIGHT)

            if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos and perception[AgentConsts.NEIGHBORHOOD_LEFT] != AgentConsts.SHELL:
                movimientos_seguros.append(AgentConsts.MOVE_LEFT)

        # Si puedo irme a un sitio seguro me voy a alguno de ellos aleatoriamente
        if movimientos_seguros:
            self.action = random.choice(movimientos_seguros)
        else:
            self.action = AgentConsts.NO_MOVE

        return self.action, False
    
    def Transit(self, perception, map):
        # Jugador muerto o command center destruido
        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X] < 0:
            return "BuscarSalida"
        
        entorno = [
            perception[AgentConsts.NEIGHBORHOOD_UP],
            perception[AgentConsts.NEIGHBORHOOD_DOWN],
            perception[AgentConsts.NEIGHBORHOOD_RIGHT],
            perception[AgentConsts.NEIGHBORHOOD_LEFT]
        ]

        # Si hay una bala y puedo disparar entonces disparo
        if AgentConsts.SHELL in entorno:
            if perception[AgentConsts.CAN_FIRE] == 1:
                return "Disparar"
            else:
                return self.id
        # Si esta el jugador, la command center u otro agente en el entorno le disparo
        if AgentConsts.PLAYER in entorno or AgentConsts.COMMAND_CENTER in entorno or AgentConsts.OTHER in entorno:
            return "Disparar"
        
        return "Explorar"