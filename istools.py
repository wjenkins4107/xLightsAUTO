#######################
### isfloat         ###
#######################

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return (False, 0)
    except TypeError:
        return (False, 1)
    else:
        # Infinity ?
        if (a == float('inf')):
            return(False, 2)
        else:
            return (True, a)

#######################
### isint           ###
#######################

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return (False, 0)
    except TypeError:
        return (False, 1)
    except OverflowError:
        return (False, 2)
    else:
        if (a == b):
            return(True, b)
        else:
            return(False, 3)

#######################
### isnumber        ###
#######################

def isnumber(s):
     (valid, number) = isint(s)
     if (valid):
         return(valid, number)
     else:
         (valid, number) = isfloat(s)
         return(valid, number)

