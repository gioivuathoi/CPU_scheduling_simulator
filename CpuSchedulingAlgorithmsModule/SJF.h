#ifndef __SHORTEST__JOB__FIRST__
#define __SHORTEST__JOB__FIRST__

// Shortest Job First Algorithmd

/* Khai báo tiêu đề tùy chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [sjf_calculate_time Hàm tính toán thời gian thuật toán SJF]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void sjf_calculate_time(Process *p, int len)
{
	int i, j;
	// Khai báo các biến sử dụng trong vòng lặp
	int curr_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ thời gian hiện tại
	int min = 0;
	// Khai báo và khởi tạo biến để lưu trữ chỉ số của phần tử có thời gian nhỏ nhất

	/* Thời gian thực thi của tiến trình được thực hiện đầu tiên */
	p[0].completed = TRUE;
	p[0].return_time = p[0].burst;
	p[0].turnaround_time = p[0].burst - p[0].arrive_time;
	p[0].waiting_time = 0;
	
	curr_time = p[0].burst;
	// Tăng thời gian hiện tại lên theo thời gian của tiến trình đã hoàn thành

	/* Duyệt qua số lượng tiến trình - 1 lần */
	for(i = 1; i < len; i++)
	{
		/* Duyệt qua số lượng tiến trình -1 */
		for (j = 1; j < len; j++)
		{
			/* Nếu quá trình này đã được hoàn thành */
			if (p[j].completed == TRUE)
				continue;
				// Đi tới vòng lặp tiếp theo

			/* Nếu quá trình này vẫn chưa hoàn tất */
			else
			{
				min = j;
				// khởi tạo biến min 
				break;
				// thoát vòng lặp
			}
		}

		/* Duyệt qua số lượng tiến trình -1 */
		for (j = 1; j < len; j++)
		{
			/* Tìm kiếm tiến trình thỏa mãn điều kiện có thời gian thực hiện nhỏ nhất */
			if ((p[j].completed == FALSE)
					&& (p[j].arrive_time <= curr_time)
						&& (p[j].burst < p[min].burst))
			{
				min = j;
				// Cập nhật tiến trình có thời gian thực hiện nhỏ nhất
			}
		}

		p[min].waiting_time = curr_time - p[min].arrive_time;
		// Tính thời gian chờ tiến trình để chạy
		p[min].completed = TRUE;
		// Thay đổi trạng thái của tiến trình được thực thi sang trạng thái hoàn thành

		curr_time += p[min].burst;
		// Tăng thời gian hiện tại lên theo thời gian thực hiện của tiến trình

		p[min].return_time = curr_time;
		// Tính toán thời gian trả về của tiến trình
		p[min].turnaround_time = p[min].return_time - p[min].arrive_time;
		// Tính toán thời gian turnaround của tiến trình
	}
}

/**
 * [sjf_print_gantt_chart Hàm hiển thị biểu đồ Gantt]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void sjf_print_gantt_chart(Process *p, int len)
{
	int i, j;
	// Khai báo các biến sử dụng trong vòng lặp

	printf("\t ");

	/* đầu ra thanh trên cùng */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("--");

		printf(" ");
	}

	printf("\n\t|");

	/* Đầu ra ID tiến trình */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst - 1; j++)
			printf(" ");

		printf("%s", p[i].id);

		for (j = 0; j < p[i].burst - 1; j++)
			printf(" ");

		printf("|");
	}

	printf("\n\t ");

	/* đầu ra thanh dưới cùng */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("--");

		printf(" ");
	}

	printf("\n\t");

	printf("0");

	/* Đầu ra thời gian thực hiện tiến trình */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("  ");

		if (p[i].turnaround_time > 9)
			printf("\b");

		printf("%d", p[i].return_time);
	}

	printf("\n");
}

/**
 * [SJF SJF hàm thực thi thuật toán]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void SJF(Process *p, int len)
{
	int i;
	// Khai báo biến để sử dụng trong vòng lặp
	int total_waiting_time = 0;
	// Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	int total_turnaround_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian turnaround
	int total_response_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian phản hồi

	process_init(p, len);
	// Gọi hàm process_init() để khởi tạo các tiến trình

	merge_sort_by_arrive_time(p, 0, len);
	// Gọi hàm merge_sort_by_arrive_time() để sắp xếp các tiến trình theo thời gian đến

	sjf_calculate_time(p, len);
	// Gọi hàm sjf_calculate_time() để tính thời gian của các tiến trình

	/* Lặp lại theo số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		p[i].return_time = p[i].turnaround_time + p[i].arrive_time;
		// Tính toán và lưu trữ thời gian trả về của tiến trình
		p[i].response_time = p[i].waiting_time;
		// Lưu trữ thời gian phản hồi của tiến trình

		total_waiting_time += p[i].waiting_time;
		// Tăng tổng thời gian chờ lên
		total_turnaround_time += p[i].turnaround_time;
		// Tăng tổng thời gian turnaround lên
		total_response_time += p[i].response_time;
		// Tăng tổng thời gian phản hồi lên
	}

	printf("\tSJF Scheduling Algorithms\n\n");

	quick_sort_by_return_time(p, len);
	// Gọi hàm quick_sort_by_return_time() để sắp xếp các tiến trình theo thời gian trả về

	sjf_print_gantt_chart(p, len);
	// Gọi hàm sjf_print_gantt_chart() để in biểu đồ Gantt

	/* In ra thời gian chờ trung bình, thời gian turnaround trung bình và thời gian phản hồi trung bình */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// Gọi hàm print_table() để in bảng dữ liệu
}

#endif
