#ifndef __PRINT__TABLE__
#define __PRINT__TABLE__

// Print Table

/* Khai báo tiêu đề tùy chỉnh */
#include "./Process.h"

/**
 * [print_table Chức năng hiển thị bảng dữ liệu tiến trình]
 * @param p [mảng cấu trúc tiến trình]
 * @param n [số lượng tiến trình]
 */
void print_table(Process p[], int n)
{
	int i;
	// Khai báo các biến sử dụng trong vòng lặp

	puts("\t+-----+------------+-------------+----------+-------------+-----------------+--------------+-----------------+");
	puts("\t| PID | Burst Time | Arrive Time | Priority | Return Time |  Response Time  | Waiting Time | Turnaround Time |");
	puts("\t+-----+------------+-------------+----------+-------------+-----------------+--------------+-----------------+");

	/* Thực hiện lặp lại theo số lượng tiến trình và định dạng thông tin để in ra */
	for (i = 0; i < n; i++)
	{
		printf("\t| %3s |     %3d    |     %3d     |    %3d   |     %3d     |      %3d        |      %3d     |        %3d      |\n",
			p[i].id, p[i].burst, p[i].arrive_time, p[i].priority, p[i].return_time, p[i].response_time, p[i].waiting_time, p[i].turnaround_time);

		puts("\t+-----+------------+-------------+----------+-------------+-----------------+--------------+-----------------+");
	}

	puts("\n");
}

#endif
