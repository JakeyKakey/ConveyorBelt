from random import choices

class Worker:
    
    def __init__(self):

        self.compA = False
        self.compB = False
        self.compAB = False
        self.workCountdown = 0

    def engageCountdown(self):
        self.workCountdown = 4

    def countdownSkip(self):
        if(self.workCountdown > 0):
            self.workCountdown -= 1
            return False
        return True

    def action(self, component):

        def checkForBoth():
            if (self.compA and self.compB):
                self.compA = False 
                self.compB = False 
                self.compAB = True
                self.engageCountdown()

        if (self.compAB):
            ready = self.countdownSkip()
            if (ready and component is None):
                self.compAB = False 
                return AB()
            else:
                return component

        if isinstance(component, A) and self.compA is False:
            self.compA = True
            checkForBoth()
            return None

        if isinstance(component, B) and self.compB is False:
            self.compB = True
            checkForBoth()
            return None
        return component 



    def display(self):
        if self.compA: return "A"
        if self.compB: return "B"
        if self.compAB: return "*"
        return "V"

class Component():
    pass

class A(Component):
    pass

class B(Component):
    pass

class AB(Component):
    pass

class ConveyorSlot:
    def __init__(self):
        self.top_worker = Worker()
        self.bottom_worker = Worker()
        self.current_stack = None 
        self.next_slot = None

    def setNext(self,conveyor):
        self.next_slot = conveyor

    def executeWorkerActions(self):

        def executeWorker(w):
            temp = self.current_stack
            self.current_stack = w.action(self.current_stack)

            if (self.current_stack == temp):
                return False
            else:
                return True

        did_work = executeWorker(self.top_worker)
        if not did_work:
            executeWorker(self.bottom_worker)
        else:
            self.bottom_worker.countdownSkip

#       if not did_work:
#           executeWorker(self.bottom_worker)
#        else:
#            self.bottom_worker.countdownSkip
    


    def insert(self, component):
    
        self.executeWorkerActions()
        self.pushAlong()
        self.current_stack = component

    def pushAlong(self):
        if self.next_slot is not None:
            self.next_slot.insert(self.current_stack)

    def display(self):
        if isinstance(self.current_stack, A): return "A"
        if isinstance(self.current_stack, B): return "B"
        if isinstance(self.current_stack, AB): return "*"
        if self.current_stack is None: return " "
        

class Belt:
    
    def __init__(self, iterations, workerPairs, AChance, BChance, NilChance):
        self.iterations = iterations
        self.workerPairs = workerPairs
        self.probsWeights = [AChance, BChance, NilChance]
        self.compOptions = [1,2,3]
        self.firstConveyor = None

    def getNextItem(self):

        choice = choices(self.compOptions, self.probsWeights)
        i = choice[0]
        if i == 1: 
            return A()
        if i == 2: 
            return B()
        if i == 3: return None
            

    def initialize(self):

        def iterate(cv, count):
                while count > 0:
                    temp = ConveyorSlot()
                    cv.setNext(temp)
                    count -= 1
                    count = iterate(temp, count)
                    return count

        headConveyor = ConveyorSlot()
        self.firstConveyor = headConveyor
        self.workerPairs -= 1

        iterate(headConveyor, self.workerPairs)

        
    def start(self):
            
            while self.iterations > 0:
                self.display()
                nextItem = self.getNextItem()
                self.firstConveyor.insert(nextItem)
                self.iterations -= 1

        


    def display(self):
        
        def iterate(slot, top, mid, bottom):
           
            if (slot is not None):
                top += slot.top_worker.display()
                top += "   "
                mid += " "
                mid += slot.display()
                mid += " |"
                bottom += slot.bottom_worker.display()
                bottom += "   "
                return iterate(slot.next_slot, top, mid, bottom)
            else: 
                return top, mid, bottom

        top_line = ""
        mid_line = ""
        bottom_line = ""

        top_line, mid_line, bottom_line = iterate(self.firstConveyor, top_line, mid_line, bottom_line)

        print(self.iterations)
        print("", top_line)
        print("-" * len(top_line))
        print(mid_line)
        print("-" * len(top_line))
        print("", bottom_line)


b = Belt(100, 3, (1/3), (1/3), (1/3))
b.initialize()
b.start()
print("finished")