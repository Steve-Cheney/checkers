import player as p
import checker as ch
import board as b
class main:

    def main():
        # Set the number of players
        def howManyPlayers():
            ans = input("How many players? (1 or 2) ")
            while(not ans.__eq__("1") and not ans.__eq__("2")):
                print("\nPlease enter either '1' or '2'.\n")
                ans = input("How many players? (1 or 2) ")
            return ans

        # Set the size of the board
        # Must be >= size 5
        def setBoardSize():
            size = input("What size board would you like to play on? (Enter a single full numnber >= 5)")
            while(int(size) < 5):
                print("\nPlease enter a number greater than or equal to 5\n")
                size = input("What size board would you like to play on? (Enter a single full numnber >= 5)")
            return int(size)

        def startGame(size, players):
            gameBoard = b.board([size,size])
            gameBoard.setInitialBoard()
            #print(gameBoard.__str__())
            #print(gameBoard.checkerListToStr())

            p = 1 # Which player is playing the turn
            while(gameBoard.endGameCheck() == 0):
                gameBoard.playTurn(p)
                if p == 1:
                    p = 2
                else:
                    p = 1
            print("**********\nCongrats! Player " + str(gameBoard.endGameCheck()) + " has won!\n**********")

        playerNum = int(howManyPlayers())
        if playerNum == 1:
            print("\nWelcome to One Player Checkers!\n")
        elif playerNum == 2:
            print("\nWelcome to Two Player Checkers!\n")

        startGame(setBoardSize(), playerNum)

    main()
