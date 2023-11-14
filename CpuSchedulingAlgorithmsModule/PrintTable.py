from CpuSchedulingAlgorithmsModule.Process import Process

 # print_table: Chức năng hiển thị bảng dữ liệu tiến trình]
 # p [mảng cấu trúc tiến trình]
 # n [số lượng tiến trình]

def print_table(p, n):

	print("\t+-----+------------+-------------+----------+-------------+-----------------+--------------+-----------------+")
	print("\t| PID | Burst Time | Arrive Time | Priority | Return Time |  Response Time  | Waiting Time | Turnaround Time |")
	print("\t+-----+------------+-------------+----------+-------------+-----------------+--------------+-----------------+")

	# Thực hiện lặp lại theo số lượng tiến trình và định dạng thông tin để in ra 
	for i in range(n):
		print("\t| %3s |     %3d    |     %3d     |    %3d   |     %3d     |      %3d        |      %3d     |        %3d      |" %(p[i].id, p[i].burst, p[i].arrive_time, p[i].priority, p[i].return_time, p[i].response_time, p[i].waiting_time, p[i].turnaround_time))
		print("\t+-----+------------+-------------+----------+-------------+-----------------+--------------+-----------------+")

	print("\n")


