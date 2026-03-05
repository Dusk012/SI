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
        obstaculos_duros = [
            AgentConsts.UNBREAKABLE, 
            AgentConsts.COMMAND_CENTER,
            AgentConsts.SEMI_UNBREKABLE
        ]

        obstaculos_blandos = [
            AgentConsts.BRICK,
            AgentConsts.SEMI_BREKABLE
        ]
        
        # Coordenadas mias y de la salida (estrella)
        mi_x = perception[AgentConsts.AGENT_X]
        mi_y = perception[AgentConsts.AGENT_Y]
        salida_x = perception[AgentConsts.EXIT_X]
        salida_y = perception[AgentConsts.EXIT_Y]
        
        distancias = {
            AgentConsts.MOVE_UP: perception[AgentConsts.NEIGHBORHOOD_DIST_UP] if perception[AgentConsts.NEIGHBORHOOD_UP] in obstaculos_duros else 100.0,
            AgentConsts.MOVE_DOWN: perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] if perception[AgentConsts.NEIGHBORHOOD_DOWN] in obstaculos_duros else 100.0,
            AgentConsts.MOVE_RIGHT: perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] if perception[AgentConsts.NEIGHBORHOOD_RIGHT] in obstaculos_duros else 100.0,
            AgentConsts.MOVE_LEFT: perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] if perception[AgentConsts.NEIGHBORHOOD_LEFT] in obstaculos_duros else 100.0
        }
        
        opuestos = {
            AgentConsts.MOVE_UP: AgentConsts.MOVE_DOWN,
            AgentConsts.MOVE_DOWN: AgentConsts.MOVE_UP,
            AgentConsts.MOVE_RIGHT: AgentConsts.MOVE_LEFT,
            AgentConsts.MOVE_LEFT: AgentConsts.MOVE_RIGHT,
            AgentConsts.NO_MOVE: AgentConsts.NO_MOVE
        }
        
        movimiento_ideal = AgentConsts.NO_MOVE
        # Hago calculos para ver si me interesa ir hacia arriba o abajo, o bien hacia la izquierda o derecha
        if abs(salida_x - mi_x) > abs(salida_y - mi_y):
            movimiento_ideal = AgentConsts.MOVE_LEFT if mi_x > salida_x else AgentConsts.MOVE_RIGHT
        else:
            movimiento_ideal = AgentConsts.MOVE_DOWN if mi_y > salida_y else AgentConsts.MOVE_UP

        # Un movimiento valido es un camino que no tenga obstaculos duros
        movimientos_validos = []
        if perception[AgentConsts.NEIGHBORHOOD_UP] not in obstaculos_duros or distancias[AgentConsts.MOVE_UP] > 0.8: movimientos_validos.append(AgentConsts.MOVE_UP)
        if perception[AgentConsts.NEIGHBORHOOD_DOWN] not in obstaculos_duros or distancias[AgentConsts.MOVE_DOWN] > 0.8: movimientos_validos.append(AgentConsts.MOVE_DOWN)
        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in obstaculos_duros or distancias[AgentConsts.MOVE_RIGHT] > 0.8: movimientos_validos.append(AgentConsts.MOVE_RIGHT)
        if perception[AgentConsts.NEIGHBORHOOD_LEFT] not in obstaculos_duros or distancias[AgentConsts.MOVE_LEFT] > 0.8: movimientos_validos.append(AgentConsts.MOVE_LEFT)

        # Misma logica que en explorar, busca caminos que no sea retroceder
        opciones_sin_retorno = [m for m in movimientos_validos if m != opuestos.get(self.action, AgentConsts.NO_MOVE)]
        opciones_finales = opciones_sin_retorno if opciones_sin_retorno else movimientos_validos

        if movimiento_ideal in opciones_finales:
            self.action = movimiento_ideal 
        elif self.action in opciones_finales:
            pass 
        elif opciones_finales:
            self.action = max(opciones_finales, key=lambda m: distancias[m])
        else:
            self.action = AgentConsts.NO_MOVE

        # Disparamos si hay muro rompible en nuestro camino
        shot = False
        direccion_a_sensor = {
            AgentConsts.MOVE_UP: AgentConsts.NEIGHBORHOOD_UP,
            AgentConsts.MOVE_DOWN: AgentConsts.NEIGHBORHOOD_DOWN,
            AgentConsts.MOVE_RIGHT: AgentConsts.NEIGHBORHOOD_RIGHT,
            AgentConsts.MOVE_LEFT: AgentConsts.NEIGHBORHOOD_LEFT
        }
        
        if self.action in direccion_a_sensor:
            sensor = direccion_a_sensor[self.action]
            if perception[sensor] in obstaculos_blandos and perception[AgentConsts.CAN_FIRE] == 1:
                shot = True

        return self.action, shot
    
    def Transit(self, perception, map):
        return self.id