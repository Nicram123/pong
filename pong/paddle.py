from turtle import Turtle

class Paddle(Turtle):
  def __init__(self, corr):
    super().__init__()
    self.x = corr[0]
    self.y = corr[1]
    self.shape('square')
    self.color('white')
    self.shapesize(stretch_wid=5, stretch_len=1)  # domyslnie 20 na 20, a wiec mamy 100 na 20 
    self.penup() # nie rysuje bialej lini 
    self.goto(self.x, self.y) # # przesuwa objekt o 350 wzdluz osi x w prawo 
  
  def go_up(self):
    new_y = self.ycor() + 20
    self.goto(self.xcor(), new_y)
    
  def go_down(self):
    new_y = self.ycor() - 20
    self.goto(self.xcor(), new_y) # nie zmiennie os x , nowe y 