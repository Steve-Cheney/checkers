##### board Class #####
## This class contains the information for the game board
## Game board X and Y starts at 1
## Game ends when one player has no more checkers left
##
## Class Variables:
## boardSize: Size 2 array of [X,Y] board size where [X] is the width of the board and [Y] is the height of the board
## boardMaxX: Width of the board as an int // taken from boardSize
## boardMaxY: Height of the board as an int // taken from boardSize
## boardStr: What the current board looks like in string form
## checkersList: List of all checker objects
## player1Score: Score increases by 1 for each captured checker
## player2Score: Score increases by 1 for each captured checker
## player1CheckerCount: How many checkers P1 has left
## player2CheckerCount: How many checkers P2 has left

import checker as ch
class board:
    boardSize = None
    boardMaxX = None
    boardMaxY = None
    boardStr = None
    checkersList = []
    player1Score = 0
    player2Score = 0
    player1CheckerCount = None
    player2CheckerCount = None

    def __init__(self, bSize):
        self.boardSize = bSize
        self.boardMaxX = bSize[0]
        self.boardMaxY = bSize[1]
        self.player1CheckerCount = self.boardMaxX * 2
        self.player2CheckerCount = self.boardMaxX * 2

    # Returns max X value of board as an int
    def getBoardMaxX(self):
        return self.boardMaxX

    # Returns max Y value of board as an int
    def getBoardMaxY(self):
        return self.boardMaxY

    # Get player 1 score
    def getP1Score(self):
        return self.player1Score

    # Get player 2 score
    def getP2Score(self):
        return self.player2Score

    # Add 1 to player score and remove checker from other player
    def addScore(self, player):
        if player == 1:
            self.player1Score += 1
            self.player2CheckerCount -= 1
        if player == 2:
            self.player2Score += 1
            self.player1CheckerCount -= 1
        else:
            return None

    # setBoard helper function
    # Displays the column numbers
    def writeColNums(self):
        cols = "  "
        for i in range(self.boardMaxX):
            cols += " " + str(i+1) + " "
        cols += "\n"
        return cols

    def setInitialBoard(self):
        self.boardStr = ""
        self.boardStr += self.writeColNums()
        for y in range(self.boardMaxY):
            for x in range(self.boardMaxX):
                if x == 0:
                    self.boardStr += str(y + 1) + " "
                # Set Os for player 1
                if y == self.boardMaxY - 1 or y == self.boardMaxY - 2:
                    self.boardStr += " O "
                    newC = ch.checker(0,x+1,y+1,self, 1)
                    self.checkersList.append(newC)
                    #print("Appeding:",str(newC))
                # Set Xs for player 2
                elif y == 0 or y == 1:
                    self.boardStr += " X "
                    newC = ch.checker(0,x+1,y+1,self, 2)
                    self.checkersList.append(newC)
                    #print("Appeding:",str(newC))
                # Set - for empty spaces
                else:
                    self.boardStr += " - "
                    newC = ch.checker(2,x+1,y+1,self, 0)
                    self.checkersList.append(newC)
                    #print("Appeding:",str(newC))
            self.boardStr += "\n"
        self.boardStr += self.writeColNums()

    # Return checker at a given [X,Y] coord
    # Return None if no checker at coord
    def getChecker(self, x, y):
        for each in self.checkersList:
            if each.checkerGetX() == x and each.checkerGetY() == y:
                return each
        return None

    # checkMove Helper Function
    # Checks if distance between 2 spaces are a valid move
    def checkDist(self, pieces, moves):
        pieceX = pieces[0]
        pieceY = pieces[1]
        moveX = moves[0]
        moveY = moves[1]
        distX = 0
        distY = 0
        if pieceX == moveX:
            if pieceY == moveY:
                return False
            distX = abs(pieceY - moveY)

        if pieceY == moveY:
            if pieceX == moveX:
                return False
            distY = abs(pieceX - moveX)

        if distX + distY <= 2:
            return True
        else:
            return False

    # playTurn Helper Function
    # Checks if move is valid
    # First array: new coords of checker, [-1,-1] if invalid move
    # Second array: coords of checker to be removed, [-1,-1] if none removed
    def checkMove(self, pieces, moves, player, canMoveAgain):
        check = [[-1,-1], [-1,-1]]
        pieceX = pieces[0]
        pieceY = pieces[1]
        moveX = moves[0]
        moveY = moves[1]
        moveT = moves[2]
        otherPlayer = -1
        if player == 1:
            otherPlayer = 2
        else:
            otherPlayer = 1
        # check if move type is not valid
        if not moveT.__eq__("L"):
            if not moveT.__eq__("R"):
                if not moveT.__eq__("F"):
                    if not moveT.__eq__("B"):
                        if not moveT.__eq__("BL"):
                            if not moveT.__eq__("BR"):
                                print("ERR: invalid move type")
                                return check
        checkerAtMove = self.getChecker(moveX, moveY)
        checkerPiece = self.getChecker(pieceX, pieceY)
        if checkerPiece == None: # if checker selected does not exist, invalid move
            print("ERR: selected checker DNE")
            return check # invalid move
        if checkerAtMove == None: # if move selected does not exist, invalid move
            print("ERR: selected space DNE")
            return check # invalid move
        if self.getChecker(pieceX, pieceY).checkerGetOwner()[0] != player: # piece selected is not owned by player
            print("ERR: you do not own the selected piece")
            return check # invalid move
        if not self.checkDist(pieces, moves): # check if move is within 1 tile
            print("ERR: move not within 1 tile")
            return check # invalid move
        if checkerAtMove.checkerGetOwner()[0] == player:
                print("ERR: trying to move to another owned checker")
                return check # invalid move
        if moveT.__eq__("B"): # check if backwards move is allowed (check if king piece)
            if self.getChecker(pieceX, pieceY).checkerGetType()[0] != 1:
                print("ERR: piece is not king")
                return check # invalid move
            else:
                # Player 1: Back traverses positive Y
                # Player 2: Back traverses negative Y
                if player == 1:
                    if not canMoveAgain:
                        if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, valid move
                            check = [[moveX, moveY], [-1,-1]]
                            #print("Valid 1 B")
                            return check
                    if self.getChecker(moveX, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX, moveY + 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX, moveY + 1], [moveX, moveY]]
                        #print("Valid 2 B")
                        return check
                if player == 2:
                    if not canMoveAgain:
                        if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, valid move
                            check = [[moveX, moveY], [-1,-1]]
                            #print("Valid 1 B")
                            return check
                    if self.getChecker(moveX, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX, moveY - 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX, moveY - 1], [moveX, moveY]]
                        #print("Valid 2 B")
                        return check

        if moveT.__eq__("BL"): # check if backwards left move is allowed (check if king piece)
            if self.getChecker(pieceX, pieceY).checkerGetType()[0] != 1:
                print("ERR: piece is not king")
                return check # invalid move
            else:
                # Player 1: Back traverses positive Y
                # Player 2: Back traverses negative Y
                if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, invalid move
                    print("ERR: cannot traverse left to empty space")
                    return check # invalid move
                if player == 1:
                    if self.getChecker(moveX - 1, moveY + 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if not canMoveAgain:
                        if self.getChecker(moveX - 1, moveY + 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                            check = [[moveX - 1, moveY + 1], [moveX, moveY]]
                            print("Valid 1 BL")
                            return check
                if player == 2:
                    if self.getChecker(moveX - 1, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if not canMoveAgain:
                        if self.getChecker(moveX - 1, moveY - 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                            check = [[moveX - 1, moveY - 1], [moveX, moveY]]
                            print("Valid 2 BL")
                            return check

        if moveT.__eq__("BR"): # check if backwards right move is allowed (check if king piece)
            if self.getChecker(pieceX, pieceY).checkerGetType()[0] != 1:
                print("ERR: piece is not king")
                return check # invalid move
            else:
                # Player 1: Back traverses positive Y
                # Player 2: Back traverses negative Y
                if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, invalid move
                    print("ERR: cannot traverse left to empty space")
                    return check # invalid move
                if player == 1:
                    if self.getChecker(moveX + 1, moveY + 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX + 1, moveY + 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX + 1, moveY + 1], [moveX, moveY]]
                        #print("Valid 1 BR")
                        return check
                if player == 2:
                    if self.getChecker(moveX + 1, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX + 1, moveY - 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX + 1, moveY - 1], [moveX, moveY]]
                        #print("Valid 1 BR")
                        return check


        if checkerAtMove == None: # if checker at the new move does not exist, invalid move
            print("ERR: OOB move")
            return check # invalid move
        else: # if checker at new move is the same owner, invalid move
            
            # if checker at new move is other player, check validity
            # Check forward move
            if moveT.__eq__("F"):
                # Player 1: Forward traverses negative Y
                # Player 2: Forward traverses positive Y
                if player == 1:
                    if not canMoveAgain:
                        if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, valid move
                            check = [[moveX, moveY], [-1,-1]]
                            #print("Valid 1 F")
                            return check
                    if self.getChecker(moveX, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX, moveY - 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX, moveY - 1], [moveX, moveY]]
                        #print("Valid 2 F")
                        return check
                if player == 2:
                    if not canMoveAgain:
                        if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, valid move
                            check = [[moveX, moveY], [-1,-1]]
                            #print("Valid 1 F")
                            return check
                    if self.getChecker(moveX, moveY + 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX, moveY + 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX, moveY + 1], [moveX, moveY]]
                        #print("Valid 2 F")
                        return check
                    
            if moveT.__eq__("L"):
                # Player 1: Left traverses negative X, negative Y
                # Player 2: Left traverses negative X, positive Y
                if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, invalid move
                        print("ERR: cannot traverse left to empty space")
                        return check # invalid move
                if player == 1:
                    if self.getChecker(moveX - 1, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX - 1, moveY - 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX - 1, moveY - 1], [moveX, moveY]]
                        #print("Valid 1 L")
                        return check
                if player == 2:
                    if self.getChecker(moveX - 1, moveY + 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX - 1, moveY + 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX - 1, moveY + 1], [moveX, moveY]]
                        #print("Valid 1 L")
                        return check
                    
            if moveT.__eq__("R"):
                # Player 1: Left traverses positive X, negative Y
                # Player 2: Left traverses positive X, positive Y
                if checkerAtMove.checkerGetOwner()[0] == 0: # if checker at new move is empty, invalid move
                        print("ERR: cannot traverse left to empty space")
                        return check # invalid move
                if player == 1:
                    if self.getChecker(moveX + 1, moveY - 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX + 1, moveY - 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX + 1, moveY - 1], [moveX, moveY]]
                        #print("Valid 1 R")
                        return check
                if player == 2:
                    if self.getChecker(moveX + 1, moveY + 1) == None: # Checker space past move DNE
                        print("ERR: checker space past capture DNE")
                        return check # invalid move
                    if self.getChecker(moveX + 1, moveY + 1).checkerGetType()[0] == 2 and checkerAtMove.checkerGetOwner()[0] == otherPlayer: # If checker past move is blank and checker at move is the other player, valid move
                        check = [[moveX + 1, moveY + 1], [moveX, moveY]]
                        #print("Valid 1 R")
                        return check
        return check
    # Check if there are more moves for the player
    def checkMoreMoves(self, pieces, player):
        check = False
        pieceX = pieces[0]
        pieceY = pieces[1]
        checkerSelected = self.getChecker(pieceX, pieceY)
        pieceType = checkerSelected.checkerGetType()[0]
        # If other player's piece is present
        #   If piece past potential capture is empty
        #       return True

        # If piece is standard
        if pieceType == 0:
            if player == 1:
                tempChecker1 = self.getChecker(pieceX, pieceY - 1)
                if tempChecker1 != None:
                    if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                        tempChecker2 = self.getChecker(pieceX, pieceY - 2)
                        if tempChecker2 != None:
                            if tempChecker2.checkerGetType()[0] == 2: 
                                check = True
                                return check
                tempChecker1 = self.getChecker(pieceX - 1, pieceY - 1)
                if tempChecker1 != None:
                    if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                        tempChecker2 = self.getChecker(pieceX - 2, pieceY - 2)
                        if tempChecker2 != None:
                            if tempChecker2.checkerGetType()[0] == 2: 
                                check = True
                                return check
                tempChecker1 = self.getChecker(pieceX + 1, pieceY - 1)
                if tempChecker1 != None:
                    if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                        tempChecker2 = self.getChecker(pieceX + 2, pieceY - 2)
                        if tempChecker2 != None:
                            if tempChecker2.checkerGetType()[0] == 2: 
                                check = True
                                return check  
            elif player == 2:
                tempChecker1 = self.getChecker(pieceX, pieceY + 1)
                if tempChecker1 != None:
                    if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                        tempChecker2 = self.getChecker(pieceX, pieceY + 2)
                        if tempChecker2 != None:
                            if tempChecker2.checkerGetType()[0] == 2: 
                                check = True
                                return check
                tempChecker1 = self.getChecker(pieceX - 1, pieceY + 1)
                if tempChecker1 != None:
                    if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                        tempChecker2 = self.getChecker(pieceX - 2, pieceY + 2)
                        if tempChecker2 != None:
                            if tempChecker2.checkerGetType()[0] == 2: 
                                check = True
                                return check
                tempChecker1 = self.getChecker(pieceX + 1, pieceY + 1)
                if tempChecker1 != None:
                    if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                        tempChecker2 = self.getChecker(pieceX + 2, pieceY + 2)
                        if tempChecker2 != None:
                            if tempChecker2.checkerGetType()[0] == 2: 
                                check = True
                                return check
            else:
                return check
        # If piece is king
        if pieceType == 1:
            tempChecker1 = self.getChecker(pieceX, pieceY - 1)
            if tempChecker1 != None:
                if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                    tempChecker2 = self.getChecker(pieceX, pieceY - 2)
                    if tempChecker2 != None:
                        if tempChecker2.checkerGetType()[0] == 2: 
                            check = True
                            return check
            tempChecker1 = self.getChecker(pieceX - 1, pieceY - 1)
            if tempChecker1 != None:
                if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                    tempChecker2 = self.getChecker(pieceX - 2, pieceY - 2)
                    if tempChecker2 != None:
                        if tempChecker2.checkerGetType()[0] == 2: 
                            check = True
                            return check
            tempChecker1 = self.getChecker(pieceX + 1, pieceY - 1)
            if tempChecker1 != None:
                if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                    tempChecker2 = self.getChecker(pieceX + 2, pieceY - 2)
                    if tempChecker2 != None:
                        if tempChecker2.checkerGetType()[0] == 2: 
                            check = True
                            return check  
            tempChecker1 = self.getChecker(pieceX, pieceY + 1)
            if tempChecker1 != None:
                if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                    tempChecker2 = self.getChecker(pieceX, pieceY + 2)
                    if tempChecker2 != None:
                        if tempChecker2.checkerGetType()[0] == 2: 
                            check = True
                            return check
            tempChecker1 = self.getChecker(pieceX - 1, pieceY + 1)
            if tempChecker1 != None:
                if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                    tempChecker2 = self.getChecker(pieceX - 2, pieceY + 2)
                    if tempChecker2 != None:
                        if tempChecker2.checkerGetType()[0] == 2: 
                            check = True
                            return check
            tempChecker1 = self.getChecker(pieceX + 1, pieceY + 1)
            if tempChecker1 != None:
                if tempChecker1.checkerGetOwner()[0] != 0 and tempChecker1.checkerGetOwner()[0] != player:
                    tempChecker2 = self.getChecker(pieceX + 2, pieceY + 2)
                    if tempChecker2 != None:
                        if tempChecker2.checkerGetType()[0] == 2: 
                            check = True
                            return check
        else:
            return check


    # playTurn Helper Function
    # Changes coords of checkers
    def changeChecker(self, startCoords, turnCoords, player):
        ogChecker = self.getChecker(startCoords[0], startCoords[1]) # Starting position of checker
        newChecker = self.getChecker(turnCoords[0][0],turnCoords[0][1]) # New space of checker
        delChecker = self.getChecker(turnCoords[1][0],turnCoords[1][1]) # Checker to be captured
        
        newChecker.checkerSetType(ogChecker.checkerGetType()[0]) # New space is now regular checker
        newChecker.checkerSetOwner(player) # Set new space's owner to be player
        
        ogChecker.checkerSetType(2) # Old space is now blank
        ogChecker.checkerSetOwner(0) # Old space owner is now None
        
        # Check if checker gets Kinged
        if player == 1:
            if newChecker.checkerGetY() == 1:
                newChecker.checkerSetType(1) # New space is now king checker
        if player == 2:
            if newChecker.checkerGetY() == self.getBoardMaxY():
                newChecker.checkerSetType(1) # New space is now king checker
        if delChecker != None: # There is a checker to be captured
            delChecker.checkerSetType(2) # Set checker to be blank
            delChecker.checkerSetOwner(0) # Set owner to be None
            self.addScore(player)
    
    # PlayTurn helper function
    # returns the move coords
    def getMoveCoords(self, pieceX, pieceY, moveT, player):
        if player == 1:
            if moveT == "F":
                moveX = pieceX
                moveY = pieceY - 1
            if moveT == "L":
                moveX = pieceX - 1
                moveY = pieceY - 1
            if moveT == "R":
                moveX = pieceX + 1
                moveY = pieceY - 1
            if moveT == "B":
                moveX = pieceX
                moveY = pieceY + 1
            if moveT == "BL":
                moveX = pieceX - 1
                moveY = pieceY + 1
            if moveT == "BR":
                moveX = pieceX + 1
                moveY = pieceY + 1
        if player == 2:
            if moveT == "F":
                moveX = pieceX
                moveY = pieceY + 1
            if moveT == "L":
                moveX = pieceX - 1
                moveY = pieceY + 1
            if moveT == "R":
                moveX = pieceX + 1
                moveY = pieceY + 1
            if moveT == "B":
                moveX = pieceX
                moveY = pieceY - 1
            if moveT == "BL":
                moveX = pieceX - 1
                moveY = pieceY - 1
            if moveT == "BR":
                moveX = pieceX + 1
                moveY = pieceY - 1
        return [moveX,moveY,moveT]
    
    # Logic for a turn
    # Player: 1 = Player 1 // 2 = Player 2
    def playTurn(self, player):
        print(str(self))
        validMove = False
        playerPiece = ""
        if player == 1:
            playerPiece = "O"
        if player == 2:
            playerPiece = "X"
        while(not validMove):
            print("Your pieces are " + playerPiece)
            print("Please pick your checker in this format: X,Y")
            pieceX = -1
            pieceY = -1
            moveT = "X"
            try:
                pieceX = int(input("X -> "))
                pieceY = int(input("Y -> "))
                pieces = [pieceX,pieceY]
                print("Please pick a move in this format: [L/R/F/B/BL/BR]")
                moveT = input("Move [L/R/F/B] -> ").upper()
                
                moves = self.getMoveCoords(pieceX, pieceY, moveT, player)
                
                moveResult = self.checkMove(pieces, moves, player, False)
                if moveResult[0] != [-1,-1]:
                    validMove = True
            except:
                print("Incorrect input")
            
            if not validMove:
                print("Please pick a valid move")

        self.changeChecker(pieces, moveResult, player)
        if moveResult[1] != [-1,-1]:
            saveOldMove = moveResult
            while(self.checkMoreMoves(moveResult[0],player)):
                print(str(self))
                print("You may move again with checker [" + str(moveResult[0][0]) + ", " + str(moveResult[0][1]) +"] Owner: " + str(self.getChecker(moveResult[0][0],moveResult[0][1]).checkerGetOwner()[1]))
                validSelection = False
                pieces = moveResult[0]
                
                while(not validSelection):
                    print("You may forfeit this move by typing X")
                    newMove = input("Move [L/R/F/B/BL/BR] -> ").upper()
                    if newMove.__eq__("L") or newMove.__eq__("R") or newMove.__eq__("F") or newMove.__eq__("B") or newMove.__eq__("BL") or newMove.__eq__("BR") or newMove.__eq__("X"):
                        if newMove.__eq__("X"):
                            validSelection = True
                            break
                        else:
                            
                            print(pieces)
                            print(moveResult)
                            pieceX = pieces[0]
                            pieceY = pieces[1]
                            
                            moves = self.getMoveCoords(pieceX, pieceY, newMove, player)

                            moveResult = self.checkMove(pieces, moves, player, True)
                            print(moveResult[0])
                            if moveResult[0] != [-1,-1]:
                                validSelection = True
                                self.changeChecker(pieces, moveResult, player)
                            else:
                                validSelection = False
                                print("Please pick a valid new move 1")
                                moveResult = saveOldMove
                    else: 
                        print("Please pick a valid new move 2")

    # Checks if the game has ended
    def endGameCheck(self):
        if self.player1CheckerCount == 0:
            return 2 # Return Player 2 has won
        if self.player2CheckerCount == 0:
            return 1 # Return Player 1 has won
        else:
            return 0 # Neither player has won yet

    # Return the board in string form
    def __str__(self):
        count = 0
        self.boardStr = ""
        self.boardStr += "Score\n  P1: " + str(self.getP1Score()) + " || P2: " + str(self.getP2Score()) + "\n"
        self.boardStr += self.writeColNums()
        for y in range(self.boardMaxY):
            for x in range(self.boardMaxX):
                if x == 0:
                    self.boardStr += str(y + 1) + " "
                self.boardStr += self.getChecker(x+1, y+1).printType()
                count += 1
            self.boardStr += "\n"
        self.boardStr += self.writeColNums()
        return self.boardStr

    # Return the list of checkers
    def checkerListToStr(self):
        out = ""
        for each in self.checkersList:
            out += str(each) + "\n"
        return out
