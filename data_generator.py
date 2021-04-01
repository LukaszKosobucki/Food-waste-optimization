import numpy as np
import matplotlib as plt
import pickle as pkl

items = pkl.load(open("items.pkl","rb"))

def separate_number_from_str(data):
    number=None
    for i in data:
        for word in i["kcal"].split():
            if word.isdigit():
                number = int(word)
        i["kcal"]=number
    return data

"""
function that generate:
random days of usability of the product
random weight of the product.
"""
def add_random_date_and_weight(data,days_spectrum, grams_100_spectrum,randomise_type="uniform"):
    if randomise_type == "uniform":
        for i in data:
            i["date"] = int(np.random.uniform(0.0,1.0)*days_spectrum +1) #in days
            i["weight"] = int(100 * (grams_100_spectrum * np.random.uniform(0.0,1.0) + 1)) #in grams 100g-1000g
    elif randomise_type == "normal":
        for i in data:
            i["date"] = int(np.random.normal(0.0,1.0)*days_spectrum +1) #in days
            i["weight"] = int(100 * (grams_100_spectrum * np.random.normal(0.0,1.0) + 1)) #in grams 100g-1000g
    return data

#example of usage
items = add_random_date_and_weight(items,24,9)
for i in items:
    print(i["date"] , "days left,", i["weight"] , "grams")

"""
we can use it to randomise number of calories of the product by 
the given percent ratio
"""
def randomise_calories(data,percent,randomise_type="uniform"):
    sum_of_calories = 0
    percent = percent/100
    data = separate_number_from_str(data)
    for i in data:
        sum_of_calories += i["kcal"]
    mean_of_calories = sum_of_calories/len(data)
    if randomise_type=="uniform":
        for i in data:
            new_percent = percent * np.random.uniform(0.0,1.0)
            loss = np.random.uniform(0.0,1.0)
            if loss > .5:
                i["kcal"] = int(i["kcal"] - mean_of_calories*new_percent)
            else:
                i["kcal"] = int(i["kcal"] + mean_of_calories * new_percent)
    elif randomise_type=="normal":
        for i in data:
            new_percent = percent * np.random.normal(0.0,1.0)
            loss = np.random.normal(0.0,1.0)
            if loss > .5:
                i["kcal"] = int(i["kcal"] - mean_of_calories * new_percent)
            else:
                i["kcal"] = int(i["kcal"] + mean_of_calories * new_percent)
    return data

#example of usage
items = randomise_calories(items,5)
for i in items:
    print(i["kcal"], "new calories number")

"""
function to add random price to the product 
STILL NEEDS TO BE DONE
"""
def add_random_price(data,percent):
    sum_of_prices = 0
    percent = percent/100
    for i in data:
        sum_of_prices += data[i]["price"]
    mean_of_prices = sum_of_prices/len(data)
    for i in data:
        new_percent = percent * np.random.rand()
        loss = np.random.rand()
        if loss > .5:
            data[i]["price"] = int(data[i]["price"] - mean_of_prices*new_percent)
        else:
            data[i]["price"] = int(data[i]["price"] + mean_of_prices * new_percent)
    return data

""""
ALSO FUNCTION FOR BATCHING DIFFERENT FRIDGES, 
WE CAN'T HAVE ONE FRIDGE WITH OVER 1k PRODUCTS
"""