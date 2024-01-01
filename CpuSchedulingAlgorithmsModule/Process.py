from typing import Any
from CpuSchedulingAlgorithmsModule.SortingFunction import mergeSort
class Process():
    def __init__(self, id:str, request_time:float, burst:float, priority:int) -> None:
        self.id = id                     # ID của process sẽ là một sequence với chiều dài ID_LEN
        self.request_time = request_time # Thời gian tiến trình yêu cầu được vào Queue
        self.arrive_time = None          # Thời gian tiến trình đến Queue
        self.waiting_time = 0            # Khoảng thời gian tiến trình wait trong queue
        self.accept_time = None          # Thời gian tiến trình bắt đầu được vào CPU
        self.return_time = None          # Thời gian mà tiến trình được trả về bởi CPU
        self.turnaround_time = 0         # Khoảng thời gian từ arrive time đến return time
        self.response_time = None        # Khoảng thời gian từ arrive time đến lúc tiến trình bắt đầu vào CPU
        self.burst = burst               # Burst CPU time của tiến trình
        self.remain_burst = burst        # Burst CPU time còn lại của process, chỉ dùng trong RR và PPS
        self.priority = priority         # Độ ưu tiên của tiến trình, sử dụng trong các thuật toán UPDATE
        self.completed = False           # Trạng thái của tiến trình
        self.execution_time = 0          # Tổng thời gian mà process đã được chạy trong CPU
        self.quantum = 0                 # Thời gian quantum, sử dụng cho RR
        self.remain_quantum = 0          # Thời gian chạy quantum của process, chỉ dùng cho RR
        self.on_cpu = False              # Xác định trạng thái đang được cpu xử lý hay đang ở ngoài
        self.continue_run = 0            # Sử dụng cho thuật toán PPS, đánh dấu thời gian execution từ lần chạy trước
        self.continue_waiting = 0
        self.force_back_to_queue = 0
        self.start_priority = priority

    def update_arrive_time(self, new_arrive_time):
        self.arrive_time = new_arrive_time
    def update_waiting_time(self, current_time, for_RR = False, continue_wait = False):
        if for_RR:
            self.waiting_time += (current_time - self.arrive_time)
        elif continue_wait:
            self.waiting_time = self.continue_waiting
            self.waiting_time += (current_time - self.force_back_to_queue)
        else:
            self.waiting_time = current_time - self.arrive_time
        
    def update_return_time(self, current_time):
        self.return_time = current_time
    def update_turnaround_time(self):
        self.turnaround_time += (self.return_time - self.arrive_time)
    def update_response_time(self, current_time):
        self.response_time = current_time - self.request_time
    def update_completed_state(self):
        self.completed = True
    def update_execution_time(self, exe_time, add = False):
        if not add:
            self.execution_time = exe_time
        else:
            self.execution_time += exe_time
    def update_priority(self, add):
        self.priority  = self.start_priority - add
    def update_on_cpu(self, value = True):
        self.on_cpu = value
    def update_request_time(self, current_time):
        self.request_time = current_time
    def update_accept_time(self, current_time):
        self.accept_time = current_time
    def update_remain_quantum(self, reset = True, decrease = None):
        if reset:
            self.remain_quantum = self.quantum
        elif decrease != None:
            if decrease >= self.remain_quantum:
                self.remain_quantum = 0
    def update_remain_burst(self, decreasing):
        self.remain_burst -= decreasing
    def update_run_condition(self, run_for = 0):
        self.continue_run = run_for
    def update_wait_condition(self, wait_for = 0, current_time = 0):
        self.continue_waiting = wait_for
        self.force_back_to_queue = current_time
class ReadyQueue():
    def __init__(self, P: list) -> None:
        self.P = P
        # print(len(self.P))
    def length(self):
        return len(self.P)
    def insert_process(self, p:Process):
        # This function adds new process into the queue, but not update the queue using scheduler yet
        self.P.append(p)
    def pop_process(self):
        # This function pops the last process in the queue, which goes into CPU or completed
        return self.P.pop()

    def reset_process(self, current_time):
        # This function reset arrive time of the process which has just been completed and want to re-run
        self.P[-1].update_arrive_time(current_time)

    def __FCFS(self):
        # We sort processes by their's arrival time
        mergeSort(self.P,0,len(self.P) - 1, "arrive")
        # print(len(self.P))

    def __SJF(self, current_time):
        # First, we need sort processes by their arrive time, but not the process with shortest-burt process at current time
        if len(self.P) > 0:
            if self.P[-1].on_cpu:
                temp = self.P[:-1]
                mergeSort(temp,0,len(temp) - 1,"arrive")
                self.P[:-1] = temp
            else:
                mergeSort(self.P,0,len(self.P) - 1, "arrive")
            # Next, we need to get all the process that has arrived
            index = 0
            for i, process in enumerate(self.P):
                if process.arrive_time < current_time:
                    index =  i
                    break
            # Because this is non-preemptive, so we do not sort the on_cpu process
            if len(self.P) > 1:
                if self.P[-1].on_cpu:
                    temp = self.P[index:-1]
                    # Next, we sort the ready processes by their burst time
                    mergeSort(temp,0,len(temp) - 1,"burst")
                    self.P[index:-1] = temp
                else:
                    temp = self.P[index:]
                    # Next, we sort the ready processes by their burst time
                    mergeSort(temp,0,len(temp) - 1,"burst")
                    self.P[index:] = temp
        # else:

    def __RR(self, quantum = 5):
        if len(self.P) > 0:
            mergeSort(self.P,0,len(self.P) - 1, "arrive")
            if not self.P[-1].on_cpu: 
                if self.P[-1].remain_burst > quantum:
                    self.P[-1].quantum = quantum
                else:
                    self.P[-1].quantum = self.P[-1].remain_burst

    def __PPS(self, quantum, current_time):
        # First, we need to sort the queue based on arrival time of each process
        mergeSort(self.P,0,len(self.P) - 1, "arrive")
        # Next, we need to get all the process that has arrived
        index = 0
        for i, process in enumerate(self.P):
            if process.arrive_time < current_time:
                index =  i
                break
        # index -= 1
# Because this is preemptive, so we need to make sure the on_cpu process will get back ready queue properly
        if len(self.P) > 1:
            temp = self.P[index:]
            # Next, we sort the ready processes by their priority
            mergeSort(temp,0,len(temp) - 1,"priority")
            self.P[index:] = temp
        # print(self.P[-1].id)

        # # Next, we check if exist highest process with same priority
        num_same = 0
        for i in range(1,len(self.P)):
            k = i * -1
            if self.P[k].priority == self.P[k-1].priority:
                num_same += 1
            else:
                break
        # Use FCFS for process with same priority
        if num_same != 0:
            temp = self.P[-1*num_same-1:]
            mergeSort(temp,0,len(temp) - 1,"arrive")
            self.P[-1*num_same-1:] = temp

    def update_queue(self, algorithm = "FCFS", current_time = 0, quantum = 5):
        if algorithm == "FCFS":
            self.__FCFS()
        elif algorithm == "SJF":
            self.__SJF(current_time)
        elif algorithm == "RR":
            self.__RR(quantum)
        elif algorithm == "PPS":
            self.__PPS(quantum, current_time)
    def get_ready_queue(self):
        return self.P





