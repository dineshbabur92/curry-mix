import os
import sys
import argparse
import numpy as np
from numpy import ndarray
import math

CURRY_PRIORITY = {'V':0,'M':1, 'N': 3} # For numeziring curry prefs
CURRY_PRIORITY_INVERSE =  {0:'V', 1:'M', 3:'V'} # 3-V because if no pref, 
                                                #   veg by default
NO_SOLUTION = False # Flag representing if there is no solution at all

def fill_encode_order_matrix(order_matrix: ndarray, curry_orders_cust: list, 
                    curry_priority: dict = CURRY_PRIORITY):
    """
    Creates order matrix, numerizes curry preferences

    Args:
    order_matrix: initialized matrix to no preference
    curry_orders_cust: list of customer orders with each element
                        being a line representing an order
    curry_priority: priority of each curry

    Returns:
    order_matrix: final matrix filled in with curry prefs
    """

    # O(n*m) - n curries, m customers
    for i, order in enumerate(curry_orders_cust):

        # splitting the line to curry prefs
        curry_pref = order.split()

        print()
        print(f"curry_pref for {i+1}th order", curry_pref)
        print("Will numerize curry prefs as priorities as above, N - no pref", 
            CURRY_PRIORITY)

        # filling in the matrix
        for j in range(0,len(curry_pref),2):
            curry = curry_pref[j+1]
            nth_curry = int(curry_pref[j])-1
            order_matrix[i][nth_curry] = curry_priority[curry]
        
    return order_matrix

def process_orders(num_curries: int, curry_orders_cust: list):
    """
    Process orders to prepare the final curry mix

    Args:
    num_curries: total no. of curries
    curry_orders_cust: list of customer orders with each element
                        being a line representing an order

    Returns:
    curry_mix: final curry mix solution
    """

    global NO_SOLUTION

    # initiliazing order matrix
    num_cust = len(curry_orders_cust)
    order_matrix = np.ndarray((num_cust, num_curries), dtype=int)
    order_matrix.fill(3)

    # filling and numerizing order_matrix
    order_matrix = fill_encode_order_matrix(order_matrix,curry_orders_cust)
    print()
    print("Thus, order_matrix\n", order_matrix)

    # least and max pref for customer - veg or meat curry
    # O(n*m) - n curries, m customers
    least_curry_pref = [ 0 if 0 in order else 1 for order in order_matrix]
    max_curry_pref = [ 1 if 1 in order else 0 for order in order_matrix]
    print()
    print("least_curry_pref", least_curry_pref)
    print("max_curry_pref", max_curry_pref)

    # intializing final curry mix
    curry_mix = np.ndarray(num_curries, dtype=int)
    curry_mix.fill(3)
    print()
    print("intial curry_mix", curry_mix)

    # if least preference is meat, filling that in curry_pref first
    #       since veg curry for these customers is not accepted
    # O(n*m) - n curries, m customers
    for i, l in enumerate(least_curry_pref):
        if l == 1: # least preference is meat
            order_curry = order_matrix[i].tolist()
            curry_mix[order_curry.index(l)] = l # add that as nth curry

    print()
    print("curry_mix after filling meat lovers", curry_mix)

    # O(n*n*m) - n curries, m customers
    for i, l in enumerate(least_curry_pref):

        # skipping meat lovers already filled in curry_mix
        if l == 1:
            continue
        
        order_curries = order_matrix[i].tolist()
        curry_index = order_curries.index(l)
        m = 1
        counter = 0
        checked_max = False
        while (curry_mix[curry_index] == m # already chosen as meat curry
            and counter<20): # to debug just in case
            try:
                # print(order_curries.tolist()[curry_index+1:])
                curry_index = order_curries.index(l, curry_index+1)
                # print(curry_index)
                counter += 1 # to debug just in case
            except:
                # print("Index not found")
                # No suitable veg curry index found in the mix
                #   Trying for meat index if there is a max pref of
                #   meat for the customer
                if max_curry_pref[i] == 1 and not checked_max:
                    checked_max = True
                    l = 1
                    m = 0
                    curry_index = order_curries.index(l)
                    # print(l, m, curry_index)
                    continue
                # If there is no meat preference and
                #   no veg curry could be added in the mix
                #   then no solution for this customer
                else:
                    NO_SOLUTION = True
                    break
        if NO_SOLUTION:
            break
        print("counter", counter)
        curry_mix[curry_index] = l # final choice of veg or meat
    
    if NO_SOLUTION:
        return

    # Inversing priority and showing as char preferences
    curry_mix = curry_mix.tolist()
    for i, curry in enumerate(curry_mix):
            curry_mix[i] = CURRY_PRIORITY_INVERSE[curry]

    print()
    print("curry_mix final", curry_mix)

    return curry_mix

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    """
    sample input file:
    2
    1 V 2 M
    1 M
    """
    parser.add_argument('--curry-orders', type=str, 
                      required=True, help='Input file having curry orders')
    args = parser.parse_args()
    curry_orders_file = args.curry_orders
    
    with open(curry_orders_file, "r") as file:
        no_curries = int(file.readline())
        curry_orders_cust = file.read().split('\n')
        
    solution = process_orders(no_curries, curry_orders_cust)

    print()
    print("============================================================")
    print()
    if not NO_SOLUTION:
        print("Final solution: ", solution)
    else:
        print("No solution exists")
    print()
    print()




    
