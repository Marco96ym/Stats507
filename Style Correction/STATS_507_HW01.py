#!/usr/bin/env python
# coding: utf-8

# # Question 0 - Markdown warmup

# ##### This is _question 0_ for [problem set 1](https://jbhender.github.io/Stats507/F21/ps/ps1.html) of [Stats 507](https://jbhender.github.io/Stats507/F21/)

# > Question 0 is about Markdown

# ##### The next question is about the **Fibonnaci sequence**, $$F_n = F_(n-2) + F_(n-1)$$. In part **a** we will define a Python function `fib_rec()`.
# ##### Below is a ...

# ### Level 3 Header

# ##### Next, we can make a bulleted list:
# + Item 1
# 
#     - detail 1
#     - detail 2
# + Item 2
# 
# ##### Finally, we can make an enumerated list:
# 
#     a. Item 1  
#     b. Item 2  
#     c. Item 3  

# # Question 1 - Fibonnaci Sequence

# a. 

# In[53]:


# recursive version:
def fib_rec(n):
    if (n == 0):
        return 0
    if (n == 1):
        return 1
    return fib_rec(n - 2) + fib_rec(n - 1)


# b.

# In[54]:


# for loop version:
def fib_for(n):
    fib_0 = 0.0
    fib_1 = 1.0
    if (n == 0):
        return fib_0
    if (n == 1):
        return fib_1
    else:
        for i in range(2, n+1):
            fib_val = fib_0 + fib_1
            fib_0 = fib_1
            fib_1 = fib_val
        return fib_val    


# c.

# In[55]:


# while loop version:
def fib_whl(n):
    fib_0 = 0.0
    fib_1 = 1.0
    if (n == 0):
        return fib_0
    if (n == 1):
        return fib_1
    i = 2
    while (i <= n):
            fib_val = fib_0 + fib_1
            fib_0 = fib_1
            fib_1 = fib_val
            i = i + 1
    return fib_val


# d.

# In[56]:


# rounding version:
import math
def fib_rnd(n):
    phi = (1 + math.sqrt(5))/2
    return round(phi**n / math.sqrt(5))


# e.

# In[57]:


# truncation version:
def fib_flr(n):
    phi = (1 + math.sqrt(5))/2
    return math.floor(phi**n / math.sqrt(5) + 1/2)


# f.

# In[ ]:


# comparison of median computation time of functions above:
import time
import statistics
from tabulate import tabulate
n_seq = [5*i for i in range(11)]
func_list = [fib_rec, fib_for, fib_whl, fib_rnd, fib_flr]

# this function return a list with median computing time of each 
# fibonnaci function given a list of n in n_seq
def compute_median_time():
    med_time_list = []
    for func in func_list:
        time_list = []
        for n in n_seq:
            start_time = time.time()
            fib_data = func(n)
            time_list.append(time.time() - start_time)
        med_time_list.append(statistics.median(time_list))
    return med_time_list

# creating a dictionary whose keys are names of fibonnaci function
# and whose rows are median computing time
dict_func_time = {'fib_rec':None, 'fib_for':None, 'fib_whl':None, 'fib_rnd':None, 'fib_flr':None}
med_time_list = compute_median_time()
i = 0
for k,v in dict_func_time.items():
    dict_func_time[k] = med_time_list[i]
    i = i + 1
    
# convert dict to a table and show it
table_func_med_time = tabulate(dict_func_time, tablefmt="fancy_grid") 
print(table_func_med_time)

# I interruped the computing process since it takes very long time


# # Question 2 - Pascal’s Triangle

# a.

# In[17]:


# binomial coefficient function 
def bino_coeff(n, k):
    if (k == 0):
        return 1
    return bino_coeff(n, k-1)*((n+1-k)/k)

# function to return a specific row in pascal triangle
# given row index n 
def get_pascal_tri_row(n):
    pascal_tri_row = [1]
    if (n == 0):
        return pascal_tri_row
    
    for k in range(1, n+1):
        col_val = int(bino_coeff(n, k))
        pascal_tri_row.append(col_val)
    return pascal_tri_row


# b.

# In[18]:


# helper function to produce multiple white space
def multi_white_spa(n):
    wht_spa = ""
    for i in range(n):
        wht_spa += " "
    return wht_spa
  
# function to print out first n row of pascal triangle 
def prin_fir_n_pascal_row(n):
    for i in range(n):
        wht_spa = multi_white_spa(n - 1 - i)
        print(wht_spa, get_pascal_tri_row(i))

prin_fir_n_pascal_row(15)
        


# # Question 3 - Statistics 101

# a.

# In[2]:


import numpy as np
from scipy import stats

# function to give point and interval estimate of 
def mean_CI_esti(data, CI, ci_format = 'θ̂[XX%CI:(θ̂L,θ̂U)]'):
    try:
        np_arr = np.array(data)
        est = np.mean(np_arr)
        level = CI
        z_val = 1/(stats.norm.cdf(1/2 + level/200))
        std_err = np.std(np_arr, ddof=1) / np.sqrt(np.size(np_arr))
        upr = est + z_val*std_err
        lwr = est - z_val*std_err
        dict_CI = {'est':est, 'lwr':lwr, 'upr':upr, 'level':level}
        if (ci_format == None): 
            return dict_CI
        else:
            return ("{est}[{level}%CI : ({lwr}, {upr})]".format_map(dict_CI))
    except:
        print("Input object is not coercable to 1d Numpy array using np.array().")
        return '\n'


# b.

# In[3]:


# helper function to count number of success in a binomial experiment
def bino_succ_cont(np_arr):
    num_succ = 0
    for val in np_arr:
            if (val == 1):
                num_succ += 1
    return num_succ


# In[4]:


# function giving different confidence interval based on different methods

def binomial_conf_intval(data, CI, method, ci_format = 'θ̂[XX%CI:(θ̂L,θ̂U)]'):
        try:
            assert (method == "Normal approximation" or 
                   method == "Clopper-Pearson interval" or 
                   method == "Jeffrey’s interval" or 
                   method == "Agresti-Coull interval" or 
                   method == "Standard Estimate")
            np_arr = np.array(data)
            sample_size = np.size(np_arr)
            num_succ = bino_succ_cont(np_arr)
            sample_proportion = num_succ/sample_size
            level = CI
            z_val = 1/(stats.norm.cdf(1/2 + level/200))
            
            if (method == "Standard Estimate"):
                return(mean_CI_esti(np_arr, level, ci_format))
                
            if (method == "Normal approximation"):
                try:
                    assert (num_succ > 12 and sample_size - num_succ > 12)
                    est = sample_proportion
                    lwr = est - z_val*np.sqrt(est*(1 - est)/sample_size)
                    upr = est + z_val*np.sqrt(est*(1 - est)/sample_size)
                    dict_CI = {'est':est, 'lwr':lwr, 'upr':upr, 'level':level}
                    if (ci_format == None): 
                        return dict_CI
                    else:
                        return ("{est}[{level}%CI : ({lwr}, {upr})]".format_map(dict_CI))
                    
                except:
                    print('Condition to apply Normal approximation is not satisfied!')
                    print('Number of success and number of failure should be both bigger than 12.')
                    
            if (method == "Clopper-Pearson interval"):
                alpha = 1 - level/100
                lwr = stats.beta.ppf(alpha/2, num_succ, sample_size - num_succ + 1)
                upr = stats.beta.ppf(1 - alpha/2, num_succ + 1, sample_size - num_succ)
                est = (lwr + upr)/2
                dict_CI = {'est':est, 'lwr':lwr, 'upr':upr, 'level':level}
                if (ci_format == None):
                    return dict_CI
                else:
                    return ("{est}[{level}%CI : ({lwr}, {upr})]".format_map(dict_CI))
                
            if (method == "Jeffrey’s interval"):
                alpha = 1 - level/100
                est = sample_proportion
                lwr = stats.beta.ppf(alpha/2, num_succ + 1/2, sample_size - num_succ + 1/2)
                upr = stats.beta.ppf(1 - alpha/2, num_succ + 1/2, sample_size - num_succ + 1/2)
                if (num_succ == 0):
                    lwr = 0 
                if (num_succ == sample_size):
                    upr = 1
                dict_CI = {'est':est, 'lwr':lwr, 'upr':upr, 'level':level}
                if (ci_format == None):
                    return dict_CI
                else:
                    return ("{est}[{level}%CI : ({lwr}, {upr})]".format_map(dict_CI))
                
                
            if (method == "Agresti-Coull interval"):
                n_head = sample_size + pow(z_val, 2)
                p_head = (num_succ + pow(z_val, 2)/2)/n_head
                est = p_head
                lwr = p_head - z_val*pow(p_head*(1 - p_head)/n_head, 1/2)
                upr = p_head + z_val*pow(p_head*(1 - p_head)/n_head, 1/2)
                dict_CI = {'est':est, 'lwr':lwr, 'upr':upr, 'level':level}
                if (ci_format == None):
                    return dict_CI
                else:
                    return ("{est}[{level}%CI : ({lwr}, {upr})]".format_map(dict_CI))
        
        except:
            print("Please make sure input data is coercable to 1d Numpy array using np.array().")
            print("Please make sure use one of following methods as the 4th parameter:")
            print("\tStandard Estimate, Normal approximation, Clopper-Pearson interval, Jeffrey’s interval, Agresti-Coull interval")
                


# c.

# In[5]:


# Create a 1d Numpy array with 42 ones and 48 zeros. 
# Construct a nicely formatted table comparing 90, 95, and 99% confidence intervals using each of the methods above (including part a) on this data. 
# Choose the number of decimals to display carefully to emphasize differences. 
# For each confidence level, which method produces the interval with the smallest width

from tabulate import tabulate
data_arr = np.ones(90)
data_arr[:48] = 0.0
np.random.shuffle(data_arr)
head = ["Methods", "Confidence Interval", "Interval Width"]
methods_lst = ["Standard Estimate", "", "", "Normal approximation", "", "", 
               "Clopper-Pearson interval", "", "", "Jeffrey’s interval", "", "", 
               "Agresti-Coull interval", "", ""]
given_ci_lst = [90, 95, 99]
ci_lst = []
interval_wid_lst = [] 

for method in methods_lst:
    if (method == ""):
        continue
    else:
        for CI in given_ci_lst:
            ci_lst.append(binomial_conf_intval(data_arr, CI, method))
            bino_coeff_ci_dict = binomial_conf_intval(data_arr, CI, method, None)
            interval_wid = round((bino_coeff_ci_dict['upr'] - bino_coeff_ci_dict['lwr']), 4)
            interval_wid_lst.append(interval_wid)
        
summary_dict = {'Methods':methods_lst, 'Confidence Interval':ci_lst, 'Interval Width':interval_wid_lst}

print(tabulate(summary_dict, headers=head, tablefmt="fancy_grid"))


# ##### I round the width of each confidence interval to 4 decimals 
# ##### From the table, we can find:     
# ##### For **_90%_** confidence level, **Agresti-Coull interval** produces the smallest interval width
# ##### For **_95%_** confidence level, **Agresti-Coull interval** produces the smallest interval width
# ##### For **_99%_** confidence level, **Agresti-Coull interval** produces the smallest interval width
