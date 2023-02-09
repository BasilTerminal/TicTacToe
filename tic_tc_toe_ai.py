# tic tac toe
import turtle as t
from random import randint
CELL = 100 # size of cell


#s=t.Screen()
s=t.getscreen()
t.tracer(0)
t.setup(width=CELL*5, height=CELL*5)
#t.screensize(CELL*5,CELL*5)
t.setworldcoordinates(-40, -40, CELL*3+40, CELL*3+40)
t.title("Хрестики-Нолики")

# размер в клетках для игрового поля
dim = 3
# ігрове поле заповнюється Х=1 О=-1
field = [0,0,0,
         0,0,0,
         0,0,0]

win = 0 # флажок хто виграв: 1:Х, -1:О, 0-нема

def drawcross(x,y):
    t.home()
    t.goto(x*CELL+CELL/2,y*CELL+CELL/2) # centr of cell

    t.goto(x*CELL+CELL/2-CELL/4,y*CELL+CELL/2-CELL/4)
    t.left(45)
    t.pendown()
    t.forward(CELL/2*1.4)
    t.penup()

    t.goto(x*CELL+CELL/2-CELL/4,y*CELL+CELL/2+CELL/4)
    t.right(90)
    t.pendown()
    t.forward(CELL/2*1.4)
    t.penup()

def drawzero(x,y):
    t.home()
    t.goto(x*CELL+CELL/2,y*CELL+CELL/4)

    t.pendown()
    t.circle(CELL/4)
    t.penup()

def check_win(field):
    ''' Перевіряється чи існує виграш
        Повертає 1 якщо виграли Х
        Повертає -1 якщо виграли О
        Повертає 0 якщо нема '''
        
    win_combination = (
        (0,1,2), (3,4,5), (6,7,8),# горизонтальные линии
        (0,3,6), (1,4,7), (2,5,8),# вертикальные линии
        (0,4,8), (2,4,6)# диагональные линии
    )
    for pos in win_combination:
        s = field[pos[0]] + field[pos[1]] + field[pos[2]]
        if s == 3:
            #print("Виграли X!")
            return 1
        elif s == -3:
            #print("Виграли 0!")
            return -1
    return 0
        
def draw_board():
    ''' Выводим игровое поле в консоль '''
    print(('_' * 8 * dim ))
    for i in range(dim-1,-1,-1):
        print (field[i*3], '\t', field[i*3+1], '\t', field[i*3+2])

def draw_XO():
    ''' малюємо на полі хрестики та нолики '''
    for x in range(dim):
        for y in range(dim):
            if field[y*dim+x] == 1:
                drawcross(x,y)
            elif field[y*dim+x] == -1:
                drawzero(x,y)

    
def check_hit(x,y):
    ''' перевіряємо чи клацнули по полі
        якщо ні повертаємо 99, (бо False приймає як 0)
        вираховуємо номери клітки
        повертаємо індекс'''
    # перевіряємо чи клацнули по полі
    if x < 0 or x > CELL*3 or y < 0 or y > CELL*3:
        return 99 # за межами полю

    # вираховуємо номери клітки
    i=int(x/CELL) # стовпчик Х
    j=int(y/CELL) # рядок У
    
    return j*dim+i

def check_restart(x,y):
    ''' перевіряємо клік по кнопкі '''
    if x > 0 and x < CELL*3 and y > -40 and y < -20 :
        return True
    return False
    
def computer_step(field):
    ''' хід компютера
        повертає номер клітини
    '''
    # створюю список вільних клітин
    available_steps = [i for i in range(dim*dim) if field[i] == 0]

    ''' Шукаємо самий близький виграшний свій ход '''
    for pos in available_steps:
        field_1 = field[:]
        field_1[pos] = -1 # ходим ноликом
        if check_win(field_1) == -1:
            return pos # знайшли, виходимо

    ''' Шукаємо самий близький виграшний чужий ход '''
    for pos in available_steps:
        field_1 = field[:]
        field_1[pos] = 1 # ходим хрестиком
        if check_win(field_1) == 1:
            return pos # знайшли, перехопили, виходимо
    

    # Якщо не знайшли найближчий виграшний хід, то робимо глибший пошук
    win_steps = (4, 0, 2, 6, 8, 1, 3, 5, 7) # список пріоритетних ходів
    for pos in win_steps: # перебираємо пріоритетні клітини
        if (pos in available_steps):
            return pos # знайшли, виходимо

def draw_text(text,x,y):
    ''' Робимо надпис на вказаних координатах '''
    t.up()
    t.goto(x,y)
    t.write(text,align='center',font=("Arial", 16, "normal"))

def draw_button_restart():
    ''' малюємо кнопку СПОЧАТКУ '''
    w=CELL*3 # ширина кнопки
    h=20 # висота кнопки
    t.color("black", "green")
    t.up()
    t.home()
    t.goto(0,-h)
    t.down()
    t.begin_fill()
    t.forward(w)
    t.right(90)
    t.forward(h)
    t.right(90)
    t.forward(w)
    t.right(90)
    t.forward(h)
    t.up()
    t.end_fill()
    draw_text("Спочатку",CELL*1.5,-h*2) # посередині і знизу


def myhit(x,y):
    ''' Обробка клика '''
    global win, field
    
    if check_restart(x,y) == True:
        print("Restart")
        win=0
        field = [0,0,0,0,0,0,0,0,0]
        draw_field()
        return
        
    if win != 0: # якщо вже виграли
        return

    if check_hit(x,y) == 99: # не в просторі поля
        return

    pos = check_hit(x,y)
    
    # перевіряємо чи вільно і ставимо свій хід хрестом
    if field[pos]==0:
        field[pos]=1
    else:# тут клацнули по зайнятій клітці
        return
    win=check_win(field)
    draw_XO() # малюємо поле
    if win == 1:
        draw_text("Виграли X!",CELL*1.5,CELL*3+20) # посередині і зверху)
        draw_button_restart()
        return
  

    # хід компьютера
 
    available_steps = [i for i in range(dim*dim) if field[i] == 0]
    if len(available_steps) == 0:
        draw_text("Ничія !",CELL*1.5,CELL*3+20) # посередині і зверху
        print("GAME OVER!")
        draw_button_restart()
        return

    # Тут є вільні клітки. Комп починає думати....
    field[computer_step(field)]=-1

    # кінець думання компа
    win=check_win(field)
    draw_XO() # малюємо поле
    if win == -1:
        draw_text("Виграли O!",CELL*1.5,CELL*3+20) # посередині і зверху
        draw_button_restart()
        return
    # друкуємо поле в консолі
    draw_board()
    
def draw_field():
    ''' малюємо поле '''

    t.reset()
    t.home()
    t.pensize(1)
    t.left(90)
    t.up()
    for i in range(4):
        t.goto(i*CELL,0)
        t.down()
        t.forward(CELL*3) # вертикальні лінії
        t.up()
    t.home()
    for i in range(4):
        t.goto(0,i*CELL)
        t.down()
        t.forward(CELL*3) # горизонтальні лінії
        t.up()

if __name__ == "__main__":
    draw_field() # малюємо поле
    s.onclick(myhit)
    t.done()
