import enum


class PAState(enum.Enum):
    IDLE = 0,
    RECIV_PACKET = 1,
    LAST_IN_PACKET = 2


class PacketArbiterModel:
    """docstring for ClassName"""
    def __init__(self):
        # self._arbiter = SimpleArbiterModel()
        self._prev_state = PAState.IDLE
        self._curr_state = PAState.IDLE
        self.grants = 0
        self.ptr = 0

    def cycle_shift_right(self, req):
        return (req >> self.ptr) | (req << (8 - self.ptr))

    def cycle_shift_left(self, gr):
        return (gr << self.ptr) | (gr >> (8 - self.ptr))

    def update_defer_ptr(self):
        return (
            self._prev_state != PAState.RECIV_PACKET
        ) and (
            self._curr_state == PAState.RECIV_PACKET
        )

    def force_update_ptr(self):
        return (
            self._prev_state != PAState.RECIV_PACKET
        ) and (
            self._curr_state == PAState.LAST_IN_PACKET
        )

    def do_arbiter(self, req, req_is_last):
        sreq = self.cycle_shift_right(req)
        sgrants = 0
        for i in range(8):
            if (sreq >> i) & 0b1:
                sgrants = (1 << i)
                break
        grants = self.cycle_shift_left(sgrants)

        grant_is_last = req_is_last & grants
        preq = sreq ^ sgrants

        ptr = 0
        for i in range(8):
            if (preq >> i) & 0b1:
                ptr = i
                break

        if grant_is_last:
            self._curr_state = PAState.LAST_IN_PACKET;
        elif req == 0:
            self._curr_state = PAState.IDLE;
        else:
            self._curr_state = PAState.RECIV_PACKET;


        if self.update_defer_ptr():
            self.defer_ptr = ptr 

        if grant_is_last:
            self.ptr += ptr if (
                self.force_update_ptr()
                ) else self.defer_ptr

        self._prev_state = self._curr_state

        # print(f"{self.ptr=}")
        # print(f"{self._prev_state=}")
        # print(f"{self._curr_state=}")

        return grants


if __name__ == '__main__':
    a = PacketArbiterModel()
    req = 0b11111111
    req_is_last = 0b11111111
    for _ in range(8):
        print(bin(a.do_arbiter(req, req_is_last)))