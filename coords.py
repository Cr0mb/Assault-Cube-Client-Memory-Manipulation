import os
import pymem
import pymem.process

process_name = "ac_client.exe"
base_address = 0x400000
local_entity_pointer_offset = 0x17E0A8

offset_x_coord = 0x4
offset_y_coord = 0x8
offset_z_coord = 0xC

prev_coords = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def read_coordinates():
    global prev_coords
    try:
        pm = pymem.Pymem(process_name)
        module = pymem.process.module_from_name(pm.process_handle, process_name) ##
        base = module.lpBaseOfDll
        
        while True:
            local_entity_addr = pm.read_int(base + local_entity_pointer_offset)
            x_coord = pm.read_float(local_entity_addr + offset_x_coord)
            y_coord = pm.read_float(local_entity_addr + offset_y_coord)
            z_coord = pm.read_float(local_entity_addr + offset_z_coord)
            
            if (x_coord, y_coord, z_coord) != prev_coords:
                prev_coords = (x_coord, y_coord, z_coord)
                clear_screen()
                
                print(f"Coordinates: ({x_coord}, {y_coord}, {z_coord})")
                
    except pymem.exception.MemoryReadError as e:
        print("Memory Read Error: {e}")
    except Exception as e:
        print("An Error occured: {e}")
        
if __name__ == "__main__":
    read_coordinates()