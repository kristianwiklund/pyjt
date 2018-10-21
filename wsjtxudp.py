import pyhamtools

import qdatastream
import hexdump


# protocol reference
# https://sourceforge.net/p/wsjt/wsjt/8190/tree/tags/wsjtx-1.8.0/NetworkMessage.hpp


def decode_decode(d,m):
    m["new"] = d.read_bool()
    m["time"] = d.read_uint32()
    m["snr"] = d.read_int32()
    m["dtime"] = d.read_double()
    m["dfreq"] = d.read_uint32()
    m["mode"] = d.read_bytes()
    m["message"] = d.read_bytes().decode("utf-8")
    m["conf"] = d.read_bool()
    m["offair"] = d.read_bool()

    m["cq"] = "CQ" in m["message"]


def decode(x):
    d = qdatastream.Deserializer(x)
    m = dict()
    
    # read header
    #print(hexdump.hexdump(x))
    
    magic = d.read_uint32()
    if magic != 0xadbccbda:
        print ("wrong magic number")
        return
    
    schema = d.read_uint32()
    #    print ("schema: "+str(schema))

    m["type"] = d.read_uint32()
    #    print ("message type: "+str(msgtype))
    
    m["id"] = d.read_bytes()
    #    print ("message id: "+mid)

    if m["type"] == 2:
        decode_decode(d,m)
        if m["cq"]:
            print(m["message"])
    return (m)
