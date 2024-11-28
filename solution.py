from typing import Dict, List, Tuple

from util import Color, Sat, User, Vector3
 
def solve(users: Dict[User, Vector3], sats: Dict[Sat, Vector3]) -> Dict[User, Tuple[Sat, Color]]:
    """Assign users to satellites respecting all constraints."""
    #user -> (satlitte, color)
    solution = {}
    #sat -> (color, userPos)
    satToColorsandPos = {}
    #sat -> Boolean if full or not
    fullSats = {}
    for sat in sats.keys():
        satToColorsandPos[sat] = []
        fullSats[sat] = False
 
    #loop through each user and try to add beam from it to a sat
    for u, userPos in users.items():
        for sat, satPos in sats.items():
            #if sat is full or new beam is not within 45 degrees of vertical, move to next sat
            if fullSats[sat]: continue
            extendedPos = userPos.__add__(userPos)
            newAngle = userPos.angle_between(satPos, extendedPos)
            if newAngle > 45.0: continue
 
            #check for beams within 10 degrees of potential new beam
            canUseSat = True
            conflictColors = []
            #loop through all (color, userPos) sat has
            for tup in satToColorsandPos[sat]:
                angle = satPos.angle_between(userPos, tup[1])
                if (angle < 10.0):
                    conflictColors.append(tup[0])
                if len(conflictColors) >= 4:
                    canUseSat = False
                    break
            if canUseSat == False: continue
 
            #assign color to beam
            for possibleColor in Color:
                if possibleColor in conflictColors:
                    continue
                else:
                    userColor = possibleColor
                    break
 
            #append to sat and solution dictionary. mark sat full is necessary
            satToColorsandPos[sat].append((userColor, userPos))
            if len(satToColorsandPos[sat]) == 32: fullSats[sat] = True
            solution[u] = (sat, userColor)
            break
 
    return solution