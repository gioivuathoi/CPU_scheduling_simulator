import CpuSchedulingAlgorithmsModule.SortingFunction as SortingFunction
from CpuSchedulingAlgorithmsModule.PrintTable import print_table


#  [Hàm tính toán độ trễ thuật toán RR rr_calculate_waiting_time ]
#  @param p   array of proocess
#  @param len number of processes
#  @param q   quantum time
def printf(a):
	print(a, end="")
def rr_calculate_waiting_time(p,len, q):

	# Khai báo các biến sử dụng trong vòng lặp
	curr_time = 0
	# Khai báo và khởi tạo một biến để lưu trữ thời gian hiện tại
	# Phân bổ bộ nhớ động một mảng để lưu trữ thời gian thực hiện còn lại cho mỗi tiến trình
    #  Phân bổ bộ nhớ động của một mảng được sử dụng để kiểm tra thời gian phản hồi.
	remain_burst_time = list()
	calc_response_time = list()
	for i in range(len):
		remain_burst_time.append(0)
		calc_response_time.append(0)
    
	# Lặp lại nhiều lần theo số lượng tiến trình */
	for i in range(len):
		remain_burst_time[i] = p[i].burst
		# Khởi tạo mảng để lưu trữ thời gian thực hiện còn lại
		calc_response_time[i] = False
		# Xác nhận việc tính toán thời gian phản hồi và khởi tạo mảng kiểm tra
	
	# Lặp lại cho đến khi tất cả các tiến trình hoàn tất */
	while True:
		check = True
		# Khởi tạo biến check 
		# Lặp lại nhiều lần theo số lượng tiến trình */
		for i in range(len):
			# Nếu thời gian thực hiện vẫn còn */
			if remain_burst_time[i] > 0:
				check = False
				# Xử lý biến kiểm tra 'check' thành giá trị FALSE
				# Nếu thời gian phản hồi chưa được tính toán
				if calc_response_time[i] == False:
					p[i].response_time = curr_time - p[i].arrive_time
					# Tính toán và lưu thời gian phản hồi
					calc_response_time[i] = True
					# Quá trình tính toán thời gian phản hồi
				# Trong trường hợp thời gian còn lại lớn hơn thời gian được cấp 
				if remain_burst_time[i] > q:

					curr_time += q
					# Tăng thời gian hiện tại lên một lượng bằng thời gian cấp phát
					remain_burst_time[i] -= q
					# Giảm thời gian còn lại của tiến trình đang chạy
				# Khi thời gian còn lại ít hơn thời gian cho phép 
				else:
					curr_time += remain_burst_time[i]
					# Thời gian hiện tại tăng theo thời gian còn lại
					p[i].waiting_time = curr_time - p[i].burst
					# Tính toán thời gian chờ
					remain_burst_time[i] = 0
					# Thay đổi thời gian còn lại về 0
				
		# Khi tất cả các quá trình được hoàn thành */
		if check == True:
			break
			# Thoát khỏi vòng lặp vô hạn


#  rr_calculate_turnaround_time hàm tính toán turnaround time]
#  @param p   [mảng cấu trúc tiến trình]
#  @param len [số lượng tiến trình]
 
def rr_calculate_turnaround_time(p,len):
	# Lặp lại nhiều lần theo số lượng tiến trình */
	for i in range(len):
		p[i].turnaround_time = p[i].burst + p[i].waiting_time - p[i].arrive_time
		# Sau khi tính toán thời gian turnaround, lưu trữ nó

#  [rr_print_gantt_chart Hàm đầu ra biểu đồ Round Robin Gantt]
#  @param p   [mảng cấu trúc tiến trình]
#  @param len [Số lượng tiến trình]
#  @param q   [thời gian cung cấp]
 
def rr_print_gantt_chart(p, len, q):
	curr_time = 0
	total_burst_time = 0
	# Khai báo và khởi tạo các biến để lưu trữ thời gian hiện tại và tổng thời gian thực hiện
	temp_total_burst_time = 0
	# Khai báo và khởi tạo các biến để lưu trữ giá trị tạm thời
	# Phân bổ bộ nhớ động một mảng để lưu trữ thời gian thực hiện còn lại cho mỗi tiến trình */
	remain_burst_time = list()
	for i in range(len):
		remain_burst_time.append(0)

	# Lặp lại nhiều lần bằng số lượng tiến trình
	for i in range(len):
		remain_burst_time[i] = p[i].burst
		# Khởi tạo mảng lưu trữ thời gian còn lại
		total_burst_time += p[i].burst
		# tổng thời gian thực hiện
	printf("\t")

	# Hiển thị thanh trạng thái giống với thuật toán tính thời gian chờ
	while True:
		check = True
		for i in range(len):
			if remain_burst_time[i] > 0:
				check = False
				if remain_burst_time[i] < q:
					printf("  ")
					for j in range(remain_burst_time[i]):
						printf("---")
				else:
					printf("  ")
					for j in range(q):
						printf("---")
				if remain_burst_time[i] > q:
					curr_time += q
					remain_burst_time[i] -= q
				else:
					curr_time += remain_burst_time[i]
					p[i].waiting_time = curr_time - p[i].burst
					remain_burst_time[i] = 0

		if check == True:
			break
	printf(" \n\t")

	for i in range(len):
		remain_burst_time[i] = p[i].burst
	# Đầu ra ID tiến trình */
	while True:
		check = True
		for i in range(len):
			if remain_burst_time[i] > 0:
				check = False
				if remain_burst_time[i] < q:
					printf("|")
					if remain_burst_time[i] != 1:
						for j in range(remain_burst_time[i]):
							printf(" ")
						printf(p[i].id)
						for j in remain_burst_time(remain_burst_time[i]):
							printf(" ")
					else:
						printf(" "+p[i].id+" ")
				else:
					printf("|")
					for j in range(q):
						printf(" ")
					printf(p[i].id)
					for j in range(q):
						printf(" ")
				if remain_burst_time[i] > q:
					curr_time += q
					remain_burst_time[i] -= q
				else:
					curr_time += remain_burst_time[i]
					p[i].waiting_time = curr_time - p[i].burst
					remain_burst_time[i] = 0
		if check == True:
			break
	printf("|\n\t")

	for i in range(len):
		remain_burst_time[i] = p[i].burst
	# đầu ra thanh dưới cùng
	while True:
		check = True
		for i in range(len):
			if remain_burst_time[i] > 0:
				check = False
				if remain_burst_time[i] < q:
					printf("  ")
					for j in range(remain_burst_time[i]):
						printf("---")
				else:
					printf("  ")
					for j in range(q):
						printf("---")

				if remain_burst_time[i] > q:
					curr_time += q
					remain_burst_time[i] -= q
				else:
					curr_time += remain_burst_time[i]
					p[i].waiting_time = curr_time - p[i].burst
					remain_burst_time[i] = 0
		if check == True:
			break
	printf("\n\t")

	for i in range(len):
		remain_burst_time[i] = p[i].burst
	curr_time = 0
	# Đầu ra thời gian xử lý */
	while True:
		check = True
		for i in range(len):
			if remain_burst_time[i] > 0:
				check = False
				if remain_burst_time[i] < q:
					printf("%-2d" %(curr_time))
					for j in range(remain_burst_time[i] - 1):
						printf("  ")
					printf("  ")
				else:
				
					printf("%-2d" %(curr_time))
					for j in range(q):
						printf("  ")
					printf("  ")
				if remain_burst_time[i] > q:
					curr_time += q
					remain_burst_time[i] -= q
				else:
					curr_time += remain_burst_time[i]
					p[i].waiting_time = curr_time - p[i].burst
					remain_burst_time[i] = 0
		if check == True:
			break

	printf("%-3d\n" %(total_burst_time))

	printf("\n")

#  * [RR hàm thực thi thuật toán]
#  * @param p       [mảng cấu trúc tiến trình]
#  * @param len     [số lượng tiến trình]
#  * @param quantum [time quantum]
 
def RR(p,len,quantum):

	total_waiting_time = 0
	# Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	total_turnaround_time = 0
	# Khai báo và khởi tạo biến để lưu trữ tổng thời gian turnaround
	total_response_time = 0
	# Khai báo và khởi tạo một biến để lưu trữ tổng thời gian phản hồi
	SortingFunction.mergeSort_arrive_time(p, 0, len-1)
	# Sắp xếp theo thời gian đến với lệnh gọi hàm merge_sort_by_arrive_time 
	rr_calculate_waiting_time(p, len, quantum)
	# Tính thời gian chờ, thời gian phản hồi bằng lệnh gọi hàm rr_calculate_waiting_time 
	rr_calculate_turnaround_time(p, len)
	# Tính thời gian quay vòng bằng lệnh gọi hàm rr_calculate_turnaround_time 
	# Lặp lại nhiều lần theo số lượng tiến trình */
	for i in range(len):
		p[i].waiting_time = p[i].turnaround_time - p[i].burst
		# Tính thời gian chờ đợi và lưu lại
		p[i].return_time = p[i].arrive_time + p[i].burst + p[i].waiting_time
		# Tính toán thời gian hoàn thành và lưu trữ
		total_waiting_time += p[i].waiting_time
		# Tăng tổng thời gian chờ
		total_turnaround_time += p[i].turnaround_time
		# Tăng tổng thời gian turnaround
		total_response_time += p[i].response_time
		# Tăng tổng thời gian phản hồi
	
	print("\tRound Robin Scheduling Algorithm (Quantum : %d)\n" %(quantum))

	rr_print_gantt_chart(p, len, quantum)
	# In biểu đồ Gantt với lệnh gọi hàm rr_print_gantt_chart 

	# Thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	print("\n\tAverage Waiting Time     : %-2.2lf" %(total_waiting_time /len))
	print("\tAverage Turnaround Time  : %-2.2lf" %(total_turnaround_time /len))
	print("\tAverage Response Time    : %-2.2lf\n" %(total_response_time / len))

	print_table(p, len)
	# Bảng dữ liệu đầu ra với lệnh gọi hàm print_table 