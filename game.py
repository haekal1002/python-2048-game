import tkinter
import random

BG_SIZE  = 500
BG_COLOR = '#BCAEA2'

PADDING_SIZE = 10
CELL_SIZE = (550-(5*PADDING_SIZE))/4
TEXT_SIZE_HEIGHT = 2
TEXT_SIZE_WIDTH = 4

CELL_COLOR_EMPTY = '#CDC1B3'
FONT_COLOR = {'2':'#746C61', '4':'#746C61'}
CELL_COLOR = {'2':'#EEE4DA', '4':'#ECE0C6'}

def num_gen():
    return '2' if random.randint(1, 10) < 10 else '4'

def random_pos():
    # generate random position for row and column
    return [random.randint(0, 3) for i in range(2)]

def game_start():
    global grid_cells
    grid_cells = []

    # making sure the random position is not the same
    while True:
        row1, column1 = random_pos()
        row2, column2 = random_pos()
        if (row1, column1) != (row2, column2):
            break
        else:
            continue
        
    print('({}, {}), ({}, {})'.format(row1, column1, row2, column2))

    for i in range(4): # row / y
        grid_row = []
        for j in range(4):# column / x
            cell = tkinter.Frame(background, width=CELL_SIZE, height=CELL_SIZE)
            if ((i, j)==(row1, column1)) or ((i, j)==(row2, column2)):
                NUM = num_gen()
                number = tkinter.Label(cell, text=NUM, justify='center',
                                        font=('clear sans', 38, 'bold'), fg=FONT_COLOR[NUM], 
                                        width=TEXT_SIZE_WIDTH, height=TEXT_SIZE_HEIGHT, bg=CELL_COLOR[NUM])                
            else:
                number = tkinter.Label(cell, text='', justify='center',
                                        font=('clear sans', 38, 'bold'), 
                                        width=TEXT_SIZE_WIDTH, height=TEXT_SIZE_HEIGHT, bg=CELL_COLOR_EMPTY)
            
            cell.grid(row=i, column=j, padx=PADDING_SIZE, pady=PADDING_SIZE)
            number.grid()
                      
            grid_row.append([number, cell])
            
        grid_cells.append(grid_row)

def grid_sort(lst, opt):
    temp = [num[0]['text'] for num in lst]
    zeroes = []
    while True:
        try:
            temp.pop(temp.index('')) # omits all zero in the list
            zeroes.append('')
        except:
            break
        
    if opt == 'Right':
        temp = zeroes+temp
    elif opt == 'Left':
        temp = temp+zeroes
        
    # comparing the sorted list with the actual list that has the num and cell data
    for i in range(4):
        if temp[i] != '':
            NUM = temp[i]
            lst[i][0].config(text=NUM, fg=FONT_COLOR[NUM], bg=CELL_COLOR[NUM])
        else:
            lst[i][0].config(text='', bg=CELL_COLOR_EMPTY)
            
    return lst
    
def update_grid(event):
    global grid_cells
    if event.keysym == 'Right':
        lst1 = grid_sort(grid_cells[0], 'Right')
        lst2 = grid_sort(grid_cells[1], 'Right')
        lst3 = grid_sort(grid_cells[2], 'Right')
        lst4 = grid_sort(grid_cells[3], 'Right')
        grid_cells = [lst1, lst2, lst3, lst4]
        
    elif event.keysym == 'Left':
        lst1 = grid_sort(grid_cells[0], 'Left')
        lst2 = grid_sort(grid_cells[1], 'Left')
        lst3 = grid_sort(grid_cells[2], 'Left')
        lst4 = grid_sort(grid_cells[3], 'Left')
        grid_cells = [lst1, lst2, lst3, lst4]

    # generate random cell
    row, column = random_pos()
    if grid_cells[row][column][0]['text'] == '':
        NUM = num_gen()
        grid_cells[row][column][0].config(text=NUM, fg=FONT_COLOR[NUM], bg=CELL_COLOR[NUM])
        print('Generate a \'{}\' at ({}, {})'.format(NUM, row, column))
                
    
# ---- main ----
root = tkinter.Tk()
root.title('2048')
root.resizable(0, 0)

background = tkinter.Frame(root, bg=BG_COLOR, width=BG_SIZE, height=BG_SIZE)
background.focus_set()
background.grid()
    
game_start()

background.bind('<Right>', update_grid)
background.bind('<Left>', update_grid)
#print(type(grid_cells[0]['text']))

root.mainloop()
    




