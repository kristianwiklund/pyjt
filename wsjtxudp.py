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
    #    print (m["mode"])
    m["messageraw"] = d.read_bytes()
    m["message"] = m["messageraw"].decode("utf-8")
    
    m["conf"] = d.read_bool()
    m["offair"] = d.read_bool()

    m["cq"] = m["message"].startswith("CQ")

    if m["cq"]:
        t = m["message"].split(" ")
        m["call"] = t[-2]
        m["grid"] = t[-1]    
        m["dx"] = len(t)>3

def readqdatetime(d):
    dt = dict()
    dt["day"] = d.read_int64()
    dt["ms"] = d.read_uint32()
    dt["tspec"] = d.read_uint8()
    if dt["tspec"] == 2:
        dt["offset"] = d.read_int32()
    if dt["tspec"] == 3:
        print ("timezones are not implemented, this will fail horribly")

    return(dt)

def decode_qso(d, m):
    m["timeoff"] = readqdatetime(d)
    m["call"] = d.read_bytes()
    m["cgrid"] = d.read_bytes()
    m["freq"] = d.read_uint64()
    m["mode"] = d.read_bytes()
    m["reportsent"] = d.read_bytes()
    m["reportrec"] = d.read_bytes()
    m["txpower"] = d.read_bytes()
    m["comments"] = d.read_bytes()
    m["name"] = d.read_bytes()
    m["timeon"] = readqdatetime(d)
    
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
        #if m["cq"]:
        #    print("CQ "+m["call"]+" " + m["grid"])
    if m["type"] == 5:
        decode_qso(d, m)
        print(m)
        
    return (m)

def encode_reply(who, ident, tid, snr, dtime, dfreq, mode, msg, conf, mods):

    e = qdatastream.Serializer()
    e.write("uint32", 0xadbccbda) # magic
    e.write("uint32", 2) #schema
    e.write("uint32", 4) 
    e.write("bytes", ident)
    e.write("uint32", tid)
    e.write("int32", snr)
    e.write("double", dtime)
    e.write("uint32", dfreq) 
    e.write("bytes", mode)
    e.write("bytes", msg)
    e.write("bool", conf)
    e.write("uint8", mods)

    # print (e.get_value())
    return (e.get_value())
    
    
