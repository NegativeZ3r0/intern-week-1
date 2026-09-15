import csv
import os
import statistics


class ManagementSystemError(Exception):
    """Base exception class for system-specific errors."""
    pass


class RecordNotFoundError(ManagementSystemError):
    pass


class DuplicateRecordError(ManagementSystemError):
    pass


class ValidationError(ManagementSystemError):
    pass


class EmployeeManager:
    FIELDNAMES = ["id", "name", "department", "role", "salary", "experience"]

    def __init__(self, filepath: str = "employees.csv"):
        self.filepath = filepath
        self.records = []
        self._initialize_storage()
        self.load_data()

    def _initialize_storage(self) -> None:
        """Create the CSV file with headers if it does not already exist."""
        try:
            if not os.path.exists(self.filepath):
                with open(self.filepath, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                    writer.writeheader()
        except OSError as e:
            raise ManagementSystemError(f"Failed to initialize file '{self.filepath}': {e}")

    def load_data(self) -> None:
        """Load and parse records from the CSV file."""
        self.records = []
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for line_num, row in enumerate(reader, start=2):
                    try:
                        self.records.append({
                            "id": str(row["id"]).strip(),
                            "name": str(row["name"]).strip(),
                            "department": str(row["department"]).strip(),
                            "role": str(row["role"]).strip(),
                            "salary": float(row["salary"]),
                            "experience": int(row["experience"]),
                        })
                    except (ValueError, KeyError) as e:
                        print(f"[Warning] Skipping malformed row {line_num}: {e}")
        except PermissionError:
            raise ManagementSystemError(f"Permission denied when reading '{self.filepath}'.")
        except OSError as e:
            raise ManagementSystemError(f"Error reading '{self.filepath}': {e}")

    def save_data(self) -> None:
        """Persist current in-memory records to the CSV file atomically."""
        temp_file = f"{self.filepath}.tmp"
        try:
            with open(temp_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows(self.records)
            os.replace(temp_file, self.filepath)
        except (OSError, PermissionError) as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise ManagementSystemError(f"Failed to save data to '{self.filepath}': {e}")

    # --- Core Operations ---

    def add_record(self, emp_id: str, name: str, dept: str, role: str, salary: float, exp: int) -> None:
        """Add a new employee record with input validation."""
        emp_id = str(emp_id).strip()
        if not emp_id or not name.strip():
            raise ValidationError("ID and Name cannot be empty.")
        if any(r["id"] == emp_id for r in self.records):
            raise DuplicateRecordError(f"Employee ID '{emp_id}' already exists.")
        if salary < 0:
            raise ValidationError("Salary must be a non-negative number.")
        if exp < 0:
            raise ValidationError("Years of experience cannot be negative.")

        record = {
            "id": emp_id,
            "name": name.strip(),
            "department": dept.strip().title(),
            "role": role.strip().title(),
            "salary": float(salary),
            "experience": int(exp),
        }
        self.records.append(record)
        self.save_data()

    def update_record(self, emp_id: str, **kwargs) -> dict:
        """Update specified fields for an existing employee."""
        record = self._find_by_id(emp_id)

        for key, value in kwargs.items():
            if value is None or key not in self.FIELDNAMES or key == "id":
                continue

            if key == "salary":
                val = float(value)
                if val < 0:
                    raise ValidationError("Salary cannot be negative.")
                record[key] = val
            elif key == "experience":
                val = int(value)
                if val < 0:
                    raise ValidationError("Experience cannot be negative.")
                record[key] = val
            else:
                str_val = str(value).strip()
                if not str_val:
                    raise ValidationError(f"{key.capitalize()} cannot be empty.")
                record[key] = str_val.title() if key in ["department", "role"] else str_val

        self.save_data()
        return record

    def delete_record(self, emp_id: str) -> dict:
        """Delete an employee record by ID."""
        record = self._find_by_id(emp_id)
        self.records.remove(record)
        self.save_data()
        return record

    def search(self, query: str) -> list:
        """Search records matching ID, name, department, or role (case-insensitive)."""
        q = query.strip().lower()
        if not q:
            return self.records.copy()
        return [
            r for r in self.records
            if q in r["id"].lower()
            or q in r["name"].lower()
            or q in r["department"].lower()
            or q in r["role"].lower()
        ]

    def filter_records(self, department: str = None, min_salary: float = None,
                       max_salary: float = None, min_exp: int = None) -> list:
        """Filter records by department, salary range, and minimum experience."""
        results = self.records
        if department:
            dept_lower = department.strip().lower()
            results = [r for r in results if r["department"].lower() == dept_lower]
        if min_salary is not None:
            results = [r for r in results if r["salary"] >= min_salary]
        if max_salary is not None:
            results = [r for r in results if r["salary"] <= max_salary]
        if min_exp is not None:
            results = [r for r in results if r["experience"] >= min_exp]
        return results

    def sort_records(self, by: str = "id", descending: bool = False) -> list:
        """Sort records by any designated attribute."""
        if by not in self.FIELDNAMES:
            raise ValidationError(f"Invalid sort field: '{by}'. Allowed: {', '.join(self.FIELDNAMES)}")
        return sorted(self.records, key=lambda x: x[by], reverse=descending)

    def get_statistics(self) -> dict:
        """Calculate statistical summaries across numeric and categorical fields."""
        if not self.records:
            return {"total_count": 0}

        salaries = [r["salary"] for r in self.records]
        experiences = [r["experience"] for r in self.records]

        # Department distribution
        dept_counts = {}
        for r in self.records:
            dept_counts[r["department"]] = dept_counts.get(r["department"], 0) + 1

        return {
            "total_count": len(self.records),
            "total_payroll": sum(salaries),
            "mean_salary": round(statistics.mean(salaries), 2),
            "median_salary": round(statistics.median(salaries), 2),
            "min_salary": min(salaries),
            "max_salary": max(salaries),
            "mean_experience": round(statistics.mean(experiences), 1),
            "department_headcounts": dept_counts,
        }

    def _find_by_id(self, emp_id: str) -> dict:
        emp_id = str(emp_id).strip()
        for r in self.records:
            if r["id"] == emp_id:
                return r
        raise RecordNotFoundError(f"Record with ID '{emp_id}' was not found.")


# --- Display Helpers & CLI ---

def display_table(records: list) -> None:
    """Print records in a formatted ASCII table."""
    if not records:
        print("\nNo records found.")
        return

    header = f"{'ID':<8} | {'Name':<20} | {'Department':<15} | {'Role':<18} | {'Salary':<12} | {'Exp (Yrs)':<10}"
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for r in records:
        print(f"{r['id']:<8} | {r['name']:<20} | {r['department']:<15} | {r['role']:<18} | {r['salary']:<12.2f} | {r['experience']:<10}")
    print("-" * len(header))


def prompt_float(prompt_text: str, allow_blank: bool = False):
    while True:
        val = input(prompt_text).strip()
        if allow_blank and not val:
            return None
        try:
            return float(val)
        except ValueError:
            print("Invalid input: Please enter a valid decimal number.")


def prompt_int(prompt_text: str, allow_blank: bool = False):
    while True:
        val = input(prompt_text).strip()
        if allow_blank and not val:
            return None
        try:
            return int(val)
        except ValueError:
            print("Invalid input: Please enter a valid whole number.")


def main():
    manager = EmployeeManager()

    while True:
        print("\n=== Employee Management System ===")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. Search Employees")
        print("5. Filter Employees")
        print("6. Sort Employees")
        print("7. View Statistics")
        print("8. View All Records")
        print("9. Exit")

        choice = input("Select an option (1-9): ").strip()

        try:
            if choice == "1":
                emp_id = input("Enter Employee ID: ")
                name = input("Enter Name: ")
                dept = input("Enter Department: ")
                role = input("Enter Role: ")
                salary = prompt_float("Enter Salary: ")
                exp = prompt_int("Enter Years of Experience: ")
                manager.add_record(emp_id, name, dept, role, salary, exp)
                print("Employee added successfully.")

            elif choice == "2":
                emp_id = input("Enter Employee ID to update: ")
                print("Leave blank to keep existing values.")
                name = input("New Name: ") or None
                dept = input("New Department: ") or None
                role = input("New Role: ") or None
                salary = prompt_float("New Salary: ", allow_blank=True)
                exp = prompt_int("New Experience: ", allow_blank=True)

                updates = {"name": name, "department": dept, "role": role, "salary": salary, "experience": exp}
                manager.update_record(emp_id, **{k: v for k, v in updates.items() if v is not None})
                print("Employee updated successfully.")

            elif choice == "3":
                emp_id = input("Enter Employee ID to delete: ")
                deleted = manager.delete_record(emp_id)
                print(f"Employee '{deleted['name']}' (ID: {deleted['id']}) deleted.")

            elif choice == "4":
                query = input("Enter search term (ID, Name, Department, or Role): ")
                display_table(manager.search(query))

            elif choice == "5":
                dept = input("Filter by Department (or press Enter to skip): ").strip() or None
                min_sal = prompt_float("Min Salary (or press Enter to skip): ", allow_blank=True)
                max_sal = prompt_float("Max Salary (or press Enter to skip): ", allow_blank=True)
                min_exp = prompt_int("Min Experience (or press Enter to skip): ", allow_blank=True)
                results = manager.filter_records(dept, min_sal, max_sal, min_exp)
                display_table(results)

            elif choice == "6":
                print(f"Available fields: {', '.join(EmployeeManager.FIELDNAMES)}")
                field = input("Sort by: ").strip().lower()
                order = input("Descending order? (y/n): ").strip().lower() == "y"
                display_table(manager.sort_records(by=field, descending=order))

            elif choice == "7":
                stats = manager.get_statistics()
                if stats.get("total_count", 0) == 0:
                    print("\nNo data available to calculate statistics.")
                else:
                    print("\n--- Summary Statistics ---")
                    print(f"Total Headcount:    {stats['total_count']}")
                    print(f"Total Payroll:      Rs. {stats['total_payroll']:,.2f}")
                    print(f"Average Salary:     Rs. {stats['mean_salary']:,.2f}")
                    print(f"Median Salary:      Rs. {stats['median_salary']:,.2f}")
                    print(f"Salary Range:       Rs. {stats['min_salary']:,.2f} - Rs. {stats['max_salary']:,.2f}")
                    print(f"Average Experience: {stats['mean_experience']} years")
                    print("Department Breakdown:")
                    for d, count in stats["department_headcounts"].items():
                        print(f"  - {d}: {count}")

            elif choice == "8":
                display_table(manager.records)

            elif choice == "9":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please select an option from 1 to 9.")

        except ManagementSystemError as err:
            print(f"[Operation Error] {err}")
        except Exception as err:
            print(f"[Unexpected Error] {err}")


if __name__ == "__main__":
    main()
