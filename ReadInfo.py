import pymem
import pymem.process
import time
import os

# Process and base address information
process_name = "ac_client.exe"
base_address = 0x400000
local_entity_pointer_offset = 0x17E0A8

# Offsets
offset_health = 0xEC
offset_x_coord = 0x4
offset_y_coord = 0x8
offset_z_coord = 0xC
offset_current_ammo = 0x140
offset_magazine_ammo = 0x11C

prev_health = None
prev_coords = None
prev_current_ammo = None
prev_magazine_ammo = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_game_info():
    global prev_health, prev_coords, prev_current_ammo, prev_magazine_ammo
    
    try:
        # Open the process
        pm = pymem.Pymem(process_name)
        
        # Get the base address of the module
        module = pymem.process.module_from_name(pm.process_handle, process_name)
        base = module.lpBaseOfDll
        
        while True:
            # Calculate the address of the local entity
            local_entity_addr = pm.read_int(base + local_entity_pointer_offset)
            
            # Read values using the offsets
            health = pm.read_int(local_entity_addr + offset_health)
            x_coord = pm.read_float(local_entity_addr + offset_x_coord)
            y_coord = pm.read_float(local_entity_addr + offset_y_coord)
            z_coord = pm.read_float(local_entity_addr + offset_z_coord)
            current_ammo = pm.read_int(local_entity_addr + offset_current_ammo)
            magazine_ammo = pm.read_int(local_entity_addr + offset_magazine_ammo)
            
            # Compare with previous values
            if (health != prev_health or
                (x_coord, y_coord, z_coord) != prev_coords or
                current_ammo != prev_current_ammo or
                magazine_ammo != prev_magazine_ammo):
                
                # Update previous values
                prev_health = health
                prev_coords = (x_coord, y_coord, z_coord)
                prev_current_ammo = current_ammo
                prev_magazine_ammo = magazine_ammo
                
                # Clear the screen
                clear_screen()
                
                # Print the values
                print(f"Health: {health}")
                print(f"Coordinates: ({x_coord}, {y_coord}, {z_coord})")
                print(f"Current Ammo: {current_ammo}")
                print(f"Magazine Ammo: {magazine_ammo}")
                
    except pymem.exception.MemoryReadError as e:
        print(f"Memory read error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    read_game_info()
