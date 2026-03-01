from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Disparar(State):

    def __init__(self, id):
        super().__init__(id)
        self.action = AgentConsts.NO_MOVE

    def Start(self, agent):
        print("Objetivo a la vista, preparando el disparo...")

    def Update(self, perception, map, agent):
        objetivos = [AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER, AgentConsts.SHELL]
        shot = False
        self.action = AgentConsts.NO_MOVE

        if perception[AgentConsts.NEIGHBORHOOD_UP] in objetivos:
            self.action = AgentConsts.MOVE_UP

        elif perception[AgentConsts.NEIGHBORHOOD_DOWN] in objetivos:
            self.action = AgentConsts.MOVE_DOWN

        elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] in objetivos:
            self.action = AgentConsts.MOVE_RIGHT

        elif perception[AgentConsts.NEIGHBORHOOD_LEFT] in objetivos:
            self.action = AgentConsts.MOVE_LEFT

        if perception[AgentConsts.CAN_FIRE] == 1:
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

        if AgentConsts.SHELL in entorno and perception[AgentConsts.CAN_FIRE] == 0:
            return "Esquivar"
        
        objetivos = [AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER, AgentConsts.SHELL]
        veo_algo = any(obj in entorno for obj in objetivos)

        if not veo_algo:
            return "Explorar"
        
        return self.id