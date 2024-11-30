# REVISION HISTORY
# Parsa     10/20/2024  Created the main script to execute the matching algorithm, including initializing dorms and processing accessible students.
# Parsa     10/30/2024  Defined weights and threshold for compatibility calculations.
# Parsa     11/05/2024  Updated the main function to pass weights and threshold to matching functions, ensuring compatibility checks are performed.
# Parsa     11/07/2024  Adjusted the assignment flow to process students' dorm choices in sequence and handle waitlisted students.
# Parsa     11/12/2024  Added validation of assignments and generation of occupancy and waitlist reports.

from Matching_Prototype import (
    create_pools, get_initialized_dorms, assign_accessible_rooms, match_students_in_pool,
    reassign_to_fallback_choices, validate_assignments, generate_reports
)
from Data import get_students

# define weights for compatibility criteria
weights = {
    "Time": 5,
    "Organization": 3,
    "Personality": 4,
    "Temperature": 2
}

def main():
    # initialize a waitlist to store unmatched students/blocks
    waitlist = []

    # step 1: get initialized dorms and student data
    dorms = get_initialized_dorms()

    # step 2: process and assign accessible students
    accessible_students = [
        s.to_dict() for s in get_students() if s.to_dict().get('Accomodations') == "Yes, I require accommodations"
    ]
    assign_accessible_rooms(dorms, accessible_students)

    # initialize assigned_students set
    global assigned_students
    assigned_students = set()

    # define the compatibility threshold
    threshold = 12  # adjust as needed

    # we will process first choices, then second, then third
    for choice_level in ["first_choice", "second_choice", "third_choice"]:
        # re-create pools excluding assigned students
        pools = create_pools()
        unmatched_entities = []
        for dorm_name, choices in pools.items():
            dorm = next((d for d in dorms if d.name == dorm_name), None)
            if dorm:
                pool = choices[choice_level]
                result = match_students_in_pool(pool, dorm, weights, waitlist, threshold)
                unmatched_entities.extend(result)

    # step 9: final validation and reporting
    issues = validate_assignments(dorms, waitlist)
    generate_reports(dorms, waitlist)
    print(issues)

if __name__ == "__main__":
    main()
