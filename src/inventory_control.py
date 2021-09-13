import math

"""
For purposes of monitoring the effectiveness of inventory management it is helpful to look at the following ratios and indexes:
Overall Inventory Turnover Ratio = Cost of goods sold / Average total inventories at cost
Raw Material Inventory Turnover Ratio = Annual consumption of raw material / Average raw material inventory
Work-in-process Inventory Turnover Ratio = Cost of manufacture / Average work in process inventory at cost
Finished Goods Inventory Turnover ratio = Cost of goods sold / Average inventory of finished goods at cost
Average Age of Raw Materials in Inventory = Average Raw Material Inventory at cost / Average Daily Purchase of Raw Materials
Average Age of Finished Goods Inventory = Average finished goods inventory at Cost / Average cost of goods manufactured per day
Out-of-stock Index = Number of times out of stock / Number of times requisitioned
Spare Parts Index = Value of Spare Parts Inventory / Value of Capital Equipment
"""


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
        """Calculates the order quantity
        :param K: order setup cost
        :param d: total demand
        :param h: holding cost

        :returns: reorder quantity
        :rtype: float
        """
        if d is None:
            d = self.demand
        if K is None:
            K = self.order
        if h is None:
            h = self.holding
        if p is None:
            p = self.shortage_cost

        if self.planned_shortage:
            return math.sqrt((2 * d * K) / h) * math.sqrt(self.shortage_cost / (self.shortage_cost + self.holding))
        else:
            return math.sqrt((2 * d * K) / h)

    def reorder_point(self, d=None, L=None):
        """Calculates the reorder point with no planned shortages.

        :param d: total demand
        :param L: lead time

        :returns: reorder point
        :rtype: float
        """
        if d is None:
            d = self.demand
        if L is None:
            L = self.lead
        return d * L

    def optimal_cycle_time(self, d=None, K=None, h=None, p=None):
        """Calculates the optimal cycle time.

        :param K: order setup cost
        :param d: total demand
        :param h: holding cost

        :returns: reorder point
        :rtype: float
        """
        if d is None:
            d = self.demand
        if K is None:
            K = self.order
        if h is None:
            h = self.holding
        if p is None:
            p = self.shortage_cost

        if self.planned_shortage:
            return math.sqrt((2 * K) / (h * d)) * math.sqrt((self.shortage_cost + self.holding) / self.shortage_cost)
        else:
            return math.sqrt((2 * K) / (h * d))

    def complete_calculations(self):
        """Calculates and prints the main 2 metrics: order quantity, optimal cycle time

        :returns: tuple of metrics
        :rtype: tuple of length 2
        """

        Q = self.optimal_order_quantity()
        t = self.optimal_cycle_time()
        Q = round(Q)
        t = round(t, 3)
        print("Optimal Order Quantity (Q*): {} units".format(Q))
        print("Optimal Cycle Time (t*): {}".format(t))


# No Planned Shortage Example

d = 500
K = 100
c = 20
h = 2
p = 0.8

model = EOQ_Model(demand=d, order=K, cost=c, holding=h,
                  planned_shortage=False, shortage_cost=p)
model.complete_calculations()

# # Planned Shortage Example

# d=500
# K=100
# c=20
# h=2
# p=0.8

# model = EOQ_Model(demand=d, order=K, cost=c, holding=h, planned_shortage=True, shortage_cost=p)
# model.complete_calculations()

# # Sensivity Analysis
# # Increase K- Expect both Q and t to increase

# d=500
# c=20
# h=2
# p=0.8
# K = [80, 100, 150, 200]

# for k in K:
#     print("K Value: {}".format(k))
#     model = EOQ_Model(demand=d, order=k, cost=c, holding=h, planned_shortage=False, shortage_cost=p)
#     model.complete_calculations()
#     print('-----------------')

# # Increase h- Expect both Q and t to decrease

# d=500
# K=100
# c=20
# p=0.8
# H = [2,4,6,8,10]

# for h in H:
#     print("h Value: {}".format(h))
#     model = EOQ_Model(demand=d, order=K, cost=c, holding=h, planned_shortage=False, shortage_cost=p)
#     model.complete_calculations()
#     print('-----------------')

# # Increase d- Expect Q to increase and t to decrease

# D=[200,400,600,800,1000]
# K=100
# c=20
# p=0.8
# h=2


# for d in D:
#     print("d Value: {}".format(d))
#     model = EOQ_Model(demand=d, order=K, cost=c, holding=h, planned_shortage=False, shortage_cost=p)
#     model.complete_calculations()
#     print('-----------------')
