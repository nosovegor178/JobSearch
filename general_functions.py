def gets_the_arithmetic_mean(numbers):
    numbers = [x for x in numbers if x]
    return float(sum(numbers)) / max(len(numbers), 1)


def predict_salary(salary_from, salary_to):
    if not salary_from:
        mid_salary = salary_to * 0.8
    elif not salary_to:
        mid_salary = salary_from * 1.2
    else:
        salary = [salary_from, salary_to]
        mid_salary = gets_the_arithmetic_mean(salary)
    return mid_salary