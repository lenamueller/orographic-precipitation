def get_max_pr_sum(event:list[float], maxval_dict: dict):
    for ws in maxval_dict.keys():
        # list must be at least as long as the window size
        if ws <= len(event): 
            maxval: float = 0.0
            number_moves = len(event) - ws+1
            for i in range(number_moves):
                window = event[i:i+ws]
                val = sum(window)
                if val > maxval:
                    maxval = val
            maxval_dict[ws].append(round(maxval,3))
    return maxval_dict

def rolling_window_multiple_events(events:list[list[float]])->dict:
    # keys are number of time steps which are the duration if multiplied by 10 min
    max_pr_sum: dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
    for e in events:
        get_max_pr_sum(e,max_pr_sum)    
    return max_pr_sum