import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1182517@arya",
    database="employee_salary"
)

cursor = db.cursor()

def add_employee():
    name = input("Enter employee name: ")
    salary = float(input("Enter salary: "))

    sql = "INSERT INTO employees (name, salary) VALUES (%s, %s)"

    try:
        cursor.execute(sql, (name, salary))
        db.commit()
        print("Employee added successfully!")

    except mysql.connector.Error as err:
        print("Error adding employee:", err)

def view_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    print("\n--- Employees ---")

    for employee in employees:
        print("ID:", employee[0],
              "| Name:", employee[1],
              "| Salary:", employee[2])


def update_salary():
    employee_id = int(input("Enter employee ID: "))
    new_salary = float(input("Enter new salary: "))

    sql = "UPDATE employees SET salary = %s WHERE id = %s"
    cursor.execute(sql, (new_salary, employee_id))
    db.commit()

    if cursor.rowcount > 0:
        print("Salary updated successfully!")
    else:
        print("Employee ID not found!")


def delete_employee():
    employee_id = int(input("Enter employee ID: "))

    sql = "DELETE FROM employees WHERE id = %s"
    cursor.execute(sql, (employee_id,))
    db.commit()

    if cursor.rowcount > 0:
        print("Employee deleted successfully!")
    else:
        print("Employee ID not found!")

def search_employee():
    employee_id = int(input("Enter employee ID: "))

    sql = "SELECT * FROM employees WHERE id = %s"
    cursor.execute(sql, (employee_id,))
    employee = cursor.fetchone()

    if employee:
        print("\nEmployee Found!")
        print("ID:", employee[0])
        print("Name:", employee[1])
        print("Salary:", employee[2])
    else:
        print("Employee not found!")

def salary_statistics():
    cursor.execute("SELECT COUNT(*), SUM(salary), AVG(salary) FROM employees")
    result = cursor.fetchone()

    count = result[0]
    total = result[1]
    average = result[2]

    print("\n===== Salary Statistics =====")
    print("Total Employees:", count)
    print("Total Salary:", total)
    print("Average Salary:", average)

def sort_by_salary():
    cursor.execute("SELECT * FROM employees ORDER BY salary DESC")
    employees = cursor.fetchall()

    print("\n===== Employees Sorted by Salary =====")

    for employee in employees:
        print("ID:", employee[0])
        print("Name:", employee[1])
        print("Salary:", employee[2])
        print("----------------------")

    employee = cursor.fetchone()

    if employee:
        print("\nEmployee Found!")
        print("ID:", employee[0])
        print("Name:", employee[1])
        print("Salary:", employee[2])
    else:
        print("Employee not found!")


while True:
    print("\n===== Employee Salary Management =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Update Salary")
    print("4. Delete Employee")
    print("5. Search Employee")
    print("6. Salary Statistics")
    print("7. Sort by Salary")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        update_salary()

    elif choice == "4":
        delete_employee()

    elif choice == "5":
        search_employee()
    elif choice == "6":
        salary_statistics()
        break
    elif choice == "7":
        sort_by_salary()
    elif choice == "8":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")

cursor.close()
db.close()