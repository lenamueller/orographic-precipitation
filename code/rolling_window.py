def rolling_intensity(event:list[float], ws_list:list[int] = [1,2,3,6,12,18,36])->dict:
    max_pr_sum: dict = {ws: [] for ws in ws_list}
    for ws in ws_list:
        # list must be at least as long as the window size
        if ws <= len(event): 
            maxval: float = 0.0
            number_moves = len(event) - ws+1
            for i in range(number_moves):
                window = event[i:i+ws]
                val = sum(window)
                if val > maxval:
                    maxval = val
            # multiply with 6 to get mm/h
            max_pr_sum[ws].append(maxval*6/ws)
    return max_pr_sum