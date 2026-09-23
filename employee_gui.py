import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ---------- MySQL Connection ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1182517@arya",
    database="employee_salary"
)

cursor = db.cursor()


# ---------- Functions ----------

def add_employee():
    name = name_entry.get().strip()
    salary = salary_entry.get().strip()

    if not name or not salary:
        messagebox.showwarning("Warning", "Please enter name and salary.")
        return

    try:
        salary = float(salary)

        sql = "INSERT INTO employees (name, salary) VALUES (%s, %s)"
        cursor.execute(sql, (name, salary))
        db.commit()

        messagebox.showinfo("Success", "Employee added successfully!")

        name_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)

        view_employees()

    except ValueError:
        messagebox.showerror("Error", "Salary must be a number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def view_employees():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    for employee in employees:
        table.insert(
            "",
            tk.END,
            values=(employee[0], employee[1], employee[2])
        )


def search_employee():
    employee_id = search_entry.get().strip()

    if not employee_id:
        messagebox.showwarning("Warning", "Enter an employee ID.")
        return

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee:
            for item in table.get_children():
                table.delete(item)

            table.insert(
                "",
                tk.END,
                values=(employee[0], employee[1], employee[2])
            )
        else:
            messagebox.showinfo("Result", "Employee not found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def update_salary():
    employee_id = search_entry.get().strip()
    new_salary = salary_entry.get().strip()

    if not employee_id or not new_salary:
        messagebox.showwarning(
            "Warning",
            "Enter Employee ID and new salary."
        )
        return

    try:
        new_salary = float(new_salary)

        cursor.execute(
            "UPDATE employees SET salary = %s WHERE id = %s",
            (new_salary, employee_id)
        )

        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success",
                "Salary updated successfully!"
            )
            view_employees()
        else:
            messagebox.showinfo("Result", "Employee not found.")

    except ValueError:
        messagebox.showerror("Error", "Salary must be a number.")


def delete_employee():
    employee_id = search_entry.get().strip()

    if not employee_id:
        messagebox.showwarning("Warning", "Enter Employee ID.")
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this employee?"
    )

    if answer:
        cursor.execute(
            "DELETE FROM employees WHERE id = %s",
            (employee_id,)
        )

        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success",
                "Employee deleted successfully!"
            )
            view_employees()
        else:
            messagebox.showinfo("Result", "Employee not found.")

def update_salary():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an employee first.")
        return

    employee = table.item(selected[0])["values"]
    employee_id = employee[0]

    new_salary = salary_entry.get()

    if new_salary == "":
        messagebox.showwarning("Warning", "Enter the new salary.")
        return

    try:
        new_salary = float(new_salary)

        cursor.execute(
            "UPDATE employees SET salary = %s WHERE id = %s",
            (new_salary, employee_id)
        )
        db.commit()

        messagebox.showinfo("Success", "Salary updated successfully!")
        salary_entry.delete(0, tk.END)
        view_employees()

    except ValueError:
        messagebox.showerror("Error", "Salary must be a number.")


def search_employee():
    name = name_entry.get()

    if name == "":
        messagebox.showwarning("Warning", "Enter employee name.")
        return

    for item in table.get_children():
        table.delete(item)

    cursor.execute(
        "SELECT * FROM employees WHERE name LIKE %s",
        ("%" + name + "%",)
    )

    employees = cursor.fetchall()

    for employee in employees:
        table.insert("", tk.END, values=employee) 

def salary_statistics():
    cursor.execute("""
        SELECT COUNT(*), SUM(salary), AVG(salary)
        FROM employees
    """)

    result = cursor.fetchone()

    total_employees = result[0]
    total_salary = result[1] or 0
    average_salary = result[2] or 0

    messagebox.showinfo(
        "Salary Statistics",
        f"Total Employees: {total_employees}\n"
        f"Total Salary: ₹{total_salary:.2f}\n"
        f"Average Salary: ₹{average_salary:.2f}"
    )


def salary_statistics():
    cursor.execute(
        "SELECT COUNT(*), SUM(salary), AVG(salary) FROM employees"
    )

    result = cursor.fetchone()

    count = result[0]
    total = result[1] or 0
    average = result[2] or 0

    messagebox.showinfo(
        "Salary Statistics",
        f"Total Employees: {count}\n"
        f"Total Salary: ₹{total:.2f}\n"
        f"Average Salary: ₹{average:.2f}"
    )


def sort_by_salary():
    for item in table.get_children():
        table.delete(item)

    cursor.execute(
        "SELECT * FROM employees ORDER BY salary DESC"
    )

    employees = cursor.fetchall()

    for employee in employees:
        table.insert(
            "",
            tk.END,
            values=(employee[0], employee[1], employee[2])
        )


def clear_fields():
    name_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    view_employees()


def close_app():
    cursor.close()
    db.close()
    root.destroy()


# ---------- GUI ----------

root = tk.Tk()
root.title("Employee Salary Management System")
root.geometry("850x600")


title = tk.Label(
    root,
    text="Employee Salary Management System",
    font=("Arial", 22, "bold")
)

title.pack(pady=15)


# Employee input section

input_frame = tk.Frame(root)
input_frame.pack(pady=10)


tk.Label(
    input_frame,
    text="Employee Name:"
).grid(row=0, column=0, padx=5, pady=5)

name_entry = tk.Entry(input_frame, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Salary:"
).grid(row=1, column=0, padx=5, pady=5)

salary_entry = tk.Entry(input_frame, width=25)
salary_entry.grid(row=1, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Employee ID:"
).grid(row=2, column=0, padx=5, pady=5)

search_entry = tk.Entry(input_frame, width=25)
search_entry.grid(row=2, column=1, padx=5, pady=5)


# Buttons

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Add Employee",
    command=add_employee,
    width=15
).grid(row=0, column=0, padx=5, pady=5)


tk.Button(
    button_frame,
    text="View Employees",
    command=view_employees,
    width=15
).grid(row=0, column=1, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Search",
    command=search_employee,
    width=15
).grid(row=0, column=2, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Update Salary",
    command=update_salary,
    width=15
).grid(row=1, column=0, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Delete",
    command=delete_employee,
    width=15
).grid(row=1, column=1, padx=5, pady=5)
tk.Button(
    button_frame,
    text="Update Salary",
    command=update_salary,
    width=15
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Search Employee",
    command=search_employee,
    width=15
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Show All",
    command=view_employees,
    width=15
).grid(row=1, column=2, padx=5, pady=5)
tk.Button(
    button_frame,
    text="Salary Statistics",
    command=salary_statistics,
    width=20
).grid(row=2, column=1, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Statistics",
    command=salary_statistics,
    width=15
).grid(row=1, column=2, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Sort by Salary",
    command=sort_by_salary,
    width=15
).grid(row=2, column=0, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=15
).grid(row=2, column=1, padx=5, pady=5)


tk.Button(
    button_frame,
    text="Exit",
    command=close_app,
    width=15
).grid(row=2, column=2, padx=5, pady=5)


# Employee table

table_frame = tk.Frame(root)
table_frame.pack(pady=15, fill="both", expand=True)


columns = ("ID", "Name", "Salary")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

table.heading("ID", text="ID")
table.heading("Name", text="Employee Name")
table.heading("Salary", text="Salary")

table.column("ID", width=80)
table.column("Name", width=300)
table.column("Salary", width=200)

table.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

table.configure(
    yscrollcommand=scrollbar.set
)


root.protocol("WM_DELETE_WINDOW", close_app)

view_employees()

root.mainloop()