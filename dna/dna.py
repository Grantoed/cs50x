import csv
from sys import argv


def main():
    # TODO: Check for command-line usage
    check_usage()
    _, database, sequence = argv

    # TODO: Read database file into a variable
    database = read_database(database)

    # TODO: Read DNA sequence file into a variable
    sequence = read_sequence(sequence)

    # TODO: Find longest match of each STR in DNA sequence
    str_occurrences = find_str_occurences(database, sequence)

    # TODO: Check database for matching profiles
    matching_profile = find_matching_profile(database, str_occurrences)
    if matching_profile:
        print(matching_profile)
    else:
        print("No match")

    return


def check_usage():
    if (len(argv) != 3):
        print("Usage: dna.py database, sequence")
        exit()


def read_database(database):
    rows = []
    try:
        with open(database) as file:
            reader = csv.DictReader(file)
            _, *strNames = reader.fieldnames
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"Error: {database} not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading {database}: {e}")
        exit(1)

    return {
        "strNames": strNames,
        "rows": rows
    }


def read_sequence(sequence):
    file = open(sequence, encoding="utf-8")
    return file.read()


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def find_str_occurences(database, sequence):
    str_occurrences = {}
    for str in database["strNames"]:
        str_occurrences[str] = longest_match(sequence, str)

    return str_occurrences


def find_matching_profile(database, str_occurrences):
    for row in database["rows"]:
        match = True
        for str_name in database["strNames"]:
            if int(row[str_name]) != str_occurrences[str_name]:
                match = False
                break
        if match:
            return row["name"]
    return None


main()
