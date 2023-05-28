import abc
import _dolphin_memory_engine as dme
from pygame import Vector3
from visualizer import mat
import struct

# written by Roeming
def floats_from_bytes(b: bytes) -> list[float]:
    ba = bytearray(b)
    n = 4
    return [struct.unpack("f", bytes(reversed(b[i:i+n])))[0] for i in range(0, len(b), n)]
    
def bytes_from_floats(*f) -> bytearray:   
    return b"".join([bytes(reversed(struct.pack("f", ff))) for ff in f])

def read_word(addr) -> int:
    hook()
    return dme.read_word(addr)

def write_word(addr, v):
    hook()
    dme.write_word(addr, v & 0xffffffff)

def read_bytes(addr, c:int):
    return dme.read_bytes(addr, c)

def write_bytes(addr, b):
    dme.write_bytes(addr, b)

def read_byte(addr) -> int:
    hook()
    return dme.read_byte(addr)

def write_byte(addr, v:int):
    hook()
    dme.write_byte(addr, v & 0xff)

def read_bool(addr) -> bool:
    return read_byte(addr) != 0

def write_bool(addr, v:bool):
    write_byte(addr, 1 if v else 0)

def read_half_word(addr) -> int:
    hook()
    return read_word(addr) >> 16
    
def write_half_word(addr, v):
    hook()
    dme.write_byte(addr+0, v >> 8 & 0xff) 
    dme.write_byte(addr+1, v & 0xff) 

def read_float(addr) -> float:
    hook()
    return dme.read_float(addr)

def write_float(addr, value):
    hook()
    dme.write_float(addr, value)

def write_vec3(addr, value:Vector3):
    hook()
    dme.write_float(addr + 0, value.x)
    dme.write_float(addr + 4, value.y)
    dme.write_float(addr + 8, value.z)

def read_vec3(addr)-> Vector3:
    hook()
    byte_output = read_bytes(addr, 0x4 * 0x3)
    return Vector3(*floats_from_bytes(byte_output))

def write_vec3(addr, v: Vector3) -> None:
    hook()
    write_bytes(addr, bytes_from_floats(v.x, v.y, v.z))

def write_mat(addr, m:mat):
    hook()
    write_bytes(addr, bytes_from_floats(*m.all_values()))

def read_mat(addr, rows, columns):
    b = read_bytes(addr, 4 * rows * columns)
    floats = floats_from_bytes(b)
    v = [[floats[a * columns + b] for b in range(columns)] for a in range(rows)]
    return mat(v)

def is_hooked(): 
    return dme.is_hooked()

def hook():
    while not is_hooked():
        dme.hook()

def unhook():
    dme.unhook()


class DolphinFloat():

    def __init__(self, address:int, struct_size = 4) -> None:
        self._addr = address
        self._struct_size = struct_size

    def read(self, index = 0) -> float:
        return read_float(self._addr + index * self._struct_size)
    
    def write(self, v:float, index = 0) -> None:
        write_float(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> float:
        return self.read()

    @live_value.setter
    def live_value(self, v:float) -> None:
        self.write(v)

class DolphinWord():

    def __init__(self, address:int, struct_size = 4) -> None:
        self._addr = address
        self._struct_size = struct_size

    def read(self, index = 0) -> int:
        return read_word(self._addr + index * self._struct_size)
    
    def write(self, v:int, index = 0) -> None:
        write_word(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> int:
        return self.read()

    @live_value.setter
    def live_value(self, v:int) -> None:
        self.write(v)


class DolphinHalfWord():

    def __init__(self, address:int, struct_size = 4) -> None:
        self._addr = address
        self._struct_size = struct_size

    def read(self, index = 0) -> int:
        return read_half_word(self._addr + index * self._struct_size)
    
    def write(self, v:int, index = 0) -> None:
        write_half_word(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> int:
        return self.read()

    @live_value.setter
    def live_value(self, v:int) -> None:
        self.write(v)


class DolphinBool():

    def __init__(self, address:int, struct_size = 1) -> None:
        self._addr = address
        self._struct_size = struct_size

    def read(self, index = 0) -> bool :
        return read_bool(self._addr + index * self._struct_size)
    
    def write(self, v:bool, index = 0) -> None:
        write_bool(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> bool:
        return self.read()

    @live_value.setter
    def live_value(self, v:bool) -> None:
        self.write(v)


class DolphinByte():
    def __init__(self, address:int, struct_size = 1) -> None:
        self._addr = address
        self._struct_size = struct_size

    def read(self, index = 0) -> int :
        return read_byte(self._addr + index * self._struct_size)
    
    def write(self, v:int, index = 0) -> None:
        write_byte(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> int:
        return self.read()

    @live_value.setter
    def live_value(self, v:int) -> None:
        self.write(v)

class DolphinMat():
    def __init__(self, address:int, dims:tuple[int, int], struct_size = 0x30) -> None:
        self._addr = address
        self._struct_size = struct_size
        self._dims = dims

    def read(self, index = 0) -> mat:
        return read_mat(self._addr + index * self._struct_size, self._dims[0], self._dims[1])
    
    def write(self, v:mat, index = 0) -> None:
        write_mat(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> mat:
        return self.read()

    @live_value.setter
    def live_value(self, v:mat) -> None:
        self.write(v)

class DolphinVec3:
    def __init__(self, address:int, struct_size = 0xc) -> None:
        self._addr = address
        self._struct_size = struct_size

    def read(self, index = 0) -> Vector3:
        return read_vec3(self._addr + index * self._struct_size)
    
    def write(self, v:Vector3, index = 0) -> None:
        write_vec3(self._addr + index * self._struct_size, v)

    @property
    def live_value(self) -> Vector3:
        return self.read()

    @live_value.setter
    def live_value(self, v:Vector3) -> None:
        self.write(v)