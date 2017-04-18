# buyLotsOfFruit.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
To run this script, type

  python buyLotsOfFruit.py

Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order
    """
    totalCost = 0.0
    for fruitName, fruitPrice in fruitPrices.items(): 	# Each Fruit along with its Price is selected from the fruitPrices dictionary.
		count = 0										# Count is used to find the number of fruits in the fruitPrice list
		count = len(fruitPrices)
		i = 0											# i stands for the iterator. It keeps incrementing everytime a match is not found and drops back to zero if a match is found.
		for fruit, numPounds in orderList:				# Each Fruit along with its weight is selected from the orderList list.
			if(fruitName == fruit):						# Each Fruit in the fruitPrice dictionary is compared with every element in the orderList till a match is found. 
				totalCost += fruitPrice*numPounds		# TotalCost is updated if match is found. Else, we increment i
				break
			else:
				i = i+1
		if(i == count):									# If no match has been found, then i is equal to the count value. Hence None is returned.
			return None
    return totalCost

# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0) ]
    print 'Cost of', orderList, 'is', buyLotsOfFruit(orderList)
