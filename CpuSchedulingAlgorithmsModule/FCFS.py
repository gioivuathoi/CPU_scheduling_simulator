import CpuSchedulingAlgorithmsModule.SortingFunction as SortingFunction
from CpuSchedulingAlgorithmsModule.PrintTable import print_table
#  FCFS :hàm thực thi thuật toán
#  p   [mảng cấu trúc tiến trình]
#  len [số lượng tiến trình]
def fcfs_print_gantt_chart(p,len):
	# khai báo biến sử dụng trong vòng lặp
	print("\t ",end="")

	# hiển thị thanh đầu trang */
	for i in range(len):
		for j in range(p[i].burst):
			print("---", end="")
		print(" ", end="")

	print("\n\t|", end="")

	# hiển thị tên tiến trình */
	for i in range(len):
		for j in range(p[i].burst):
			print(" ", end="")
		print(p[i].id, end="")
		for j in range(p[i].burst):
			print(" ", end="")
		print("|",end="")

	print("\n\t ", end="")

	# hiển thị thanh dưới cùng */
	for i in range(len):
		for j in range(p[i].burst):
			print("---", end="")
		print("  ", end="")
	print("\n\t", end="")
	# hiển thị thời gian tiến trình */
	print("0",end="")

	for i in range(len):
		for j in range(p[i].burst):
			print("  ", end="")

		if p[i].return_time > 9:
			print("\b", end="")

		print(p[i].return_time, end=" ")
	print("\n", end="")
	
def FCFS(p,len:int):

	total_waiting_time = 0
	# khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	total_turnaround_time = 0
	# Khai báo và khởi tạo biến để lưu trữ thời gian hoàn thành toàn bộ quy trình
	total_response_time = 0
	# Khai báo và khởi tạo biến để lưu trữ tổng thời gian phản hồi
	total_return_time = 0
	# khai báo và khởi tạo biến để lưu trữ tổng thời gian trả về

	SortingFunction.mergeSort_arrive_time(p, 0, len-1)
	# sắp xếp theo thời gian đến với lệnh gọi hàm merge_sort_by_arrive_time 

	# thực thi tiến trình đầu tiên xuất hiện
	p[0].return_time = p[0].burst
	p[0].turnaround_time = p[0].return_time - p[0].arrive_time
	p[0].response_time = 0
	p[0].waiting_time = 0

	# tăng tổng lên bằng số tiến trình đã thực thi */
	total_response_time += p[0].response_time
	total_waiting_time += p[0].waiting_time
	total_turnaround_time += p[0].turnaround_time
	total_return_time += p[0].burst

	# tính toán tuần tự từ tiến trình tiếp theo */
	for i in range(1,len):
		# tính toán mỗi thành viên trong tiến trình */
		p[i].waiting_time = total_return_time - p[i].arrive_time
		p[i].return_time = total_return_time + p[i].burst
		p[i].turnaround_time = p[i].return_time - p[i].arrive_time
		p[i].response_time = p[i].waiting_time

		# tăng lên tuỳ theo số tiến trình đã thực thi */
		total_return_time += p[i].burst
		total_waiting_time += p[i].waiting_time
		total_turnaround_time += p[i].turnaround_time
		total_response_time += p[i].response_time

	print("\tFCFS Scheduling Algorithm\n")

	fcfs_print_gantt_chart(p, len)
	# in biểu đồ gantt với lệnh gọi hàm fcfs_print_gantt_chart
	# thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	print("\n\tAverage Waiting Time     : %-2.2lf" %(total_waiting_time / float(len)))
	print("\tAverage Turnaround Time  : %-2.2lf" %(total_turnaround_time / float(len)))
	print("\tAverage Response Time    : %-2.2lf\n" %(total_response_time / float(len)))

	print_table(p, len)
	# print_table bảng dữ liệu đầu ra với lệnh gọi hàm

