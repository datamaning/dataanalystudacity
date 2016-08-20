#!/usr/bin/python
import numpy

def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    sq_errs = (predictions - net_worths) ** 2
    x = sq_errs < numpy.percentile(sq_errs, 90)
    cleaned_data = zip(ages[x], net_worths[x], sq_errs[x])

    return cleaned_data

