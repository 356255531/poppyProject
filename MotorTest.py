import pypot.dynamixel
ports = pypot.dynamixel.get_available_ports()

print('available ports:', ports)

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')


Feasible Angle Test
angleBefore = list(dxl_io.get_present_position((36, )))[0]
while 1:
	if abs(angleBefore - list(dxl_io.get_present_position((37, )))[0]) > 0.5:
		print angleBefore
		angleBefore = list(dxl_io.get_present_position((37, )))[0]
print angleBefore

