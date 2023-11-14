# Preemptive Priority Scheduling Algorithm
import CpuSchedulingAlgorithmsModule.SortingFunction as SortingFunction
from CpuSchedulingAlgorithmsModule.PrintTable import print_table
import sys
#  pps_calculate_time PPS Hàm tính thời gian thuật toán]
#  @param p   [description]
#  @param len [description]
def printf(a):
	print(a, end ="")
def pps_calculate_time(p, len):
    current_time = 0
    total_burst_time = 0
	# Khai báo một biến để lưu tổng thời gian thực hiện
    k = 0
	# Khai báo và khởi tạo số để lưu số tiến trình hiện đang thực thi
	# Phân bổ bộ nhớ động một mảng để lưu trữ thời gian thực hiện còn lại cho mỗi tiến trình
    remain_burst_time = list()
    count = list()
    for i in range(len):
        remain_burst_time.append(0)
        count.append(0)
	# Phân bổ bộ nhớ động của một mảng được sử dụng để kiểm tra thời gian phản hồi. */

	# Lặp lại nhiều lần bằng số lượng tiến trình */
    for i in range(len):
        count[i] = 0
		# khởi tạo mảng count
        remain_burst_time[i] = p[i].burst
		# Khởi tạo mảng remain_burst_time
        total_burst_time += p[i].burst
		# Đặt lại tổng thời gian thực hiện còn lại
	
	# Lặp lại cho đến khi thời gian hiện tại đạt tổng thời gian thực hiện */
    while current_time < total_burst_time:
        priority = sys.maxsize
		# Khởi tạo mức độ ưu tiên thành INT_MAX

		# Nếu thời gian đến nhỏ hơn thời gian đến của tiến trình được nhập cuối cùng. */
        if current_time <= p[len - 1].arrive_time:
			# Lặp lại nhiều lần bằng số lượng tiến trình
            for i in range(len):
				# Nếu nó không được hoàn thành, thời gian đến nhỏ hơn hoặc bằng thời gian hiện tại và mức độ ưu tiên nhỏ hơn mức ưu tiên hiện tại. */
                if (p[i].completed) == False and (p[i].arrive_time <= current_time) and (priority > p[i].priority):
                    priority = p[i].priority
					# Cập nhật ưu tiên
                    k = i
					# Cập nhật chỉ mục quy trình
		# Khi không có thêm quy trình mới nào xuất hiện */
        else:
			# Lặp lại nhiều lần bằng số lượng tiến trình */
            for i in range(len):
				# Nếu chưa hoàn thành và mức độ ưu tiên nhỏ hơn mức ưu tiên hiện tại */
                if (p[i].completed == False) and (priority > p[i].priority):
                    priority = p[i].priority
					# Cập nhật ưu tiên
                    k = i
					# Cập nhật chỉ mục tiến trình
		# Khi tiến trình đã chọn được bắt đầu lần đầu tiên */
        if count[k] == 0:
            count[k] += 1
			# Không phải là khởi chạy ban đầu
            p[k].response_time = current_time
			# Lưu thời gian phản hồi của tiến trình đang chạy
        remain_burst_time[k] -= 1
		# Giảm thời gian còn lại của tiến trình thực hiện
        current_time += 1
		# Tăng thời gian hiện tại
		# Khi thời gian thực hiện còn lại của tiến trình trở thành 0 */
        if remain_burst_time[k] == 0:
            p[k].completed = True
# Thay đổi trạng thái để hoàn thành
            p[k].waiting_time = current_time - p[k].burst - p[k].arrive_time
# Tính toán thời gian chờ
            p[k].return_time = current_time
# Tính toán thời gian trả về
#  pps_print_gantt_chart: hàm hiển thị biểu đồ Gantt
#  @param p   [mảng cấu trúc tiến trình]
#  @param len [số lượng tiến trình]

def pps_print_gantt_chart(p,len):
	total_burst_time = 0
	current_time = 0
	previous_time = 0
	# Khai báo các biến bổ sung để lưu trữ thời gian tiến trình trước đó đã chạy
	k, pre_k = 0,0
	# Khai báo biến bổ sung để lưu trữ số tiến trình trước đó
	# Khai báo một biến để lưu trữ khoảng cách giữa các tiến trình mới được khởi chạy
	count = list()
	remain_burst_time = list()
	for i in range(len):
		count.append(0)
		remain_burst_time.append(0)

	for i in range(len):
		remain_burst_time[i] = p[i].burst
		total_burst_time += p[i].burst
		p[i].completed = False
		count[i] = 0

	printf("\t ")

	# Thực hiện cùng một thuật toán và xuất ra thanh trên cùng */
	while current_time < total_burst_time:
		priority = sys.maxsize
		if current_time <= p[len - 1].arrive_time:
			for i in range(len):
				if (p[i].completed == False)and (p[i].arrive_time <= current_time):
					if priority > p[i].priority:
						priority = p[i].priority
						k = i
		else:
			for i in range(len):
				if p[i].completed == False:
					if priority > p[i].priority:
						priority = p[i].priority
						k = i
		# Nếu quy trình này khác với quy trình được thực hiện trước đó */
		if pre_k != k:
			printf(" ")
			# hiển thị khoảng trắng
		printf("---")
		remain_burst_time[k] -= 1
		current_time += 1
		pre_k = k
		# Lưu tiến trình trước đos
		if remain_burst_time[k] == 0:
			p[k].completed = True

	for i in range(len):
		remain_burst_time[i] = p[i].burst
		p[i].completed = False
	printf("\n\t|")
	current_time = 0

	# Thực thi cùng một thuật toán và in ra ID tiến trình. So sánh với tiến trình trước đó và điều chỉnh khoảng cách sử dụng \b */
	while current_time < total_burst_time:
		priority = sys.maxsize
		if current_time <= p[len - 1].arrive_time:
			for i in range(len):
				if (p[i].completed == False) and (p[i].arrive_time <= current_time):
					if priority > p[i].priority:
						priority = p[i].priority
						k = i
		else:
			for i in range(len):
				if p[i].completed == False:
					if priority > p[i].priority:
						priority = p[i].priority
						k = i
		if current_time == 0:
			count[k]+= 1
			printf("  ")
		else:
			# Nếu quy trình này khác với quy trình trước đó */
			if pre_k != k:
				num = count[pre_k] + 1
				# lưu khoảng thời gian giữa hai tiến trình
				count[pre_k] = 0
				# Đặt lại số lượng tiến trình trước đó
				count[k] += 1
				# Tăng số lượng tiến trình hiện tại
				# hiển thị \b bằng mức chênh lệch giữa hai tiến trình */
				for i in range(num):
					printf("\b")

				# Đầu ra ID tiến trình trước đó */
				printf(p[pre_k].id)

				# In khoảng trống theo khoảng thời gian */
				for i in range(num-2):
					printf("  ")
				printf("|  ")
			# nếu cùng 1 tiến trình */
			else:
				# Tăng số lượng quy trình hiện tại
				count[k] += 1
				printf("  ")
				# hiển thị khoảng trắng
				# Khi quá trình cuối cùng được thực hiện */
				if current_time == total_burst_time - 1:
					num = count[pre_k] + 1
					count[pre_k] = 0
					count[k] += 1
					for i in range(num):
						printf("\b")
					printf(p[pre_k].id)
					for i in range(num-1):
						printf("  ")
		pre_k = k
		remain_burst_time[k] -= 1
		current_time += 1
		if remain_burst_time[k] == 0:
			p[k].completed = True
	
	for i in range(len):
		remain_burst_time[i] = p[i].burst
		p[i].completed = False
	printf("|\n\t")
	current_time = 0

	# hiển thị thanh dưới cùng bằng thuật toán tương tự */
	printf(" ")
	while current_time < total_burst_time:
		priority = sys.maxsize
		if current_time <= p[len - 1].arrive_time:
			for i in range(len):
				if (p[i].completed == False) and (p[i].arrive_time <= current_time):
					if priority > p[i].priority:
						priority = p[i].priority
						k = i
		else:
			for i in range(len):
				if p[i].completed == False:
					if priority > p[i].priority:
						priority = p[i].priority
						k = i		
		
		if pre_k != k:
			printf(" ")
		printf("---")
		remain_burst_time[k] -= 1
		current_time += 1
		pre_k = k
		if remain_burst_time[k] == 0:
			p[k].completed = True
	for i in range(len):
		remain_burst_time[i] = p[i].burst
		p[i].completed = False
	current_time = 0
	num = 0
	printf("\n\t")
	# Thực hiện cách tương tự như in ID tiến trình, nhưng in thời gian thay vì ID tiến trình */
	while current_time <= total_burst_time:
		if total_burst_time != current_time:
			priority = sys.maxsize
			if current_time <= p[len - 1].arrive_time:
				for i in range(len):
					if (p[i].completed == False) and (p[i].arrive_time <= current_time):
						if priority > p[i].priority:
							priority = p[i].priority
							k = i
			else:
				for i in range(len):
					if (p[i].completed == False) and (priority > p[i].priority):
						priority = p[i].priority
						k = i
			if pre_k != k:
				for i in range(num):
					if current_time != 0:
						printf("  ")

				if current_time != 0:
					printf(" ")

				printf("%-2d" %(current_time))
				num = 0
				previous_time = current_time
			else:
				num += 1
			remain_burst_time[k] -= 1
			current_time += 1
			pre_k = k
			if remain_burst_time[k] == 0:
				p[k].completed = True
		else:
			for i in range(current_time-previous_time-1):
				printf("  ")
			printf(" ")
			printf("%-2d" %(current_time))
			break
	printf("\n")

#  PPS PPS hàm thực thi thuật toán]
#  @param p   [mảng cấu trúc tiến trình]
#  @param len [số lượng tiến trình]
 
def PPS(p,len):
	# Khai báo các biến sử dụng trong vòng lặp
	total_waiting_time = 0
	# Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	total_turnaround_time = 0
	# Khai báo và khởi tạo một biến để lưu trữ tổng thời gian xử lý
	total_response_time = 0
	# Khai báo và khởi tạo một biến để lưu trữ tổng thời gian phản hồi
	SortingFunction.mergeSort_arrive_time(p, 0, len-1)
	# Sắp xếp theo thời gian đến với lệnh gọi hàm merge_sort_by_arrive_time 
	pps_calculate_time(p, len)
	# Tính thời gian tiến trình bằng lệnh gọi hàm pps_calculate_time

	# Lặp lại nhiều lần theo số lượng tiến trình */
	for i in range(len):
		p[i].turnaround_time = p[i].return_time - p[i].arrive_time
		# tính toán Turnaround Time
		total_waiting_time += p[i].waiting_time
		# Tăng tổng thời gian chờ 
		total_turnaround_time += p[i].turnaround_time
		# Tăng tổng thời gian xử lý
		total_response_time += p[i].response_time
		# Tăng tổng thời gian phản hồi
	

	print("\tPreemptive Priority Scheduling Algorithm\n")

	pps_print_gantt_chart(p, len)
	# In biểu đồ Gantt với lệnh gọi hàm pps_print_gantt_chart 

	# Thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	print("\n\tAverage Waiting Time     : %-2.2lf" %(total_waiting_time / len))
	print("\tAverage Turnaround Time  : %-2.2lf" %(total_turnaround_time / len))
	print("\tAverage Response Time    : %-2.2lf\n" %(total_response_time / len))

	print_table(p, len)
	# Bảng dữ liệu đầu ra với lệnh gọi hàm print_table 