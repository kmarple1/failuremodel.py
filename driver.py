"""A sample driver for failuremodel."""

# Author: Kyle Marple
# Date: 2017.06.13

import failuremodel

pf = failuremodel.PredictFail()

pf.predict("test01", 100, 0)
pf.predict("test02", 1, 1200)
pf.predict("test03", 50, 50)
pf.predict("test04", 10, 10)
pf.predict("test05", 100, 100)

# extracting queue for manual handling
"""
x = pf.get_alert_queue()
while not x.empty():
    y = x.pop_alert()
    print(y)
"""

# built-in printing
pf.print_alerts()
pf.clear_alerts()
