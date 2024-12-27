# Define the Unicode character U+2009 (THIN SPACE)
target_unicode_char = "\u2009"

# Input file and output file names
input_file = "input.txt"
output_file = "output.txt"

# Open the input file in read mode and the output file in write mode
with open(input_file, "r", encoding="utf-8") as in_file, open(output_file, "w", encoding="utf-8") as out_file:
    # Iterate through each line in the input file
    for line in in_file:
        # Remove all occurrences of the target Unicode character from the line
        line_without_thin_space = line.replace(target_unicode_char, "")

        # Write the modified line to the output file
        out_file.write(line_without_thin_space)

# Print a message to confirm the operation
print(f"Removed U+2009 from {input_file} and saved the result in {output_file}")
