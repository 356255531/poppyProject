from ARL_package import CodeFramework, VrepClasses, Learning, Rewards, MathematicalClasses, PoppyClasses
import pypot.dynamixel
import time

positionMatrix = (7, 5)
moving_average = list([])
mov_avg_number = 10
num_episodes = 50
epsilon = 0.1
gamma = 0.7
learning_rate = 0.3
number_of_test_runs = 1
rewards_time_series = list()

################################### Initialize Poppy ###################################
ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)
port = ports[0]
print('Using the first on the list', port)
dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

states_actions = CodeFramework.GridStateActionSpace2D(dimensions=positionMatrix, allow_diag_actions=True)
poppy_observer = PoppyClasses.CVStateObserver(positionMatrix)
poppy_actor = PoppyClasses.actorPoppy(dxl_io,positionMatrix)

test_actions = [(1,0),(-1,0),(0,1),(0,-1)]

poppy_actor.come_to_zero()
time.sleep(1)
print 'ready'

for ta in test_actions:
    poppy_actor.perform_action(ta)
    print ta
    time.sleep(3)