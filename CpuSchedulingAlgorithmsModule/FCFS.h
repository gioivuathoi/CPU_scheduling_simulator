#ifndef __FIRST__COME__FIRST__SERVED__
#define __FIRST__COME__FIRST__SERVED__

// FCFS Algorithm

/* khai báo tiêu đề tuỳ chỉnh */
#include "./Process.h"
#include "./SortingFunction.h"
#include "./PrintTable.h"

/**
 * [fcfs_print_gantt_chart chức năng xuất biểu đồ gantt]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void fcfs_print_gantt_chart(Process *p, int len)
{
	int i, j;
	// khai báo biến sử dụng trong vòng lặp

	printf("\t ");

	/* hiển thị thanh đầu trang */
	for (i = 0; i < len; i++)
	{
		for (j = 0; j < p[i].burst; j++)
			printf("--");

		printf(" ");
	}

	printf("\n\t|");

	/* hiển thị tên tiến trình */
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
 * [FCFS FCFS hàm thực thi thuật toán]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */
void FCFS(Process *p, int len)
{
	int i;
	// khai báo các biến sử dụng trong vòng lặp
	int total_waiting_time = 0;
	// khai báo và khởi tạo một biến để lưu tổng thời gian chờ
	int total_turnaround_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ thời gian hoàn thành toàn bộ quy trình
	int total_response_time = 0;
	// Khai báo và khởi tạo biến để lưu trữ tổng thời gian phản hồi
	int total_return_time = 0;
	// khai báo và khởi tạo biến để lưu trữ tổng thời gian trả về

	process_init(p, len);
	// process_init khởi tạo một tiến trình bằng lệnh gọi hàm

	merge_sort_by_arrive_time(p, 0, len);
	// merge_sort_by_arrive_time sắp xếp theo thời gian đến với lệnh gọi hàm

	/* thực thi tiến trình đầu tiên xuất hiện */
	p[0].return_time = p[0].burst;
	p[0].turnaround_time = p[0].return_time - p[0].arrive_time;
	p[0].response_time = 0;
	p[0].waiting_time = 0;

	/* tăng tổng lên bằng số tiến trình đã thực thi */
	total_response_time += p[0].response_time;
	total_waiting_time += p[0].waiting_time;
	total_turnaround_time += p[0].turnaround_time;
	total_return_time += p[0].burst;

	/* tính toán tuần tự từ tiến trình tiếp theo */
	for (i = 1; i < len; i++)
	{
		/* tính toán mỗi thành viên trong tiến trình */
		p[i].waiting_time = total_return_time - p[i].arrive_time;
		p[i].return_time = total_return_time + p[i].burst;
		p[i].turnaround_time = p[i].return_time - p[i].arrive_time;
		p[i].response_time = p[i].waiting_time;

		/* tăng lên tuỳ theo số tiến trình đã thực thi */
		total_return_time += p[i].burst;
		total_waiting_time += p[i].waiting_time;
		total_turnaround_time += p[i].turnaround_time;
		total_response_time += p[i].response_time;
	}

	printf("\n\tFCFS Scheduling Algorithm\n\n");

	fcfs_print_gantt_chart(p, len);
	// fcfs_print_gantt_chart in biểu đồ gantt với lệnh gọi hàm

	/* 평균 대기시간, 턴어라운드 타임, 응답 시간 출력 */
	printf("\n\tAverage Waiting Time     : %-2.2lf\n", (double)total_waiting_time / (double)len);
	printf("\tAverage Turnaround Time  : %-2.2lf\n", (double)total_turnaround_time / (double)len);
	printf("\tAverage Response Time    : %-2.2lf\n\n", (double)total_response_time / (double)len);

	print_table(p, len);
	// print_table bảng dữ liệu đầu ra với lệnh gọi hàm
}

#endif
