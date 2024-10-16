from logging import exception
from time import sleep
import numpy as np

searching_vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
# MAX limits the size of the board because it is specified in the 'descubre' exercise section
# The rest of the functions treat the matrix as a dynamic matrix
MAX = 8
game_table = np.zeros((MAX, MAX), dtype=int)

#This function counts the number of mines near the selected cell recursively using 'searching_vectors' vectors
def how_many_mines(table, i, j, search_vectors, c=0):
    if not search_vectors:
        return c
    else:
        ni, nj = i + search_vectors[0][0], j + search_vectors[0][1]
        if 0 <= ni < table.shape[0] and 0 <= nj < table.shape[1]:
            if table[ni,nj] == -1:
                c += 1
        return how_many_mines(table, i, j, search_vectors[1:], c)

#This function edits the minesweeper table to create the table that shows where are the bombs to the client.
def count_cell_mines(table,i=0,j=0):
    if table[i][j] != -1:
        table[i][j] = how_many_mines(table,i,j,searching_vectors)
    if i < table.shape[0] - 1:
        i = i + 1
        return count_cell_mines(table,i,j)
    else:
        if j < table.shape[1] - 1:
            i = 0
            j = j + 1
            return count_cell_mines(table,i,j)
        else:
            return table

#This function replace the values of the selected depending on the value of the cell
def descubre(table,i,j):
    if table.shape != (8, 8):
        exception('Table dimensions are incorrect')
        return True, table
    else:
        table_aux = table.copy()
        #Me veo obligado a hacer una copia de table ya que por lo visto el parámetro se envía por referencia
        minesweeper_table =  count_cell_mines(table_aux)
        del table_aux

        def mine_near():
            game_table[i][j] = -2
            return False, table

        def no_mines():
            region = minesweeper_table[max(0, i - 1):min(i + 2, 8),max(0, j - 1):min(j + 2, 8)]
            table[max(0, i - 1):min(i + 2, 8), max(0, j - 1):min(j + 2, 8)] = region
            #No entiendo bien el warning del segundo parámetro
            region = np.where(region == -1, 0, region)
            game_table[max(0, i - 1):min(i + 2, 8), max(0, j - 1):min(j + 2, 8)] = region
            return False, table

        def mine():
            return True, table

        switch = [
            (lambda x: x == -1, mine),
            (lambda x: x == 0, no_mines),
            (lambda x: x > 0, mine_near)
        ]

        def evaluate_cases(value):
            for case, action in switch:
                if case(value):
                    return action()
            return True, table

        return evaluate_cases(table[i][j])

#This function is the mail function of the game
def minesweeper():
    table = np.random.randint(-1, 1, size=(MAX, MAX))
    finish = False
    print('MINESWEEPER\n\n')
    sleep(1)
    print('\nTHESE ARE THE MINES')
    print(table)
    sleep(3)
    print('\nTHIS IS YOUR GAME')
    print(game_table)
    sleep(1)
    while not finish:
        try:
            j, i = 0, 0

            while True:
                try:
                    i = int(input('\nIntruduce row :'))
                    j = int(input('Intruduce column :'))
                    if i < MAX and j < MAX:
                        break
                    else:
                        print(f"Out of bounds!\n")
                except ValueError as e:
                    print(f"Error: {e}. Please input a valid number.")

            if i >= MAX or j >= MAX:
                raise ValueError
            finish, table = descubre(table, i, j)
            print("\n")

            if finish:
                print(table)
                print("BOOOOOOOOOOOMMM YOU LOST")
            else:
                print("CONTINUE!\n")
                print(game_table)
            sleep(1)

        except ValueError as e:
            print(f"Error: {e}. Please input a valid number.")


minesweeper()
