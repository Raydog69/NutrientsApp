
def fill_gaps_alternative(list):
    index_value = {}
    for value in list:
        if value:
            index_value[value.index] = value
    
    return filled_values

# Test the function with the provided list
values = [None, None, 55, 70, None, None, None, 80, None]
filled_values = fill_gaps_alternative(values)
print("Filled Values:", filled_values)

# Detailed Analysis
if filled_values == [None, None, 55, 70, 73.33333333333333, 76.66666666666667, 80, 80, None]:
    print(filled_values)
