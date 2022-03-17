import struct
# общий пакет с фреймами регулировать на web можно галочками
HIBYTE = b'\
\x00\xC0\xC1\x01\xC3\x03\x02\xC2\xC6\x06\x07\xC7\x05\xC5\xC4\x04\
\xCC\x0C\x0D\xCD\x0F\xCF\xCE\x0E\x0A\xCA\xCB\x0B\xC9\x09\x08\xC8\
\xD8\x18\x19\xD9\x1B\xDB\xDA\x1A\x1E\xDE\xDF\x1F\xDD\x1D\x1C\xDC\
\x14\xD4\xD5\x15\xD7\x17\x16\xD6\xD2\x12\x13\xD3\x11\xD1\xD0\x10\
\xF0\x30\x31\xF1\x33\xF3\xF2\x32\x36\xF6\xF7\x37\xF5\x35\x34\xF4\
\x3C\xFC\xFD\x3D\xFF\x3F\x3E\xFE\xFA\x3A\x3B\xFB\x39\xF9\xF8\x38\
\x28\xE8\xE9\x29\xEB\x2B\x2A\xEA\xEE\x2E\x2F\xEF\x2D\xED\xEC\x2C\
\xE4\x24\x25\xE5\x27\xE7\xE6\x26\x22\xE2\xE3\x23\xE1\x21\x20\xE0\
\xA0\x60\x61\xA1\x63\xA3\xA2\x62\x66\xA6\xA7\x67\xA5\x65\x64\xA4\
\x6C\xAC\xAD\x6D\xAF\x6F\x6E\xAE\xAA\x6A\x6B\xAB\x69\xA9\xA8\x68\
\x78\xB8\xB9\x79\xBB\x7B\x7A\xBA\xBE\x7E\x7F\xBF\x7D\xBD\xBC\x7C\
\xB4\x74\x75\xB5\x77\xB7\xB6\x76\x72\xB2\xB3\x73\xB1\x71\x70\xB0\
\x50\x90\x91\x51\x93\x53\x52\x92\x96\x56\x57\x97\x55\x95\x94\x54\
\x9C\x5C\x5D\x9D\x5F\x9F\x9E\x5E\x5A\x9A\x9B\x5B\x99\x59\x58\x98\
\x88\x48\x49\x89\x4B\x8B\x8A\x4A\x4E\x8E\x8F\x4F\x8D\x4D\x4C\x8C\
\x44\x84\x85\x45\x87\x47\x46\x86\x82\x42\x43\x83\x41\x81\x80\x40'
LOBYTE = b'\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40'
# возвращает значение
def pack(type, *data):
    return struct.pack(type, *data)
# возвращает строку байтов
def unpack(type, *data):
    return struct.unpack(type, *data)
# считаем crc
def crc_calculate(frame):
    i = 2
    crc = 0x00
    while i < len(frame):
        crc = crc + frame[i]
        i = i + 1
    while crc > 256:
        crc = crc - 256
    return pack('B', crc)
# создаем пакет
def pack_rs232(control_byte_1, control_byte_2, data):
    const = pack('BB', 0x55, 0xAA)
    cb_1 = pack('B', control_byte_1)
    l = pack('B', 6 + len(data))
    cb_2 = pack('B', control_byte_2)
    d = data
    frame = const + cb_1 + l + cb_2 + d
    frame = frame + crc_calculate(frame)
    return frame
# распаковать пакет
def unpack_rs232(type, frame):
    return struct.unpack(type, frame[5:len(frame) - 1])[0]
# упаковать в modbus
def pack_modbus(rs232_frame):
    wrapper = bytes([0x01, 0x17, 0x40, 0x55, 0x00, 0x04, 0x40, 0xAA, 0x00, 0x04])
    wrapper = wrapper + pack('B', rs232_frame[3])
    wrapper = wrapper + rs232_frame
    hi, lo = crc16(wrapper)
    wrapper = wrapper + pack('BB', hi, lo)
    return wrapper
# распаковать из modbus
def unpack_modbus(type, frame):
    return struct.unpack(type, frame[16:len(frame) - 3])[0]
# расчет crc16 modbus
def crc16(data):
    crchi = 0xFF
    crclo = 0xFF
    for byte in data:
        index = crchi ^ int(byte)
        crchi = crclo ^ LOBYTE[index]
        crclo = HIBYTE[index]
    # print("{0:02X} {1:02X}".format(crclo, crchi)),
    return crchi, crclo
# отправка данных по com
def to_serial(com):
    print()
if __name__ == '__main__':
    print(bytes([0x55, 0xAA, 0x28, 0x0A, 0x01, 0x00, 0x00, 0x33, 0x43, 0xA9]))
    print(pack_rs232(40, 1, pack('f', 179.0)))

    frame = bytes([0x55, 0xAA, 0x28, 0x0A, 0x01, 0x00, 0x00, 0x33, 0x43, 0xA9])

    print(frame)
    print(unpack_rs232('f',frame))

    z = bytes([0x01, 0x17, 0x40, 0x55, 0x00, 0x04, 0x40, 0xAA, 0x00, 0x04, 0x0A, 0x55, 0xAA, 0x28, 0x0A, 0x01, 0x00, 0x00, 0x33, 0x43, 0xA9, 0x6C, 0x6B])
    print(pack_modbus(pack_rs232(40, 1, pack('f', 179.0))))
    print(unpack_modbus('f', z))

    # frame = const_1
    # print(frame)
    # frame = bytes([const_1, const_2, control_byte_1, frame_len, control_byte_2, data])
    # print(frame)
    # print(crc_calculate(frame))


    # b = bytes(bb)
    # print(b)
    # b = b.hex()
    # print(type(b))

    # zz = 0.279296875
    # data = pack('ff', zz, zz)
    # print(data)
    # print(unpack('ff', data))

    # print(b[2]) # преобразовать в hex
    # d = struct.unpack('f', b)
    # print(d[0])



    # работает


    #
    # # скомпоновать байты
    # c = b + z
    # print(c)
    #
    # # распарсить из байтов
    # print()
    # print(int((z).hex()))
    #
    # print("Sum stroka")
    # sum = [0x01, 0x17, 0x40, 0x55, 0x00, 0x04, 0x40, 0xAA, 0x00, 0x04, 0x0A, 0x55, 0xAA, 0x28, 0x0A, 0x01,
    #         0x00, 0x00, 0x33, 0x43, 0xA9, 0x6C, 0x6B]
    # print(bytes(sum))

    #
    #

    # req = [ 0x01, 0x07, 0x01, 0x68]
    # s = 0
    # for r in req:
    #     s = s + r
    # print(hex(s))