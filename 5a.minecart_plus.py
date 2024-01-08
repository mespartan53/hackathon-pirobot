'''
    Line Following program for Picar-X:

    Pay attention to modify the reference value of the grayscale module 
    according to the practical usage scenarios.
    Auto calibrate grayscale values:
        Please run ./calibration/grayscale_calibration.py
    Manual modification:
        Use the following: 
            px.set_line_reference([1400, 1400, 1400])
        The reference value be close to the middle of the line gray value
        and the background gray value.

'''
from picarx import Picarx
from time import sleep
import readchar

px = Picarx()
# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])
# manual modify reference value
px.set_line_reference([80, 78, 71])

current_state = None

px_power = 25 #20
power_modifier = 0.5 #0.25
offset = 30
reverse_delay = 0.1

def get_status(val_list):
    _state = px.get_line_status(val_list)  # [bool, bool, bool], 0 means line, 1 means background
    if _state == [0, 0, 0]:
        return 'stop'
    elif _state[1] == 1:
        return 'forward'
    elif _state[0] == 1:
        return 'right'
    elif _state[2] == 1:
        return 'left'
    
last_gm_state = ''
key = 'z'

if __name__=='__main__':
    try:
        while True:
            if key == 'z':
                print('Would you like to adjust any values (y/n): ')
                key = readchar.readkey()
                key = key.lower()

            if key == 'y':
                px_power = float(input('Enter speed: '))
                power_modifier = float(input('Enter speed modifier: '))
                offset = float(input('Enter turn offset: '))
                reverse_delay = float(input('Enter reverse delay: '))

                print('Press any key to start.')
                readchar.readkey()
                key = 'n'

            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("gm_val_list: %s, %s, %s"%(gm_val_list, gm_state, last_gm_state))

            if gm_state == "stop":
                px.stop()
                
                if last_gm_state == 'left':
                    px.set_dir_servo_angle(-offset)
                    px.forward(-px_power)
                    sleep(reverse_delay)
                    
                elif last_gm_state == 'right':
                    px.set_dir_servo_angle(offset)
                    px.forward(-px_power)
                    sleep(reverse_delay)
                    
            elif gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
                
            elif gm_state == 'left':
                px.set_dir_servo_angle(offset)
                px.forward(px_power*power_modifier)
                last_gm_state = gm_state
                
            elif gm_state == 'right':
                px.set_dir_servo_angle(-offset)
                px.forward(px_power*power_modifier)
                last_gm_state = gm_state
    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)


                
