class Process():
    def __init__(self, id:str, arrive_time:float, burst:float, priority:int) -> None:
        self.id = id    # ID của process sẽ là một sequence với chiều dài ID_LEN
        self.arrive_time = arrive_time   #Thời gian tiến trình đến Queue
        self.waiting_time = 0    # Thời gian tiến trình wait trong queue
        self.return_time = 0      # Return time của tiến trình
        self.turnaround_time = 0  #Turn around time của tiến trình, sử dụng cho các thuật toán UPDATE
        self.response_time = 0   #Response time của tiến trình
        self.burst = burst       #Burst CPU time của tiến trình
        self.priority = priority      #Độ ưu tiên của tiến trình, sử dụng trong các thuật toán UPDATE
        self.completed = False        #Trạng thái của tiến trình



