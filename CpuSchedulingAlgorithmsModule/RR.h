#ifndef __Round__ROBIN__
#define __Round__ROBIN__

// Round Robin Scheduling

/* Khai báo tiêu đề tùy chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [Hàm tính toán độ trễ thuật toán RR rr_calculate_waiting_time ]
 * @param p   [description]
 * @param len [description]
 * @param q   [description]
 */
void rr_calculate_waiting_time(Process *p, int len, Quantum q)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp
	int curr_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ thời gian hiện tại

	/* Phân bổ bộ nhớ động một mảng để lưu trữ thời gian thực hiện còn lại cho mỗi tiến trình */
	int *remain_burst_time = (int *)malloc(sizeof(int) * len);
	/* Phân bổ bộ nhớ động của một mảng được sử dụng để kiểm tra thời gian phản hồi. */
	int *calc_response_time = (int *)malloc(sizeof(int) * len);

	/* Lặp lại nhiều lần theo số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		// Khởi tạo mảng để lưu trữ thời gian thực hiện còn lại
		calc_response_time[i] = FALSE;
		// Xác nhận việc tính toán thời gian phản hồi và khởi tạo mảng kiểm tra
	}

	/* Lặp lại cho đến khi tất cả các tiến trình hoàn tất */
	while (TRUE)
	{
		int check = TRUE;
		// Khởi tạo biến check 

		/* Lặp lại nhiều lần theo số lượng tiến trình */
		for (i = 0; i < len; i++)
		{
			/* Nếu thời gian thực hiện vẫn còn */
			if (remain_burst_time[i] > 0)
			{
				check = FALSE;
				// Xử lý biến kiểm tra 'check' thành giá trị FALSE

				/* Nếu thời gian phản hồi chưa được tính toán */
				if (calc_response_time[i] == FALSE)
				{
					p[i].response_time = curr_time - p[i].arrive_time;
					// Tính toán và lưu thời gian phản hồi
					calc_response_time[i] = TRUE;
					// Quá trình tính toán thời gian phản hồi
				}

				/* Trong trường hợp thời gian còn lại lớn hơn thời gian được cấp */
				if (remain_burst_time[i] > q)
				{
					curr_time += q;
					// Tăng thời gian hiện tại lên một lượng bằng thời gian cấp phát
					remain_burst_time[i] -= q;
					// Giảm thời gian còn lại của tiến trình đang chạy
				}

				/* Khi thời gian còn lại ít hơn thời gian cho phép */
				else
				{
					curr_time += remain_burst_time[i];
					// Thời gian hiện tại tăng theo thời gian còn lại
					p[i].waiting_time = curr_time - p[i].burst;
					// Tính toán thời gian chờ
					remain_burst_time[i] = 0;
					// Thay đổi thời gian còn lại về 0
				}
			}
		}

		/* Khi tất cả các quá trình được hoàn thành */
		if (check == TRUE)
			break;
			// Thoát khỏi vòng lặp vô hạn
	}

	free(remain_burst_time);
	// Phân bổ bộ nhớ mảng được cấp phát động
}

/**
 * [rr_calculate_turnaround_time hàm tính toán turnaround time]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void rr_calculate_turnaround_time(Process *p, int len)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp

	/* Lặp lại nhiều lần theo số lượng tiến trình */
	for (i = 0; i < len; i++)
		p[i].turnaround_time = p[i].burst + p[i].waiting_time - p[i].arrive_time;
		// Sau khi tính toán thời gian turnaround, lưu trữ nó
}

/**
 * [rr_print_gantt_chart Hàm đầu ra biểu đồ Round Robin Gantt]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [Số lượng tiến trình]
 * @param q   [thời gian cung cấp]
 */
void rr_print_gantt_chart(Process *p, int len, Quantum q)
{
	int i, j;
	// Khai báo các biến sử dụng trong vòng lặp
	int curr_time = 0, total_burst_time = 0;
	// Khai báo và khởi tạo các biến để lưu trữ thời gian hiện tại và tổng thời gian thực hiện
	int temp_total_burst_time = 0;
	// Khai báo và khởi tạo các biến để lưu trữ giá trị tạm thời

	/* Phân bổ bộ nhớ động một mảng để lưu trữ thời gian thực hiện còn lại cho mỗi tiến trình */
	int *remain_burst_time = (int *)malloc(sizeof(int) * len);

	/* Lặp lại nhiều lần bằng số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
		// Khởi tạo mảng lưu trữ thời gian còn lại
		total_burst_time += p[i].burst;
		// tổng thời gian thực hiện
	}

	printf("\t");

	/* Hiển thị thanh trạng thái giống với thuật toán tính thời gian chờ */
	while (TRUE)
	{
		int check = TRUE;

		for (i = 0; i < len; i++)
		{
			if (remain_burst_time[i] > 0)
			{
				check = FALSE;

				if (remain_burst_time[i] < q)
				{
					printf(" ");
					for (j = 0; j < remain_burst_time[i]; j++)
						printf("--");
				}

				else
				{
					printf(" ");
					for (j = 0; j <= q; j++)
						printf("--");
				}

				if (remain_burst_time[i] > q)
				{
					curr_time += q;
					remain_burst_time[i] -= q;
				}

				else
				{
					curr_time += remain_burst_time[i];
					p[i].waiting_time = curr_time - p[i].burst;
					remain_burst_time[i] = 0;
				}


			}
		}

		if (check == TRUE)
			break;
	}

	printf(" \n\t");

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
	}

	/* Đầu ra ID tiến trình */
	while (TRUE)
	{
		int check = TRUE;

		for (i = 0; i < len; i++)
		{
			if (remain_burst_time[i] > 0)
			{
				check = FALSE;

				if (remain_burst_time[i] < q)
				{
					printf("|");

					if (remain_burst_time[i] != 1)
					{
						for (j = 0; j <= remain_burst_time[i] / 2; j++)
							printf(" ");

						printf("%2s", p[i].id);

						for (j = 0; j <= remain_burst_time[i] / 2; j++)
							printf(" ");
					}

					else
						printf("%2s", p[i].id);
				}

				else
				{
					printf("|");

					for (j = 0; j < q; j++)
						printf(" ");

					printf("%2s", p[i].id);

					for (j = 0; j < q; j++)
						printf(" ");
				}

				if (remain_burst_time[i] > q)
				{
					curr_time += q;
					remain_burst_time[i] -= q;
				}

				else
				{
					curr_time += remain_burst_time[i];
					p[i].waiting_time = curr_time - p[i].burst;
					remain_burst_time[i] = 0;
				}


			}
		}

		if (check == TRUE)
			break;
	}

	printf("|\n\t");

	for (i = 0; i < len; i++)
	{
		remain_burst_time[i] = p[i].burst;
	}

	/* đầu ra thanh dưới cùng */
	while (TRUE)
	{
		int check = TRUE;

		for (i = 0; i < len; i++)
		{
			if (remain_burst_time[i] > 0)
			{
				check = FALSE;

				if (remain_burst_time[i] < q)
				{
					printf(" ");
					for (j = 0; j < remain_burst_time[i]; j++)
						printf("--");
				}

				else
				{
					printf(" ");
					for (j = 0; j <= q; j++)
						printf("--");
				}

				if (remain_burst_time[i] > q)
				{
					curr_time += q;
					remain_burst_time[i] -= q;
				}

				else
				{
					curr_time += remain_burst_time[i];
					p[i].waiting_time = curr_time - p[i].burst;
					remain_burst_time[i] = 0;
				}


			}
		}

		if (check == TRUE)
			break;
	}

	printf("\n\t");

	for (i = 0; i < len; i++)
		remain_burst_time[i] = p[i].burst;

	curr_time = 0;

	/* Đầu ra thời gian xử lý */
	while (TRUE)
	{
		int check = TRUE;

		for (i = 0; i < len; i++)
		{
			if (remain_burst_time[i] > 0)
			{
				check = FALSE;

				if (remain_burst_time[i] < q)
				{
					printf("%-2d", curr_time);

					for (j = 0; j < remain_burst_time[i] - 1; j++)
						printf("  ");

					printf(" ");
				}

				else
				{
					printf("%-2d", curr_time);

					for (j = 0; j < q; j++)
						printf("  ");

					printf(" ");
				}

				if (remain_burst_time[i] > q)
				{
					curr_time += q;
					remain_burst_time[i] -= q;
				}

				else
				{
					curr_time += remain_burst_time[i];
					p[i].waiting_time = curr_time - p[i].burst;
					remain_burst_time[i] = 0;
				}
			}
		}

		if (check == TRUE)
			break;
	}

	printf("%-3d\n", total_burst_time);

	printf("\n");

	free(remain_burst_time);
	// Giải phóng bộ nhớ của mảng được phân bổ bộ nhớ động
}

/**
 * [RR hàm thực thi thuật toán]
 * @param p       [mảng cấu trúc tiến trình]
 * @param len     [số lượng tiến trình]
 * @param quantum [time quantum]
 */
void RR(Process *p, int len, Quantum quantum)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp
	int total_waiting_time = 0;
	// Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	int total_turnaround_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian turnaround
	int total_response_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ tổng thời gian phản hồi

	process_init(p, len);
	// Khởi tạo một tiến trình bằng lệnh gọi hàm process_init 

	merge_sort_by_arrive_time(p, 0, len);
	// Sắp xếp theo thời gian đến với lệnh gọi hàm merge_sort_by_arrive_time 

	rr_calculate_waiting_time(p, len, quantum);
	// Tính thời gian chờ, thời gian phản hồi bằng lệnh gọi hàm rr_calculate_waiting_time 

	rr_calculate_turnaround_time(p, len);
	// Tính thời gian quay vòng bằng lệnh gọi hàm rr_calculate_turnaround_time 

	/* Lặp lại nhiều lần theo số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		p[i].waiting_time = p[i].turnaround_time - p[i].burst;
		// Tính thời gian chờ đợi và lưu lại
		p[i].return_time = p[i].arrive_time + p[i].burst + p[i].waiting_time;
		// Tính toán thời gian hoàn thành và lưu trữ

		total_waiting_time += p[i].waiting_time;
		// Tăng tổng thời gian chờ
		total_turnaround_time += p[i].turnaround_time;
		// Tăng tổng thời gian turnaround
		total_response_time += p[i].response_time;
		// Tăng tổng thời gian phản hồi
	}

	printf("\tRound Robin Scheduling Algorithm ( Quantum : %d )\n\n", quantum);

	rr_print_gantt_chart(p, len, quantum);
	// In biểu đồ Gantt với lệnh gọi hàm rr_print_gantt_chart 

	/* Thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// Bảng dữ liệu đầu ra với lệnh gọi hàm print_table 
}

#endif
