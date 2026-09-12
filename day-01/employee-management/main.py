class Employee:
    def __init__(self, emp_id: str, name: str, department: str, salary: float):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary


class EmployeeManager:
    def __init__(self):
        self.employees = {}

    def _render_table(self, records: dict):
        if not records:
            print("\nNo records found.")
            return
        print("\n" + "=" * 65)
        print(f"{'ID':<10} {'Name':<20} {'Department':<18} {'Salary':<12}")
        print("-" * 65)
        for emp_id, emp in records.items():
            print(f"{emp_id:<10} {emp.name:<20} {emp.department:<18} {emp.salary:<12.2f}")
        print("=" * 65)

    def add(self):
        print("\n--- Add Employee ---")
        emp_id = input("Enter Employee ID: ").strip()
        if not emp_id:
            print("Error: ID cannot be empty.")
            return
        if emp_id in self.employees:
            print(f"Error: Employee with ID '{emp_id}' already exists.")
            return

        name = input("Enter Name: ").strip()
        dept = input("Enter Department: ").strip()

        try:
            salary = float(input("Enter Salary: "))
            if salary < 0:
                print("Error: Salary cannot be negative.")
                return
        except ValueError:
            print("Error: Invalid numeric value for salary.")
            return

        self.employees[emp_id] = Employee(emp_id, name, dept, salary)
        print(f"Employee '{name}' added successfully.")

    def update(self):
        print("\n--- Update Employee ---")
        emp_id = input("Enter Employee ID to update: ").strip()
        if emp_id not in self.employees:
            print(f"Error: No employee found with ID '{emp_id}'.")
            return

        emp = self.employees[emp_id]
        print(f"Updating ID {emp_id} (Leave blank to keep current value)")

        new_name = input(f"New Name [{emp.name}]: ").strip()
        new_dept = input(f"New Department [{emp.department}]: ").strip()
        new_salary_str = input(f"New Salary [{emp.salary}]: ").strip()

        if new_name:
            emp.name = new_name
        if new_dept:
            emp.department = new_dept
        if new_salary_str:
            try:
                val = float(new_salary_str)
                if val < 0:
                    print("Error: Salary cannot be negative. Value kept unchanged.")
                else:
                    emp.salary = val
            except ValueError:
                print("Invalid input. Salary kept unchanged.")

        print(f"Employee '{emp_id}' updated successfully.")

    def delete(self):
        print("\n--- Delete Employee ---")
        emp_id = input("Enter Employee ID to delete: ").strip()
        if emp_id in self.employees:
            deleted = self.employees.pop(emp_id)
            print(f"Employee '{deleted.name}' (ID: {emp_id}) deleted.")
        else:
            print(f"Error: No employee found with ID '{emp_id}'.")

    def search(self):
        print("\n--- Search Employee ---")
        query = input("Search by ID or Name: ").strip().lower()
        matches = {
            emp_id: emp for emp_id, emp in self.employees.items()
            if query in emp_id.lower() or query in emp.name.lower()
        }
        self._render_table(matches)

    def list_all(self):
        print("\n--- All Employees ---")
        self._render_table(self.employees)

    def filter_by_department(self):
        print("\n--- Filter by Department ---")
        dept = input("Enter Department: ").strip().lower()
        filtered = {
            emp_id: emp for emp_id, emp in self.employees.items()
            if emp.department.lower() == dept
        }
        self._render_table(filtered)

    def show_highest_salary(self):
        print("\n--- Highest Salary ---")
        if not self.employees:
            print("No employee records available.")
            return
        top_id = max(self.employees, key=lambda k: self.employees[k].salary)
        self._render_table({top_id: self.employees[top_id]})

    def show_average_salary(self):
        print("\n--- Average Salary ---")
        if not self.employees:
            print("No employee records available.")
            return
        total = sum(emp.salary for emp in self.employees.values())
        avg = total / len(self.employees)
        print(f"Total Employees: {len(self.employees)}")
        print(f"Average Salary:  ${avg:,.2f}")


def main():
    manager = EmployeeManager()

    menu = {
        "1": manager.add,
        "2": manager.update,
        "3": manager.delete,
        "4": manager.search,
        "5": manager.list_all,
        "6": manager.filter_by_department,
        "7": manager.show_highest_salary,
        "8": manager.show_average_salary,
    }

    while True:
        print("\n=== EMPLOYEE MANAGEMENT SYSTEM ===")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. Search Employee")
        print("5. List All Employees")
        print("6. Filter by Department")
        print("7. Highest Paid Employee")
        print("8. Average Salary")
        print("9. Exit")

        choice = input("\nSelect an option (1-9): ").strip()

        if choice == "9":
            print("Exiting application.")
            break
        elif choice in menu:
            menu[choice]()
        else:
            print("Invalid selection. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
