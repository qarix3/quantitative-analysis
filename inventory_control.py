import math

class EOQ_Model:
    
    def __init__(self, demand=0, order=0, holding=0, cost=0, lead=0, planned_shortage=False, shortage_cost=0):
        self.demand = demand
        self.order = order
        self.holding = holding
        self.lead = lead
        self.cost = cost
        self.planned_shortage = planned_shortage
        self.shortage_cost = shortage_cost
        
    def optimal_order_quantity(self, d=None, K=None, h=None, p=None):
        '''Calculates the order quantity
        :param K: order setup cost
        :param d: total demand
        :param h: holding cost

        :returns: reorder quantity
        :rtype: float
        '''
        if d is None:
            d = self.demand
        if K is None:
            K = self.order
        if h is None:
            h = self.holding
        if p is None:
            p = self.shortage_cost
        
        if self.planned_shortage:
            return math.sqrt((2*d*K)/h) * math.sqrt(self.shortage_cost/(self.shortage_cost + self.holding))
        else:
            return math.sqrt((2*d*K)/h)

    def reorder_point(self, d=None, L=None):
        '''Calculates the reorder point with no planned shortages.

        :param d: total demand
        :param L: lead time

        :returns: reorder point
        :rtype: float
        '''
        if d is None:
            d = self.demand
        if L is None:
            L = self.lead
        return d * L
    
    def optimal_cycle_time(self, d=None, K=None, h=None, p=None):
        '''Calculates the optimal cycle time.

        :param K: order setup cost
        :param d: total demand
        :param h: holding cost
        
        :returns: reorder point
        :rtype: float
        '''
        if d is None:
            d = self.demand
        if K is None:
            K = self.order
        if h is None:
            h = self.holding
        if p is None:
            p = self.shortage_cost
        
        if self.planned_shortage:
            return math.sqrt((2*K)/(h*d)) * math.sqrt((self.shortage_cost + self.holding)/self.shortage_cost)
        else:
            return math.sqrt((2*K)/(h*d))
    
    def complete_calculations(self):
        '''Calculates and prints the main 2 metrics: order quantity, optimal cycle time
        
        :returns: tuple of metrics
        :rtype: tuple of length 2
        '''
        
        Q = self.optimal_order_quantity()
        t = self.optimal_cycle_time()
        Q = round(Q)
        t = round(t, 3)
        print("Optimal Order Quantity (Q*): {} units".format(Q))
        print("Optimal Cycle Time (t*): {}".format(t))