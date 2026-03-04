from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Disparar(State):

    def __init__(self, id):
        super().__init__(id)
        self.action = AgentConsts.NO_MOVE

    def Start(self, agent):
        print(f"[{self.id}] ¡Objetivo fijado! Fuego a discreción...")

    def Update(self, perception, map, agent):
        objetivos = [AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER, AgentConsts.SHELL, AgentConsts.OTHER]
        shot = False
        self.action = AgentConsts.NO_MOVE

        blanco_fijado = False

        if perception[AgentConsts.NEIGHBORHOOD_UP] in objetivos:
            self.action = AgentConsts.MOVE_UP
            blanco_fijado = True

        elif perception[AgentConsts.NEIGHBORHOOD_DOWN] in objetivos:
            self.action = AgentConsts.MOVE_DOWN
            blanco_fijado = True

        elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] in objetivos:
            self.action = AgentConsts.MOVE_RIGHT
            blanco_fijado = True

        elif perception[AgentConsts.NEIGHBORHOOD_LEFT] in objetivos:
            self.action = AgentConsts.MOVE_LEFT
            blanco_fijado = True

        if blanco_fijado and perception[AgentConsts.CAN_FIRE] == 1:
            shot = True

        return self.action, shot
    
    def Transit(self, perception, map):
        
        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X] < 0:
            return "BuscarSalida"
        
        entorno = [
            perception[AgentConsts.NEIGHBORHOOD_UP],
            perception[AgentConsts.NEIGHBORHOOD_DOWN],
            perception[AgentConsts.NEIGHBORHOOD_RIGHT],
            perception[AgentConsts.NEIGHBORHOOD_LEFT]
        ]

        direccion_a_sensor = {
            AgentConsts.MOVE_UP: AgentConsts.NEIGHBORHOOD_UP,
            AgentConsts.MOVE_DOWN: AgentConsts.NEIGHBORHOOD_DOWN,
            AgentConsts.MOVE_RIGHT: AgentConsts.NEIGHBORHOOD_RIGHT,
            AgentConsts.MOVE_LEFT: AgentConsts.NEIGHBORHOOD_LEFT
        }
        
        sensor_apuntando = direccion_a_sensor.get(self.action, -1)
        peligro_flanco = False
        
        sensores = [AgentConsts.NEIGHBORHOOD_UP, AgentConsts.NEIGHBORHOOD_DOWN, AgentConsts.NEIGHBORHOOD_RIGHT, AgentConsts.NEIGHBORHOOD_LEFT]
        
        for sensor in sensores:
            if perception[sensor] == AgentConsts.SHELL and sensor != sensor_apuntando:
                peligro_flanco = True

        if peligro_flanco and perception[AgentConsts.CAN_FIRE] == 0:
            return "Esquivar"
        
        objetivos = [AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER, AgentConsts.SHELL, AgentConsts.OTHER]
        veo_algo = any(obj in entorno for obj in objetivos)

        if not veo_algo:
            return "Explorar"
        
        return self.id