import tkinter
import random
from colorama import init, Fore, Style

BG_SIZE  = 500
BG_COLOR = '#BCAEA2'

PADDING_SIZE = 10
CELL_SIZE = (BG_SIZE-(5*PADDING_SIZE))/4
TEXT_SIZE_HEIGHT = 2
TEXT_SIZE_WIDTH = 4

CELL_COLOR_EMPTY = '#CDC1B3'
CELL_COLOR = {'2':'#eee4da', '4':'#ede0c8', '8':'#f2b179', '16':'#f59563',
              '32':'#f67c5f', '64':'#f65e3b', '128':'#edcf72', '256':'#edcc61',
              '512':'#edc850', '1024':'#edc53f', '2048':'#edc22e', '4096':'#eee4da',
              '8192': '#edc22e', '16384':'#f2b179', '32768':'#f59563', '65536':'#f67c5f'}
              
FONT_COLOR  = {'2':'#776e65', '4':'#776e65', '8':'#f9f6f2', '16':'#f9f6f2',
              '32':'#f9f6f2', '64':'#f9f6f2', '128':'#f9f6f2', '256':'#f9f6f2',
              '512':'#f9f6f2', '1024':'#f9f6f2', '2048':'#f9f6f2', '4096':'#776e65',
              '8192':'#f9f6f2', '16384':'#776e65', '32768':'#776e65', '65536':'#f9f6f2'}

def title_frame():
    global label_score
    top_frame = tkinter.Frame(root, bg='#FBF8EF', width=655, height=100)
    label = tkinter.Label(top_frame, text='2048', font=('clear sans', 50, 'bold'), fg='#706E62', bg='#FBF8EF')
    label_score = tkinter.Label(top_frame, text='0', font=('clear sans', 50, 'bold'), fg='#706E62', bg='#FBF8EF')
    
    top_frame.pack()
    label.place(relx=0.05, rely=0.060)
    label_score.place(relx=0.6, rely=0.060)

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
            grid_row.append(number)
            
        grid_cells.append(grid_row)

def text_extract(lst):
    temp = []
    for i in range(4):
        num_row = [lst[i][j]['text'] for j in range(4)]
        temp.append(num_row)
    return temp

# merging two cells with the same value
def merge_cells(grid_object, opt):
    list_numbers = text_extract(grid_object)
    
    if opt == 'Right':
        for i in range(4):
            for j in range(3, -1, -1):
                if j == 0:
                    continue
                if (list_numbers[i][j] == list_numbers[i][j-1]) and (list_numbers[i][j] != ''):
                    list_numbers[i][j] = str(int(list_numbers[i][j])*2)
                    list_numbers[i][j-1] = ''
                    try:
                        label_score['text'] = str(int(label_score['text'])+int(list_numbers[i][j]))
                    except:
                        pass
    elif opt == 'Left':
        for i in range(4):
            for j in range(4):
                if j == 3:
                    continue
                if (list_numbers[i][j] == list_numbers[i][j+1]) and (list_numbers[i][j] != ''):
                    list_numbers[i][j] = str(int(list_numbers[i][j])*2)
                    list_numbers[i][j+1] = ''
                    try:
                        label_score['text'] = str(int(label_score['text'])+int(list_numbers[i][j]))
                    except:
                        pass
    
    global grid_cells
    grid_cells = fusion_matrix(grid_object, list_numbers)

# comparing the grid object and a matrix with text in it
# and changing the label value of grid object based on the matrix's texts
def fusion_matrix(grid_object, matrix_text):
    for i in range(4):
        for j in range(4):
            if matrix_text[i][j] != '':
                NUM = matrix_text[i][j]
                grid_object[i][j].config(text=NUM, fg=FONT_COLOR[NUM], bg=CELL_COLOR[NUM])
            else:
                grid_object[i][j].config(text='', bg=CELL_COLOR_EMPTY)

    return grid_object
    
def grid_sort(lst, opt):
    global grid_cells
    zeroes = []
    temp = text_extract(lst)
    
    for i in range(4):
        zero_row = []
        while True:
            try:
                temp[i].pop(temp[i].index('')) # omits all zero in the list
                zero_row.append('')
            except:
                break
        zeroes.append(zero_row)
    for i in range(4):
        if opt == 'Right':
            temp[i] = zeroes[i]+temp[i]
        elif opt == 'Left':
            temp[i] = temp[i]+zeroes[i]

    # comparing the sorted list with
    # the actual list that has the num and cell data   
    grid_cells = fusion_matrix(lst, temp)

def transpose(lst):
    new_matrix = []
    for i in range(4):
        temp = [lst[j][i] for j in range(4)]
        new_matrix.append(temp)

    return new_matrix

def print_grid(lst):
    grid = text_extract(grid_cells)
    for i in range(4):
        print('[ ', end='')
        for j in range(4):
            if grid[i][j]=='':
                print('0, ', end='')
            else:
                print(Fore.GREEN + grid[i][j] + Style.RESET_ALL + ', ', end='')
        print(']')
    print()

def check_status(grid_object):
    temp = text_extract(grid_object)
    for i in range(4):
        try:
            temp[i].index('')
            return False
        except:
            continue
        
    return True
    
def update_grid(event):
    global grid_cells
    grid_before_state = text_extract(grid_cells)
    
    if event.keysym == 'Right':
        print('<Right>')
        grid_sort(grid_cells, 'Right')
        merge_cells(grid_cells, 'Right')
        grid_sort(grid_cells, 'Right')
    elif event.keysym == 'Left':
        print('<Left>')
        grid_sort(grid_cells, 'Left')
        merge_cells(grid_cells, 'Left')
        grid_sort(grid_cells, 'Left')
    elif event.keysym == 'Down':
        print('<Down>')
        grid_sort(transpose(grid_cells), 'Right')
        merge_cells(grid_cells, 'Right')
        grid_sort(grid_cells, 'Right')
        grid_cells = transpose(grid_cells)
    elif event.keysym == 'Up':
        print('<Up>')
        grid_sort(transpose(grid_cells), 'Left')
        merge_cells(grid_cells, 'Left')
        grid_sort(grid_cells, 'Left')
        grid_cells = transpose(grid_cells)
        
    # generate random cell
    # only generate new cell if the pre-existing cell structure isn't the same as before
    if grid_before_state != text_extract(grid_cells):
        while True:
            row, column = random_pos()
            if grid_cells[row][column]['text'] == '':
                NUM = num_gen()
                grid_cells[row][column].config(text=NUM, fg=FONT_COLOR[NUM], bg=CELL_COLOR[NUM])
                break

    print_grid(grid_cells)
    
# ---- main ----
root = tkinter.Tk()
root.title('2048')
root.geometry('655x670')
root.resizable(0, 0)

background = tkinter.Frame(root, bg=BG_COLOR, width=BG_SIZE, height=BG_SIZE)
background.focus_set()
background.pack(side='bottom')

game_start()
title_frame()

background.bind('<Right>', update_grid)
background.bind('<Left>', update_grid)
background.bind('<Down>', update_grid)
background.bind('<Up>', update_grid)

root.mainloop()
    




