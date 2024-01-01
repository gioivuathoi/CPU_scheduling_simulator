from CpuSchedulingAlgorithmsModule.Process import ReadyQueue, Process

def run_FCFS(static:list, current_time, dynamic: Process = None):
    # "static" is a list of processes which is created by info from file process.txt and process add by user
    # this parameter is updated over time. "dynamic" is a new process which is added by user in real time
    # First we need to check if there is process in queue
    if len(static) == 0:
        return 0
    ready_queue = ReadyQueue(static)
    if dynamic != None:
        ready_queue.insert_process(dynamic)
    # Before scheduling, we need to update waiting time for each process
    for i in range(ready_queue.length()):
        ready_queue.P[i].update_waiting_time(current_time)
    # Now, we sort all process with FCFS
    ready_queue.update_queue(algorithm="FCFS")
    # After sort, the process at tail of the queue will be pop out and update it's properties
    run_process = ready_queue.pop_process()
    # We need to check to make sure the process we run is the uncompleted one
    while run_process.completed == True:
        if ready_queue.length() == 0:
            return 0
        run_process = ready_queue.pop_process()
    # Now, we update all properties of the process
    run_process.update_response_time(current_time)
    run_process.update_return_time(current_time + run_process.burst_time)
    run_process.turnaround_time()
    run_process.update_completed_state()
    run_process.update_execution_time(run_process.burst_time)
    # We return the process to be excecute and burst time which will be used for GUI
    return run_process, run_process.burst_time

def run_SJF(static:list, current_time, dynamic: Process = None):
    # "static" is a list of processes which is created by info from file process.txt and process add by user
    # this parameter is updated over time. "dynamic" is a new process which is added by user in real time
    # First we need to check if there is process in queue
    if len(static) == 0:
        return 0
    ready_queue = ReadyQueue(static)
    if dynamic != None:
        ready_queue.insert_process(dynamic)
    # Before scheduling, we need to update waiting time for each process
    for i in range(ready_queue.length()):
        ready_queue.P[i].update_waiting_time(current_time)
    # Now, we sort all process with burst time
    ready_queue.update_queue(algorithm="SJF")
    # After sort, the process at tail of the queue will be pop out and update it's properties
    run_process = ready_queue.pop_process()
    # We need to check to make sure the process we run is the uncompleted one
    while run_process.completed == True:
        if ready_queue.length() == 0:
            return 0
        run_process = ready_queue.pop_process()
    # Now, we update all properties of the process
    run_process.update_response_time(current_time)
    run_process.update_return_time(current_time + run_process.burst_time)
    run_process.turnaround_time()
    run_process.update_completed_state()
    run_process.update_execution_time(run_process.burst_time)
    # We return the process to be excecute and burst time which will be used for GUI
    return run_process, run_process.burst_time
    
def run_RR(static:list, current_time, dynamic: Process = None):

    if len(static) == 0:
        return 0
    ready_queue = ReadyQueue(static)
    if dynamic != None:
        ready_queue.insert_process(dynamic)
    # Before scheduling, we need to update waiting time for each process
    for i in range(ready_queue.length()):
        ready_queue.P[i].update_waiting_time(current_time)

    ready_queue.update_queue(algorithm="RR")
    run_process = ready_queue.pop_process()
    if run_process.remain_burst == 0:
        run_process.update_completed_state()
    else:
        run_process.update_arrive_time(current_time)
        ready_queue.insert_process(run_process)

    run_process.update_response_time(current_time)
    run_process.update_return_time(current_time + run_process.burst_time)
    run_process.turnaround_time()
    run_process.update_execution_time(run_process.quantum)
    return run_process, run_process.quantum

