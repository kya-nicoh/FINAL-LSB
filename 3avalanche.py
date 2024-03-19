def calculate_difference(text1, text2):
    """Calculate the percentage difference between two texts."""
    max_length = max(len(text1), len(text2))
    min_length = min(len(text1), len(text2))
    
    # Count differing characters in overlapping part
    differences = sum(ch1 != ch2 for ch1, ch2 in zip(text1[:min_length], text2[:min_length]))
    
    # Add the extra characters from the longer text
    differences += max_length - min_length
    
    return (differences / max_length) * 100

def avalanche_effect_test(text1, text2):
    """Test the avalanche effect between two texts."""
    difference_percentage = calculate_difference(text1, text2)
    return difference_percentage

if __name__ == "__main__":
    text1 = "-15 8 -15 2 31 -23 -4 -1 29 -1 -14 -25 28 23 22 27 -5 13 -27 -3 -16 -1 -28 7 -8 21 2 13 14 17 -9 -23 22 -10 -4 11 -20 -23 -24 32 5 25 -2 15 -9 -7 -14 15 25 -23 -10 21 12 5 -22 29 11 23 14 7 -21 -13 -2 -26 4 -20 16 10 -5 18 -15 -5 -26 10 -2 -20 -9 5 23 21 -6 -5 22 24 0 -29 5 -14 -16 -4 -14 26 -13 15 -18 -1 -7 -27 -15 -3 6 24 2 -3 29 -14 -7"
    text2 = "-21 20 -26 29 10 -21 3 -19 -16 -2 24 -4 -1 -7 9 -6 29 -15 -6 23 -15 0 -16 28 -3 16 -28 -22 11 23 -6 -9 21 1 31 -28 1 26 4 25 1 -1 -10 14 -28 -12 -20 -2 -26 -23 12 2 -23 16 -2 27 -19 12 31 -6 -2 -25 -4 -21 1 10 13 13 1 13 4 -29 13 -29 -27 19 -8 23 -14 18 9 16 6 -15 23 -2 -9 9 -4 32 19 13 -21 -7 24 23 9 -18 -23 -24 1 32 -16 -4 14 -2 -15"
    
    difference_percentage = avalanche_effect_test(text1, text2)
    print(f"Avalanche effect: {difference_percentage:.2f}%")
