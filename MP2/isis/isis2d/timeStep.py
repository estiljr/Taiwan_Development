def next_ts_solver(solver, currentTs):
    
    if 'tvd' in solver:
        if currentTs > 1.0:
            return 'tvd', 1.0
        elif currentTs > 0.75:
            return 'tvd', 0.75
        elif currentTs > 0.5:
            return 'tvd', 0.5
        elif currentTs > 0.25:
            return 'tvd', 0.25
        elif currentTs > 0.2:
            return 'tvd', 0.2
        elif currentTs > 0.125:
            return 'tvd', 0.125
        elif currentTs > 0.1:
            return 'tvd', 0.1
        else:
            ''' This is used to flag that the model shouldn't be run with a shortened TS '''
            return 'tvd', 0.0  
    elif 'adi' in solver: 
        if currentTs > 5.0:
            return 'adi', 5.0
        elif currentTs > 2.0:
            return 'adi',2.0
        elif currentTs > 1.0:
            return 'adi',1.0
        elif currentTs >  0.5:
            return 'adi', 0.5
        elif currentTs >  0.25:
            return 'adi', 0.25
        else:
            return 'tvd' , 1  

if __name__ == '__main__':
    pass