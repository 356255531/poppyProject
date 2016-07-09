from ARL_package.VrepClasses import ObserverVrep, ActorVrep
from ARL_package.StateActionSetting import StateActionSpaceMath, StateActionSpaceVrep

dimension = (5, 3)
vrepStateActionSpace = StateActionSpaceVrep(dimension)
vrepObserver = ObserverVrep(vrepStateActionSpace, dimension)
vrepActor = ActorVrep(vrepObserver)
vrepActor.initialise_episode()
print vrepObserver.get_current_state()