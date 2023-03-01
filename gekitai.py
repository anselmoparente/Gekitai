class Piece: #input color output this piece is belong to which player
    def __init__ (self,color):
        self.color= color
        if str(color) == "BLACK":
            p = "X"
        elif str(color) == "RED":
            p = "O"
        else:
            p ="Empty"

        self.player = p
    def __str__(self):
        return self.player
        
    
   
    
class Player:
    def __init__(self, color, N):
        self.color =color
        self.size = N
        
    #to get input from user    
    def get_input (self):
        ans = False
        while ans == False:
            ans =True
            x = list(input(f"Player {Piece(str(self.color))}'s turn: ").replace(" ",""))
            if len(x) >2:
                print("Invalid move!")
                ans = False 
                continue
            a, b = x[0], x[1]
            valid=[]
            num=[]
            for i in range (self.size):
                valid.append(chr(97+i))
            for j in range (self.size):
                num.append(str(j+1))
            if a.lower().strip() not in valid: #check if the move is invalid
                print("Invalid move!")
                ans = False
                continue
            if b not in num:
                print("Invalid move!")
                ans = False
        y = ord(a.lower().strip())-96
        x = int(b)
        choice = (x,y)
        return choice #return a tuple of input
    
class Board:
    def __init__(self,rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [["Empty" for x in range(cols+2)] for y in range(rows+2)] #create a 2D list from [0][0] to [N+1][N+1]
        
    def get_piece(self,x,y):
        check=str(self.cells[x][y]) #check what the piece belong to
        return check

class Gekitai(Board): 
    def __init__(self, N: int = 6, P: int = 8, L: int = 3):
        self.rows = N 
        self.cols = N #self.rows==self.cols
        self.line = L
        self.num_of_pieces= P
        self.cells = [["Empty" for x in range(N+2)] for y in range(N+2)] 
        
    def is_move_valid(self, x, y): #check if the move valid
        
        if str(Board.get_piece(self,x,y))=="Empty" and 1<=x<= self.rows and 1<=y<= self.cols: # check if the input out of boundary
            return True
        else:
            return False

            
    def move(self, x:int, y:int):

        if 1 <= x <= self.rows and 1 <= y <= self.cols: #apply the move to update the board
            if self.cells[x-1][y]!= "Empty" and self.cells[x-2][y]=="Empty" and x>= 2: #inequeality to avoid out of list boundary
                self.cells[x-2][y]= self.cells[x-1][y]
                self.cells[x-1][y]= "Empty"
            if self.cells[x+1][y]!= "Empty" and self.cells[x+2][y]=="Empty" and x <= self.rows-1:
                self.cells[x+2][y]= self.cells[x+1][y]
                self.cells[x+1][y]= "Empty"
            if self.cells[x][y-1]!= "Empty" and self.cells[x][y-2]=="Empty" and y>=2:
                self.cells[x][y-2]= self.cells[x][y-1]
                self.cells[x][y-1]= "Empty"
            if self.cells[x][y+1]!= "Empty" and self.cells[x][y+2]=="Empty" and y <= self.rows-1:
                self.cells[x][y+2]= self.cells[x][y+1]
                self.cells[x][y+1]= "Empty"
            if self.cells[x-1][y+1]!= "Empty" and self.cells[x-2][y+2]=="Empty" and x>= 2 and y <= self.rows-1:
                self.cells[x-2][y+2]= self.cells[x-1][y+1]
                self.cells[x-1][y+1]= "Empty"
            if self.cells[x+1][y+1]!= "Empty" and self.cells[x+2][y+2]=="Empty" and x <= self.rows-1 and y <= self.rows-1:
                self.cells[x+2][y+2]= self.cells[x+1][y+1]
                self.cells[x+1][y+1]= "Empty"
            if self.cells[x-1][y-1]!= "Empty" and self.cells[x-2][y-2]=="Empty" and x>= 2 and y>=2:
                self.cells[x-2][y-2]= self.cells[x-1][y-1]
                self.cells[x-1][y-1]= "Empty"
            if self.cells[x+1][y-1]!= "Empty" and self.cells[x+2][y-2]=="Empty" and x <= self.rows-1 and y>=2 :
                self.cells[x+2][y-2]= self.cells[x+1][y-1]
                self.cells[x+1][y-1]= "Empty"
                
        for i in range(self.rows+2): #check if any piece are pushed outside the board then clear it
            if str(self.cells[0][i]) != "Empty":
                self.cells[0][i] = "Empty"
            if str(self.cells [i][0]) != "Empty":
                self.cells [i][0] = "Empty"
            if str(self.cells[i][self.rows+1]) != "Empty":
                self.cells[i][self.rows+1] = "Empty"
            if str(self.cells[self.rows+1][i]) != "Empty":
                self.cells[self.rows+1][i] = "Empty"
            
        
    def pieces_in_line(self): #check if any L pieces formed a line
        players=["X","O"]
        for player in players:            
            for i in range (self.rows):
                hori_ct=0
                vert_ct=0
                diag_ct1=0
                diag_ct2=0
                for j in range (self.cols):
                    # horizontal
                    if str(self.cells[i+1][j+1]) == str(player):
                        hori_ct+=1
                    else:
                        hori_ct=0
                    if hori_ct == int(self.line):
                        return True
                    # vertical
                    if str(self.cells[j+1][i+1]) == str(player):
                        vert_ct+=1
                    if vert_ct == int(self.line):
                        return True
                    if str(self.cells[j+1][i+1]) != str(player):
                        vert_ct=0
                    
                    if i+1-j>=1:
                        if str(self.cells[i+1-j][j+1]) == str(player):
                            diag_ct1+=1
                        if diag_ct1 == int(self.line):
                            return True
                        if str(self.cells[i+1-j][j+1]) != str(player):
                            diag_ct1=0
                    # top left to bottom right
                    if i+j+1<=self.rows:
                        if str(self.cells[i+1+j][j+1]) == str(player):
                            diag_ct2+=1
                        if diag_ct2 == int(self.line):
                            return True
                        if str(self.cells[i+1+j][j+1]) != str(player):
                            diag_ct2=0
    
    def print (self): #display the updated board
            print("  ",end="")
            for i in range (self.rows):
                print ("  "+chr(i+65)+" ", end="")
            print("")
            print("  ",end="")
            for i in range (self.rows):
                print("+---",end="")
            print("+")
            for j in range(self.cols):
                print(j+1,end=" ")
                for k in range (self.rows):
                    if str(self.cells[j+1][k+1])=="X":
                        print("| X ", end="")
                    if str(self.cells[j+1][k+1])=="O":
                        print("| O ", end="")
                    if self.cells[j+1][k+1]=="Empty":
                        print("|   ", end="")
                print(("|"))
                print("  ",end="")
                for i in range (self.rows):
                    print("+---",end="")
                print("+")
            ct = 0 #count the number that piece on board
            for i in range (self.cols):
                for j in range (self.rows):
                    if str(self.cells [i+1][j+1])=="X":
                        ct+=1
            if ct == self.num_of_pieces:
                print ("X:[ ]")
            else:
                print ("X: ["+"'X', "*(self.num_of_pieces-ct-1)+"'X']") #print the list of pieces they have
            ct = 0
            for i in range (self.cols):
                for j in range (self.rows):
                    if str(self.cells [i+1][j+1])=="O":
                        ct+=1
            if ct == self.num_of_pieces:
                print ("O:[ ]")
            else:
                print ("O: ["+"'O', "*(self.num_of_pieces-ct-1)+"'O']")
            return ""

    def game_over(self):  #check if it meets the winning conditions
        X_ct = 0
        for i in range (self.cols):
            for j in range (self.rows):
                if str(self.cells [i+1][j+1])=="X":
                    X_ct+=1 
        
        O_ct = 0
        for i in range (self.cols):
            for j in range (self.rows):
                if str(self.cells [i+1][j+1])=="O":
                    O_ct+=1
      
        if Gekitai.pieces_in_line(self)== True: #form line
            return True

        if X_ct== self.num_of_pieces: #all X pieces put on board
            return True
    
        if O_ct == self.num_of_pieces:#all O pieces put on board
            return True
                
        return False
            
    def start(self): 
        a = False
        while a == False: #loop until it breaks
            print(Gekitai.print(self))
            x, y= Player("BLACK",self.rows).get_input()
            while Gekitai.is_move_valid(self,x, y)==False:
                print("Invalid move!")
                x,y = Player("BLACK",self.rows).get_input()
                
            self.cells[x][y]= Piece('BLACK') #input to board
            Gekitai.move(self,x,y)
            if Gekitai.game_over(self)== True:
                print ("Game over:")
                print(Gekitai.print(self))
                print("Player X wins!")
                exit()
            
            print(Gekitai.print(self))
        
            x, y= Player("RED",self.rows).get_input()
            while Gekitai.is_move_valid(self,x, y)==False:
                print("Invalid move!")
                x,y = Player("RED",self.rows).get_input()
                
            self.cells[x][y]= Piece("RED") #input to board
            Gekitai.move(self,x,y)
            if Gekitai.game_over(self)== True:
                print ("Game over:")
                print(Gekitai.print(self))
                print("Player O wins!")
                exit()
            
        
        
if __name__ == '__main__':
    game = Gekitai(6, 8, 3)
    game.start()