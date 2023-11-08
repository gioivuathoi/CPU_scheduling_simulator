#ifndef __HIGHEST__RESPONSE__RATIO__NEXT__
#define __HIGHEST__RESPONSE__RATIO__NEXT__

// HRN Algorithm

/* Khai báo tiêu đề tuỳ chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [hrn_print_gantt_chart Hàm hiển thị biểu đồ Gantt]
 * @param p   [mảng cấu thúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void hrn_print_gantt_chart(Process *p, int len)
{
	int i, j;
	// khai báo các biến sử dụng trong vòng lặp

	printf("\t ");

	/* hiển thị thanh đầu trang */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("--");

		printf(" ");
	}

	printf("\n\t|");

	/* hiển thị ID tiến trình */
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

	/* hiển thị thanh dưới cùng */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("--");

		printf(" ");
	}

	printf("\n\t");

	/* hiển thị thời gian tiến trình */
	printf("0");

	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("  ");

		if (p[i].return_time > 9)
			printf("\b");

		printf("%d", p[i].return_time);
	}

	printf("\n");
}

/**
 * [HRN HRN hàm thực thi thuật toán]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void HRN(Process *p, int len)
{
	int i, j;
	// khai báo các biến sử dụng trong vòng lặp
	int time, loc;
	// Khai báo một biến để lưu trữ thời gian và vị trí tiến trình hiện tại
	int total_burst_time = 0;
	// khai báo và khởi tạo một biến để lưu trữ tổng thời gian thực hiện
	int total_waiting_time = 0;
	// khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	int total_turnaround_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ thời gian hoàn thành toàn bộ quy trình
	int total_response_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian phản hồi

	float hrr, temp;
	// hrr Khai báo một biến để lưu trữ mức độ ưu tiên của thuật toán

	process_init(p, len);
	// process_init khởi tạo một tiến trình bằng lệnh gọi hàm

	/* lặp lại nhiều lần bằng số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		total_burst_time += p[i].burst;
		// tổng thời gian thực hiện
	}

	merge_sort_by_arrive_time(p, 0, len);
	// merge_sort_by_arrive_time sắp xếp thời gian đến với lệnh gọi hàm

	/* Lặp lại cho đến khi thời gian hiện tại bằng tổng thời gian thực hiện */
	for (time = p[0].arrive_time; time < total_burst_time;)
	{
		hrr = -9999;
		// Đặt lại mức độ ưu tiên về -9999

		/* Lặp lại nhiều lần bằng số lượng tiến trình */
		for (i = 0; i < len; i++)
		{
			/* Nếu quá trình đã đến nhưng chưa hoàn thành */
			if ((p[i].arrive_time <= time)
					&& (p[i].completed != TRUE))
			{
				temp = (p[i].burst + (time - p[i].arrive_time)) / p[i].burst;
				// (Tính toán mức độ ưu tiên dựa trên thời gian thực hiện + thời gian chờ)/thời gian thực hiện

				/* Nếu mức độ ưu tiên cao hơn */
				if (hrr < temp)
				{
					hrr = temp;
					// Cập nhật giá trị ưu tiên
					loc = i;
					// Cập nhật chỉ mục
				}
			}
		}

		time += p[loc].burst;
		// Tăng thời gian hiện tại theo thời gian của tiến trình thực hiện

		/* Tính toán thông tin thời gian tiến trình được thực hiện */
		p[loc].waiting_time = time - p[loc].arrive_time - p[loc].burst;
		p[loc].turnaround_time = time - p[loc].arrive_time;
		p[loc].return_time = p[loc].turnaround_time + p[loc].arrive_time;
		p[loc].response_time = p[loc].waiting_time;
		p[loc].completed = TRUE;

		total_waiting_time += p[loc].waiting_time;
		// Tăng tổng thời gian chờ
		total_turnaround_time += p[loc].turnaround_time;
		// Tăng tổng thời gian xử lý
		total_response_time += p[loc].response_time;
		// Tăng tổng thời gian phản hồi
	}

	quick_sort_by_return_time(p, len);
	// quick_sort_by_return_time Sắp xếp thời gian trả về theo lệnh gọi hàm

	printf("\tHighest Response Ratio Next Scheduling Algorithm\n\n");

	hrn_print_gantt_chart(p, len);
	// hrn_print_gantt_chart In biểu đồ Gantt với lệnh gọi hàm

	/* Thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// In bảng dữ liệu bằng cách gọi hàm print_table
}

#endif
