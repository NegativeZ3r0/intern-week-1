export interface Employee {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  department: string;
  role: string;
  salary: number;
  joinDate: string;
}

export type EmployeePayload = Omit<Employee, 'id'>;

export type SortField = 'firstName' | 'salary' | 'joinDate' | 'department';
export type SortOrder = 'asc' | 'desc';

export interface FilterCriteria {
  searchQuery: string;
  department: string;
  sortField: SortField;
  sortOrder: SortOrder;
}
