import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import logging

with open('/home/systems/Desktop/ActuatorTester/name.txt', 'r') as file:
    fileName = file.read()

file_path = '/home/systems/Desktop/Data/' + fileName + '.csv'

def create_logger(name):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler('/home/systems/Desktop/ActuatorTester/log/Grapher.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set the format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

def update(i):
	df = pd.read_csv(file_path)
	
	df = df.tail(390000)

	time_column = df['Time']
	angle_column = df['Angle']
	voltage_column = df['Voltage']
	
	ax1.clear()
	ax1.set_xlabel('Time')
	#ax1.set_xticklabels(time_column)
	
	ax1.set_ylabel('Angle', color = 'red')
	ax1.plot(time_column, angle_column, color = 'red')
	#ax1.set_yticklabels(angle_column)
	
	ax2.clear()
	ax2.set_ylabel('Voltage', color = 'blue')
	#ax2.set_yticklabels(voltage_column)
	ax2.autoscale(enable=True, axis='y')
	ax2.plot(time_column, voltage_column, color = 'blue') 

logger = create_logger('Grapher')

logger.info("Started Grapher Script")
fig = plt.figure()
plt.title('Actuator Test: ' + fileName)
plt.xticks([]) 
plt.yticks([]) 

ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)


logger.info("Started Animation")

try: 
	ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
	plt.show()
except Exception as err: 
	logger.error(f"Grapher Program: Unexpected {err=}, {type(err)=}")
	print(f"Grapher Program: Unexpected {err=}, {type(err)=}")
finally:
	plt.close()
	logger.error("Closing Plot")
