__author__ = 'troyhughes'



"""
    This file is used for map translations and calculations.

"""



def getValue(x, y, map, width):
    """
    get the value at the x,y location of a 1d rep of a 2d map
    :param x: x location
    :param y: y location
    :param map: 1 dimensional rep of a 2d map
    :param width: width of the 2d map
    :return: value at the x,y location
    """
    return map[y*width+x]

def setValue(x, y, value, map, width):
    """
    Set the value at x,y on a arrayList map
    :param x: x location
    :param y: Y location
    :param value: Value to set
    :param map: 1 dimensional representation of a 2d map
    :param width: width of the 2 dimensional map
    :return: 1d rep of the 2d map with the change.
    """
    map[y*width+x] = value
    return map

def outofBounds(x,y,width):
    return not (x >= width or y >= width or x < 0 or y < 0)

def getNeighbors(x, y, map, width, FOUR_EXPAND):
    if map is None:
        raise RuntimeError("Map is none")

    four_expand = [(x+1,y),
                   (x-1,y),
                   (x,y+1),
                   (x,y-1)]
    eight_expand = []; eight_expand.extend(four_expand)
    eight_expand.extend([(x+1,y+1),
                         (x+1,y-1),
                         (x-1,y-1),
                         (x-1,y+1)])
    ret_list = []
    num_expand = []
    ## Pick how many surrounding nodes to expand
    if FOUR_EXPAND: num_expand.extend(four_expand)
    else: num_expand.extend(eight_expand)

    for v in num_expand:
        try:
            tx,ty = v
            ## Screen out the values that are out of bounds
            if outofBounds(tx,ty,width):
                continue
            inbound_value = getValue(x,y,map,width)
            ret_list.append(tx,ty,inbound_value)

        except Exception,e:
            print "Something else has errored in 'getNeighhbors'"
            raise e


    return ret_list
