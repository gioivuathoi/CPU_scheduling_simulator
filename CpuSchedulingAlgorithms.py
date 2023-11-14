from CpuSchedulingAlgorithmsModule import FCFS, PPS, RR, SJF
from CpuSchedulingAlgorithmsModule.Process import Process

def main():
    #  Khai báo và khởi tạo các biến sử dụng trong vòng lặp
    quantum = 2
    #  Khai báo biến để lưu trữ phân bổ thời gian
    processes = []
    process_num = 0
    # Khai báo một biến con trỏ để cấp phát động mảng cấu trúc tiến trình
    with open("F:/Subjects/os/cpu-scheduling-simulator/process.txt", "r") as f:
        lines = f.readlines()
        process_num = int(lines[0][:-1])
        print("Quantum: ", lines[-1])
        quantum = int(lines[-1])
        lines = lines[1:-1]
        for line in lines:
            info = line[:-1].split(" ")
            process_id = info[0]
            arrive_time = int(info[1])
            burst_time = int(info[2])
            priority = int(info[3])
            print(info)
            process = Process(process_id,arrive_time,burst_time,priority)
            processes.append(process)
    process_num = len(processes)
    print("Number of process: %d " %(process_num))
    print("Done create process!")
    # Thực thi thuật toán First Come First Served bằng cách gọi hàm FCFS  */
    print("┏                                                                                                                             ┓\n\n")
    FCFS.FCFS(processes, process_num)
    print("┗                                                                                                                             ┛\n\n")
    # Thực thi thuật toán Shortest Job First bằng cách gọi hàm SJF */
    print("┏                                                                                                                             ┓\n\n")
    SJF.SJF(processes, process_num)
    print("┗                                                                                                                             ┛\n\n")
    # Chạy thuật toán Round Robin bằng cách gọi hàm RR */
    print("┏                                                                                                                             ┓\n\n")
    RR.RR(processes, process_num, quantum)
    print("┗                                                                                                                             ┛\n\n")
    # Thực thi thuật toán Preemptive Priority Scheduling bằng cách gọi hàm PPS */
    print("┏                                                                                                                             ┓\n\n")
    PPS.PPS(processes, process_num)
    print("┗                                                                                                                             ┛\n\n")
    return 0

main()