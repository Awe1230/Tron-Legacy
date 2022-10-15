class Enemy():
#Creates the enemy


    @staticmethod
    def isin(t, x):
        #Checks if t: (a, b) is in x (a, b, c, d, e)
        for i in x:
            if t == i[:2] or t == i[2:5]:
                return True
        return False


        
    def __init__(self, x, y, z, s, scale, numbers, trail):
        #Makes an enemy
        self.pX = x
        self.pY = y
        self.pZ = z
        self.trail = trail
        self.cardinal = 0
        self.pS = s
        self.scale = scale
        self.alive = True
        self.numbers = numbers
        self.pastX = self.pX
        self.pastZ = self.pZ
        self.playerT = [self.pastX, self.pastZ, self.pX, self.pZ, "orange"]
        trail.append(self.playerT)
        self.change = False



    def move(self):
        #Moves the enemy with speed pS based on cardinal
        if self.alive:
            if self.cardinal % 2 == 1:
                if self.cardinal % 4 == 1:
                    self.pX = self.pX + self.pS
                else:
                    self.pX = self.pX - self.pS
            else:
                if self.cardinal % 4 == 0:
                    self.pZ = self.pZ + self.pS
                else:
                    self.pZ = self.pZ - self.pS


                    
    def simulate(self):
        #Simulates a move
        x, z = self.pX, self.pZ
        if self.cardinal % 2 == 1:
            if self.cardinal % 4 == 1:
                x = x + self.pS*10
            else:
                x = x - self.pS*10
        else:
            if self.cardinal % 4 == 0:
                z = z + self.pS*10
            else:
                z = z - self.pS*10
        return x, z



    def changeCardinal(self):
        #Changes the direction of the enemy
        self.cardinal = self.cardinal - 1



    def guess(self):
        #Makes sure the enemy does not go off the grid
        if (abs(abs(self.pX) - self.numbers) < 32 and self.cardinal % 2 == 1) or (abs(self.pZ - self.numbers) < 32 and self.cardinal % 4 == 0) or (abs(self.pZ) < 32 and self.cardinal % 4 == 2):
            self.change = True



    def produceTrail(self):
        #Adds on to the trail
        if self.alive:
            if self.pX % (self.scale) == self.pZ % (self.scale) == 0:
                self.trail.append((self.pX, self.pZ, self.pastX, self.pastZ, "orange"))
                self.pastX, self.pastZ = self.pX, self.pZ
            self.playerT[:4] = [self.pastX, self.pastZ, self.pX, self.pZ]



    def doesItIntersect(self):
        #Checks if the enemy hit the trail
        if abs(self.pX) > self.numbers or self.pZ < 0 or self.pZ > self.numbers:
            self.alive = False
        if Enemy.isin((self.pX, self.pZ), self.trail):
            self.alive = False
            
    

        
    