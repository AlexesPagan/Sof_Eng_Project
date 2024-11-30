# REVISION HISTORY
# Parsa     10/20/2024  Set up initial imports and global variables for the matching algorithm.
# Parsa     10/30/2024  Implemented the calculate_compatibility function to compute compatibility scores between students based on their preferences and assigned weights to each criterion.
# Parsa     11/05/2024  Updated the assign_block_to_room function to skip compatibility checks within blocks (among roommates who have chosen to live together), assuming they are compatible by choice. Adjusted the function to perform compatibility checks between blocks and existing occupants in a room when assigning blocks to rooms that already have occupants.
# Parsa     11/07/2024  Modified the assign_room_to_student function to consider partially occupied rooms when assigning individual students. Implemented compatibility checks between the student and existing occupants in a room before assigning the student to that room.
# Parsa     11/07/2024  Modified the calculate_compatibility function to handle missing data gracefully by skipping over any preferences where data is missing rather than reducing the compatibility score unfairly.
# Parsa     11/12/2024  Updated the create_pools function to include default data in placeholders for roommates who did not submit applications, ensuring accurate compatibility checks.
# Parsa     11/18/2024  Updated function signatures for assign_block_to_room() and assign_room_to_student() to accept weights and threshold parameters for compatibility calculations.
# Parsa     11/24/2024  Added checks to prevent errors due to missing data in placeholders. Adjusted the matching logic to handle edge cases, such as when no compatible rooms are available.


from Data import Dorm, get_responses, trim_response_data
from Data import get_students_by_dorm_choice
from Data import db, firestore

assigned_students = set()

def assign_accessible_rooms(dorms, accessible_students):
    """
    Assign accessible students to designated accessible rooms.
    """
    accessible_dorm_names = {"Moonlight Hall", "Aurora Hall", "Solstice Hall"}
    accessible_room_numbers = [f"Rm{i:02}" for i in range(1, 6)]  # rooms Rm01 to Rm05

    for student in accessible_students:
        dorm_choices = [
            student.get("1stRA_dorm_choice"),
            student.get("2ndRA_dorm_choice"),
            student.get("3rdRA_dorm_choice")
        ]
        assigned = False

        for dorm_name in dorm_choices:
            if dorm_name in accessible_dorm_names:
                dorm = next((d for d in dorms if d.name == dorm_name), None)
                if dorm:
                    for i, room in enumerate(dorm.rooms):
                        if room.room_number in accessible_room_numbers and not room.is_occupied and room.is_accessible:
                            try:
                                room.add_student(student, dorm_name=dorm.name, room_index=i)
                                assigned_students.add(student['ID'])
                                print(f"Assigned {student['ID']} to accessible room {room.room_number} in {dorm.name}")
                                assigned = True
                                break
                            except ValueError as e:
                                print(f"Error assigning accessible student: {e}")
                                continue
                    if assigned:
                        break
        if not assigned:
            print(f"Could not assign accessible student {student['ID']} to any of their choices.")



#fetch the initialized dorms from firestore
def get_initialized_dorms():
    """
    Retrieve all initialized dorms from Firestore.
    """
    dorm_docs = db.collection('dorms').stream()
    dorms = []
    for doc in dorm_docs:
        dorm_data = doc.to_dict()
        dorm = Dorm(dorm_data['name'], dorm_data['housing_style'], dorm_data['capacity'])

        # load room data into the Dorm objects
        for room_data in dorm_data['rooms']:
            room = Dorm.Room(room_data['room_number'], room_data['capacity'],
                             is_occupied=room_data['is_occupied'],
                             is_accessible=room_data['is_accessible'])
            dorm.add_room(room)
        dorms.append(dorm)
    return dorms

def create_pools():
    """
    Create pools of students for each dorm based on their dorm choices, excluding already assigned students,
    and grouping students into blocks based on roommate IDs.
    """
    def exclude_assigned(students):
        return [s for s in students if s['ID'] not in assigned_students]

    def group_students(students, student_dict):
        blocks = []
        single_students = []
        processed_ids = set()

        for student in students:
            if student['ID'] in processed_ids:
                continue  # student already processed
            roommate_ids = student.get('roommate_ids', [])
            if roommate_ids:
                block = [student]
                processed_ids.add(student['ID'])
                for roommate_id in roommate_ids:
                    if roommate_id in processed_ids:
                        continue  # roommate already processed
                    roommate = student_dict.get(roommate_id)
                    if roommate:
                        block.append(roommate)
                        processed_ids.add(roommate_id)
                    else:
                        # roommate did not submit form response; create a placeholder
                        roommate_placeholder = {
                            'ID': roommate_id,
                            'Accomodations': 'No, I do not require accommodations',
                            'roommate_ids': [],
                            # setting default answers matching the inviting student's preferences
                            'Personality': student.get('Personality'),
                            'Time': student.get('Time'),
                            'Activity': student.get('Activity'),
                            'Temperature': student.get('Temperature'),
                            'Organization': student.get('Organization'),
                            'House_Style': student.get('House_Style')
                        }
                        block.append(roommate_placeholder)
                        processed_ids.add(roommate_id)
                blocks.append(block)
            else:
                single_students.append(student)
                processed_ids.add(student['ID'])
        return blocks + single_students  # blocks first, then singles

    pools = {}

    # list of all dorms
    dorm_names = ["Moonlight Hall", "Comet Hall", "Nebula Hall", "Aurora Hall", "Solstice Hall", "Eclipse Hall"]

    for dorm_name in dorm_names:
        # getting students who chose this dorm as their first choice
        first_choice_students, student_dict = get_students_by_dorm_choice(dorm_name, "1st")
        first_choice_students = exclude_assigned(first_choice_students)
        first_choice_grouped = group_students(first_choice_students, student_dict)

        # similarly for second and third choices
        second_choice_students, _ = get_students_by_dorm_choice(dorm_name, "2nd")
        second_choice_students = exclude_assigned(second_choice_students)
        second_choice_grouped = group_students(second_choice_students, student_dict)

        third_choice_students, _ = get_students_by_dorm_choice(dorm_name, "3rd")
        third_choice_students = exclude_assigned(third_choice_students)
        third_choice_grouped = group_students(third_choice_students, student_dict)

        pools[dorm_name] = {
            "first_choice": first_choice_grouped,
            "second_choice": second_choice_grouped,
            "third_choice": third_choice_grouped,
        }

    return pools

def assign_students_in_pools(pools, dorms):
    """
    Match and assign students to rooms within each pool, excluding already assigned students.
    """
    for dorm_name, choices in pools.items():
        dorm = next((d for d in dorms if d.name == dorm_name), None)
        if dorm:
            # process each choice level in a first-come, first-serve manner
            for choice_level in ["first_choice", "second_choice", "third_choice"]:
                entities = choices[choice_level]
                # exclude already assigned students or blocks
                entities = [
                    e for e in entities if not any(
                        s['ID'] in assigned_students for s in (e if isinstance(e, list) else [e])
                    )
                ]
                for entity in entities:
                    if isinstance(entity, list):  # it's a block
                        assigned = assign_block_to_room(dorm, entity)
                        if assigned:
                            print(f"Assigned block {[s['ID'] for s in entity]} to room in {dorm_name}")
                        else:
                            print(f"No available room for block {[s['ID'] for s in entity]} in {dorm_name}")
                    else:  # single student
                        assigned = assign_room_to_student(dorm, entity)
                        if assigned:
                            print(f"Assigned {entity['ID']} to room in {dorm_name}")
                        else:
                            print(f"No available room for {entity['ID']} in {dorm_name}")


def assign_room_to_student(dorm, student, weights, threshold):
    """
    Assign a student to a room in the given dorm based on their preferences,
    including `RA` choices if the student requires accommodations.
    """
    if student['ID'] in assigned_students:
        return False  # student already assigned

    requires_accommodation = student.get("Accomodations") == "Yes, I require accommodations"

    #mapping of room type strings to capacities
    room_type_to_capacity = {
        'Single': 1,
        'Double': 2,
        'Triple': 3,
        'Quad': 4,
        'Quint': 5
    }

    if requires_accommodation:
        room_type_preferences = ['Single']  # accessible rooms are single rooms
    else:
        room_type_preferences = []
        if dorm.housing_style == "Suite":
            room_choices = [
                student.get("1stRSS_room_choice"),
                student.get("2ndRSS_room_choice"),
                student.get("3rdRSS_room_choice")
            ]
        else:
            room_choices = [
                student.get("1stRST_room_choice"),
                student.get("2ndRST_room_choice"),
                student.get("3rdRST_room_choice")
            ]
        for choice in room_choices:
            if choice:
                room_type_preferences.append(choice)

    for room_type in room_type_preferences:
        capacity_required = room_type_to_capacity.get(room_type)
        if capacity_required is None:
            print(f"Unrecognized room type '{room_type}' for student {student['ID']}. Skipping this preference.")
            continue  #skipping if room_type is not recognized
        for i, room in enumerate(dorm.rooms):
            #skipping accessible rooms if student doesn't require accommodation
            if not requires_accommodation and room.is_accessible:
                continue
            # for accessible students, ensure room is accessible
            if requires_accommodation and not room.is_accessible:
                continue
            if room.capacity == capacity_required and len(room.students) < room.capacity:
                # check compatibility if room is partially occupied
                compatible = True
                for occupant in room.students:
                    score = calculate_compatibility(student, occupant, weights)
                    if score < threshold:
                        compatible = False
                        print(f"Student {student['ID']} is incompatible with occupant {occupant['ID']} (score: {score}) in room {room.room_number}")
                        break
                if not compatible:
                    continue  # try next room
                try:
                    room.add_student(student, dorm_name=dorm.name, room_index=i)
                    assigned_students.add(student['ID'])
                    print(f"Assigned student {student['ID']} to room {room.room_number} in dorm {dorm.name}.")
                    return True
                except ValueError as e:
                    print(f"Error assigning student: {e}")
                    continue
    return False


def match_students_in_pool(pool, dorm, weights, waitlist, threshold=12):
    """
    Match students or blocks in a pool based on compatibility.
    """
    unmatched_entities = []
    assigned_indices = []

    for index, entity in enumerate(pool):
        if isinstance(entity, list):  #if it's a block
            # check if any student in the block is already assigned
            if any(s['ID'] in assigned_students for s in entity):
                continue  # skip this block
            assigned = assign_block_to_room(dorm, entity, weights, threshold)
            if assigned:
                assigned_indices.append(index)
            else:
                unmatched_entities.append(entity)
        else:  # single student
            if entity['ID'] in assigned_students:
                continue  #skip already assigned student
            assigned = assign_room_to_student(dorm, entity, weights, threshold)
            if assigned:
                assigned_indices.append(index)
            else:
                unmatched_entities.append(entity)

    # remove assigned entities from the pool
    for index in sorted(assigned_indices, reverse=True):
        del pool[index]

    return unmatched_entities


def assign_to_room(dorm, students, waitlist):
    """
    Assign a pair or block of students to an available room.
    """
    block_size = len(students)  # total number of students in the block
    for i, room in enumerate(dorm.rooms):
        if not room.is_occupied and room.capacity >= block_size:
            try:
                for student in students:
                    room.add_student(student, dorm_name=dorm.name, room_index=i)  # ensure block assignment
                    assigned_students.add(student['ID'])  # track assigned students globally
                print(f"Assigned block {[s['ID'] for s in students]} to room {room.room_number} in {dorm.name}")
                return True
            except ValueError as e:
                print(f"Error assigning student block: {e}")
    #add the block to the waitlist if no room is available
    waitlist.append({
        "students": students,
        "dorm": dorm.name
    })
    print(f"No available room found for block {[s['ID'] for s in students]}. Added to waitlist.")
    return False

def calculate_compatibility(person1, person2, weights):
    """
    Calculate compatibility score based on weighted preferences.
    """
    score = 20  # The starting score
    for question, weight in weights.items():
        answer1 = person1.get(question)
        answer2 = person2.get(question)
        if answer1 is None or answer2 is None:
            continue  # skip this question if data is missing
        if answer1 != answer2:
            score -= weight
    return score


def average_group_score(group1, group2, weights):
    """
    Calculate average compatibility between two groups.
    """
    scores = []
    for member1 in group1:
        for member2 in group2:
            score = calculate_compatibility(member1, member2, weights)
            scores.append(score)
    return sum(scores) / len(scores) if scores else 0

def match_and_assign_rooms(pools, dorms, threshold=12):
    """
    Match students and assign them to rooms based on compatibility.
    """
    for dorm_name, choices in pools.items():
        dorm = next((d for d in dorms if d.name == dorm_name), None)
        if dorm:
            for choice_level in ["first_choice", "second_choice", "third_choice"]:
                students = choices[choice_level]
                for student in students:
                    assigned = assign_room_with_match(dorm, student, threshold)
                    if not assigned:
                        print(f"No suitable match found for {student['ID']} in {dorm_name}")

def assign_room_with_match(dorm, student, threshold, weights):
    """
    Attempt to assign a student to a room based on compatibility.
    """
    for room in dorm.rooms:
        if not room.is_occupied:
            for occupant in room.students:
                compatibility = calculate_compatibility(student, occupant, weights)
                if compatibility >= threshold:
                    room.add_student(student)
                    return True
    return False

def assign_block_to_room(dorm, block, weights, threshold):
    """
    Assign a block of students to a room in the given dorm, considering their room type preferences.
    """
    block_size = len(block)
    first_student = block[0]

    requires_accommodation = any(s.get("Accomodations") == "Yes, I require accommodations" for s in block)

    #mapping of room type strings to capacities
    room_type_to_capacity = {
        'Single': 1,
        'Double': 2,
        'Triple': 3,
        'Quad': 4,
        'Quint': 5
    }

    #get room type preferences from the first student
    if requires_accommodation:
        room_type_preferences = ['Single']  # accessible rooms are single rooms
    else:
        room_type_preferences = []
        if dorm.housing_style == "Suite":
            room_choices = [
                first_student.get("1stRSS_room_choice"),
                first_student.get("2ndRSS_room_choice"),
                first_student.get("3rdRSS_room_choice")
            ]
        else:
            room_choices = [
                first_student.get("1stRST_room_choice"),
                first_student.get("2ndRST_room_choice"),
                first_student.get("3rdRST_room_choice")
            ]
        for choice in room_choices:
            if choice:
                room_type_preferences.append(choice)

    #skip compatibility checks within the block
    #we assume students in the block have chosen to live together and are compatible

    for room_type in room_type_preferences:
        capacity_required = room_type_to_capacity.get(room_type)
        if capacity_required is None:
            print(f"Unrecognized room type '{room_type}' for block starting with student {first_student['ID']}. Skipping this preference.")
            continue  # skipping if room_type is not recognized
        if capacity_required < block_size:
            continue  # room type capacity less than block size, skip
        for i, room in enumerate(dorm.rooms):
            if room.is_occupied:
                continue  # skip occupied rooms

            if room.capacity != capacity_required:
                continue  # room capacity doesn't match

            # check compatibility with existing occupants (if there is any)
            compatible = True
            for occupant in room.students:
                for student in block:
                    score = calculate_compatibility(student, occupant, weights)
                    if score < threshold:
                        compatible = False
                        print(f"Block {[s['ID'] for s in block]} is incompatible with occupant {occupant['ID']} (score: {score})")
                        break
                if not compatible:
                    break

            if not compatible:
                continue  # try next room

            # assign block to room
            try:
                for student in block:
                    room.add_student(student, dorm_name=dorm.name, room_index=i)
                    assigned_students.add(student['ID'])  # mark as assigned
                print(f"Assigned block {[s['ID'] for s in block]} to room {room.room_number} in {dorm.name}")
                return True
            except ValueError as e:
                print(f"Error assigning block: {e}")
        # if no exact match found, try rooms with larger capacity
        for i, room in enumerate(dorm.rooms):
            if room.is_occupied:
                continue  # skip occupied rooms

            if room.capacity < block_size:
                continue  # room capacity too small

            # skip accessible rooms if block doesn't require accommodation
            if not requires_accommodation and room.is_accessible:
                continue
            # for blocks requiring accommodations, ensure room is accessible
            if requires_accommodation and not room.is_accessible:
                continue

            # check compatibility with existing occupants (if any)
            compatible = True
            for occupant in room.students:
                for student in block:
                    score = calculate_compatibility(student, occupant, weights)
                    if score < threshold:
                        compatible = False
                        print(f"Block {[s['ID'] for s in block]} is incompatible with occupant {occupant['ID']} (score: {score})")
                        break
                if not compatible:
                    break

            if not compatible:
                continue  # try next room

            # assign block to room
            try:
                for student in block:
                    room.add_student(student, dorm_name=dorm.name, room_index=i)
                    assigned_students.add(student['ID'])  # Mark as assigned
                print(f"Assigned block {[s['ID'] for s in block]} to room {room.room_number} in {dorm.name}")
                return True
            except ValueError as e:
                print(f"Error assigning block: {e}")

    print(f"No suitable room found for block {[s['ID'] for s in block]} in {dorm.name}")
    return False


def reassign_to_fallback_choices(unmatched_entities, pools, dorms, weights, waitlist, threshold=12):
    """
    Reassign unmatched students or blocks to their fallback dorm choices (second or third choice).
    """
    for entity in unmatched_entities:
        # get second and third dorm choices for the entity
        second_choice = entity.get("second_dorm_choice")
        third_choice = entity.get("third_dorm_choice")

        for choice in [second_choice, third_choice]:
            if choice and choice in pools:
                print(f"Attempting reassignment of {entity['ID']} to {choice}")

                # get the fallback dorm and its pool
                pool = pools[choice]["first_choice"]
                dorm = next((d for d in dorms if d.name == choice), None)

                # add the entity to the pool and try matching
                if dorm:
                    pool.append(entity)
                    result = match_students_in_pool(pool, dorm, weights, threshold)

                    # check if the entity was successfully assigned
                    if entity not in pool:
                        print(f"{entity['ID']} successfully reassigned to {choice}")
                        break  # Exit fallback reassignment loop

        else:
            # if no match was found, log to waitlist
            print(f"{entity['ID']} could not be assigned to any fallback dorm. Adding to waitlist.")
            waitlist.append({
                "ID": entity["ID"],
                "second_choice": second_choice,
                "third_choice": third_choice
            })

def validate_assignments(dorms, waitlist):
    """
    Validate room assignments and waitlist.
    """
    issues = []

    for dorm in dorms:
        for room in dorm.rooms:
            if len(room.students) > room.capacity:
                issues.append({
                    "dorm": dorm.name,
                    "room": room.room_number,
                    "students": [s["ID"] for s in room.students],
                    "message": "Room over-occupied!"
                })

    if not issues:
        print("Validation passed: All assignments are within capacity.")
    else:
        print("Validation issues found:")
        for issue in issues:
            print(issue)

    print(f"Waitlist contains {len(waitlist)} students/blocks.")
    return issues

def generate_reports(dorms, waitlist):
    """
    Generate and print reports for room assignments and waitlist.
    """
    print("\n--- Occupancy Report ---")
    for dorm in dorms:
        print(f"Dorm: {dorm.name}")
        for room in dorm.rooms:
            print(f"  Room {room.room_number} - Occupied: {len(room.students)}/{room.capacity}")
            print(f"    Students: {[s['ID'] for s in room.students]}")

    print("\n--- Waitlist Report ---")
    if waitlist:
        print(f"{len(waitlist)} students/blocks are waitlisted:")
        for student in waitlist:
            print(f"  ID: {student['ID']} - Second Choice: {student['second_choice']}, Third Choice: {student['third_choice']}")
    else:
        print("No students/blocks are waitlisted.")
