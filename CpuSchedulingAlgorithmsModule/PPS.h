#ifndef __PREEMPTIVE__PRIORITY__SCHEDULING__
#define __PREEMPTIVE__PRIORITY__SCHEDULING__

// Preemptive Priority Scheduling Algorithm

/* Khai báo tiêu đề tùy chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [pps_calculate_time PPS Hàm tính thời gian thuật toán]
 * @param p   [description]
 * @param len [description]
 */
void pps_calculate_time(Process *p, int len)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp
	int priority;
	// Khai báo biến để ưu tiên lưu trữ
	int current_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ thời gian hiện tại
	int total_burst_time = 0;
	// Khai báo một biến để lưu tổng thời gian thực hiện
	int k = 0;
	// Khai báo và khởi tạo số để lưu số tiến trình hiện đang thực thi

	/* Phân bổ bộ nhớ động một mảng để lưu trữ thời gian thực hiện còn lại cho mỗi tiến trình */
	int *remain_burst_time = (int *)malloc(sizeof(int) * len);
	/* Phân bổ bộ nhớ động của một mảng được sử dụng để kiểm tra thời gian phản hồi. */
	int *count = (int *)malloc(sizeof(int) * len);

	/* Lặp lại nhiều lần bằng số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		count[i] = 0;
		// khởi tạo mảng count
		remain_burst_time[i] = p[i].burst;
		// Khởi tạo mảng remain_burst_time
		total_burst_time += p[i].burst;
		// Đặt lại tổng thời gian thực hiện còn lại
	}

	/* Lặp lại cho đến khi thời gian hiện tại đạt tổng thời gian thực hiện */
	while (current_time < total_burst_time)
	{
		priority = INT_MAX;
		// Khởi tạo mức độ ưu tiên thành INT_MAX

		/* Nếu thời gian đến nhỏ hơn thời gian đến của tiến trình được nhập cuối cùng. */
		if (current_time <= p[len - 1].arrive_time)
		{
			/* Lặp lại nhiều lần bằng số lượng tiến trình */
			for (i = 0; i < len; i++)
			{
				/* Nếu nó không được hoàn thành, thời gian đến nhỏ hơn hoặc bằng thời gian hiện tại và mức độ ưu tiên nhỏ hơn mức ưu tiên hiện tại. */
				if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time)
							&& (priority > p[i].priority))
				{
					priority = p[i].priority;
					// Cập nhật ưu tiên
					k = i;
					// Cập nhật chỉ mục quy trình
				}
			}
		}

		/* Khi không có thêm quy trình mới nào xuất hiện */
		else
		{
			/* Lặp lại nhiều lần bằng số lượng tiến trình */
			for (i = 0; i < len; i++)
			{
				/* Nếu chưa hoàn thành và mức độ ưu tiên nhỏ hơn mức ưu tiên hiện tại */
				if ((p[i].completed == FALSE)
						&& (priority > p[i].priority))
				{
					priority = p[i].priority;
					// Cập nhật ưu tiên
					k = i;
					// Cập nhật chỉ mục tiến trình
				}
			}
		}

		/* Khi tiến trình đã chọn được bắt đầu lần đầu tiên */
		if (count[k] == 0)
		{
			count[k]++;
			// Không phải là khởi chạy ban đầu
			p[k].response_time = current_time;
			// Lưu thời gian phản hồi của tiến trình đang chạy
		}

		remain_burst_time[k]--;
		// Giảm thời gian còn lại của tiến trình thực hiện
		current_time++;
		// Tăng thời gian hiện tại

		/* Khi thời gian thực hiện còn lại của tiến trình trở thành 0 */
		if (remain_burst_time[k] == 0)
		{
			p[k].completed = TRUE;
			// Thay đổi trạng thái để hoàn thành
			p[k].waiting_time = current_time - p[k].burst - p[k].arrive_time;
			// Tính toán thời gian chờ
			p[k].return_time = current_time;
			// Tính toán thời gian trả về
		}
	}

	/* Giải phóng bộ nhớ của mảng được phân bổ bộ nhớ động */
	free(remain_burst_time);
	free(count);
}

/**
 * [pps_print_gantt_chart: hàm hiển thị biểu đồ Gantt]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void pps_print_gantt_chart(Process *p, int len)
{
	int i;
	int total_burst_time = 0;
	int current_time = 0, previous_time = 0;
	// Khai báo các biến bổ sung để lưu trữ thời gian tiến trình trước đó đã chạy
	int k, pre_k = 0;
	// Khai báo biến bổ sung để lưu trữ số tiến trình trước đó
	int priority, num;
	// Khai báo một biến để lưu trữ khoảng cách giữa các tiến trình mới được khởi chạy

	int *count = (int *)malloc(sizeof(int) * len);
	int *remain_burst_time = (int *)malloc(sizeof(int) * len);

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		total_burst_time += p[i].burst;
		p[i].completed = FALSE;
		count[i] = 0;
	}

	printf("\t ");

	/* Thực hiện cùng một thuật toán và xuất ra thanh trên cùng */
	while (current_time < total_burst_time)
	{
		priority = INT_MAX;

		if (current_time <= p[len - 1].arrive_time)
		{
			for (i = 0; i < len; i++)
			{
				if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time))
				{
					if (priority > p[i].priority)
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}
		}

		else
		{
			for (i = 0; i < len; i++)
			{
				if (p[i].completed == FALSE)
				{
					if (priority > p[i].priority)
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}
		}

		/* Nếu quy trình này khác với quy trình được thực hiện trước đó */
		if (pre_k != k)
			printf(" ");
			// hiển thị khoảng trắng

		printf("--");
		remain_burst_time[k]--;
		current_time++;
		pre_k = k;
		// Lưu tiến trình trước đó

		if (remain_burst_time[k] == 0)
			p[k].completed = TRUE;
	}

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		p[i].completed = FALSE;
	}

	printf("\n\t|");
	current_time = 0;

	/* Thực thi cùng một thuật toán và in ra ID tiến trình. So sánh với tiến trình trước đó và điều chỉnh khoảng cách sử dụng \b */
	while (current_time < total_burst_time)
	{
		priority = INT_MAX;

		if (current_time <= p[len - 1].arrive_time)
		{
			for (i = 0; i < len; i++)
			{
				if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time))
				{
					if (priority > p[i].priority)
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}
		}

		else
		{
			for (i = 0; i < len; i++)
			{
				if (p[i].completed == FALSE)
				{
					if (priority > p[i].priority)
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}
		}

		if (current_time == 0)
		{
			count[k]++;
			printf("  ");
		}

		else
		{
			/* Nếu quy trình này khác với quy trình trước đó */
			if (pre_k != k)
			{
				num = count[pre_k] + 1;
				// lưu khoảng thời gian giữa hai tiến trình
				count[pre_k] = 0;
				// Đặt lại số lượng tiến trình trước đó
				count[k]++;
				// Tăng số lượng tiến trình hiện tại
				/* hiển thị \b bằng mức chênh lệch giữa hai tiến trình */
				for (i= 0; i < num; i++)
					printf("\b");

				/* Đầu ra ID tiến trình trước đó */
				printf("%2s", p[pre_k].id);

				/* In khoảng trống theo khoảng thời gian */
				for (i = 0; i < num - 2; i++)
					printf(" ");

				printf("|  ");
			}

			/* nếu cùng 1 tiến trình */
			else
			{
				// Tăng số lượng quy trình hiện tại
				count[k]++;

				printf("  ");
				// hiển thị khoảng trắng

				/* Khi quá trình cuối cùng được thực hiện */
				if (current_time == total_burst_time - 1)
				{
					num = count[pre_k] + 1;
					count[pre_k] = 0;
					count[k]++;

					for (i = 0; i < num; i++)
						printf("\b");

					printf("%2s", p[pre_k].id);

					for (i = 0; i < num - 2; i++)
						printf(" ");
				}
			}
		}

		pre_k = k;
		remain_burst_time[k]--;
		current_time++;

		if (remain_burst_time[k] == 0)
			p[k].completed = TRUE;
	}

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		p[i].completed = FALSE;
	}

	printf("|\n\t");
	current_time = 0;

	/* hiển thị thanh dưới cùng bằng thuật toán tương tự */
	while (current_time < total_burst_time)
	{
		priority = INT_MAX;

		if (current_time <= p[len - 1].arrive_time)
		{
			for (i = 0; i < len; i++)
			{
				if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time))
				{
					if (priority > p[i].priority)
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}
		}

		else
		{
			for (i = 0; i < len; i++)
			{
				if (p[i].completed == FALSE)
				{
					if (priority > p[i].priority)
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}
		}

		if (pre_k != k)
			printf(" ");

		printf("--");

		remain_burst_time[k]--;
		current_time++;
		pre_k = k;

		if (remain_burst_time[k] == 0)
			p[k].completed = TRUE;
	}

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		p[i].completed = FALSE;
	}

	current_time = 0;
	num = 0;
	printf("\n\t");

	/* Thực hiện cách tương tự như in ID tiến trình, nhưng in thời gian thay vì ID tiến trình */
	while (current_time <= total_burst_time)
	{
		if (total_burst_time != current_time)
		{
			priority = INT_MAX;

			if (current_time <= p[len - 1].arrive_time)
			{
				for (i = 0; i < len; i++)
				{
					if ((p[i].completed == FALSE)
							&& (p[i].arrive_time <= current_time))
					{
						if (priority > p[i].priority)
						{
							priority = p[i].priority;
							k = i;
						}
					}
				}
			}

			else
			{
				for (i = 0; i < len; i++)
				{
					if ((p[i].completed == FALSE)
							&& (priority > p[i].priority))
					{
						priority = p[i].priority;
						k = i;
					}
				}
			}


			if (pre_k != k)
			{
				for (i = 0; i < num && current_time != 0; i++)
					printf("  ");

				if (current_time != 0)
					printf(" ");

				printf("%-2d", current_time);
				num = 0;

				previous_time = current_time;
			}

			else
				num++;

			remain_burst_time[k]--;
			current_time++;
			pre_k = k;

			if (remain_burst_time[k] == 0)
				p[k].completed = TRUE;
		}

		else
		{
			for (i = 0; i < current_time - previous_time - 1; i++)
				printf("  ");
			printf(" ");

			printf("%-2d", current_time);

			break;
		}
	}

	printf("\n");

	free(count);
	free(remain_burst_time);
}

/**
 * [PPS PPS hàm thực thi thuật toán]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void PPS(Process *p, int len)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp
	int total_waiting_time = 0;
	// Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	int total_turnaround_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ tổng thời gian xử lý
	int total_response_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ tổng thời gian phản hồi

	process_init(p, len);
	// Khởi tạo một tiến trình bằng lệnh gọi hàm process_init

	merge_sort_by_arrive_time(p, 0, len);
	// Sắp xếp theo thời gian đến với lệnh gọi hàm merge_sort_by_arrive_time 

	pps_calculate_time(p, len);
	// Tính thời gian tiến trình bằng lệnh gọi hàm pps_calculate_time

	/* Lặp lại nhiều lần theo số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		p[i].turnaround_time = p[i].return_time - p[i].arrive_time;
		// tính toán Turnaround Time
		total_waiting_time += p[i].waiting_time;
		// Tăng tổng thời gian chờ 
		total_turnaround_time += p[i].turnaround_time;
		// Tăng tổng thời gian xử lý
		total_response_time += p[i].response_time;
		// Tăng tổng thời gian phản hồi
	}

	printf("\tPreemptive Priority Scheduling Algorithm\n\n");

	pps_print_gantt_chart(p, len);
	// In biểu đồ Gantt với lệnh gọi hàm pps_print_gantt_chart 

	/* Thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// Bảng dữ liệu đầu ra với lệnh gọi hàm print_table 
}

#endif
