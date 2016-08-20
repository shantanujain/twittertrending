from random import randint
import heapq
import collections
import time
import plotly as py
import plotly.graph_objs as go




compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

datasetA = []
datasetB = []
datasetC = []

hash_tableA10 = {}
hash_tableB10 = {}
hash_tableC10 = {}

hash_tableA40 = {}
hash_tableB40 = {}
hash_tableC40 = {}

hash_tableA70 = {}
hash_tableB70 = {}
hash_tableC70 = {}

hash_tableA100 = {}
hash_tableB100 = {}
hash_tableC100 = {}

hash_tableA150 = {}
hash_tableB150 = {}
hash_tableC150 = {}



######################## Generating Datasets ########################

def createDataset(dataset, n1, start1, end1, check, n2, start2, end2):
	
	for i in range(0, n1):
		x = randint(start1, end1)
		y = randint(start1, end1)
		pt = [x, y]
		dataset.append(pt)
	
	if check:
		for i in range(0, n2):
			x = randint(start2, end2)
			y = randint(start2, end2)
			pt = [x, y]
			dataset.append(pt)



############################ Naive KNN ##############################

def naiveKNN(dataset, point, k):

	answer = []

	hash_distances = {}
	nearest = []
	
	for i in dataset:
		distance = (point[0]-i[0])**2 + (point[1]-i[1])**2

		if distance != 0:
			#value = str(i[0]) + "," + str(i[1])
			if not distance in hash_distances:
				hash_distances[distance] = []
				hash_distances[distance].append(i)
			else:
				hash_distances[distance].append(i)

			nearest.append(distance)


		
	k_nearest = heapq.nsmallest(k, nearest, key=None)

	#print k_nearest

	for i in k_nearest:
		answer.append(hash_distances[i].pop())

	return answer

	


####################### 1-Dimensional Hashing #######################

def createHashTable(dataset, hash_table, bucket_size):
	
	no_of_buckets = {}
	bucket_index = {}

	for i in dataset:
		
		key = '{0:012b}'.format(i[0])[:6]+'{0:012b}'.format(i[1])[:6]

		if not key in no_of_buckets:
			no_of_buckets[key] = 0

		if not key in bucket_index:
			bucket_index[key] = 0
		
		if not key in hash_table:
			hash_table[key] = []
			hash_table[key].append([])
			hash_table[key][no_of_buckets[key]].append(i)
			bucket_index[key] += 1
			
			if bucket_index[key] >= bucket_size:
				no_of_buckets[key] += 1
				bucket_index[key] = 0
				hash_table[key].append([])
		
		else:
			hash_table[key][no_of_buckets[key]].append(i)
			bucket_index[key] += 1
			if bucket_index[key] >= bucket_size:
				no_of_buckets[key] += 1
				bucket_index[key] = 0
				hash_table[key].append([])

####################### 1-Dimensional Hashing for experiment #######################

def createHashTableExp(dataset, hash_table, bucket_size):
	
	hash_space = []

	no_of_buckets = {}
	bucket_index = {}
	count = 0
	totalpoints = 0
	for i in dataset:
		
		key = '{0:012b}'.format(i[0])[:6]+'{0:012b}'.format(i[1])[:6]

		if not key in no_of_buckets:
			no_of_buckets[key] = 0

		if not key in bucket_index:
			bucket_index[key] = 0
		
		if not key in hash_table:
			hash_table[key] = []
			hash_table[key].append([])
			hash_table[key][no_of_buckets[key]].append(i)
			bucket_index[key] += 1
			
			if bucket_index[key] >= bucket_size:
				no_of_buckets[key] += 1
				bucket_index[key] = 0
				hash_table[key].append([])
		
		else:
			hash_table[key][no_of_buckets[key]].append(i)
			bucket_index[key] += 1
			if bucket_index[key] >= bucket_size:
				no_of_buckets[key] += 1
				bucket_index[key] = 0
				hash_table[key].append([])


		count += 1
		totalpoints += 1
		
		if(count == 1000):
			count = 0
			totalbuckets = 0
			for keykey in no_of_buckets:
				totalbuckets += no_of_buckets[keykey] + 1
			den = totalbuckets*bucket_size
			utilzation = (float)(totalpoints)/(float)(den)
			hash_space.append(utilzation)	
	
	return hash_space

####################### KNN for 1-D Hashing ########################


def hashKNN(hash_table, point, k):

	answer = []

	hash_distances = {}
	nearest = []

	for key in hash_table:
		for i in hash_table[key]:
			for j in i:
				distance = (j[0]-point[0])**2 + (j[1]-point[1])**2
				if distance != 0:
					if not distance in hash_distances:
						hash_distances[distance] = []
						hash_distances[distance].append(j)
					else:
						hash_distances[distance].append(j)
					
					nearest.append(distance)


				
	k_nearest = heapq.nsmallest(k, nearest, key=None)

	#print k_nearest

	for i in k_nearest:
		answer.append(hash_distances[i].pop())

	return answer


###################################### 2-D Grid #########################################

def create2DGrid(dataset, n, bucket_size):

	grid = [[[] for x in range(n)] for y in range(n)]

	no_of_buckets = [[-1 for x in range(n)] for y in range(n)]
	bucket_index = [[0 for x in range(n)] for y in range(n)]
	
	for pair in dataset:
		
		i = pair[0]/100
		j = pair[1]/100
		
		if no_of_buckets[i][j] == -1:
			
			grid[i][j].append([])
			no_of_buckets[i][j] += 1
			grid[i][j][no_of_buckets[i][j]].append(pair)
			bucket_index[i][j] += 1
		
		else:
			if bucket_index[i][j] >= bucket_size:
				
				no_of_buckets[i][j] += 1
				grid[i][j].append([])
				grid[i][j][no_of_buckets[i][j]].append(pair)
				bucket_index[i][j] = 1
			
			else:
				
				grid[i][j][no_of_buckets[i][j]].append(pair)
				bucket_index[i][j] += 1

	return grid

###################################### 2-D Grid for experiment #########################################

def create2DGridExp(dataset, n, bucket_size):

	grid = [[[] for x in range(n)] for y in range(n)]

	grid_space = []

	no_of_buckets = [[-1 for x in range(n)] for y in range(n)]
	bucket_index = [[0 for x in range(n)] for y in range(n)]
	
	count = 0
	totalpoints = 0

	for pair in dataset:
		
		i = pair[0]/100
		j = pair[1]/100
		
		if no_of_buckets[i][j] == -1:
			
			grid[i][j].append([])
			no_of_buckets[i][j] += 1
			grid[i][j][no_of_buckets[i][j]].append(pair)
			bucket_index[i][j] += 1
		
		else:
			if bucket_index[i][j] >= bucket_size:
				
				no_of_buckets[i][j] += 1
				grid[i][j].append([])
				grid[i][j][no_of_buckets[i][j]].append(pair)
				bucket_index[i][j] = 1
			
			else:
				
				grid[i][j][no_of_buckets[i][j]].append(pair)
				bucket_index[i][j] += 1

		count += 1
		totalpoints += 1
		
		if(count == 1000):
			count = 0
			totalbuckets = 0
			for ii in no_of_buckets:
				for jj in ii:
					totalbuckets += jj + 1
			den = totalbuckets*bucket_size
			utilzation = (float)(totalpoints)/(float)(den)
			grid_space.append(utilzation)

	return grid_space


def gridComputeDistances(matrix, row, column, hash_distances, nearest, point, length):

	if row >= 0 and row < length and column >= 0 and column < length:
		
		for i in matrix[row][column]:
			for j in i:
				distance = (j[0]-point[0])**2 + (j[1]-point[1])**2
				if distance != 0:
					if not distance in hash_distances:
						hash_distances[distance] = []
						hash_distances[distance].append(j)
					else:
						hash_distances[distance].append(j)
					
					nearest.append(distance)


				######### KNN for 2-D Grid ##########

def gridKNN(grid, point, n, k):

	answer = []

	hash_distances = {}
	nearest = []


	i = point[0]/100
	j = point[1]/100
	
	################### Searching in the adjacent cells #####################

	gridComputeDistances(grid, i, j, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i+1, j, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i-1, j, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i, j+1, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i, j-1, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i+1, j+1, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i+1, j-1, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i-1, j+1, hash_distances, nearest, point, n)
	gridComputeDistances(grid, i-1, j-1, hash_distances, nearest, point, n)

	#########################################################################
	
	
	k_nearest = heapq.nsmallest(k, nearest, key=None)

	#print k_nearest

	for i in k_nearest:
		answer.append(hash_distances[i].pop())

	return answer





#####################################################################################




createDataset(datasetA, 50000, 0, 900, False, 0, 0, 0)
createDataset(datasetB, 25000, 0, 600, True, 25000, 600, 1600)
createDataset(datasetC, 50000, 0, 1200, False, 0, 0, 0)

createHashTable(datasetA, hash_tableA10, 10)
createHashTable(datasetA, hash_tableA40, 40)
createHashTable(datasetA, hash_tableA70, 70)
createHashTable(datasetA, hash_tableA100, 100)
createHashTable(datasetA, hash_tableA150, 150)

hash_tablesA = {'10': hash_tableA10, '40': hash_tableA40, '70': hash_tableA70, '100': hash_tableA100, '150': hash_tableA150}



createHashTable(datasetB, hash_tableB10, 10)
createHashTable(datasetB, hash_tableB40, 40)
createHashTable(datasetB, hash_tableB70, 70)
createHashTable(datasetB, hash_tableB100, 100)
createHashTable(datasetB, hash_tableB150, 150)

hash_tablesB = {'10': hash_tableB10, '40': hash_tableB40, '70': hash_tableB70, '100': hash_tableB100, '150': hash_tableC150}

createHashTable(datasetC, hash_tableC10, 10)
createHashTable(datasetC, hash_tableC40, 40)
createHashTable(datasetC, hash_tableC70, 70)
createHashTable(datasetC, hash_tableC100, 100)
createHashTable(datasetC, hash_tableC150, 150)

hash_tablesC = {'10': hash_tableC10, '40': hash_tableC40, '70': hash_tableC70, '100': hash_tableC100, '150': hash_tableC150}


gridA10 = create2DGrid(datasetA, 10, 10)
gridA40 = create2DGrid(datasetA, 10, 40)
gridA70 = create2DGrid(datasetA, 10, 70)
gridA100 = create2DGrid(datasetA, 10, 100)
gridA150 = create2DGrid(datasetA, 10, 150)

gridsA = {'10': gridA10, '40': gridA40, '70': gridA70, '100': gridA100, '150': gridA150}


gridB10 = create2DGrid(datasetB, 17, 10)
gridB40 = create2DGrid(datasetB, 17, 40)
gridB70 = create2DGrid(datasetB, 17, 70)
gridB100 = create2DGrid(datasetB, 17, 100)
gridB150 = create2DGrid(datasetB, 17, 150)

gridsB = {'10': gridB10, '40': gridB40, '70': gridB70, '100': gridB100, '150': gridB150}

gridC10 = create2DGrid(datasetC, 13, 10)
gridC40 = create2DGrid(datasetC, 13, 40)
gridC70 = create2DGrid(datasetC, 13, 70)
gridC100 = create2DGrid(datasetC, 13, 100)
gridC150 = create2DGrid(datasetC, 13, 150)

gridsC = {'10': gridC10, '40': gridC40, '70': gridC70, '100': gridC100, '150': gridC150}


pointreadings = [x for x in range(50001) if x%1000 == 0]





########################### Experiment 2 ############################

trash = {}

hash_space10 = createHashTableExp(datasetA, trash, 10)
grid_space10 = create2DGridExp(datasetA, 10, 10)

trash = {}

hash_space70 = createHashTableExp(datasetA, trash, 70)
grid_space70 = create2DGridExp(datasetA, 10, 70)

tracehash10 = go.Scatter(
    x = pointreadings,
    y = hash_space10,
    name = '1-D Hashing',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
tracegrid10 = go.Scatter(
    x = pointreadings,
    y = grid_space10,
    name = '2-D Grid',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

tracehash70 = go.Scatter(
    x = pointreadings,
    y = hash_space70,
    name = '1-D Hashing',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
tracegrid70 = go.Scatter(
    x = pointreadings,
    y = grid_space70,
    name = '2-D Grid',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

layout10 = dict(title = 'Bucket Size:10,  Dataset A',
              xaxis = dict(title = 'No. of Points', autorange = True),
              yaxis = dict(title = 'Space Utilzation', autorange = True),
              )

layout70 = dict(title = 'Bucket Size:70,  Dataset A',
              xaxis = dict(title = 'No. of Points', autorange = True),
              yaxis = dict(title = 'Space Utilzation', autorange = True),
              )

data1d = [tracehash10, tracegrid10]
data2d = [tracehash70, tracegrid70]

fig2 = dict(data=data1d, layout=layout10)
py.offline.plot(fig2, filename='styled-line2')

fig3 = dict(data=data2d, layout=layout70)
py.offline.plot(fig3, filename='styled-line3')


########################### Experiment 3 ############################

hash_5 = []
grid_5 = []

hash_10 = []
grid_10 = []

tot1 = 0
tot2 = 0

variable_bucket_sizes = ['10', '40', '70', '100', '150']

#naiveKNN(datasetA, datasetA[0], 5)

for bucketsize in variable_bucket_sizes:
	tot1 = 0.0
	tot2 = 0.0
	for i in range(0, 30):
		j = randint(0, 49999)
		#print "Point:",datasetA[j]
		
		start_time = time.time()
		answer_hash = hashKNN(hash_tablesB[bucketsize], datasetB[j], 100)
		end_time = time.time()

		tot1 += end_time - start_time
		
		start_time = time.time()
		answer_grid = gridKNN(gridsB[bucketsize], datasetB[j], 17, 100)
		end_time = time.time()

		tot2 = end_time - start_time

		#naiveKNN(datasetA, datasetA[j], 5)



	x = (float)(tot1/30.0)
	y = (float)(tot2/30.0)
	hash_5.append(x)
	grid_5.append(y)

for bucketsize in variable_bucket_sizes:
	tot1 = 0.0
	tot2 = 0.0
	for i in range(0, 30):
		j = randint(0, 49999)
		#print "Point:",datasetA[j]
		
		start_time = time.time()
		answer_hash = hashKNN(hash_tablesB[bucketsize], datasetB[j], 200)
		end_time = time.time()

		tot1 += end_time - start_time
		
		start_time = time.time()
		answer_grid = gridKNN(gridsB[bucketsize], datasetB[j], 17, 200)
		end_time = time.time()

		tot2 = end_time - start_time

		#naiveKNN(datasetA, datasetA[j], 5)

	x = (float)(tot1/30.0)
	y = (float)(tot2/30.0)
	hash_10.append(x)
	grid_10.append(y)

trace1d_5 = go.Scatter(
    x = variable_bucket_sizes,
    y = hash_5,
    name = 'K = 100',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
trace1d_10 = go.Scatter(
    x = variable_bucket_sizes,
    y = hash_10,
    name = 'K = 200',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

trace2d_5 = go.Scatter(
    x = variable_bucket_sizes,
    y = grid_5,
    name = 'K = 5',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
trace2d_10 = go.Scatter(
    x = variable_bucket_sizes,
    y = grid_10,
    name = 'K = 10',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

layout1d = dict(title = '1-D Hashing Dataset B',
              xaxis = dict(title = 'Bucket Size', autorange = True),
              yaxis = dict(title = 'Time (seconds)', autorange = True),
              )

layout2d = dict(title = '2-D Grid Dataset B',
              xaxis = dict(title = 'Bucket Size', autorange = True),
              yaxis = dict(title = 'Time (seconds)', autorange = True),
              )

data1d = [trace1d_5, trace1d_10]
data2d = [trace2d_5, trace2d_10]

fig4 = dict(data=data1d, layout=layout1d)
py.offline.plot(fig4, filename='styled-line4')

fig5 = dict(data=data2d, layout=layout2d)
py.offline.plot(fig5, filename='styled-line5')

########################### Experiment 4 ############################

trash = {}

hash_space10 = createHashTableExp(datasetB, trash, 10)
grid_space10 = create2DGridExp(datasetB, 17, 10)

trash = {}

hash_space70 = createHashTableExp(datasetB, trash, 70)
grid_space70 = create2DGridExp(datasetB, 17, 70)

tracehash10 = go.Scatter(
    x = pointreadings,
    y = hash_space10,
    name = '1-D Hashing',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
tracegrid10 = go.Scatter(
    x = pointreadings,
    y = grid_space10,
    name = '2-D Grid',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

tracehash70 = go.Scatter(
    x = pointreadings,
    y = hash_space70,
    name = '1-D Hashing',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
tracegrid70 = go.Scatter(
    x = pointreadings,
    y = grid_space70,
    name = '2-D Grid',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

layout10 = dict(title = 'Bucket Size:10,  Dataset B',
              xaxis = dict(title = 'No. of Points', autorange = True),
              yaxis = dict(title = 'Space Utilzation', autorange = True),
              )

layout70 = dict(title = 'Bucket Size:70,  Dataset B',
              xaxis = dict(title = 'No. of Points', autorange = True),
              yaxis = dict(title = 'Space Utilzation', autorange = True),
              )

data1d = [tracehash10, tracegrid10]
data2d = [tracehash70, tracegrid70]

fig6 = dict(data=data1d, layout=layout10)
py.offline.plot(fig6, filename='styled-line6')

fig7 = dict(data=data2d, layout=layout70)
py.offline.plot(fig7, filename='styled-line7')

########################### Experiment 5 ############################

hash_5 = []
grid_5 = []

hash_10 = []
grid_10 = []

tot1 = 0
tot2 = 0

variable_bucket_sizes = ['10', '40', '70', '100', '150']

#naiveKNN(datasetA, datasetA[0], 5)



for bucketsize in variable_bucket_sizes:
	tot1 = 0.0
	tot2 = 0.0
	for i in range(0, 30):
		j = randint(0, 49999)
		#print "Point:",datasetA[j]
		
		start_time = time.time()
		answer_hash = hashKNN(hash_tablesC[bucketsize], datasetC[j], 100)
		end_time = time.time()

		tot1 += end_time - start_time
		
		start_time = time.time()
		answer_grid = gridKNN(gridsC[bucketsize], datasetC[j], 13, 100)
		end_time = time.time()

		tot2 = end_time - start_time

		#naiveKNN(datasetA, datasetA[j], 5)

	x = (float)(tot1/30.0)
	y = (float)(tot2/30.0)
	hash_5.append(x)
	grid_5.append(y)

for bucketsize in variable_bucket_sizes:
	tot1 = 0.0
	tot2 = 0.0
	for i in range(0, 30):
		j = randint(0, 49999)
		#print "Point:",datasetA[j]
		
		start_time = time.time()
		answer_hash = hashKNN(hash_tablesC[bucketsize], datasetC[j], 200)
		end_time = time.time()

		tot1 += end_time - start_time
		
		start_time = time.time()
		answer_grid = gridKNN(gridsC[bucketsize], datasetC[j], 13, 200)
		end_time = time.time()

		tot2 = end_time - start_time

		#naiveKNN(datasetA, datasetA[j], 5)

	x = (float)(tot1/30.0)
	y = (float)(tot2/30.0)
	hash_10.append(x)
	grid_10.append(y)

trace1d_5 = go.Scatter(
    x = variable_bucket_sizes,
    y = hash_5,
    name = 'K = 100',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
trace1d_10 = go.Scatter(
    x = variable_bucket_sizes,
    y = hash_10,
    name = 'K = 200',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

trace2d_5 = go.Scatter(
    x = variable_bucket_sizes,
    y = grid_5,
    name = 'K = 100',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
trace2d_10 = go.Scatter(
    x = variable_bucket_sizes,
    y = grid_10,
    name = 'K = 200',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

layout1d = dict(title = '1-D Hashing Dataset C',
              xaxis = dict(title = 'Bucket Size', autorange = True),
              yaxis = dict(title = 'Time (seconds)', autorange = True),
              )

layout2d = dict(title = '2-D Grid Dataset C',
              xaxis = dict(title = 'Bucket Size', autorange = True),
              yaxis = dict(title = 'Time (seconds)', autorange = True),
              )

data1d = [trace1d_5, trace1d_10]
data2d = [trace2d_5, trace2d_10]

fig8 = dict(data=data1d, layout=layout1d)
py.offline.plot(fig8, filename='styled-line8')

fig9 = dict(data=data2d, layout=layout2d)
py.offline.plot(fig9, filename='styled-line9')




########################### Experiment 6 ############################

trash = {}

hash_space10 = createHashTableExp(datasetC, trash, 10)
grid_space10 = create2DGridExp(datasetC, 13, 10)

trash = {}

hash_space70 = createHashTableExp(datasetC, trash, 70)
grid_space70 = create2DGridExp(datasetC, 13, 70)

tracehash10 = go.Scatter(
    x = pointreadings,
    y = hash_space10,
    name = '1-D Hashing',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
tracegrid10 = go.Scatter(
    x = pointreadings,
    y = grid_space10,
    name = '2-D Grid',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

tracehash70 = go.Scatter(
    x = pointreadings,
    y = hash_space70,
    name = '1-D Hashing',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
tracegrid70 = go.Scatter(
    x = pointreadings,
    y = grid_space70,
    name = '2-D Grid',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

layout10 = dict(title = 'Bucket Size:10,  Dataset C',
              xaxis = dict(title = 'No. of Points', autorange = True),
              yaxis = dict(title = 'Space Utilzation', autorange = True),
              )

layout70 = dict(title = 'Bucket Size:70,  Dataset C',
              xaxis = dict(title = 'No. of Points', autorange = True),
              yaxis = dict(title = 'Space Utilzation', autorange = True),
              )

data1d = [tracehash10, tracegrid10]
data2d = [tracehash70, tracegrid70]

fig10 = dict(data=data1d, layout=layout10)
py.offline.plot(fig10, filename='styled-line10')

fig11 = dict(data=data2d, layout=layout70)
py.offline.plot(fig11, filename='styled-line11')



########################### Experiment 1 ############################



hash_5 = []
grid_5 = []

hash_10 = []
grid_10 = []

tot1 = 0
tot2 = 0

variable_bucket_sizes = ['10', '40', '70', '100', '150']

#naiveKNN(datasetA, datasetA[0], 5)

for bucketsize in variable_bucket_sizes:
	tot1 = 0.0
	tot2 = 0.0
	for i in range(0, 30):
		j = randint(0, 49999)
		#print "Point:",datasetA[j]
		
		start_time = time.time()
		answer_hash = hashKNN(hash_tablesA[bucketsize], datasetA[j], 100)
		end_time = time.time()

		tot1 += end_time - start_time
		
		start_time = time.time()
		answer_grid = gridKNN(gridsA[bucketsize], datasetA[j], 10, 100)
		end_time = time.time()

		tot2 = end_time - start_time

		

		#naiveKNN(datasetA, datasetA[j], 5)

	x = (float)(tot1/30.0)
	y = (float)(tot2/30.0)
	hash_5.append(x)
	grid_5.append(y)

for bucketsize in variable_bucket_sizes:
	tot1 = 0.0
	tot2 = 0.0
	for i in range(0, 30):
		j = randint(0, 49999)
		#print "Point:",datasetA[j]
		
		start_time = time.time()
		answer_hash = hashKNN(hash_tablesA[bucketsize], datasetA[j], 200)
		end_time = time.time()

		tot1 += end_time - start_time
		
		start_time = time.time()
		answer_grid = gridKNN(gridsA[bucketsize], datasetA[j], 10, 200)
		end_time = time.time()

		tot2 = end_time - start_time

		

		#naiveKNN(datasetA, datasetA[j], 5)

	x = (float)(tot1/30.0)
	y = (float)(tot2/30.0)
	hash_10.append(x)
	grid_10.append(y)

trace1d_5 = go.Scatter(
    x = variable_bucket_sizes,
    y = hash_5,
    name = 'K = 100',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
trace1d_10 = go.Scatter(
    x = variable_bucket_sizes,
    y = hash_10,
    name = 'K = 200',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

trace2d_5 = go.Scatter(
    x = variable_bucket_sizes,
    y = grid_5,
    name = 'K = 100',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
trace2d_10 = go.Scatter(
    x = variable_bucket_sizes,
    y = grid_10,
    name = 'K = 200',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
    )

layout1d = dict(title = '1-D Hashing Dataset A',
              xaxis = dict(title = 'Bucket Size', autorange = True),
              yaxis = dict(title = 'Time (seconds)', autorange = True),
              )

layout2d = dict(title = '2-D Grid Dataset A',
              xaxis = dict(title = 'Bucket Size', autorange = True),
              yaxis = dict(title = 'Time (seconds)', autorange = True),
              )

data1d = [trace1d_5, trace1d_10]
data2d = [trace2d_5, trace2d_10]

fig = dict(data=data1d, layout=layout1d)
py.offline.plot(fig, filename='styled-line')

fig1 = dict(data=data2d, layout=layout2d)
py.offline.plot(fig1, filename='styled-line1')











