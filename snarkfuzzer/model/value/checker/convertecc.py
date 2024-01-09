import model.value.eccmath.eccapi as ecc

def varConvert(prevalue):
    if (isinstance(prevalue, int)):
        return ecc.FF(prevalue)
    
    elif (isinstance(prevalue, tuple)):
        if (len(prevalue) == 2):
            if (isinstance(prevalue[0], int) and isinstance(prevalue[1], int)):
                # G1
                return ecc.G1(*prevalue)
            elif (isinstance(prevalue[0], tuple) and isinstance(prevalue[1], tuple)):
                # G2
                return ecc.G2(*prevalue)
            else:
                raise ValueError
        elif (len(prevalue) == 12):
            return ecc.GT(prevalue)
        else:
            raise ValueError
        
    elif (isinstance(prevalue, list)):
        value = []
        for item in prevalue:
            postvalue = varConvert(item)
            value.append(postvalue)
        return value
    else:
        raise ValueError