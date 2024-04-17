import time
import threading

# Ref: https://github.com/rdbende/Sun-Valley-ttk-theme
# Install: pip install sv-ttk
from wifi_communicator import WiFiCommunicator, OutMessage


class WirelessDataPipe():
    '''
    '''
    ON_BUTTON_STR = 'ON'
    OFF_BUTTON_STR = 'OFF'
    ON_COLOR = 'green'
    OFF_COLOR = 'red'
    data = ""
    def __init__(self, communicator: WiFiCommunicator) -> None:
        '''
        '''
        # The wifi communicator object
        self._communicator = communicator

        # Incoming messages handler
        self._end_signal = False
        self._msgs_thread_handle = threading.Thread(target=self.__messages_receiving_thread, daemon=True)
        self._msgs_thread_handle.start()
        
    # ------------------------------- #
    #  Update the screen periodically #
    # ------------------------------- #

    def __messages_receiving_thread(self):
    
        if not self._end_signal:
            message = self._communicator.get_message()
            self.data = message.data
            if message.require_acknowledgment:
                msg = OutMessage(data='A')
                self._communicator.send_message(msg)
            
            time.sleep(0.001)

    def __update(self):
        '''
        This is called each 1ms to update the GUI elements and do periodic actions
        '''
        return

    def update_messages(self):
        self.__messages_receiving_thread()

    def get_string(self):
        return self.data
    
    def get_data(self):
        lista = self.data.split(" ")    
        aux = []
        for i in lista:
            try:
                if (float(i) or i.isdigit()):
                    aux.append(float(i))
            except ValueError:
                continue

        return aux
