import adafruit_rfm9x
import busio
from digitalio import DigitalInOut
import board
import time



#Don't start this file. Start the RadioStarter.py to use this file to prevent errors from crashing it 
RADIO_FREQ_MHZ = 868.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi= busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
try:
    # Radio
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
    print('RFM9x: Detected')
except RuntimeError as error:
    print('RFM9x Error: ', error)


while True:
    data_received=None
    try:
        data_recieved=rfm9x.receive()
    except Exception():
        pass
    if data_received is not None:
        store_file=open("Data_store.txt","a")#keep for the ground station
        receive_file=open("Data_received.txt","w")
        receive_file.write(data_received)
        store_file.write(data_received+"\n")#keep for ground station
        store_file.close()#keep for ground station
        receive_file.close()
    send_file= open("Data_to_send.txt","r")
    data_send=send_file.readline()
    rfm9x.send(data_send)
    send_file.close()
