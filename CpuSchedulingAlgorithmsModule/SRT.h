#ifndef __SHORTEST__REMAINING__TIME
#define __SHORTEST__REMAINING__TIME

// Shortest Remaining Time Algorithm

/* Khai báo tiêu đề tùy chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [srt_calculate_time Hàm tính toán thời gian thuật toán SRT]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void srt_calculate_time(Process *p, int len)
{
	int i;
	// Khai báo biến để sử dụng trong vòng lặp
	int current_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ thời gian hiện tại
	int total_burst_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian thực thi
	int shortest_remain_time;
	// Khai báo biến để lưu trữ chỉ số của phần tử có thời gian nhỏ nhất
	int k = 0;
	// Khai báo và khởi tạo biến để lưu trữ số tiến trình đang thực thi hiện tại

	/* Cấp phát bộ nhớ động để lưu trữ thời gian còn lại của mỗi tiến trình */
	int *remain_burst_time = (int *)malloc(sizeof(int) * len);
	/* Cấp phát bộ nhớ động của một mảng được sử dụng để kiểm tra thời gian phản hồi. */
	int *count = (int *)malloc(sizeof(int) * len);

	/* Lặp lại theo số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		count[i] = 0;
		// Khởi tạo mảng count
		remain_burst_time[i] = p[i].burst;
		// Khởi tạo mảng remain_burst_time 
		total_burst_time += p[i].burst;
		// Khởi tạo tổng thời gian thực thi còn lại
	}

	/* Lặp cho đến khi thời gian hiện tại bằng tổng thời gian thực thi */
	while (current_time < total_burst_time)
	{
		shortest_remain_time = INT_MAX;
		// Khởi tạo chỉ số của công việc nhỏ nhất với INT_MAX

		/* Nếu thời gian đến của công việc cuối cùng lớn hơn thời gian hiện tại */
		if (current_time <= p[len - 1].arrive_time)
		{
			/* Lặp lại theo số lượng tiến trình */
			for (i = 0; i < len; i++)
			{
				/* Nếu công việc chưa hoàn thành, và thời gian đến của nó nhỏ hơn hoặc bằng thời gian hiện tại, 
    					và thời gian thực hiện còn lại ít hơn thời gian công việc tối thiểu hiện tại */
				if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time)
							&& (shortest_remain_time > remain_burst_time[i]))
				{
					shortest_remain_time = remain_burst_time[i];
					// Cập nhật thời gian thực hiện tối thiểu
					k = i;
					// Cập nhật chỉ số của tiến trình có thời gian thực hiện tối thiểu
				}
			}
		}

		/* Trường hợp không còn tiến trình mới nào đến nữa */
		else
		{
			/* Lặp lại theo số lượng tiến trình */
			for (i = 0; i < len; i++)
			{
				/* Nếu công việc chưa hoàn thành và thời gian thực hiện còn lại ít hơn thời gian thực hiện 
    				tối thiểu hiện tại */
				if ((p[i].completed == FALSE)
						&& (shortest_remain_time > remain_burst_time[i]))
				{
					shortest_remain_time = remain_burst_time[i];
					// Cập nhật thời gian thực hiện tối thiểu
					k = i;
					// Cập nhật chỉ số của tiến trình có thời gian thực hiện tối thiểu
				}
			}
		}

		/* Nếu tiến trình được chọn bắt đầu lần đầu tiên */
		if (count[k] == 0)
		{
			count[k]++;
			// Đánh dấu rằng đó không phải là lần thực thi đầu tiên
			p[k].response_time = current_time;
			// Lưu trữ thời gian phản hồi của tiến trình đang thực hiện
		}

		remain_burst_time[k]--;
		// Giảm thời gian còn lại của tiến trình đã thực hiện
		current_time++;
		// Tăng thời gian hiện tại

		/* Nếu thời gian còn lại của tiến trình giảm xuống 0 */
		if (remain_burst_time[k] == 0)
		{
			p[k].completed = TRUE;
			// Đổi trạng thái thành đã hoàn thành
			p[k].waiting_time = current_time - p[k].burst - p[k].arrive_time;
			// Tính toán thời gian chờ
			p[k].return_time = current_time;
			// Tính toán thời gian trả về
		}
	}

	/* Giải phóng bộ nhớ đã cấp phát cho mảng động */
	free(count);
	free(remain_burst_time);
}

/**
 * [srt_print_gantt_chart Hàm in biểu đồ Gantt]
 * @param p   [Mảng cấu trúc tiến trình]
 * @param len [Số lượng tiến trình]
 */
void srt_print_gantt_chart(Process *p, int len)
{
	int i;
	int total_burst_time = 0;
	int current_time = 0, previous_time;
	// Khai báo thêm biến để lưu trữ thời gian tiến trình trước đó đã chạy
	int k, pre_k = 0;
	// Khai báo thêm biến để lưu trữ số thứ tự của tiến trình trước đó
	int shortest_remain_time, num;
	// Khai báo thêm biến để lưu trữ khoảng cách giữa hai tiến trình mới được chạy

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

	/* In thanh tiêu đề trong khi thực hiện cùng một thuật toán */
	while (current_time < total_burst_time)
	{
		shortest_remain_time = INT_MAX;

		if (current_time <= p[len - 1].arrive_time)
		{
			for (i = 0; i < len; i++)
			{
				if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time))
				{
					if (shortest_remain_time > remain_burst_time[i])
					{
						shortest_remain_time = remain_burst_time[i];
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
					if (shortest_remain_time > remain_burst_time[i])
					{
						shortest_remain_time = remain_burst_time[i];
						k = i;
					}
				}
			}
		}

		/* Nếu tiến trình hiện tại khác với tiến trình đã thực hiện trước đó */
		if (pre_k != k)
			printf(" ");
			// In dấu cách

		printf("--");
		remain_burst_time[k]--;
		current_time++;
		pre_k = k;
		// Lưu trữ tiến trình đã thực hiện trước đó

		if (remain_burst_time[k] == 0)
			p[k].completed = TRUE;
	}

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		p[i].completed = FALSE;
	}

	current_time = 0;
	printf("\n\t|");

	/* Thực thi cùng một thuật toán và in ID tiến trình. 
 	So sánh với tiến trình trước đó và sử dụng \b để điều chỉnh khoảng cách */
	while (current_time <= total_burst_time)
	{
		/* Nếu thời gian hiện tại khác với tổng thời gian thực thi */
		if (current_time != total_burst_time)
		{
			shortest_remain_time = INT_MAX;

			if (current_time <= p[len - 1].arrive_time)
			{
				for (i = 0; i < len; i++)
				{
					if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time)
							&& (shortest_remain_time > remain_burst_time[i]))
					{
						shortest_remain_time = remain_burst_time[i];
						k = i;
					}
				}
			}

			else
			{
				for (i = 0; i < len; i++)
				{
					if ((p[i].completed == FALSE)
						&& (shortest_remain_time > remain_burst_time[i]))
					{
						shortest_remain_time = remain_burst_time[i];
						k = i;
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
				/* Nếu tiến trình hiện tại khác với tiến trình trước đó */
				if (pre_k != k)
				{
					num = count[pre_k] + 1;
					// Lưu trữ sự khác biệt về thời gian giữa hai tiến trình
					count[pre_k] = 0;
					// Khởi tạo lại bieens đếm của tiến trình trước đó
					count[k]++;
					// Tăng biến đếm của tiến trình hiện tại

					/* In dấu cách bằng với sự khác biệt về thời gian giữa hai tiến trình */
					for (i = 0; i < num; i++)
						printf("\b");

					/* In ID của tiến trình trước đó */
					printf("%2s", p[pre_k].id);

					/* In các khoảng trắng để điều chỉnh khoảng cách */
					for (i = 0; i < num - 2; i++)
						printf(" ");

					printf("|  ");
				}

				/* Nếu tiến trình hiện tại giống với tiến trình trước đó */
				else
				{
					count[k]++;
					// Tăng biến đếm của tiến trình hiện tại

					printf("  ");
					// In dấu cách
				}
			}

			pre_k = k;
			remain_burst_time[k]--;
			current_time++;

			if (remain_burst_time[k] == 0)
				p[k].completed = TRUE;
		}

		/* Nếu thời gian thực thi hiện tại bằng tổng thời gian thực thi */
		else
		{
			/* In các dấu \b trong thời gian thực hiện trước đó */
			for (i = 0; i < count[pre_k] + 1; i++)
				printf("\b");

			/* In ID của tiến trình hiện tại */
			printf("%2s", p[k].id);

			/* In các khoảng trắng để điều chỉnh khoảng cách */
			for (i = 0; i < count[pre_k] - 1; i++)
				printf(" ");

			break;
			// Thoát khỏi vòng lặp
		}
	}

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		p[i].completed = FALSE;
	}

	current_time = 0;
	printf("|\n\t");

	/* Sử dụng cùng một thuật toán để in thanh tiêu đề phía dưới */
	while (current_time < total_burst_time)
	{
		shortest_remain_time = INT_MAX;

		if (current_time <= p[len - 1].arrive_time)
		{
			for (i = 0; i < len; i++)
			{
				if ((p[i].completed == FALSE)
					&& (p[i].arrive_time <= current_time)
						&& (shortest_remain_time > remain_burst_time[i]))
				{
					shortest_remain_time = remain_burst_time[i];
					k = i;
				}
			}
		}

		else
		{
			for (i = 0; i < len; i++)
			{
				if ((p[i].completed == FALSE)
					&& (shortest_remain_time > remain_burst_time[i]))
				{
					shortest_remain_time = remain_burst_time[i];
					k = i;
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
	printf("\n\t");

	/* In ID tiến trình và hiển thị thời gian tương tự */
	while (current_time <= total_burst_time)
	{
		if (total_burst_time != current_time)
		{
			shortest_remain_time = INT_MAX;

			if (current_time <= p[len - 1].arrive_time)
			{
				for (i = 0; i < len; i++)
				{
					if ((p[i].completed == FALSE)
						&& (p[i].arrive_time <= current_time)
							&& (shortest_remain_time > remain_burst_time[i]))
					{
						shortest_remain_time = remain_burst_time[i];
						k = i;
					}
				}
			}

			else
			{
				for (i = 0; i < len; i++)
				{
					if ((p[i].completed == FALSE)
						&& (shortest_remain_time > remain_burst_time[i]))
					{
						shortest_remain_time = remain_burst_time[i];
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

	/* Giải phóng bộ nhớ đã cấp phát cho mảng động */
	free(count);
	free(remain_burst_time);
}

/**
 * [SRT  Gọi hàm SRT thực thi thuật toán]
 * @param p   [Mảng cấu trúc tiến trình]
 * @param len [Số lượng tiến trình]
 */
void SRT(Process *p, int len)
{
	int i;
	// Khai báo biến sử dụng trong vòng lặp
	int total_waiting_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian chờ
	int total_turnaround_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian turnaround
	int total_response_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian phản hồi

	process_init(p, len);
	// Gọi hàm process_init để khởi tạo tiến trình

	merge_sort_by_arrive_time(p, 0, len);
	// Gọi hàm merge_sort_by_arrive_time để sắp xếp theo thời gian đến

	srt_calculate_time(p, len);
	// Gọi hàm srt_calculate_time để tính thời gian của các tiến trình

	/* Lặp lại theo số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		p[i].turnaround_time = p[i].return_time - p[i].arrive_time;
		// Tính toán thời gian turnaround
		total_waiting_time += p[i].waiting_time;
		// Tăng tổng thời gian chờ lên
		total_turnaround_time += p[i].turnaround_time;
		// Tăng tổng thời gian turnaround lên
		total_response_time += p[i].response_time;
		// Tăng tổng thời gian phản hồi lên
	}

	printf("\tShortest Remaining Time Algorithm\n\n");

	srt_print_gantt_chart(p, len);
	// Gọi hàm srt_print_gantt_chart để in biểu đồ Gantt

	/* In ra thời gian chờ trung bình, thời gian turnaround trung bình và thời gian phản hồi trung bình */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// Gọi hàm print_table để in bảng dữ liệu
}

#endif
