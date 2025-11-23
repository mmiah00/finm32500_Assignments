'''
⚙️ Step 4: Matching Engine Simulator
Objective: Simulate realistic order execution outcomes.

Requirements:

Randomly determine whether orders are filled, partially filled, or canceled.
There are no specific requirements on how many orders should be partially filled or rejected.
Return execution details for each order.
Implementation Target:

A MatchingEngine class that simulates order matching and execution outcomes.
'''

import random 

class MatchingEngine: 
    def __init__(self):
        self.orders = {} # key = order id, value = order details (filled, partially filled, canceled)

    def execute_order(self, order):
        outcome = random.choices(
            ['filled', 'partially_filled', 'canceled'],
            weights=[0.5, 0.3, 0.2],
            k=1
        )[0]

        if outcome == 'filled':
            executed_size = order.size
        elif outcome == 'partially_filled':
            executed_size = random.randint(1, order.size - 1)
        else:  # canceled
            executed_size = 0

        execution_details = {
            'order_id': order.order_id,
            'outcome': outcome,
            'executed_size': executed_size,
            'remaining_size': order.size - executed_size
        }

        self.orders[order.order_id] = execution_details

        return execution_details