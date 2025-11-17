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

    def record_ouput(self):
        # TODO: report to file
        print()
    
    def run_basic_algorithm(self):
        #TODO: algorithm to calculate the answer here
        print(f"First String: {self.str1}")
        print(f"Second String: {self.str2}")
    
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

basicObj = BasicAlgorithm("/some/path/to/file/input1.txt", "output_sample.txt")
basicObj.read_input()
basicObj.run_basic_algorithm()
print()