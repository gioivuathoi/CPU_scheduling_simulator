

/* Khai báo tệp tiêu đề tùy chỉnh */
#include "CpuSchedulingAlgorithms.h"

int main()
{
    int process_count = 0;
    // Khai báo và khởi tạo một biến để lưu trữ số lượng tiến trình
    int i = 0;
    //  Khai báo và khởi tạo các biến sử dụng trong vòng lặp

    Quantum quantum;
    //  Khai báo biến để lưu trữ phân bổ thời gian
    Process *process;
    // Khai báo một biến con trỏ để cấp phát động mảng cấu trúc tiến trình

    /* Mở khai báo fp con trỏ tệp và process.txt ở chế độ đọc.  */
    FILE *fp = fopen("process.txt", "r");

    /* Nếu mở file không thành công */
    if (fp == NULL)
    {
        printf("FILE OPEN ERROR!\n");
        return 0; // Chấm dứt hàm chính sau khi xuất ngoại lệ
    }

    fscanf(fp, " %d", &process_count);
    // Đọc dữ liệu số nguyên từ file và lưu nó vào process_count

    /*  Cấp phát động mảng cấu trúc quy trình lên tới số process_count */
    process = (Process *)malloc(sizeof(Process) * process_count);

    /* Lặp lại số lần bằng số tiến trình */
    while (i < process_count)
    {
        fscanf(fp, "%s %d %d %d",
                process[i].id, &process[i].arrive_time, &process[i].burst, &process[i].priority);
        // Đọc dữ liệu tiến trình từ file và lưu vào mảng
        i++;
        //  di chuyển tới mảng tiếp theo
    }

    fscanf(fp, " %d", &quantum);
    // Đọc dữ liệu số nguyên từ tệp và lưu trữ dưới dạng lượng tử

    /* Thực thi thuật toán First Come First Served bằng cách gọi hàm FCFS  */
    puts("┏                                                                                                                             ┓\n\n");
    FCFS(process, process_count);
    puts("┗                                                                                                                             ┛\n\n");

    /* Thực thi thuật toán Shortest Job First bằng cách gọi hàm SJF */
    puts("┏                                                                                                                             ┓\n\n");
    SJF(process, process_count);
    puts("┗                                                                                                                             ┛\n\n");

    /* Chạy thuật toán Round Robin bằng cách gọi hàm RR */
    puts("┏                                                                                                                             ┓\n\n");
    RR(process, process_count, quantum);
    puts("┗                                                                                                                             ┛\n\n");

    /* Thực thi thuật toán Highest Response Ratio Next bằng cách gọi hàm HRN */
    puts("┏                                                                                                                             ┓\n\n");
    HRN(process, process_count);
    puts("┗                                                                                                                             ┛\n\n");

    /* Thực thi thuật toán Non-Preemptive Priority Scheduling  bằng cách gọi hàm NPPS */
    puts("┏                                                                                                                             ┓\n\n");
    NPPS(process, process_count);
    puts("┗                                                                                                                             ┛\n\n");

    /* Thực thi thuật toán Preemptive Priority Scheduling bằng cách gọi hàm PPS */
    puts("┏                                                                                                                             ┓\n\n");
    PPS(process, process_count);
    puts("┗                                                                                                                             ┛\n\n");

    /* Thực thi thuật toán Shortes Remaining Time bằng cách gọi hàm SRT */
    puts("┏                                                                                                                             ┓\n\n");
    SRT(process, process_count);
    puts("┗                                                                                                                             ┛\n\n");

    fclose(fp);
    // Đóng con trỏ file đang mở fp.

    free(process);
    // Giải phóng mảng cấu trúc tiến trình đã cấp phát bộ nhớ

    system("pause");
    // Ngăn không cho cửa sổ console tắt
    return 0;
    // kết thúc hàm chính
}
