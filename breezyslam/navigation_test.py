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
        for i in range(0, size):
            mapbytes[row * size + i] = int(toks[i])
        row += 1
    fd.close()

    return mapbytes



mapconfig = MapConfig()
router = TentacleRouter(mapconfig, 0.4, 0.8)

#router.getRoute(position, mapbytes)
mapbytes = loadMapbytes()
position = (mapconfig.pixelsTomm(322), mapconfig.pixelsTomm(117))


route = router.getRoute(position, mapbytes)
pos = route.popleft()
print pos
mapconfig.drawPlus(mapconfig.mmToPixels(pos[0]), mapconfig.mmToPixels(pos[1]), 50, 0, mapbytes)

mapconfig.drawCross(mapconfig.mmToPixels(position[0]), mapconfig.mmToPixels(position[1]), 50, 0, mapbytes)
mapconfig.safeaspng(mapbytes, 'test.png')