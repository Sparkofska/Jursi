from threading import Timer

class BgJob():
    '''
    Background Job. Starting threads periodically with given period.
    '''

    def __init__(self, period, function):
        '''
        period: seconds to wait until next iteration
        function: action to call on each iteration
        '''
        self._period = period
        self._function = function
        self._is_stopped = False


    def start(self):
        if self._is_stopped:
            return

        timer = Timer(self._period, self.start)
        timer.start() # start new thread for next iteration

        self._function()

    def stop(self):
        self._is_stopped = True
