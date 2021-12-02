# This is a sample Python script.

def flag_duplicate_entries(arr, c_num):
    # This function will be used to identify groups of duplicated values in a particular column of data.
    # It assumes arr is passed as a numpy array, and c_num as an int.
    print("Called flag_duplicate_entries.")
    # In a for-loop, compare current and previous values.
    len_array = arr.shape[0]
    for i in range(len_array-1):
        print("flag_duplicate_entries: In for loop...")


# Main code for testing function below.
# Load in desired numpy array; will test on Kos' data since I know there was some bias in the sensor and some stops \
# where the sensor got over-saturated.

