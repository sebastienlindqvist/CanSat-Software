import time
import board
import busio
import digitalio
import adafruit_rfm9x

RADIO_FREQ_MHZ = 868.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi= busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
btnA = digitalio.DigitalInOut(board.D5)
btnA.direction = digitalio.Direction.INPUT
btnA.pull = digitalio.Pull.UP

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
print("RFM9x detected")
rfm9x.tx_power=23
#rfm9x.rx_power=20


try: 
    
    prev_packet= None
    count=0
    while True:
        
        packet = None

        packet = rfm9x.receive()
        if packet is not None:
            prev_packet = packet
            packet_text = str(prev_packet, "ascii")
            #print(packet_text)
            print("Received (ASCII): {0}".format(packet_text),count)
            rssi = rfm9x.last_rssi
            print("Received signal strength: {0} dB".format(rssi))
            #time.sleep(1)
            count=count+1
        button_a_data = bytes("goodbye ","utf-8")
        rfm9x.send(bytes("goodbye","utf-8"))
        count=count+1
        #print("sent data")

except RuntimeError as error:
    print("RFM9x Error: ",error)
