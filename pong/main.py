from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
import time
from scoreboard import Scoreboard
import socket
import pickle
import _tkinter
import server

screen = Screen()
screen.bgcolor('black')
screen.setup(width=800, height=600)
#screen.title('Pong')
screen.tracer(0) # wylaczenie animacji 

FORMAT = 'utf-8'
HEADER = 70
PORT = 4900
SERVER = '192.168.118.124'
ADDR = (SERVER, PORT) 

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()


screen.listen() # nasluchuje na wcisniete klawisze 
screen.onkey(r_paddle.go_up, 'Up') # funkcja wywolana po wcisnieciu gornej strzalki 
screen.onkey(r_paddle.go_down, 'Down') # 


screen.listen() # nasluchuje na wcisniete klawisze 
screen.onkey(l_paddle.go_up, 'w') # funkcja wywolana po wcisnieciu gornej strzalki 
screen.onkey(l_paddle.go_down, 's') # 




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.setblocking(False)

def send(msg):
  message = pickle.dumps(msg)
  message_len = len(message)
  send_len = str(message_len).encode(FORMAT)
  send_len += b' ' * ( HEADER - len(send_len) )
  client.send(send_len + message)

def receive_data():
  try:
    data_header = client.recv(HEADER).decode(FORMAT)
    if data_header:
      print('eluwina')
      data_len = int(data_header.strip())
      serialized_data = b""
      while len(serialized_data) < data_len:
        serialized_data += client.recv(data_len - len(serialized_data))
      obj = pickle.loads(serialized_data)
      return obj
    return None
  except Exception as e:
    return None
    
def update_game_state(state):
    ball.setx(state['ball'][0])
    ball.sety(state['ball'][1])
    l_paddle.setx(state['l_paddle'][0])
    l_paddle.sety(state['l_paddle'][1])
    r_paddle.setx(state['r_paddle'][0])
    r_paddle.sety(state['r_paddle'][1])
    scoreboard.l_score = state['scores'][0]
    scoreboard.r_score = state['scores'][1]
    #screen = state['screen']
    scoreboard.update_scoreboard()
    
    



# zawsze gdy wylaczamy animacje trzeba updatowac po nic nie bedzie widoczne 
try:
  game_is_on = True
  iteration = 0
  clients = server.return_clients()
  while game_is_on and len(clients) > 1:
    time.sleep(0.1)
    #ball.move_speed
    screen.update()
    ball.move()
    
    
    # Detect collision with wall 
    if ball.ycor() > 280 or ball.ycor() < -280:
      # needs to bounce
      ball.bounce_y()
      
    # Detect collision with paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
      ball.bounce_x()
      
    # Detect R paddle missed 
    if ball.xcor() > 380:
      ball.reset_position()
      scoreboard.l_point()
    
    # Detect L paddle missed
    if ball.xcor() < -380:
      ball.reset_position()
      scoreboard.r_point()
      
    game_state = {
          'ball': (ball.xcor(), ball.ycor()),
          'l_paddle': (l_paddle.xcor(), l_paddle.ycor()),
          'r_paddle': (r_paddle.xcor(), r_paddle.ycor()),
          'scores': (scoreboard.l_score, scoreboard.r_score),
          
      }
      
    send(game_state)
    #if time.time() % 0.1 < 0.01:  # Odbieranie danych co 100 ms

    updated_state = receive_data()
    if updated_state:
        print('elllllooooo')
        update_game_state(updated_state)
        
    time.sleep(0.01) 
except _tkinter.TclError as e:
    print(f"Błąd: {e}. Ekran turtle został zamknięty.")
finally:
    screen.bye()

screen.exitonclick() 