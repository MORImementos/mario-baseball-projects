import dolphin_memory_engine as dme
from dme_gui import display_window
import time

"""read game in real time using dolphin memory engine, and display the values of the hit quality in real time"""

contact_quality = 0x80890954
contact_type = 0x808909A2

try:
    if not dme.is_hooked():
        dme.hook()
except:
    pass


cqual = round(dme.read_float(contact_quality),3)

while True:
    #print(cqual)
    #display_window(cqual)
    ctype = dme.read_byte(contact_type)
    cq = round(dme.read_float(contact_quality),3)
    if cq != cqual:
        if ctype == 0 or ctype == 4:
            print("Sour")
            print(str(round(cqual * 100, 1)) + "%")
            print("\n")
            cqual = cq
            continue
        elif ctype == 1 or ctype == 3:
            print("Nice")
            print(str(round(cqual * 100, 1)) + "%")
            print("\n")
            cqual = cq
            continue
        elif ctype == 2:
            print("Sour")
            print(str(round(cqual * 100, 1)) + "%")
            print("\n")
            cqual = cq
            continue
    display_window(cqual, cq)








    # while True:
    #     time.sleep(0.2)
    #     cqual = dme.read_float(contact_quality)
    #
    #     if cqual != cq:
    #         print(cq)
    #         cq = cqual



