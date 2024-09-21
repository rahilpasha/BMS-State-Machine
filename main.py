from time import sleep
from data_record import *
from sensor import Voltmeter, Ammeter, Thermistor
from accumulator import Accumulator

def create_Li4P25RT():
	voltmeter = Voltmeter(0.01)
	ammeter = Ammeter(0.004)
	thermistor = Thermistor(-40, 120)
	Li4P25RT = Accumulator(1, voltmeter, ammeter, thermistor, 
			min_voltage=2.5, max_voltage=4.2, 
			max_charge_amp=15, max_discharge_amp=60, 
			min_charge_temp=0, max_charge_temp=45, min_discharge_temp=-20, max_discharge_temp=60)
	return Li4P25RT


def state_of_charge(accumulator, voltage):
	safe_voltage = accumulator.MAX_VOLTAGE * 0.95
	return (voltage - accumulator.MIN_VOLTAGE) / (safe_voltage - accumulator.MIN_VOLTAGE)


def check_faults(accumulator, state, data):

	status = "OK"	

	# temperature fault
	if state == "CHARGING" or state == "FULLY_CHARGED":
		if data.temperature < accumulator.MIN_CHARGE_TEMP or data.temperature > accumulator.MAX_CHARGE_TEMP:
			print("Temperature Fault while Charging")
			status = "FAULT"
		elif data.temperature < accumulator.MIN_CHARGE_TEMP * 1.1 or data.temperature > accumulator.MAX_CHARGE_TEMP * 0.9:
			print("Temperature Warning while Charging")
			status = "WARNING"
	elif state == "PRECHARGE" or state == "TRACTIVE":
		if data.temperature < accumulator.MIN_DISCHARGE_TEMP or data.temperature > accumulator.MAX_DISCHARGE_TEMP:
			print("Temperature Fault while Discharging")
			status = "FAULT"
		elif data.temperature < accumulator.MIN_DISCHARGE_TEMP * 1.1 or data.temperature > accumulator.MAX_DISCHARGE_TEMP * 0.9:
			print("Temperature Warning while Discharging")
			status = "WARNING"
	
	# voltage fault
	if data.voltage < accumulator.MIN_VOLTAGE or data.voltage > accumulator.MAX_VOLTAGE:
		print("Voltage Fault")
		status = "FAULT"
	elif data.voltage < accumulator.MIN_VOLTAGE * 1.05 or data.voltage > accumulator.MAX_VOLTAGE * 0.95:
		print("Voltage Warning")
		if status != "FAULT":
			status = "WARNING"
	
	# current fault
	if state == "CHARGING":
		if data.current > accumulator.MAX_CHARGE_AMP:
			print("Overcharge Fault")
			status = "FAULT"
		elif data.current > accumulator.MAX_CHARGE_AMP * 0.8:
			print("Overcharge Warning")
			if status != "FAULT":
				status = "WARNING"
	elif state == "PRECHARGE" or state == "TRACTIVE":
		if abs(data.current) > accumulator.MAX_DISCHARGE_AMP:
			print("Overdischarge Fault")
			status = "FAULT"
		elif abs(data.current) > accumulator.MAX_DISCHARGE_AMP * 0.8:
			print("Overdischarge Warning")
			if status != "FAULT":
				status = "WARNING"

	return status


def main():

	# Initialize the global variables
	accumulator = create_Li4P25RT()
	MEASUREMENT_CYCLE = 1

	SLEEP_TIMEOUT = 5
	sleep_coundown = SLEEP_TIMEOUT

	WARNING_TIMEOUT = 3
	warning_countdown = WARNING_TIMEOUT
	
	state = "IDLE"

	# Initialize the data stream and take the first reading
	data_stream = load_file('tractive_fault_test.txt', MEASUREMENT_CYCLE)
	data = data_stream(0)

	# Start the while loop for the data stream
	i = 1
	while data != -1:

		# Display the current state and sensor data
		if state != "SLEEP":
			print("\n", state, data)

		match state:
			case "IDLE":
				
				# Check for sleep conditions
				if abs(data.current) < accumulator.ammeter.detectable_current:
					sleep_coundown -= MEASUREMENT_CYCLE
				if sleep_coundown < 1:
					state = "SLEEP"
					sleep_coundown = SLEEP_TIMEOUT
					print("Entering Sleep Mode")

				# Check for charging or dischargig current
				if data.current > accumulator.ammeter.detectable_current:
					state = "CHARGING"

					# Reset sleep countdown
					sleep_coundown = SLEEP_TIMEOUT

				elif data.current < -accumulator.ammeter.detectable_current:
					state = "PRECHARGE"
					print("Close Shutdown Circuit\nOpen Precharge Circuit")

					# Reset sleep countdown
					sleep_coundown = SLEEP_TIMEOUT

				
			
			case "SLEEP":
				# Change to IDLE/INIT stae if current is detected
				if abs(data.current) > accumulator.ammeter.detectable_current:
					state = "IDLE"
			
			case "CHARGING":
				
				SoC = state_of_charge(accumulator, data.voltage)
				print(f'State of Charge: {round(SoC * 100, 2)}%')

				# Change to fully charged state if SoC is above 95%
				if SoC > 0.95:
					state = "FULLY_CHARGED"
				# If charging stops before fully charged, return to idle state
				if abs(data.current) < accumulator.ammeter.detectable_current:
					state = "IDLE"


			case "FULLY_CHARGED":
				
				# Check if the current charging the battery is above 50% of max charge current allowed
				if data.current > (accumulator.MAX_CHARGE_AMP * 5):
					state = "FAULT"
					print("Overcharge Detected")
				# If any current is detected then return a warning
				elif data.current > accumulator.ammeter.detectable_current:
					state = "Warning"
					print("Fully Charged, please disconnect charger")
				# Otherwise, go back to idle state
				else:
					state = "IDLE"
					print("Charging Complete")

			case "PRECHARGE":
				
				# If accumulator is charging then return to idle state
				if data.current > -accumulator.ammeter.detectable_current:
					state = "IDLE"
				
				# Check tractive system voltage
				if data.tractive_voltage > data.voltage * 0.88 and data.tractive_voltage < data.voltage * 0.95:
					state = "TRACTIVE"
					print("Close AIRs\nTractive System Ready to Drive")
				elif data.tractive_voltage > data.voltage * .95:
					state = "FAULT"
					print("Tractive System Voltage too high\nOpen Shutdown Circuit")

			case "TRACTIVE":

				# If the car turns off and current stops flowing, return to idle state
				if data.current > -accumulator.ammeter.detectable_current:
					state = "IDLE"
				
				# Check the state of charge
				SoC = state_of_charge(accumulator, data.voltage)
				print(f'State of Charge: {round(SoC * 100, 2)}%')
				

			case "WARNING":

				# Check if the warning has persisted for too long
				warning_countdown -= MEASUREMENT_CYCLE
				if warning_countdown < 1:
					state = "FAULT"
					print("FAULT: Warning has persisted for too long")
					warning_countdown = WARNING_TIMEOUT
				
				# Check if the warning has been cleared
				if check_faults(accumulator, state, data) == "OK":
					if abs(data.current) < accumulator.ammeter.detectable_current:
						state = "IDLE"
					elif data.current > accumulator.ammeter.detectable_current:
						state = "CHARGING"
					elif data.current < -accumulator.ammeter.detectable_current:
						state = "TRACTIVE"

			case "FAULT":

				print("Open Shutdown Circuit and AIRs")
				# Check if the fault has been cleared
				if fault_status == "OK":
					state = "IDLE"
					print("Fault Cleared")

		# Check for faults
		fault_status = check_faults(accumulator, state, data)
		if fault_status != "OK":
			# If a fault is detected, change the state appropriately
			state = fault_status
		else:
			# Reset the warning countdown if no faults are detected
			warning_countdown = WARNING_TIMEOUT

		data = data_stream(i)
		i += 1
		sleep(MEASUREMENT_CYCLE)
	
	print("Data Stream ended")

	# while data flow incoming (incoming data isn't blank)
		# switch case statement for each state
		# when a warning/fault value is recorded call a function that carries out the warning/fault state requirements
			# - use the switch case just to see if the warning has persisted and should be switched to a fault state or back to normal operation

		# get a new reading
		# wait for the measurement cycle
		



if __name__ == "__main__":
	main()
