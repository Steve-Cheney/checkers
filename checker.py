##### checker Class #####
## This class contains the information for a singular checker game piece
##
## Class Variables:
## checkerType: 0 = standard game piece // 1 = king game piece // 2 = blank spot
## checkerX: x coordinate on the gameboard // starts at 1
## checkerY: y coordinate on the gameboard // starts at 1
## gameBoard: the game board object passed in
## checkerOwner: the owner (player) of the checker piece // 0 = none // 1 = P1 // 2 == P2
import board
class checker:
    checkerType = None
    checkerX = None
    checkerY = None
    gameBoard = None
    checkerOwner = None

    def __init__(self,tp, x, y, b, o):
        # Check for exceptions
        if type(tp)!=int:
            raise Exception("Type type must be an int")
        if tp != 0:
            if tp != 1:
                if tp != 2:
                    raise Exception("Type type must be 0, 1, or 2")
        if type(x)!=int:
            raise Exception("X type must be an int")
        if x > b.getBoardMaxX() or x <=0:
            raise Exception("X coord must be within board size")
        if type(y)!=int:
            raise Exception("Y type must be an int")
        if y > b.getBoardMaxY() or y <=0:
            raise Exception("Y coord must be within board size")
        if type(o)!=int:
            raise Exception("Owner type must be an int")
        if o != 0:
            if o != 1:
                if o != 2:
                    raise Exception("Owner must be 0, 1, or 2")

        self.checkerType = tp
        self.checkerX = x
        self.checkerY = y
        self.gameBoard = b
        self.checkerOwner = o


    # Returns array of checker type
    # [0] = int of type //     0      ||    1   ||    2
    # [1] = str of type // 'standard' || 'king' || 'blank'
    def checkerGetType(self):
        ansStr = ""
        if self.checkerType == 0:
            ansStr = "standard"
            ans = [self.checkerType, ansStr]
            return ans
        if self.checkerType == 1:
            ansStr = "king"
            ans = [self.checkerType, ansStr]
            return ans
        else:
            ansStr = "blank"
            ans = [self.checkerType, ansStr]
            return ans

    # Returns X coord of checker as an int
    def checkerGetX(self):
        return self.checkerX

    # Returns Y coord of checker as an int
    def checkerGetY(self):
        return self.checkerY

    # Returns array of owner type
    # [0] = int of owner ||   0  ||   1  ||  2
    # [1] = str of owner || None || 'P1' || 'P2'
    def checkerGetOwner(self):
        ansStr = ""
        if self.checkerOwner == 0:
            ansStr = None
        elif self.checkerOwner == 1:
            ansStr = "P1"
        else:
            ansStr = "P2"
        ans = [self.checkerOwner, ansStr]
        return ans

    # Set type of checker
    # int of type ||     0      ||   1    ||    2
    #             || 'standard' || 'king' || 'blank'
    def checkerSetType(self,tp):
        if type(tp)!=int:
            raise Exception("type must be an int")
        if tp != 0:
            if tp != 1:
                if tp != 2:
                    raise Exception("type must be 0, 1, or 2")
        #print("CHANGING TYPE TO", str(tp))
        self.checkerType = tp

    # Set owner of checker
    # int of owner  ||   0  ||   1  ||   2
    #               || None || 'P1' || 'P2'
    def checkerSetOwner(self,o):
        if type(o)!=int:
            raise Exception("type must be an int")
        if o != 0:
            if o != 1:
                if o != 2:
                    raise Exception("Owner must be 0, 1, or 2")
        self.checkerOwner = o

    # Set x coord of checker
    # Must be an int
    def checkerSetX(self,x):
        if type(x)!=int:
            raise Exception("type must be an int")
        if x > self.gameBoard.getBoardMaxX() or x <=0:
            raise Exception("X coord must be within board size")
        self.checkerX = x

    # Set y coord of checker
    # Must be an int
    def checkerSetY(self,y):
        if type(y)!=int:
            raise Exception("type must be an int")
        if y > self.gameBoard.getBoardMaxY() or y <=0:
            raise Exception("X coord must be within board size")
        self.checkerY = y

    # To string of checker information
    def __str__(self):
        return "[X,Y]: [" + str(self.checkerX) + "," + str(self.checkerY) + "] Type: " + str(self.checkerGetType()[1]) + " Owner: " + str(self.checkerGetOwner()[1])

    # To string of checker type
    # 0 = - // 1 = O // 2 == X
    def printType(self):
        owner = self.checkerOwner
        tp = self.checkerType

        if owner == 0:
            return " - "
        if owner == 1:
            if tp == 0:
                return " O "
            if tp == 1:
                return " U "
        if owner == 2:
            if tp == 0:
                return " X "
            if tp == 1:
                return " Z "
        else:
            return " E " # Error
