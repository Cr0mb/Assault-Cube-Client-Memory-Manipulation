import os
import pymem
import pymem.process

# Process and base address information
process_name = "ac_client.exe"
base_address = 0x400000
local_entity_pointer_offset = 0x17E0A8

# Offsets
offset_health = 0xEC
offset_current_ammo = 0x140
offset_magazine_ammo = 0x11C

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_local_entity_address(pm):
    # Get module information for the process
    module = pymem.process.module_from_name(pm.process_handle, process_name)
    base = module.lpBaseOfDll
    
    # Read the pointer to the local entity from the calculated address
    local_entity_addr = pm.read_int(base + local_entity_pointer_offset)
    return local_entity_addr

def change_value(pm, local_entity_addr, offset, value, value_type):
    """
    Change the game value at a specified offset relative to the local entity address.
    
    Parameters:
    - pm (pymem.Pymem): The pymem process manager instance.
    - local_entity_addr (int): The memory address of the local entity.
    - offset (int): Offset from the local entity address where the value is located.
    - value (int or float): New value to write at the specified offset.
    - value_type (str): Type of the value ('int' or 'float').
    """
    if value_type == 'int':
        # Write an integer value to the specified offset
        pm.write_int(local_entity_addr + offset, value)
        print(f"Value at offset {hex(offset)} set to: {value}")
    elif value_type == 'float':
        # Write a float value to the specified offset
        pm.write_float(local_entity_addr + offset, value)
        print(f"Value at offset {hex(offset)} set to: {value}")

def main():
    try:
        pm = pymem.Pymem(process_name)
        local_entity_addr = get_local_entity_address(pm)
        
        while True:
            clear_screen()
            print("Welcome to AC Client Hacking Menu\n")
            print("Select an option to modify:")
            print("1. Health")
            print("2. Current Ammo")
            print("3. Magazine Ammo")
            print("4. Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                clear_screen()
                new_value = int(input("Enter new health value: "))
                # Write an integer value to the specified offset for health
                change_value(pm, local_entity_addr, offset_health, new_value, 'int')
                input("Press Enter to continue...")  
            elif choice == '2':
                clear_screen()
                new_value = int(input("Enter new current ammo value: "))
                change_value(pm, local_entity_addr, offset_current_ammo, new_value, 'int')
                input("Press Enter to continue...")  
            elif choice == '3':
                clear_screen()
                new_value = int(input("Enter new magazine ammo value: "))
                change_value(pm, local_entity_addr, offset_magazine_ammo, new_value, 'int')
                input("Press Enter to continue...")  
            elif choice == '4':
                clear_screen()
                print("Exiting...")
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...") 
    
    except pymem.exception.MemoryReadError as e:
        print(f"Memory read error: {e}")
    except pymem.exception.MemoryWriteError as e:
        print(f"Memory write error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
