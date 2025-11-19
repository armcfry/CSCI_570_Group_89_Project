import sys 
from resource import * 
import time 
import psutil 

class BasicAlgorithm:
    def __init__(self, input_file: str, output_file:str):
        self.input_file = input_file
        self.output_file = output_file
        self.str1 = ""
        self.str2 = ""
        self.alpha_vals = {"A_A": 0, "A_C": 110, "A_G": 48, "A_T": 94,
                           "C_A": 110, "C_C": 0, "C_G": 118, "C_T": 48,
                           "G_A": 48, "G_C": 118, "G_G": 0, "G_T": 110,
                           "T_A": 94, "T_C": 48, "T_G": 110, "T_T": 0}
        self.delta = 30
        self.aligned_result = []
        self.time_taken = 0.0
        self.memory = 0
        self.min_cost_align = 0

    def read_input(self) -> str:
        str_info = []
        string = ""
        indeces = []

        with open(self.input_file, "r") as file_object:
            lines = file_object.readlines()
        for line in lines:
            line = line.strip()
            # if line is int
            if line.isdigit():
                indeces.append(int(line))
            else:
                if string != "":
                    # this is a new string, save the old one
                    str_info.append({"string": string, "indeces": indeces})
                    string = ""
                    indeces = []
                    # set new string
                    string = line
                else:
                    # this is the first string, set it
                    string = line
                    
        # store final string
        str_info.append({"string": string, "indeces": indeces})

        # create strings to use in algorithm
        self.str1 = self.generate_strings(str_info[0]["string"], str_info[0]["indeces"])
        self.str2 = self.generate_strings(str_info[1]["string"], str_info[1]["indeces"])

    def generate_strings(self, start_string:str, indeces:list) -> str:
       current_string = start_string
       for index in indeces:
            current_string = current_string[:index+1] + current_string + current_string[index+1:]
       return current_string

    def record_output(self):
        with open(self.output_file, "w+") as output:
            output.writelines(str(self.min_cost_align) + "\n")
            output.writelines(self.aligned_result[0] + "\n")
            output.writelines(self.aligned_result[1] + "\n")
            output.writelines(str(self.time_taken) + "\n")
            output.writelines(str(self.memory))
    
    def run_basic_algorithm(self):
        # initialize first column
        for row in range(1, len1 + 1):
            matrix[row][0] = row * self.delta

        # initialize first row
        for col in range(1, len2 + 1):
            matrix[0][col] = col * self.delta

        # fill the matrix using recurrence:
        for row in range(1, len1 + 1):
            for col in range(1, len2 + 1):
                matrix[row][col] = min(
                    matrix[row - 1][col] + self.delta,  # delete from str1 (gap in str2)
                    matrix[row][col - 1] + self.delta,  # insert into str1 (gap in str1)
                    matrix[row - 1][col - 1] + self.alpha_vals[self.str1[row - 1] + "_" + self.str2[col - 1]]  # match/mismatch
                )

        # reconstruct the optimal alignment
        str1_aligned = []  # aligned version of str1
        str2_aligned = []  # aligned version of str2

        row = len1
        col = len2

        while row > 0 or col > 0:
            # Case 1: came from matrix[row-1][col] → deletion (gap in str2)
            if row > 0 and matrix[row][col] == matrix[row - 1][col] + self.delta:
                str1_aligned.append(self.str1[row - 1])
                str2_aligned.append("_")  # gap
                row -= 1

            # Case 2: came from matrix[row][col-1] → insertion (gap in str1)
            elif col > 0 and matrix[row][col] == matrix[row][col - 1] + self.delta:
                str1_aligned.append("_")  # gap
                str2_aligned.append(self.str2[col - 1])
                col -= 1

            # Case 3: came from matrix[row-1][col-1] → match or mismatch
            else:
                str1_aligned.append(self.str1[row - 1])
                str2_aligned.append(self.str2[col - 1])
                row -= 1
                col -= 1

        # strings are compiled backwards, so reverse them
        str1_aligned.reverse()
        str2_aligned.reverse()

        self.aligned_result.append("".join(str1_aligned))
        self.aligned_result.append("".join(str2_aligned))

    
    def process_memory(self): 
        process = psutil.Process() 
        memory_info = process.memory_info() 
        memory_consumed = int(memory_info.rss/1024) 
        return memory_consumed 

    def time_wrapper(self): 
        start_time = time.time() 
        self.run_basic_algorithm() 
        end_time = time.time() 
        time_taken = (end_time - start_time)*1000 
        return time_taken 

if __name__ == '__main__':
    file_input = sys.argv[1]
    file_output = sys.argv[2]

    basicObj = BasicAlgorithm(file_input, file_output)
    basicObj.read_input()

    len1 = len(basicObj.str1)
    len2 = len(basicObj.str2)

    # initialize 2d matrix:
    matrix = []
    for _ in range(len1 + 1):
        row = []
        for _ in range(len2 + 1):
            row.append(0)
        matrix.append(row)
    
    # call algorithm
    basicObj.time_taken = basicObj.time_wrapper()
    basicObj.memory = basicObj.process_memory()
    basicObj.min_cost_align = matrix[len1][len2]

    # compile and record results
    basicObj.record_output()


    print()