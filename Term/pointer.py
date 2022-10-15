class Pointer():
#Makes a button


    def __init__(self, x0, y0, x1, y1, x, y, text):
        #Makes button
        self.rectangle = x0, y0, x1, y1
        self.expanded = x0 - x, y0 - y, x1 + x, y1 + y
        self.text = text
        self.expand = False



    def drawRectangle(self, canvas):
        #Draws a button
        x0, y0, x1, y1 = self.rectangle
        if self.expand:
            x0, y0, x1, y1 = self.expanded
        width = x1 - x0
        height = y1 - y0
        margin = min(width, height)/10
        canvas.create_rectangle(x0-margin, y0-margin, x1+margin, y1+margin, fill = "cyan", outline = "cyan")
        canvas.create_rectangle(x0, y0, x1, y1, outline = "black", fill = "black")
        canvas.create_text(x0 + width/2, y0 + height/2, text = self.text, fill = "cyan", font = ("Ubuntu", int(min(width, height)/2), "bold"))



    def givePointer(self):
        #Gives the bounding coordinates
        if self.expand:
            return self.expanded
        else:
            return self.rectangle



    def inPoint(self, x, y):
        #Checks if x and y are inside the button
        x0, y0, x1, y1 = self.rectangle
        if self.expand:
            x0, y0, x1, y1 = self.expanded
        return x0 <= x <= x1 and y0 <= y <= y1
    


