# This is a sample Python script.
import numpy as np
import matplotlib.pyplot as plt


def flag_duplicate_entries(arr, c_num, dup_num):
    # This function will be used to identify groups of duplicated values in a particular column of data.
    # It assumes arr is passed as a numpy array, and c_num as an int.
    print("Called flag_duplicate_entries.")
    # In a for-loop, compare current and previous values.
    len_array = arr.shape[0]
    len_c = len(c_num)
    counter = 0  # Initialize the counter to 0.
    flagged_duplicates = np.zeros((len_array, len_c), dtype=bool)
    # Only change values to true since the array is initialized as size len_array with False values.
    for l in range(len_c):
        for i in range(1, len_array):
            # print("flag_duplicate_entries: In for loop...")
            # print(arr[i-1, c_num[l]], "and", arr[i, c_num[l]])
            if arr[i-1, c_num[l]]-arr[i, c_num[l]] == 0:
                # Value duplicated.
                # print("Duplicate identified at index:", i)
                counter += 1
                # What to do if the counter reaches desired threshold of instances of duplicates.
                if counter == dup_num-1:
                    # first instance of counter being dup_num, identified adequate duplication.
                    print("Found duplicates in amount equivalent to", dup_num)
                    for j in range(dup_num):
                        # print("Chain of duplicates of length", dup_num, "achieved.")
                        flagged_duplicates[i-dup_num+1+j][l] = True
                elif counter >= dup_num:
                    # All other instances of counter > dup_num.
                    # print("Found duplicates in amount greater than", dup_num)
                    flagged_duplicates[i][l] = True
                # else:
                    # Counter < dup_num.
                    # print("Not enough duplicates to start flagging yet.")
            elif counter >= dup_num:  # ie. value and its next are not duplicates but it was just a chain so I need to \
                # the last value.
                print("There was a chain of duplicates, but it ended at length:", counter + 1)
                counter = 0
            else:
                # Value not duplicated, and there was no previous chain.
                print("No duplicate here:", i)
                counter = 0
        print("Reached final value in array in column:", l)
        # Reset the counter for cycling through each row in the array to 0.
        counter = 0
    # Passes a column vector of boolean values that indicate indices where duplicate values occur.
    return flagged_duplicates


# Main code for testing function below.
# Load in desired numpy array; will test on Kos' data since I know there was some bias in the sensor and some stops \
# where the sensor got over-saturated.
# file_path = "C:/Users/CSTAR/Desktop/ML-Force/build-ForceLD64/Forces/Kos-2021-11-25.txt"
file_path = "C:/Users/carol/Downloads/Kos-2021-11-25.txt"
# Open the file.
g = open(file_path, "r")
# Load the data as a numpy array.
temp = np.asarray(np.loadtxt(g, dtype='double', delimiter=", "))

# Define current header being used.
column_names = ['Time', 'Pos_X', 'Pos_Y', 'Pos_Z', 'Vel_X', 'Vel_Y', 'Vel_Z', 'C_Force', 'Angle_X', 'Angle_Y',
                'Angle_Z', 'F_Force_X', 'F_Force_Y', 'F_Force_Z', 'A_Force_X', 'A_Force_Y', 'A_Force_Z',
                'A_Force_X_Filt', 'A_Force_Y_Filt', 'A_Force_Z_Filt', 'A_Force_X_Left', 'A_Force_Y_Left',
                'A_Force_Z_Left']

# col_num = [column_names.index("Pos_X"), column_names.index("Pos_Y"), column_names.index("Pos_Z")]
col_num = [column_names.index("C_Force")]
# Call the function being tested.
duplic_num = 2
all_flags = flag_duplicate_entries(temp, col_num, duplic_num)

# Make colorized graph of test to check flagging values.
# reduced_all_flags = np.zeros(len(all_flags), dtype=bool)
# for i in range(len(all_flags)):
#     reduced_all_flags[i] = all_flags[i][0] & all_flags[i][1] & all_flags[i][2]
#     if reduced_all_flags[i]:
#         print("Holding in place at point", i)
# not_all_flags = [not k for k in reduced_all_flags]
not_all_flags = [not k for k in all_flags]
all_flags = [not k for k in not_all_flags]
# Make graph of values with different colours, red for duplicate.
t = column_names.index("Time")
# c = [column_names.index("Pos_X"), column_names.index("Pos_Y"), column_names.index("Pos_Z")]
# plt.plot(temp[not_all_flags, t], temp[not_all_flags, c[0]], 'go', label="Not duplicated x")
# plt.plot(temp[not_all_flags, t], temp[not_all_flags, c[1]], 'b-', label="Not duplicated y")
plt.plot(temp[not_all_flags, t], temp[not_all_flags, col_num[0]], 'mo', label="Not duplicated force command")
plt.plot(temp[all_flags, t], temp[all_flags, col_num[0]], 'ro', label="Duplicated force command")
plt.title("Flagging Locations Force Command is Duplicated at 0")
plt.xlabel("Time")
plt.ylabel("Force [N]")
plt.legend(loc='upper right')
plt.show()
print("End of program.")
