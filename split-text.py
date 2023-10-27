# Open the original analogy test file for reading
with open('word-test.txt', 'r') as f:
    lines = f.readlines()

# Define output files
semantic_file = open('semantic-test.txt', 'w+')
syntactic_file = open('syntactic-test.txt', 'w+')

# Counter for section headers
header_count = 0

# Loop through the lines and write to appropriate file
for line in lines:
    # Check for section headers
    if line.startswith(":"):
        header_count += 1

    # Write the line to the appropriate file based on header count
    if header_count < 6:
        semantic_file.write(line)
    else:
        syntactic_file.write(line)

# Close the output files
semantic_file.close()
syntactic_file.close()