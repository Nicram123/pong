from turtle import Turtle
import _tkinter

class Ball(Turtle):
  def __init__(self):
    super().__init__()
    self.color('white')
    self.shape('circle')
    self.penup()
    self.x_move = 10
    self.y_move = 10
    self.move_speed = 0.1
    
  def move(self):
    try:
      new_x = self.xcor() + self.x_move
      new_y = self.ycor() + self.y_move
      self.goto(new_x, new_y)
    except _tkinter.TclError as e:
            print(f"Błąd: {e}. Sprawdź, czy ekran turtle jest nadal otwarty.")
  
  def bounce_y(self):
    self.y_move *= -1
    
  def bounce_x(self):
    self.x_move *= -1
    self.move_speed *= 0.9
    
  def reset_position(self):
    self.goto(0,0)
    self.move_speed = 0.1
    self.bounce_x()
    
    
                                  