# KF2_FastLeveling (Change all level's max exp to 2)

# Requirements
import pymem
import pymem.process
import pymem.pattern
import pymem.memory
import pymem.ressources.kernel32
import pymem.ressources.structure
from os import system, name
from time import sleep

# from pymem pattern
def pattern_scan_all(handle, pattern, *, return_multiple=False):
    next_region = 0
    found = []
    while next_region < 0x7FFFFFFF0000:
        next_region, page_found = pymem.pattern.scan_pattern_page(
            handle,
            next_region,
            pattern,
            return_multiple=return_multiple
        )
        if not return_multiple and page_found:
            return page_found
        if page_found:
            found += page_found
    if not return_multiple:
        return None
    return found

def clear():
    if name == 'nt':
        _ = system('cls')
        print("Killing Floor 2 | Fast Leveling")
    else:
        _ = system('clear')
        print("Killing Floor 2 | Fast Leveling")

clear()

# Finding Killing floor 2 for get handle to process using pymem
while True:
    try:
        pm = pymem.Pymem("KFGame.exe")
        print("Process ID:",pm.process_id, "Game found!")
        sleep(1)
        break
    except:
        print("Please run Killing Floor 2, waiting for game...")
        sleep(1)
        clear()

# AoB of All Level's max exp for checking level up and showing on GUI
bytes_pattern_MaxEXP = b"\\x1B\\x03\\x00\\x00\\xAC\\x03\\x00\\x00\\x58\\x04\\x00\\x00\\x23\\x05\\x00\\x00\\x14\\x06\\x00\\x00\\x31\\x07\\x00\\x00\\x82\\x08\\x00\\x00\\x10\\x0A\\x00\\x00\\xE7\\x0B\\x00\\x00\\x14\\x0E\\x00\\x00\\xA7\\x10\\x00\\x00\\xB3\\x13\\x00\\x00\\x4D\\x17\\x00\\x00\\x90\\x1B\\x00\\x00\\x9B\\x20\\x00\\x00\\x92\\x26\\x00\\x00\\xA0\\x2D\\x00\\x00\\xF8\\x35\\x00\\x00\\xD7\\x3F\\x00\\x00\\x84\\x4B\\x00\\x00\\x54\\x59\\x00\\x00\\xAB\\x69\\x00\\x00\\xFF\\x7C\\x00\\x00\\xDC\\x93\\x00\\x00\\xE7\\xAE"

# AoB of All level's max exp patched to 2
bytes_patched_MaxEXP = b"\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00"

# scan the entire address and print all address found
while True:
    try:
        print("AoB scanning...")
        allLevel_maxExp_addrs = pattern_scan_all(pm.process_handle, bytes_pattern_MaxEXP, return_multiple=True)
    except:
        print("Scan failed, Please running this when you are in game not lauching the game! try again")
        break
    isFound = False
    gotPatched = True

    # read bytes from address
    if allLevel_maxExp_addrs :
        gotPatched = False
        print("Found address:")
        isFound = True
        for addr in allLevel_maxExp_addrs:
            print("-", hex(addr))

    # patching all found address
    if isFound and not gotPatched :
        print("Patching bytes...")
        for addr in allLevel_maxExp_addrs:
            pymem.memory.write_bytes(pm.process_handle, addr, bytes_patched_MaxEXP, 98)
            print("-", hex(addr), "patched")
        gotPatched = True
        break
