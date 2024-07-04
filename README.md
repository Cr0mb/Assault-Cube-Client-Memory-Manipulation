# Assault-Cube-Client-Memory-Manipulation
This repository demonstrates how to manipulate memory values within the AssaultCube game using Python and pymem. This is useful for games and applications where you want to read and modify in-game variables.
```
Local Entity Pointer = "ac_client.exe" + 17E0A8
preferred_imagebase (ac_client.exe) = 0x400000 

Offset Health (4 Bytes) = 0xEC
Offset X Coordinate (Float) = 0x4
Offset Y Coordinate (Float) = 0x8
Offset Z Coordinate (Float) = 0xC
Offset Current Ammo (4 Bytes) = 0x140
Offset Magazine Ammo (4 Bytes) = 0x11C
```


To find the given value for each offset is simple:

1. Calculate Local Entity Address:
   
```
local_entity_address = 0x400000 + 0x17E0A8
```

3. Calculate Memory Addresses:
   
```
Health: local_entity_address + 0xEC
X Coordinate (Float): local_entity_address + 0x4
Y Coordinate (Float): local_entity_address + 0x8
Z Coordinate (Float): local_entity_address + 0xC
Current Ammo: local_entity_address + 0x140
Magazine Ammo: local_entity_address + 0x11C
```


## EXPLANATION

1. Base Address and Local Entity Pointer Offset:
base_address for ac_client.exe is given as ```0x400000```.

local_entity_pointer_offset is given as ```0x17E0A8```.

2. Calculate Local Entity Address:
The local entity address can be obtained by adding the local_entity_pointer_offset to the base_address.

```
local_entity_address = base_address + local_entity_pointer_offset
```

3. Offsets
Each offset specifies how far into the structure or object the desired value is located. These offsets are given in hexadecimal format.

4. Calculation:
Offset Health For example

```offset_health = 0xEC```

To get the actual memory address where the health value is located:

```health_address = local_entity_address + offset_health```

This gives you the specific memory address where the health value can be read or written.



## How I found the local Entity Pointer, offsets, and imagebase.
1. Scan for the health value
2. Take damage
3. Scan again
4. Now we have our health value, save in memory list

## Finding health value offset (initially)
1.. Click the memory address "Find out what writes to this address," and now we have our health offset ```0xEC```.

## Finding the local Entity Pointer
- Option 1
1. Take the memory address for the health value, and put it into the scan with a new scan; make sure to checkbox "Hex"
2. Here you should see a list of pointers and hopefully some are highlighted green. The green pointers are static, so this is what your looking for.
3. You should see something like "{module}"+{hex} within the memory address information; this is known as the pointer.

Example: ```"ac_client.exe" + 17E0A8```

This means that the memory is coming from {module}, and the pointer is {hex}

If you were to add the offset instructions to this for the health value, you will get the dynamic memory address for the health value.

For example, the Health offset is 0xEC, and the local entity pointer is "ac_client.exe" + 17E0A8.
- Option 2
1. Take the memory address for the health value, right click, and click "Generate PointerMap," save this as PointerMap1.
2. Restart the game, repeat process to find the memory address to health value, and do the same thing again.
Do this about 5 times.
3. Next, you want to click the memory address again, and select, "PointerScan for this address,"
4. Let this load, and then what you will have left is all of the memory addresses that stayed concurrent, or static, through each pointermap scan.

## Directing the local Entity Pointer to calculate the dynamic memory address for the health value
Base = ```ac_client.exe```

Pointer = ```0x17E0A8```

Offset = ```0xEC```

1. We need the base address for ```ac_client.exe```, to find this go to "Tools" and then dissect the PE headers, here you will find the prefered imagebase.
In my case, it is ```0x400000```, so ```ac_client.exe = 0x400000```. Some games will randomize this, so it may be hard to find.

You will notice now that if we click, "Add Address Manually," and set it as a pointer, we can input

```"ac_client.exe" + 17E0A8```

on the bottom box, then in the instructions we can include the offset, "EC," and now we should have our health value.


## Finding more Offsets
1. To find more offsets, simply add a new address manually, and input what we found for the base module and the pointer for the local entity, which was ```"ac_client.exe" + 17E0A8```

2. Do not include any instructions or offsets, and press "ok"
3. Next you want to click "Browse this memory region," and then go to tools and click, "Dissect data/structures"
4. Here you want to go to the top, "Structures," and click, "Define new structure," 
  - It should already give you a structure class name, for example in assault cube it is "playerent"
  - In here, you will see all of the offsets for your local entity player.
## Testing offsets for accuracy
You can test to see if these theories actually work by looking at there values after calculating with the pointer that we found.

So say we want to test this for the X coordinates of my local player, which would be a float.

1. Click "Add address manually," and enter the pointer you found. ```"ac_client.exe" + 17E0A8```
   
Next, we want to use the offset of our x coordinate, or the instruction, in here as well, which, for me is `0004,` or just `4,` because we can ignore any 0's infront of a value with hex.

Then lastly, but not least, make sure to change, "4 Byte," to "Float," and press ok. You should now see the correct value that corresponds to your X axis, you can repeat this process with any offset.
