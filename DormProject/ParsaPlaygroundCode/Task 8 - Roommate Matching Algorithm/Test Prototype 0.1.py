# Revision History
# Name                  Date                Description
# Parsa Jafaripour      10/28/2024          Created the first prototype of the matching algorithm. Using the threshold tactic and starting the compatibility score from 100.

# Example of list of student responses from Google sheets.
student_responses = [
    ["H123456789", "No", "Morning", "Extroverted", "Disorganized", "Stay in", "Hot"],
    ["H987654321", "Yes", "Night", "Introverted", "Organized", "Go out", "Cold"]
]

# Defining questions weights
weights = [10,0.2,0.2,0.1,0.1,0.2,0.1] # Can adjust later based on importance.

def calculate_compatibility(student1, student2):
    score = 100 # We start the compatibility at 100
    for i, (response1, response2) in enumerate(zip(student1, student2)):
        if response1 != response2:
            score -= weights[i] * 10 # This deducts 10% of the total score based on the weight.
    return score

def match_students(students):
    matches = []
    threshold = 70 # Setting the threshold to 70, but this can change as well.
    for i in range(len(students)):
        for j in range(i + 1, len(students)):
            compatibility_score = calculate_compatibility((students[i][1:]), students[j][1:]) # Skipping the first element from the answers (ID)
            if compatibility_score >= threshold:
                matches.append((students[i][0], students[j][0], compatibility_score))
            else:
                print(f"This pair {students[i][0]} and {students[j][0]} are not compatible. {compatibility_score}")
    return matches



matched_pairs = match_students(student_responses)
for pair in matched_pairs:
    print(f"Matched {pair[0]} and {pair[1]} with compatibility score of {pair[2]}%")
