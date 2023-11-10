#ifndef __NON__PREEMPTIVE__PRIORITY__SCHEDULING__
#define __NON__PREEMPTIVE__PRIORITY__SCHEDULING__

// Non-preemptive Priority Scheduling Algorithm

/* khai báo tiêu đề tuỳ chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [npps_calculate NPPS Hàm tính thời gian thuật toán]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void npps_calculate(Process *p, int len)
{
	int i, j;
	// Khai báo các biến sử dụng trong vòng lặp
	int check;
	// Khai báo một biến để kiểm tra xem tất cả các tiến trình đã hoàn thành chưa
	int min;
	// Khai báo một biến để lưu trữ chỉ số ưu tiên cao nhất
	int time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ thời gian hiện tại

	/* Thực hiện quá trình sớm nhất và tính toán thời gian của nó */
	p[0].return_time = p[0].burst;
	p[0].turnaround_time = p[0].return_time - p[0].arrive_time;
	p[0].response_time = 0;
	p[0].completed = TRUE;

	time = p[0].burst;
	// Tăng thời gian hiện tại theo thời gian tiến trình đã thực hiện

	/* Lặp lại cho đến khi tất cả các quá trình hoàn tất */
	while (TRUE)
	{
		min = INT_MAX;
		// Khởi tạo một biến để lưu trữ giá trị nhỏ nhất
		check = FALSE;
		// Xác nhận hoàn thành tất cả các quy trình Khởi tạo các biến

		/* Lặp lại nhiều lần bằng số lượng tiến trình -1 */
		for (i = 1; i < len; i++)
		{
			/* Có mức độ ưu tiên thấp hơn mức ưu tiên hiện tại
			Nếu tiến trình chưa chạy và đã đến */
			if ((p[min].priority > p[i].priority)
				&& (p[i].completed == FALSE)
					&& (p[i].arrive_time <= time))
			{
				min = i;
				// Cập nhật chỉ mục tiến trình ưu tiên tối thiểu
				check = TRUE;
				// Chỉ ra rằng có những tiến trình còn lại để chạy
			}
		}

		/* Khi tất cả các quá trình được hoàn thành */
		if (check == FALSE)
			break;
			// thoát vòng lặp

		/* Tính toán thời gian tiến trình đã chọn */
		p[min].response_time = time - p[min].arrive_time;
		p[min].return_time = time + p[min].burst;
		p[min].turnaround_time = p[min].return_time - p[min].arrive_time;
		p[min].waiting_time = time - p[min].arrive_time;
		p[min].completed = TRUE;

		time += p[min].burst;
		// Tăng thời gian hiện tại theo thời gian tiến trình đã thực hiện
	}
}

/**
 * [npps_print_gantt_chart hiển thị biểu đồ Gantt]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void npps_print_gantt_chart(Process *p, int len)
{
	int i, j;
	// Khai báo các biến sử dụng trong vòng lặp

	printf("\t ");

	/* hiển thị đầu ra thanh trên cùng */
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

	/* 하단 바 출력 */
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
 * [NPPS NPPS hàm thực thi thuật toán]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void NPPS(Process *p, int len)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp
	int total_waiting_time = 0;
	// Khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	int total_turnaround_time = 0;
	//  Khai báo và khởi tạo biến để lưu trữ thời gian hoàn thành toàn bộ tiến trình
	int total_response_time = 0;
	// Khai báo và khởi tạo một biến để lưu trữ tổng thời gian phản hồi

	process_init(p, len);
	//  Khởi tạo một tiến trình bằng lệnh gọi hàm process_init

	merge_sort_by_arrive_time(p, 0, len);
	//  Sắp xếp theo thời gian đến với lệnh gọi hàm merge_sort_by_arrive_time
	npps_calculate(p, len);
	//  Tính thời gian bằng lệnh gọi hàm npps_calculate

	/* Lặp lại nhiều lần bằng số lượng tiến trình */
	for (i = 0; i < len; i++)
	{
		total_waiting_time += p[i].waiting_time;
		// Tăng tổng thời gian chờ 
		total_turnaround_time += p[i].turnaround_time;
		// Tăng tổng thời gian xử lý
		total_response_time += p[i].response_time;
		// Tăng tổng thời gian phản hồi
	}

	quick_sort_by_return_time(p, len);
	// Sắp xếp theo thời gian trả về theo lệnh gọi hàm quick_sort_by_return_time 
	printf("\tNon-preemptive Priority Scheduling Algorithm\n\n");

	npps_print_gantt_chart(p, len);
	// In biểu đồ Gantt bằng cách gọi hàm npps_print_gantt_chart

	/* Thời gian chờ trung bình, thời gian hoàn thành, thời gian đáp ứng đầu ra */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// In bảng dữ liệu bằng cách gọi hàm print_table
}

#endif
