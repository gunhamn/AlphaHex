import ast
if __name__ == "__main__":
    with open('output.txt', 'r') as file:
    # Initialize a counter for arrays meeting the condition
        count = 0
        num = 0
        # Iterate through each line in the file
        for line in file:
            # Strip any leading/trailing whitespace and split the line by '], '
            elements = line.strip().split('], ')

            # Extract the first element as a list
            first_element = [int(x) for x in elements[0].strip('[[]').split(',')]

            # Extract the second element as an array
            second_element_str = elements[1].rstrip(']') +']'

            second_element = ast.literal_eval(second_element_str)
            # Check if the first element is [5, 1] and if the second value of the second element is higher than the first
            if first_element == [1, 5] :
                num+=1
            
                if second_element[1] >= second_element[0]:
                # Increment the counter
                    count += 1
    print(f" correct: {count} out of {num}")