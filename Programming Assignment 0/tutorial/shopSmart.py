# shopSmart.py
# ------------
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
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
	"""
		orderList: List of (fruit, numPound) tuples
		fruitShops: List of FruitShops
	"""
	
	lis = list()										#This creates an empty list where every shop along with the totalCost will be added as a tuple
	for shopp in fruitShops:							#Loop for going through each shop in the list of shops
		t = (shopp, shopp.getPriceOfOrder(orderList))	#This variable stores the Shop name along with the cost associated for the order.
		lis.append(t) 									#The tuple is appended to the list
	
	# The Entire list is ready by the end of the above loop. The list consists of each Shop name along with the cost of the order if placed in the shop.
	
	#The following code is used to find the lowest total cost along with its corresponding shop. 
	
	min = lis[0][1]					#By Default, the first shop is assumed to be the lowest. This is a suitable assumption when comparison takes place.
	shopN = lis[0][0]  				#Going by the above logic, since the first shop cost is assumed to be minimum, the corresponding shop is to be returned if we dont find another shop which is cheaper.
	for shopName, Cost in lis:		#This loop iterates through each shop in the list of shop and associated cost
		if min>Cost :				#This is to check if the current shop's cost is less than that of the lowest cost found so far. If this evaluates to true, then the new lower cost is updated and its corresponding shop is updated as the best shop.
			min = Cost
			shopN = shopName;
    
	return shopN		#At the end of the above loop, we get the best shop which has the lowest totalCost. This shop is returned to the calling place of the function.

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print "For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName()
  orders = [('apples',3.0)]
  print "For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName()
