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
        # Array de obstaculos que usamos para saber si hay algo a la vista
        obstaculos = [
            AgentConsts.UNBREAKABLE, 
            AgentConsts.BRICK, 
            AgentConsts.COMMAND_CENTER,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.SEMI_BREKABLE
        ]
        
        # Diccionario de distancias para seleccionar el camino mas largo
        distancias = {
            AgentConsts.MOVE_UP: perception[AgentConsts.NEIGHBORHOOD_DIST_UP] if perception[AgentConsts.NEIGHBORHOOD_UP] in obstaculos else 100.0,
            AgentConsts.MOVE_DOWN: perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] if perception[AgentConsts.NEIGHBORHOOD_DOWN] in obstaculos else 100.0,
            AgentConsts.MOVE_RIGHT: perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] if perception[AgentConsts.NEIGHBORHOOD_RIGHT] in obstaculos else 100.0,
            AgentConsts.MOVE_LEFT: perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] if perception[AgentConsts.NEIGHBORHOOD_LEFT] in obstaculos else 100.0
        }

        # Sirve para dar marcha atras si llegamos a un camino sin salida
        opuestos = {
            AgentConsts.MOVE_UP: AgentConsts.MOVE_DOWN,
            AgentConsts.MOVE_DOWN: AgentConsts.MOVE_UP,
            AgentConsts.MOVE_RIGHT: AgentConsts.MOVE_LEFT,
            AgentConsts.MOVE_LEFT: AgentConsts.MOVE_RIGHT,
            AgentConsts.NO_MOVE: AgentConsts.NO_MOVE
        }

        # Un movimiento valido es aquel que no tiene obstaculos y el camino es suficientemente largo
        movimientos_validos = []
        if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos or distancias[AgentConsts.MOVE_UP] > 0.8: movimientos_validos.append(AgentConsts.MOVE_UP)
        if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos or distancias[AgentConsts.MOVE_DOWN] > 0.8: movimientos_validos.append(AgentConsts.MOVE_DOWN)
        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos or distancias[AgentConsts.MOVE_RIGHT] > 0.8: movimientos_validos.append(AgentConsts.MOVE_RIGHT)
        if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos or distancias[AgentConsts.MOVE_LEFT] > 0.8: movimientos_validos.append(AgentConsts.MOVE_LEFT)

        # Busco caminos que no sea volver por donde vine
        opciones_sin_retorno = [m for m in movimientos_validos if m != opuestos.get(self.action, AgentConsts.NO_MOVE)]
        # Si hay posibilidad de seguir, sigo, en caso contrario retrocedo
        opciones_finales = opciones_sin_retorno if opciones_sin_retorno else movimientos_validos

        if self.action in opciones_finales:
            pass # Seguimos nuestra inercia actual sin mirar atrás
        elif opciones_finales:
            # Elegimos el pasillo más largo
            self.action = max(opciones_finales, key=lambda m: distancias[m])
        else:
            self.action = AgentConsts.NO_MOVE
                
        return self.action, False
    
    def Transit(self,perception, map):
        # El jugador o el command center han muerto
        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X] < 0:
            return "BuscarSalida"
        
        entorno = [
            perception[AgentConsts.NEIGHBORHOOD_UP],
            perception[AgentConsts.NEIGHBORHOOD_DOWN],
            perception[AgentConsts.NEIGHBORHOOD_RIGHT],
            perception[AgentConsts.NEIGHBORHOOD_LEFT]
        ]

        # Comprobamos si no hay balas en ninguna direccion
        if AgentConsts.SHELL in entorno:
            if perception[AgentConsts.CAN_FIRE] == 1:
                return "Disparar"
            else:
                return "Esquivar"
        if AgentConsts.PLAYER in entorno or AgentConsts.COMMAND_CENTER in entorno or AgentConsts.OTHER in entorno:
            return "Disparar"

        return self.id
    
    def Reset(self):
        self.action = random.randint(1,4)
        self.updateTime = 0