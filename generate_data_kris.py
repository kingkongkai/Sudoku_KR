import numpy as np

rows_wave_centered = np.ones((9,9))
for row in range(9):
	if row < 5:
		rows_wave_centered[row] *= row+1
	else:
		rows_wave_centered[row] *= 9-row
# print rows_wave_centered
rows_wave_centered /= sum(rows_wave_centered)



left_rows = np.ones((9, 9))
for row in range(3):
	left_rows[row] *= 3
# print left_rows
left_rows /= sum(left_rows)


center_rows = np.ones((9,9))
for row in range(3,6):
	center_rows[row] *= 3
# print center_rows
center_rows /= sum(center_rows)







bla = np.zeros((9,9))

def fill_blocks(grid, blocks, value):
	for row in range(9):
		for col in range(9):
			for block in blocks:
				if row in [3*block[0]+x for x in range(3)] and col in [3*block[1]+x for x in range(3)]:
					grid[row,col] = value

	return grid

print fill_blocks(bla, [(0,0), (2,1)], 3)