import socket
import csv
import re
import time
import logging

# --------------- TODO: ADD Filename and Cycle Number ----------- #
fileName = "TestAhmad"
cycle_num = 50  # Number of test cycles. A cycle is one full move out and in.
# --------------------------------------------------------------- #

global file_path
Actuator_ip = '192.168.0.36'
Actuator_port = 5001
Local_ip = '192.168.0.150'
Local_port = 5000

allowed_move_time = 195  # Seconds

msg_GetCurrentPos 	= b'ADD_MESSAGE_HERE'
msg_GetStatus		    = b'ADD_MESSAGE_HERE'
msg_GetError 		    = b'ADD_MESSAGE_HERE'
msg_moveIn 			    = b'ADD_MESSAGE_HERE'
msg_moveOut 		    = b'ADD_MESSAGE_HERE'
msg_GetCurrent 		  = b'ADD_MESSAGE_HERE'
msg_Stop		 	      = b'ADD_MESSAGE_HERE'


def create_logger(name):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler('./log/ActuatorTesting.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set the format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


def saveData(data, path):
    if any(x is None for x in data):
        # logger.info("Null array Removed")ss
        pass
    else:
        with open(path, 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)


def udpGetDataInteger():
    try:
        data_binary, addr = sock.recvfrom(4096)  # buffer size is 1024 bytes
    except Exception as err:
        logger.error(f"udpGetDataInteger: Unexpected {err=}, {type(err)=}")

    data_str = data_binary.decode('utf-8')
    match = re.search(r'\r(\d+)', data_str)

    if match:
        dataRaw = match.group(1)
        return dataRaw
    else:
        logger.warning(f"udpGetDataInteger: Matched None - DaraStr = {data_str}")
        return None


def udpGetDataFloat():
    try:
        data_binary, addr = sock.recvfrom(4096)  # buffer size is 1024 bytes
    except Exception as err:
        logger.error(f"udpGetDataFloat: Unexpected {err=}, {type(err)=}")

    data_str = data_binary.decode('utf-8')
    match = re.findall(r"[-+]?\d*\.\d+", data_str)

    if match:
        return match[0]
    else:
        logger.warning(f"udpGetDataFloat: Matched None - DaraStr = {data_str}")
        return (None)


def stop_Command():
    sock.sendto(msg_Stop, (Actuator_ip, Actuator_port))


def move_Out():
    sock.sendto(msg_moveOut, (Actuator_ip, Actuator_port))


def move_In():
    sock.sendto(msg_moveIn, (Actuator_ip, Actuator_port))


def getAngle():
    sock.sendto(msg_GetCurrentPos, (Actuator_ip, Actuator_port))
    var = udpGetDataFloat()
    if var is None:
        return None
    else:
        return var


def getCurrentValue():
    sock.sendto(msg_GetCurrent, (Actuator_ip, Actuator_port))
    var = udpGetDataFloat()
    if var is None:
        return None
    else:
        return var


def getStatusCode():
    sock.sendto(msg_GetStatus, (Actuator_ip, Actuator_port))
    var = udpGetDataInteger()
    if var is None:
        return None
    else:
        return int(var)


def getErrorCode():
    sock.sendto(msg_GetError, (Actuator_ip, Actuator_port))
    var = udpGetDataInteger()
    if var is None:
        return None
    else:
        return int(var)


def startOnceCycle(currentcycle, startTime):
    savedData = []
    oneCycleStartTime = time.time()

    while (time.time() - oneCycleStartTime) < allowed_move_time:
        savedData[0] = currentcycle + 1
        savedData[1] = round(time.time() - startTime, 4)
        savedData[2] = getAngle()
        savedData[3] = getCurrentValue()
        savedData[4] = getStatusCode()
        savedData[5] = getErrorCode()

        saveData(savedData, file_path)
        print(savedData)
    # time.sleep(refreshRate)


# -------- Main -------- #
def main():
    # --------Prepare File-------- #
    global logger
    global sock

    file_path = './Data/' + fileName + '.csv'
    logger = create_logger(fileName)

    savedData = ["Cycle Num", "Time", "Angle", "Voltage", "Status Bit", "Error Bit"]
    saveData(savedData, file_path)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((Local_ip, Local_port))
        logger.info("Bind to Local Ip and port Successful")
    except Exception as err:
        print(f"Main Program - Unexpected {err=}, {type(err)=}")
        logger.error(f"Main Program -Unexpected {err=}, {type(err)=}")

    start_time = time.time()
    getAngle()

    try:
        for i in range(cycle_num):
            logger.info(f"New Cycle Start {i}")

            move_Out()
            startOnceCycle(i, start_time)
            move_In()
            startOnceCycle(i, start_time)

        logger.info('All Cycles Complete')
        stop_Command()
        logger.info('Testing Complete. Actuator Stopped')
        print('Testing Complete. Actuator Stopped')

    except KeyboardInterrupt as err:
        # Code to handle the interrupt (e.g., perform cleanup)
        logger.warning(f"Main Program was interrupted by user; {err=}, {type(err)=}")

    except Exception as err:
        logger.error(f"Main Program Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
