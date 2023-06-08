#Created by the spectacular sam. Minesweeper font made by someone else though.
import pygame, sys, time, random
pygame.init()

def make_lst(file_name):
    output = []
    file = open(file_name,"r")
    str_file = file.read()
    file.close()
    x = a = 0
    y = []
    for i in range(len(str_file)):
        if str_file[i] == "'":
            a = i+1
            while str_file[a] != "'" and a < len(str_file)-1:
                a += 1
            if x % 2 == 0:
                y.append(str_file[i+1:a])
            if len(y) == 2:
                output.append(y)
                y = []
            i = a
            x +=1           
    return(output)

def change_lst(lst,file_name):
    file = open(file_name,"w")
    file.write(str(lst))
    file.close()

def make_tuple(string):
    output = []
    x = False
    for i in range(len(string)):
        if string[i].isdigit() == True:
            x = True
        else:
            if x == True:
                a = i
                while string[a-1].isdigit() == True:
                    a = a-1
                output.append(int(string[a:i]))
                x = False
    return tuple(output)

#pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#pygame.display.set_mode((int(SETTINGS[1][1]),int(SETTINGS[2][1])))

def home_screen(options_needed):
    global screen, width_squares, height_squares
    screen = pygame.display.set_mode((int(SETTINGS[1][1]),int(SETTINGS[2][1])))  
    pygame.display.set_caption(SETTINGS[3][1]) 
    screen.fill(make_tuple(SETTINGS[6][1])) 
    a = 1
    width_squares = 0
    while a + int(SETTINGS[0][1]) + 1 < int(SETTINGS[1][1]):
        b = 1
        height_squares = 0 
        while b  + int(SETTINGS[0][1]) + 1 < int(SETTINGS[2][1]): 
            pygame.draw.rect(screen,make_tuple(SETTINGS[5][1]),(a,b,int(SETTINGS[0][1]),int(SETTINGS[0][1]))) 
            b = b + int(SETTINGS[0][1]) +1 
            height_squares += 1 
        a += int(SETTINGS[0][1]) + 1 
        width_squares += 1 
    option("MINESWEEPER",1,(0,0,0))
    if options_needed == True:
        option("PLAY",4,(0,0,0))
        option("SETTINGS",6,(0,0,0))
    pygame.display.update()

def text(text,text_colour,square_x,square_y,background_colour,update_needed):
    pygame.draw.rect(screen,background_colour,(square_x * int(SETTINGS[0][1]) + square_x - int(SETTINGS[0][1]),square_y * int(SETTINGS[0][1]) + square_y - int(SETTINGS[0][1]),int(SETTINGS[0][1]),int(SETTINGS[0][1])))
    font = pygame.font.Font("mine-sweeper.ttf",int(SETTINGS[7][1]))
    textsurface = font.render(text, True, text_colour)
    textrect = textsurface.get_rect()
    textrect.center = (square_x * int(SETTINGS[0][1]) - int(SETTINGS[0][1])//2 + square_x,square_y * int(SETTINGS[0][1]) - int(SETTINGS[0][1])//2 + square_y)
    screen.blit(textsurface, textrect)
    if update_needed == True:
        pygame.display.update()

def option(name,x,colour):
    for i in range(len(name)):
        text(name[i],colour,i+1+(width_squares-len(name))//2,x,make_tuple(SETTINGS[4][1]),False)

def refresh(settings):
    global SETTINGS
    SETTINGS = settings
    home_screen(True)
def check_neighbours(test,a,b):
    total = 0
    output = []
    if b > 0:
        output.append([a,b-1,1])
        if bombs[a][b-1] == 9:
            total += 1
    if b < len(bombs[a])-1:
        output.append([a,b+1,2])
        if bombs[a][b+1] == 9:
            total += 1
    if a > 0:
        output.append([a-1,b,3])
        if bombs[a-1][b] == 9:
            total +=1
        if b > 0:
            output.append([a-1,b-1,4])
            if bombs[a-1][b-1] == 9:
                total += 1
        if b < len(bombs[a])-1:
            output.append([a-1,b+1,5])
            if bombs[a-1][b+1] == 9:
                total += 1
    if a < len(bombs)-1:
        output.append([a+1,b,6])
        if bombs[a+1][b] == 9:
            total += 1
        if b > 0:
            output.append([a+1,b-1,7])
            if bombs[a+1][b-1] == 9:
                total += 1
        if b < len(bombs[a])-1:
            output.append([a+1,b+1,8])
            if bombs[a+1][b+1] == 9:
                total += 1
    if test == 9:
        return total
    elif test == 0:
        return output
    
def display_it(pos_x,pos_y):
    if showing[pos_y][pos_x] == 0 and pos_y != 0:
        showing[pos_y][pos_x] = 1
        if bombs[pos_y][pos_x] == 9:
            text("*",make_tuple(SETTINGS[10][1]),pos_x+1,pos_y+1,make_tuple(SETTINGS[4][1]),True)
            lose()
        elif bombs[pos_y][pos_x] == 0:
            text("",make_tuple(SETTINGS[10][1]),pos_x+1,pos_y+1,make_tuple(SETTINGS[4][1]),True)
            lst = check_neighbours(0,pos_y,pos_x)
            for i in range(len(lst)):
                if lst[i][0] != 0:
                    display_it(lst[i][1],lst[i][0])
        else:
            text(str(bombs[pos_y][pos_x]),make_tuple(SETTINGS[13+bombs[pos_y][pos_x]][1]),pos_x+1,pos_y+1,make_tuple(SETTINGS[4][1]),True)
        total = 0
        for a in range(len(showing)):
            for b in range(len(showing[a])):
                if showing[a][b] != 1:
                    total += 1
        if total == int(SETTINGS[8][1])+width_squares:
            win()
def create_lsts():
    global bombs, showing
    mines = random.sample(range(0,width_squares*(height_squares-1)),int(SETTINGS[8][1]))
    mines.sort()
    a = []
    b = []
    for i in mines:
        a.append(i//width_squares+1)
        b.append(i-(i//width_squares*width_squares))
    a.append(height_squares+100)
    b.append(width_squares+100)
    i = []
    s = []
    bombs = []
    showing = []
    c = 0
    for y in range(height_squares):
        for x in range(width_squares):
            if a[c] == y and b[c] == x:
                i.append(9)
                s.append(0)
                c += 1
            else:
                i.append(0)
                s.append(0)
        bombs.append(i)
        showing.append(s)
        i = []
        s = []
    for a in range(len(bombs)):
        for b in range(len(bombs[a])):
            if bombs[a][b] == 0 and a != 0:
                bombs[a][b] = check_neighbours(9,a,b)
                
def start():
    global bombs, showing
    home_screen(False)
    pygame.display.update()
    x = hold(False,True)
    create_lsts()
    if x != None:
        while bombs[x[0]][x[1]] != 0:
            create_lsts()
        display_it(x[1],x[0])
        
def win():
    option("MINESWEEPER",1,(0,250,0))
    pygame.display.update()
    hold(True,False)
    
def lose():
    global running, playing
    option("MINESWEEPER",1,make_tuple(SETTINGS[11][1]))
    for a in range(len(bombs)):
        for b in range(len(bombs[a])):
            if bombs[a][b] == 9:
                if showing[a][b] == 2:
                    text("`",make_tuple(SETTINGS[13][1]),b+1,a+1,make_tuple(SETTINGS[5][1]),False)
                else:
                    text("*",make_tuple(SETTINGS[12][1]),b+1,a+1,make_tuple(SETTINGS[5][1]),False)
    pygame.display.update()
    hold(True,False)

def hold(win_lose,safe_start):
    global playing, running 
    internal = True
    while internal == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                internal = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = False
                    internal = False
                elif event.key == pygame.K_r or event.key == pygame.K_RETURN:
                    start()
                    internal = False
                elif event.key == pygame.K_b or event.key == pygame.K_m:
                    home_screen(True)
                    playing = False
                    internal = False
                elif event.key == pygame.K_x:
                    a = make_lst("settings - Copy.txt")
                    file = open("settings.txt","w")
                    file.write(str(a))
                    file.close()
                    refresh(make_lst("settings.txt"))
                    playing = False
                    internal = False
            elif event.type == pygame.MOUSEBUTTONUP and win_lose == True:
                start()
                internal = False
            elif event.type == pygame.MOUSEBUTTONUP and win_lose == False:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if playing != True:
                    if int(SETTINGS[0][1])*3+3 < mouse_y < int(SETTINGS[0][1])*4+6 and (width_squares - 4) // 2*int(SETTINGS[0][1])-1< mouse_x < ((width_squares - 4) // 2+4)*int(SETTINGS[0][1])-1:
                        playing = True
                        start()
                        internal = False
                else:
                    x_axis = mouse_x//(int(SETTINGS[0][1])+1)
                    y_axis = mouse_y//(int(SETTINGS[0][1])+1)
                    if event.button == 1:
                        if 0 <= y_axis <= height_squares-1 and 0<= x_axis <= width_squares-1 and safe_start == False:
                            display_it(x_axis,y_axis)
                            internal = False
                        elif 0 <= y_axis <= height_squares-1 and 0<= x_axis <= width_squares-1:
                            return y_axis,x_axis
                    if event.button == 3:
                        if 0 <= y_axis <= height_squares-1 and 0<= x_axis <= width_squares-1 and showing[y_axis][x_axis] != 1:
                            if showing[y_axis][x_axis] == 0:
                                showing[y_axis][x_axis] = 2
                                text("`",make_tuple(SETTINGS[9][1]),x_axis+1,y_axis+1,make_tuple(SETTINGS[5][1]),True)
                                total = 0
                                for a in range(len(showing)):
                                    for b in range(len(showing[a])):
                                        if showing[a][b] == 2 and bombs[a][b] == 9:
                                            total += 1
                                if total == int(SETTINGS[8][1]):
                                    win() 
                                internal = False
                            elif showing[y_axis][x_axis] == 2:
                                text("",make_tuple(SETTINGS[9][1]),x_axis+1,y_axis+1,make_tuple(SETTINGS[5][1]),True)
                                showing[y_axis][x_axis] = 0
                                internal = False
                    
refresh(make_lst("settings.txt"))
playing = False
running = True
while running == True:
    hold(False,False)
