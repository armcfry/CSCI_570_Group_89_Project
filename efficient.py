import sys
import time
import psutil

class EfficientAlgorithm:
    def __init__(self, input_file: str, output_file: str):
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

    # reuse read_input and generate_strings from basic

    def read_input(self):
        str_info = []
        string = ""
        indeces = []

        with open(self.input_file, "r") as file_object:
            lines = file_object.readlines()
        for line in lines:
            line = line.strip()
            if line.isdigit():
                indeces.append(int(line))
            else:
                if string != "":
                    str_info.append({"string": string, "indeces": indeces})
                    string = ""
                    indeces = []
                    string = line
                else:
                    string = line
        str_info.append({"string": string, "indeces": indeces})
        self.str1 = self.generate_strings(str_info[0]["string"], str_info[0]["indeces"])
        self.str2 = self.generate_strings(str_info[1]["string"], str_info[1]["indeces"])

    def generate_strings(self, start_string: str, indeces: list) -> str:
        current_string = start_string
        for index in indeces:
            current_string = current_string[:index+1] + current_string + current_string[index+1:]
        return current_string

    def record_output(self):
        # also reuse from basic
        with open(self.output_file, "w+") as output:
            output.writelines(str(self.min_cost_align) + "\n")
            output.writelines(self.aligned_result[0] + "\n")
            output.writelines(self.aligned_result[1] + "\n")
            output.writelines(str(self.time_taken) + "\n")
            output.writelines(str(self.memory))

    def process_memory(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_consumed = int(memory_info.rss / 1024)
        return memory_consumed

    def time_wrapper(self):
        start_time = time.time()
        self.run_efficient_algorithm()
        end_time = time.time()
        time_taken = (end_time - start_time) * 1000
        return time_taken

    # full dp for small cases, modified from basic.py
    def full_dp_small(self, X: str, Y: str):
        #Standard DP for small subproblems |X| <= 1 or |Y| <= 1).
        #Returns aligned strings (aligned_X, aligned_Y).
        lenX = len(X)
        lenY = len(Y)

        # Create local DP matrix of size (lenX+1) x (lenY+1)
        dp = [[0] * (lenY + 1) for _ in range(lenX + 1)]

        # Initialize first column: align X[0..i] with empty string
        for i in range(1, lenX + 1):
            dp[i][0] = i * self.delta

        # Initialize first row: align empty string with Y[0..j]
        for j in range(1, lenY + 1):
            dp[0][j] = j * self.delta

        # Fill the DP table
        for i in range(1, lenX + 1):
            for j in range(1, lenY + 1):
                cost_gap_Y = dp[i - 1][j] + self.delta  # gap in Y (delete from X)
                cost_gap_X = dp[i][j - 1] + self.delta  # gap in X (insert into X)
                pair_key = X[i - 1] + "_" + Y[j - 1]
                cost_match = dp[i - 1][j - 1] + self.alpha_vals[pair_key]  # match / mismatch
                dp[i][j] = min(cost_gap_Y, cost_gap_X, cost_match)

        # Backtracking to reconstruct alignment
        aligned_X = []
        aligned_Y = []

        i, j = lenX, lenY
        while i > 0 or j > 0:
            # Case 1: came from dp[i-1][j] → deletion in Y (gap in Y)
            if i > 0 and dp[i][j] == dp[i - 1][j] + self.delta:
                aligned_X.append(X[i - 1])
                aligned_Y.append("_")
                i -= 1

            # Case 2: came from dp[i][j-1] → insertion in X (gap in X)
            elif j > 0 and dp[i][j] == dp[i][j - 1] + self.delta:
                aligned_X.append("_")
                aligned_Y.append(Y[j - 1])
                j -= 1

            # Case 3: came from dp[i-1][j-1] → match or mismatch
            else:
                aligned_X.append(X[i - 1])
                aligned_Y.append(Y[j - 1])
                i -= 1
                j -= 1

        # The strings are built backwards, so reverse them
        aligned_X.reverse()
        aligned_Y.reverse()

        return "".join(aligned_X), "".join(aligned_Y)
        #pass

    # TODO:forward DP, O(len(Y)) space?
    def nw_score_prefix(self, X: str, Y: str):
        pass

    # TODO:backward DP
    def nw_score_suffix(self, X: str, Y: str):
        pass

    # TODO:Hirschberg Recursive Divide-and-Conquer Algorithm, the one mentioned in Lecture 8
    def hirschberg(self, X: str, Y: str):
        #  Recursive Hirschberg algorithm.
        #  Returns a pair (aligned_X, aligned_Y).
        # base case：len(X)==0 / len(Y)==0 / small，use full_dp_small
        # otherwise recursive backward and forward
        pass

    # Efficient algorithm main Entry
    def run_efficient_algorithm(self):
        aligned_X, aligned_Y = self.hirschberg(self.str1, self.str2)
        self.aligned_result = [aligned_X, aligned_Y]
        # Run Hirschberg on the two generated strings, store alignment and compute final alignment cost.
        self.min_cost_align = self.compute_cost(aligned_X, aligned_Y)

    def compute_cost(self, a: str, b: str) -> int:
        cost = 0
        for x, y in zip(a, b):
            if x == "_" or y == "_":
                cost += self.delta
            else:
                cost += self.alpha_vals[x + "_" + y]
        return cost

    # Unit test for full_dp_small
    def test_full_dp_small(self):
        test_cases = [
            ("A", "G"),
            ("A", "A"),
            ("A", ""),
            ("", "T"),
            ("AG", "A"),
            ("AG", "GA"),
            ("G", "TA"),
            ("AC", "GT"),
        ]

        for X, Y in test_cases:
            aligned_X, aligned_Y = self.full_dp_small(X, Y)
            cost = self.compute_cost(aligned_X, aligned_Y)
            print("X =", X, " Y =", Y)
            print("  aligned X:", aligned_X)
            print("  aligned Y:", aligned_Y)
            print("  cost:", cost)
            print("-" * 40)



if __name__ == "__main__":

    # If run without arguments then unit test
    if len(sys.argv) == 1:
        print("Running full_dp_small() unit tests...\n")
        tester = EfficientAlgorithm("", "")
        tester.test_full_dp_small()
        sys.exit(0)

    # Else normal workflow
    file_input = sys.argv[1]
    file_output = sys.argv[2]

    eff = EfficientAlgorithm(file_input, file_output)
    eff.read_input()

    eff.time_taken = eff.time_wrapper()
    eff.memory = eff.process_memory()
    eff.record_output()
