class texts():
#Makes the text parse with a cursor blink


    def __init__(self, x, speed):
        #Makes an object
        self.x, self.y, self.text, self.font, self.rgb, self.anchor = x
        self.increment = 0
        self.speed = speed
        self.skip = 0


        
    def drawText(self, canvas):
        #Draws the text based on how high the increment is (parses through)
        textcursor = ""
        increment = int(self.increment//20*self.speed)
        if self.increment // 10% 2 == 1:
            textcursor = "|"
        canvas.create_text(self.x, self.y, text = self.text[:increment+self.skip]+textcursor, fill = self.rgb, font = self.font, anchor = self.anchor)


        
    def incrementer(self, num):
        #Updates increment
        self.increment = self.increment + num


