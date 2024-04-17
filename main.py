# Example of usage:
# If you have a process that is already running, you can import the function
# that will allow to access the data without waiting for the network.
# This is done by using Queue from thread
from queue import Queue
import threading
from WirelessDataPipe import WirelessDataPipe
from wifi_communicator import WiFiCommunicator
import time

def WifiConnection(queue):
    communicator = WiFiCommunicator(max_buffer_sz=128)
    connection = WirelessDataPipe(communicator= communicator)
    print("Done Setup ...")
    while(1):
        connection.update_messages()
        # connection.get_string() return a string "LUX %vol °C %rH" separated by comas
        # connection.get_data() return a list of the measurements [LUX,%vol,°C,%rH] can be access by index 
        #print("get_string(): ", connection.get_string())
        #print("get_data(): ", connection.get_data())

        #-------------------------------------------#
        # you can set a value
        queue.put(connection.get_data())

def main():
    # Create a queue to pass the value from the thread to the main program
    queue = Queue()
    
    # Create and start the thread
    thread = threading.Thread(target=WifiConnection, args=(queue,))
    thread.start()
    
    # Main program continues to run
    print("Main program is running...")

    i = 0

    # Keep checking if the result is available
    while True:
        if not queue.empty():
            result = queue.get()
            print("Result from thread:", result)
        else:
            # Print something while waiting
            print("Main program is still running... ",i)
            i+=1
            time.sleep(0.25)
        
        

if __name__ == '__main__':
    main()
    