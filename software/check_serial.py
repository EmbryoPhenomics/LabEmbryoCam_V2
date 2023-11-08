from serial.tools import list_ports
import serial
import time
import multiprocessing as mp

def check_port(port, queue):
    port = serial.Serial(port, 115200)
    time.sleep(1)

    out = str(port.readline())
    
    if 'joystick' in out:
        queue.put('joystick')
    else:
        queue.put('stage')
    
    port.close()

def check_devices():
    ports = list_ports.grep('/dev/ttyACM*')
    names = [p.device for p in ports]

    manual_control_port = None
    xyz_port = None
    
    for p in names:
        queue = mp.Queue()
        proc = mp.Process(target=check_port, args=(p, queue))
        proc.start()
               
        time.sleep(2)
        print(queue.empty())
        if queue.empty():
            xyz_port = p
        else:
            port_type = queue.get()
            print(port_type)
            if 'joystick' in port_type:
                manual_control_port = p
        
        proc.terminate()
        queue.close()

    print(manual_control_port, xyz_port)
    return manual_control_port, xyz_port

print(check_devices())