import logging
import copy

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s- %(message)s")
# logging.disable(logging.CRITICAL)


# add last column which is max of special exam or (mean score of final exams)
def add_last_column(department_to_change, test_index_list):
    # print(department_to_change)
    for index in range(len(department_to_change)):
        to_add = 0
        for test in test_index_list:
            to_add += int(department_to_change[index][test])
        to_add /= len(test_index_list)
        to_add = max(float(to_add), float(department_to_change[index][6]))
        department_to_change[index].append(to_add)


# add people to department
def add_people_department(department_not_changed, departments_add, limit, tests_indexes_f):
    for department_name in department_not_changed:
        add_last_column(department_not_changed[department_name], tests_indexes_f[department_name])

        # sort department according to last column (descending) and according to last name [0], first name[1]
        department_not_changed[department_name].sort(
            key=lambda x: (-float(x[len(department_not_changed[department_name]) - 1]), x[0], x[1]))
        # if sum of people in departments already added and to be added is less than limit -> add both
        if len(department_not_changed[department_name]) + len(departments_add[department_name]) < limit:
            departments_add[department_name].extend(department_not_changed[department_name])
            department_not_changed[department_name] = []
        # add to department_add from department_not_changed people up to the limit
        else:
            departments_add[department_name].extend(
                department_not_changed[department_name][:limit - len(departments_add[department_name])])

            del department_not_changed[department_name][:limit - len(departments_add[department_name])]


# print single department
def print_department(department_print, test_id):
    for person_print in department_print:
        print("{} {} {}".format(person_print[0], person_print[1], float(person_print[test_id])))


# print all departments
def print_department_all(departments_print):
    for department_single_print in departments_print:
        test_id = 10
        departments_print[department_single_print].sort(key=lambda x: (-float(x[test_id]), x[0], x[1]))
        print(department_single_print)
        print_department(departments_print[department_single_print], test_id)
        print()


# save departments to files
def save_departments(departments_save):
    test_id = 10
    for department_single_save in departments_save:

        departments_save[department_single_save].sort(key=lambda x: (-float(x[test_id]), x[0], x[1]))
        with open(department_single_save + ".txt", "w") as file:
            for person_save in departments_save[department_single_save]:
                file.write("{} {} {}\n".format(person_save[0], person_save[1], float(person_save[test_id])))


if __name__ == '__main__':
    logging.debug("Start of program")

    # list of departments which will be used for coping
    departments_not_modified = {"Biotech": [], "Chemistry": [], "Engineering": [],
                                "Mathematics": [], "Physics": []}
    departments = copy.deepcopy(departments_not_modified)

    # indexes of tests for each department
    tests_indexes = {"Biotech": [2, 3], "Chemistry": [3], "Engineering": [4, 5], "Mathematics": [4], "Physics": [2, 4]}
    people_limit = int(input())
    filename = "applicant_list_7.txt"

    # order of students departments priorities
    order_list = (7, 8, 9)
    for i in order_list:
        departments_previous = copy.deepcopy(departments_not_modified)
        with open(filename) as f:
            for line in f:
                # if person is already added to department - skip
                if any(line.split()[0] in person_search and line.split()[1] in person_search
                       for department_search in departments.values() for person_search in department_search):
                    # print(i)
                    continue
                # if person is not qualified. add him to temporary departments
                departments_previous[line.split()[i]].append(line.split())

        add_people_department(departments_previous, departments, people_limit, tests_indexes)

    save_departments(departments)
    logging.debug("End of program")
