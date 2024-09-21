def create_charging_test():
	with open("charging_test.txt", "w") as f:
		for i in range(5):
			f.write(f'{2.9 + (i*0.1)} {0} {i} {i * 10}\n')
		for i in range(3):
			f.write(f'{3.3} {0} {5} {20}\n')
		

def create_sleep_test():
	with open("sleep_test.txt", "w") as f:
		for i in range(7):
			f.write(f'{3.5} {0} {0} {20}\n')
		for i in range(3):
			f.write(f'{3.5} {0} {5} {20}\n')


def create_fully_charged_test():
	with open("fully_charged_test.txt", "w") as f:
		for i in range(10):
			f.write(f'{3.5 + i*.05} {0} {i} {20 + i}\n')
		for i in range(4):
			f.write(f'{3.95} {0} {0} {29 - i}\n')


def create_charging_fault_test():
	with open("charging_fault_test.txt", "w") as f:
		for i in range(7):
			f.write(f'{3.3 + i*.1} {0} {i} {20 + i*5}\n')
		for i in range(3):
			f.write(f'{3.9} {0} {0} {45 - i*5}\n')


def create_tractive_test():
	with open("tractive_test.txt", "w") as f:
		for i in range(4):
			f.write(f'{3.9 - i*.05} {i * 1.15} {-i} {20 + i}\n')
		for i in range(7):
			f.write(f'{3.7 - i*.05} {0} {-i-4} {24 + i}\n')


def create_precharge_fault_test():
	with open("precharge_fault_test.txt", "w") as f:
		for i in range(4):
			f.write(f'{3.9 - i*.05} {i * 1.2} {-i} {20 + i}\n')
		for i in range(2):
			f.write(f'{3.75} {0} {0} {24 - i}\n')


def create_tractive_fault_test():
	with open("tractive_fault_test.txt", "w") as f:
		for i in range(4):
			f.write(f'{3.9 - i*.05} {i * 1.15} {-i} {20 + i}\n')
		for i in range(5):
			f.write(f'{3.7 - i*.05} {0} {-i-4} {24 + i*10}\n')
		for i in range(3):
			f.write(f'{3.45} {0} {0} {54 - i*10}\n')


create_charging_test()
create_sleep_test()
create_fully_charged_test()
create_charging_fault_test()
create_tractive_test()
create_precharge_fault_test()
create_tractive_fault_test()
