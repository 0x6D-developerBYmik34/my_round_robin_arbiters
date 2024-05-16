

class SimpleArbiterModel:
    '''8bit requesters arbiter'''

    def __init__(self):
        self.pointer = 0;
        self.grants = 0;

    def _monitor_point_ovf(self):
        if self.pointer >= 8:
            self.pointer = 0

    def do_arbiter(self, req: int) -> int:
        if req == 0:
            return 0

        while True:
            self.grants = req & (1 << self.pointer)
            self.pointer += 1
            if self.grants:
                break

        self._monitor_point_ovf()
        return self.grants
        

    
