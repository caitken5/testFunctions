# This is a sample Python script.
import numpy as np
import matplotlib.pyplot as plt
import os


def flag_duplicate_entries(arr, c_num, dup_num):
    # This function will be used to identify groups of duplicated values in a particular column of data.
    # It assumes arr is passed as a numpy array, and c_num as an int.
    print("Called flag_duplicate_entries.")
    # In a for-loop, compare current and previous values.
    len_array = arr.shape[0]
    len_c = len(c_num)
    counter = 0
    flagged_duplicates = np.zeros((len_array, len_c), dtype=bool)
    # Only change values to true since the array is initialized as size len_array with False values.
    for l in range(len_c):
        for i in range(len_array-1):
            # print("flag_duplicate_entries: In for loop...")
            print(arr[i, c_num[l]], "and", arr[i+1, c_num[l]])
            if arr[i, c_num[l]]-arr[i+1, c_num[l]] == 0:
                # Value duplicated.
                print("Duplicate identified at index:", i)
                counter += 1
                # What to do if the counter reaches desired threshold of instances of duplicates.
                if counter == dup_num:
                    # first instance of counter being dup_num, identified adequate duplication.
                    print("Found duplicates in amount equivalent to", dup_num)
                    for j in range(dup_num):
                        print("Chain of duplicates of length", dup_num, "achieved.")
                        flagged_duplicates[i-9+j] = True
                elif counter > 10:
                    # All other instances of counter > dup_num.
                    print("Found duplicates in amount greater than", dup_num)
                    flagged_duplicates[i] = True
                else:
                    # Counter < dup_num.
                    print("Not enough duplicates to start flagging yet.")
            elif counter >= 10:  # ie. value and its next are not duplicates but it was just a chain so I need to track \
                # the last value.
                print("There was a chain of duplicates, but it ended. Tracking last duplicated value...")
                flagged_duplicates[i] = True
                counter = 0
            else:
                # Value not duplicated, and there was no previous chain.
                print("No duplicate here:", i)
                counter = 0
        # TODO: Check special case for last value in array.
        print("Reached final value in array.")
        if counter >= 10:
            flagged_duplicates[len_array-1] = True
    # Passes a column vector of boolean values that indicate indices where duplicate values occur.
    return flagged_duplicates


# Main code for testing function below.
# Load in desired numpy array; will test on Kos' data since I know there was some bias in the sensor and some stops \
# where the sensor got over-saturated.
file_path = "C:/Users/CSTAR/Desktop/ML-Force/build-ForceLD64/Forces/Kos-2021-11-25.txt"
# Open the file.
g = open(file_path, "r")
# Load the data as a numpy array.
temp = np.asarray(np.loadtxt(g, dtype='double', delimiter=", "))

# Define current header being used.
column_names = ['Time', 'Pos_X', 'Pos_Y', 'Pos_Z', 'Vel_X', 'Vel_Y', 'Vel_Z', 'C_Force', 'Angle_X', 'Angle_Y',
                'Angle_Z', 'F_Force_X', 'F_Force_Y', 'F_Force_Z', 'A_Force_X', 'A_Force_Y', 'A_Force_Z',
                'A_Force_X_Filt', 'A_Force_Y_Filt', 'A_Force_Z_Filt', 'A_Force_X_Left', 'A_Force_Y_Left',
                'A_Force_Z_Left']

# Isolate A_Force_Z to check for sensor saturation.
col_num = [column_names.index("Pos_X"), column_names.index("Pos_Y"), column_names.index("Pos_Z")]
# Call the function being tested.
duplic_num = 10000
all_flags = flag_duplicate_entries(temp, col_num, duplic_num)

# Make colorized graph of test to check flagging values.
reduced_all_flags = np.zeros(len(all_flags), dtype=bool)
for i in range(len(all_flags)):
    reduced_all_flags[i] = all_flags[i][0] & all_flags[i][1] & all_flags[i][2]
    if reduced_all_flags[i]:
        print("Holding in place at point", i)
not_all_flags = [not k for k in reduced_all_flags]
# not_dup_array = temp[not_all_flags, :]
# dup_array = temp[all_flags, :]
# Check if it worked correctly.
# sum_array = dup_array.shape[0] + not_dup_array.shape[0]
# print(sum_array, temp.shape[0])

# Make graph of values with different colours, red for duplicate.
t = column_names.index("Time")
c = column_names.index("A_Force_Z")
plt.plot(temp[not_all_flags, t], temp[not_all_flags, c], 'go', label="Not duplicated")
plt.plot(temp[reduced_all_flags, t], temp[reduced_all_flags, c], 'ro', label="Duplicated")
plt.title("Flagging Locations End Effector is not moving to check for Bias")
plt.xlabel("Time")
plt.ylabel("Force")
plt.legend()
plt.show()
print("End of program.")
