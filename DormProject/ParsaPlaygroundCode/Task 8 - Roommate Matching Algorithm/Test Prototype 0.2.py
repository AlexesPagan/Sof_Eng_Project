# Revision History
# Name                  Date                Description
# Parsa Jafaripour      11/03/2024          Created the second prototype of the matching algorithm. Using the threshold tactic and starting the compatibility score from 20.
# Parsa Jafaripour      11/04/2024          Updated to dynamically manage group mergers and handle non-preference members.

def calculate_compatibility(person1, person2, weights):
    """
    Calculate the compatibility score between two persons based on weighted mismatches.
    """
    score = 20  # Starting score
    for question, weight in weights.items():
        if person1.get(question) != person2.get(question):
            score -= weight
    return score

def average_group_score(group1, group2, weights):
    """
    Calculate average compatibility score between two groups, considering only those who filled out preferences.
    """
    scores = []
    for member1 in group1:
        for member2 in group2:
            if 'preferences_filled' in member1 and 'preferences_filled' in member2:
                score = calculate_compatibility(member1, member2, weights)
                scores.append(score)
    return sum(scores) / len(scores) if scores else 0

def match_and_merge_groups(groups, threshold=12):
    """
    Match groups of students to each other based on their average compatibility score.
    Merges groups or individuals into new blocks if compatible.
    """
    needs_accommodation, eligible_for_matching = filter_accommodations(groups)
    assign_accommodation_rooms(needs_accommodation)
    merged_blocks = []

    while eligible_for_matching:
        current_group = eligible_for_matching.pop(0)
        best_match = None
        best_score = threshold  # Start with threshold to ensure only suitable matches are considered
        for i, other_group in enumerate(eligible_for_matching):
            if any(member.get('preferences_filled') for member in other_group):  # Ensure there is at least one member with preferences
                avg_score = average_group_score(current_group, other_group, weights)
                if avg_score > best_score:
                    best_score = avg_score
                    best_match = i
        if best_match is not None:
            # Merge groups into a new block
            current_group.extend(eligible_for_matching.pop(best_match))
            merged_blocks.append(current_group)
        else:
            # If no suitable match found, append the current group as is
            merged_blocks.append(current_group)

    return merged_blocks

def filter_accommodations(groups):
    """
    Filter out groups needing special accommodations.
    """
    needs_accommodation = []
    other_groups = []
    for group in groups:
        if any(member.get("RequiresAccommodation") == "Yes" for member in group):
            needs_accommodation.append(group)
        else:
            other_groups.append(group)
    return needs_accommodation, other_groups

def assign_accommodation_rooms(groups):
    """
    Assign designated accommodation rooms to those requiring special conditions.
    """
    for group in groups:
        print(f"Assigned to accommodation room: Group starting with ID {group[0]['id']}")

# Sample groups for testing the matching algorithm
groups = [
    # Group 1: Three members, no special accommodations
    [
        {"id": "H123456789", "MorningPerson": "Yes", "Cleanliness": "Yes", "Social": "Yes", "Temperature": "Warm", "RequiresAccommodation": "No", "preferences_filled": True},
        {"id": "H123456790", "MorningPerson": "Yes", "Cleanliness": "No",  "Social": "Yes",  "Temperature": "Cool", "RequiresAccommodation": "No", "preferences_filled": True},
        {"id": "H123456791", "MorningPerson": "No",  "Cleanliness": "Yes", "Social": "Yes", "Temperature": "Warm", "RequiresAccommodation": "No", "preferences_filled": True}
    ],
    # Group 2: Single member, needs accommodation
    [
        {"id": "H987654321", "RequiresAccommodation": "Yes", "preferences_filled": False}
    ],
    # Group 3: Two members, no special accommodations
    [
        {"id": "H112233445", "MorningPerson": "No",  "Cleanliness": "No",  "Social": "Yes", "Temperature": "Warm", "RequiresAccommodation": "No", "preferences_filled": True},
        {"id": "H112233446", "MorningPerson": "Yes", "Cleanliness": "Yes", "Social": "Yes", "Temperature": "Warm", "RequiresAccommodation": "No", "preferences_filled": True}
    ],
    # Group 4: Two members, one without preferences
    [
        {"id": "H223344556", "MorningPerson": "No", "Cleanliness": "No", "Social": "No",  "Temperature": "Cool", "RequiresAccommodation": "No", "preferences_filled": True},
        {"id": "H334455667", "preferences_filled": False}  # This member does not participate in preference matching
    ]
]

# Weights for each question based on their importance
weights = {
    "MorningPerson": 6,  # Highest importance
    "Cleanliness": 4,
    "Social": 3,
    "Temperature": 3   # Least important
}

# Execute the matching algorithm with the sample data
matched_blocks = match_and_merge_groups(groups)
print("Final Matched Blocks:", matched_blocks)

