from navigation.tentaclerouter import TentacleRouter
from mapconfig import MapConfig

def loadMapbytes():
    filename = 'result'

    fd = open(filename, 'rt')
    s = fd.readline()
    print s
    s = fd.readline()
    print s
    toks = s.split()[0:-1]
    size = int(toks[0])

    mapbytes = bytearray(size * size)

    row = 0
    print len(mapbytes)
    while True:
        s = fd.readline()
        if len(s) == 0:
            break

        toks = s.split(' ')  # ignore ''
        print len(toks)
        for i in range(0, size):
            mapbytes[row * size + i] = int(toks[i])
        row += 1
    fd.close()

mapconfig = MapConfig()
router = TentacleRouter(mapconfig, 0.4, 0.8)

#router.getRoute(position, mapbytes)
loadMapbytes()

