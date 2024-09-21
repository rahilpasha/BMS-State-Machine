class Sensor:
	def __init__(self, type):
		self.type = type


class Voltmeter(Sensor):
	def __init__(self, detectable_voltage):
		super().__init__("Voltmeter")
		self.detectable_voltage = detectable_voltage


class Ammeter(Sensor):
	def __init__(self, detectable_current):
		super().__init__("Ammeter")
		self.detectable_current = detectable_current


class Thermistor(Sensor):
	def __init__(self, min_temp, max_temp):
		super().__init__("Thermistor")
		self.lowest_temp = min_temp
		self.highest_temp = max_temp