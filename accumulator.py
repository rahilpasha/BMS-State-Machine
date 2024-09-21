class Accumulator:
	def __init__(self, cells, voltmeter, ammeter, thermistor,
			  min_voltage, max_voltage,
			  max_charge_amp, max_discharge_amp,
			  min_charge_temp, max_charge_temp, min_discharge_temp, max_discharge_temp):
		self.cells = cells
		self.voltmeter = voltmeter
		self.ammeter = ammeter
		self.thermistor = thermistor
		self.MIN_VOLTAGE = min_voltage
		self.MAX_VOLTAGE = max_voltage
		self.MAX_CHARGE_AMP = max_charge_amp
		self.MAX_DISCHARGE_AMP = max_discharge_amp
		self.MIN_CHARGE_TEMP = min_charge_temp
		self.MAX_CHARGE_TEMP = max_charge_temp
		self.MIN_DISCHARGE_TEMP = min_discharge_temp
		self.MAX_DISCHARGE_TEMP = max_discharge_temp
	

	def cell_balancing(self, cells, current):
		pass
	
