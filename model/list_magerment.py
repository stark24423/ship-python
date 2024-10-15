class List_Manager:
    def __init__(self):
        self.TL = []
        self.LL0 = []
        self.LL1 = []
        self.LL2 = []
        self.LL0_head = 0
        self.LL1_head = 1
        self.LL2_head = 2


    def TL_push(self, cell):
        cell.vis = 1
        self.TL.append(cell)

    def assign_TL_to_LL(self):
        while self.TL:
            cell = self.TL.pop()
            if self.LL0_head<= cell.AT < self.LL0_head+1:
                self.LL0.append(cell)
            elif self.LL1_head<= cell.AT < self.LL1_head+1:
                self.LL1.append(cell)
            elif self.LL2_head<= cell.AT < self.LL2_head+1:
                self.LL2.append(cell)


