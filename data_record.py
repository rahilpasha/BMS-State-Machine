# Initialize the time variable to 0
time = 0

# Define the data_record class
class data_record:
	def __init__(self, voltage, tractive_voltage, current, temperature, measurement_cycle=1):
		self.voltage = voltage
		self.tractive_voltage = tractive_voltage
		self.current = current
		self.temperature = temperature

		global time
		self.time = time
		time += measurement_cycle
	
	
	def __repr__(self):

		# If the tractive_voltage is 0, then the accumulator is not in the precharge state so it doesn't need to be displayed
		if self.tractive_voltage == 0:
			return f'at time: {self.time}\nVoltage: {self.voltage}\tCurrent: {self.current}\tTemperature: {self.temperature}'
		else:
			return f'at time: {self.time}\nVoltage: {self.voltage}\tPrecharge Circuit Voltage: {self.tractive_voltage}\tCurrent: {self.current}\tTemperature: {self.temperature}'


# Define the load_file function
def load_file(file, measurement_cycle=1):
	# Define the read_data function
	def read_data(line):
		with open(file, 'r') as f:
			try:
				# Read the line of the file
				data = f.readlines()[line].split()
			except:
				# Return -1 if the file reaches the end
				return -1

		# Return a data_record object
		return data_record(round(float(data[0]),2), round(float(data[1]),2), round(float(data[2]),2), round(float(data[3]),2), measurement_cycle)
		
	return read_data
	
