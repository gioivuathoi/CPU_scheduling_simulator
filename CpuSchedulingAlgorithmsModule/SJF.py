# Shortest Job First Algorithm
import CpuSchedulingAlgorithmsModule.SortingFunction as SortingFunction
from CpuSchedulingAlgorithmsModule.PrintTable import print_table

 # [sjf_calculate_time Hàm tính toán thời gian thuật toán SJF]
 # @param p   [mảng cấu trúc tiến trình]
 # @param len [số lượng tiến trình]
def printf(a):
	print(a, end="")
def sjf_calculate_time(p,len):

	# Khai báo các biến sử dụng trong vòng lặp
	curr_time = 0
	# Khai báo và khởi tạo một biến để lưu trữ thời gian hiện tại
	min = 0
	# Khai báo và khởi tạo biến để lưu trữ chỉ số của phần tử có thời gian nhỏ nhất

	# Thời gian thực thi của tiến trình được thực hiện đầu tiên
	p[0].completed = True
	p[0].return_time = p[0].burst
	p[0].turnaround_time = p[0].burst - p[0].arrive_time
	p[0].waiting_time = 0
	
	curr_time = p[0].burst
	# Tăng thời gian hiện tại lên theo thời gian của tiến trình đã hoàn thành

	# Duyệt qua số lượng tiến trình - 1 lần */
	for i in range(len):
		# Duyệt qua số lượng tiến trình -1
		for j in range(len):
			# Nếu quá trình này đã được hoàn thành */
			if p[j].completed == True:
				continue
				# Đi tới vòng lặp tiếp theo
			# Nếu quá trình này vẫn chưa hoàn tất
			else:
				min = j
				# khởi tạo biến min 
				break
				# thoát vòng lặp
		# Duyệt qua số lượng tiến trình -1 */
		for j in range(len):
			# Tìm kiếm tiến trình thỏa mãn điều kiện có thời gian thực hiện nhỏ nhất */
			if (p[j].completed == False) and (p[j].arrive_time <= curr_time) and (p[j].burst < p[min].burst):
				min = j
				# Cập nhật tiến trình có thời gian thực hiện nhỏ nhất
		p[min].waiting_time = curr_time - p[min].arrive_time
		# Tính thời gian chờ tiến trình để chạy
		p[min].completed = True
		# Thay đổi trạng thái của tiến trình được thực thi sang trạng thái hoàn thành

		curr_time += p[min].burst
		# Tăng thời gian hiện tại lên theo thời gian thực hiện của tiến trình

		p[min].return_time = curr_time
		# Tính toán thời gian trả về của tiến trình
		p[min].turnaround_time = p[min].return_time - p[min].arrive_time
		# Tính toán thời gian turnaround của tiến trình

#  [sjf_print_gantt_chart Hàm hiển thị biểu đồ Gantt]
#  @param p   [mảng cấu trúc tiến trình]
#  @param len [số lượng tiến trình]

def sjf_print_gantt_chart(p,len):

	printf("\t ")
	# đầu ra thanh trên cùng
	for i in range(len):
		for j in range(p[i].burst):
			printf("--")
		printf(" ")
	printf("\n\t|")
	# Đầu ra ID tiến trình
	for i in range(len):
		for j in range(p[i].burst -1):
			printf(" ")
		printf(p[i].id)
		for j in range(p[i].burst -2):
			printf(" ")
		printf("|")
	printf("\n\t ")

	# đầu ra thanh dưới cùng */
	for i in range(len):
		for j in range(p[i].burst):
			printf("--")
		printf(" ")
	printf("\n\t")
	printf("0")
	# Đầu ra thời gian thực hiện tiến trình */
	for i in range(len):
		for j in range(p[i].burst):
			printf("  ")
		if p[i].turnaround_time > 9:
			printf("\b")
		printf(p[i].return_time)
	printf("\n")

#  SJF hàm thực thi thuật toán
#  @param p   [mảng cấu trúc tiến trình]
#  @param len [số lượng tiến trình]

def SJF(p,len):
	# Khai báo biến để sử dụng trong vòng lặp
	total_waiting_time = 0
	# Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	total_turnaround_time = 0
	# Khai báo và khởi tạo biến để lưu trữ tổng thời gian turnaround
	total_response_time = 0
	# Khai báo và khởi tạo biến để lưu trữ tổng thời gian phản hồi
	SortingFunction.mergeSort_arrive_time(p, 0, len-1)
	# Gọi hàm merge_sort_by_arrive_time() để sắp xếp các tiến trình theo thời gian đến
	sjf_calculate_time(p, len)
	# Gọi hàm sjf_calculate_time() để tính thời gian của các tiến trình
	# Lặp lại theo số lượng tiến trình */
	for i in range(len):
		p[i].return_time = p[i].turnaround_time + p[i].arrive_time
		# Tính toán và lưu trữ thời gian trả về của tiến trình
		p[i].response_time = p[i].waiting_time
		# Lưu trữ thời gian phản hồi của tiến trình
		total_waiting_time += p[i].waiting_time
		# Tăng tổng thời gian chờ lên
		total_turnaround_time += p[i].turnaround_time
		# Tăng tổng thời gian turnaround lên
		total_response_time += p[i].response_time
		# Tăng tổng thời gian phản hồi lên
	print("\tSJF Scheduling Algorithms\n")
	SortingFunction.quickSort_by_return_time(p, 0, len-1)
	# Gọi hàm quick_sort_by_return_time() để sắp xếp các tiến trình theo thời gian trả về
	sjf_print_gantt_chart(p, len)
	# Gọi hàm sjf_print_gantt_chart() để in biểu đồ Gantt
	# In ra thời gian chờ trung bình, thời gian turnaround trung bình và thời gian phản hồi trung bình */
	print("\n\tAverage Waiting Time     : %-2.2lf" %(total_waiting_time / len))
	print("\tAverage Turnaround Time  : %-2.2lf" %(total_turnaround_time / len))
	print("\tAverage Response Time    : %-2.2lf\n" %(total_response_time / len))
	print_table(p, len)
	# Gọi hàm print_table() để in bảng dữ liệu
