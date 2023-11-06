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

typedef int Quantum; // 시간 할당량 Quantum 키워드 사용

/**
 * [process_init 프로세스 초기화 함수]
 * @param p   [프로세스 구조체 배열]
 * @param len [프로세스 갯수]
 */

/* Hàm khởi tạo các process */
void process_init(Process p[], int len)
{
    int i;

    /* Sẽ khởi tạo */
    for (i = 0; i < len; i++)
    {
        p[i].waiting_time = 0;   // 대기 시간 초기화
        p[i].return_time = 0;    // 반환 시간 초기화
        p[i].response_time = 0;  // 응답 시간 초기화
        p[i].completed = FALSE;  // 완료 상태 초기화
    }
}

#endif
