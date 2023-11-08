#ifndef __PROCESS__
#define __PROCESS__

// Process

/* Khai báo file header sẽ sử dụng trong chương trình */
#include <stdio.h>
#include <stdlib.h>

/* Ta định nghĩa một số constant sẽ được sử dụng trong chương trình */
#define ID_LEN 20   // Chiều dài ID của một process
#define TRUE 1
#define FALSE 0

/* Xây dựng một process */
typedef struct _process
{
    char id[ID_LEN];       // ID của process sẽ là một sequence với chiều dài ID_LEN
    int arrive_time;       // Thời gian tiến trình đến Queue
    int waiting_time;      // Thời gian tiến trình wait trong queue
    int return_time;       // Return time của tiến trình
    int turnaround_time;   // Turn around time của tiến trình, sử dụng cho các thuật toán UPDATE
    int response_time;     // Response time của tiến trình
    int burst;             // Burst CPU time của tiến trình
    int priority;          // Độ ưu tiên của tiến trình, sử dụng trong các thuật toán UPDATE
    int completed;         // Trạng thái của tiến trình
} Process;

typedef int Quantum; // Sử dụng từ khóa 'Quantum' cho thời gian cung cấp

/**
 * [process_init hàm khởi tạo tiến trình]
 * @param p   [mảng cấu trúc tiến trình]
 * @param len [số lượng tiến trình]
 */

/* Hàm khởi tạo các process */
void process_init(Process p[], int len)
{
    int i;

    /* Sẽ khởi tạo */
    for (i = 0; i < len; i++)
    {
        p[i].waiting_time = 0;   // Khởi tạo thời gian chờ
        p[i].return_time = 0;    // Khởi tạo thời gian trả về
        p[i].response_time = 0;  // Khởi tạo thời gian phản hồi
        p[i].completed = FALSE;  // Khởi tạo trạng thái hoàn thành
    }
}

#endif
