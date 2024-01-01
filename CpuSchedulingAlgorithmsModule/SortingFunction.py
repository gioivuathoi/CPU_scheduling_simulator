
def compare_by_return_time(a,b):
	if a.return_time < b.return_time:
		return -1
	elif a.return_time > b.return_time:
		return 1
	return 0

# p: Mảng cấu trúc tiến trình
# len: Số lượng tiến trình
 
# Function to find the partition position
def partition(array, low, high):

	# choose the rightmost element as pivot
	pivot = array[high].return_time

	# pointer for greater element
	i = low - 1

	# traverse through all elements
	# compare each element with pivot
	for j in range(low, high):
		if array[j].return_time <= pivot:
			# If element smaller than pivot is found
			# swap it with the greater element pointed by i
			i = i + 1
			# Swapping element at i with element at j
			(array[i], array[j]) = (array[j], array[i])

	# Swap the pivot element with the greater element specified by i
	(array[i + 1], array[high]) = (array[high], array[i + 1])
	# Return the position from where partition is done
	return i + 1

# function to perform quicksort


def quickSort_by_return_time(array, low, high):
	if low < high:
		# Find pivot element such that
		# element smaller than pivot are on the left
		# element greater than pivot are on the right
		pi = partition(array, low, high)
		# Recursive call on the left of pivot
		quickSort_by_return_time(array, low, pi - 1)
		# Recursive call on the right of pivot
		quickSort_by_return_time(array, pi + 1, high)



# arr   [Mảng cần sắp xếp]
# left  [Chỉ số bên trái của mảng]
# mid   [Chỉ số giữa của mảng]
# right [Chỉ số bên phải của mảng]

# Python program for implementation of MergeSort

# Merges two subarrays of arr[].
# First subarray is arr[l..m]
# Second subarray is arr[m+1..r]

def merge(arr, l, m, r, type):
	n1 = m - l + 1
	n2 = r - m

	# create temp arrays
	L = [0] * (n1)
	R = [0] * (n2)

	# Copy data to temp arrays L[] and R[]
	for i in range(0, n1):
		L[i] = arr[l + i]

	for j in range(0, n2):
		R[j] = arr[m + 1 + j]

	# Merge the temp arrays back into arr[l..r]
	i = 0	 # Initial index of first subarray
	j = 0	 # Initial index of second subarray
	k = l	 # Initial index of merged subarray

	while i < n1 and j < n2:
		if type == "arrive":
			left = L[i].arrive_time
			right = R[j].arrive_time
			# print(left)
			# print(right)
		elif type == "burst":
			left = L[i].burst
			right = R[j].burst
		elif type == "priority":
			left = L[i].priority
			right = R[j].priority
		if left >= right:
			arr[k] = L[i]
			i += 1
		else:
			arr[k] = R[j]
			j += 1
		k += 1

	# Copy the remaining elements of L[], if there are any
	while i < n1:
		arr[k] = L[i]
		i += 1
		k += 1

	# Copy the remaining elements of R[], if there are any
	while j < n2:
		arr[k] = R[j]
		j += 1
		k += 1

# l is for left index and r is right index of the
# sub-array of arr to be sorted

def mergeSort(arr, l, r, type):
	if l < r:
		# Same as (l+r)//2, but avoids overflow for
		# large l and h
		m = l+(r-l)//2
		# Sort first and second halves
		mergeSort(arr, l, m, type)
		mergeSort(arr, m+1, r, type)
		merge(arr, l, m, r, type)
	

