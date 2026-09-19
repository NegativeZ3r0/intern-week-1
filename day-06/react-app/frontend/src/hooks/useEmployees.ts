import { useMemo, useState } from 'react';
import type { Employee, FilterCriteria } from '../types/employee';

export function useEmployeeFilter(employees: Employee[]) {
  const [criteria, setCriteria] = useState<FilterCriteria>({
    searchQuery: '',
    department: 'ALL',
    sortField: 'firstName',
    sortOrder: 'asc',
  });

  const processedEmployees = useMemo(() => {
    return employees
      .filter((emp) => {
        // Search across multiple fields
        const query = criteria.searchQuery.toLowerCase();
        const matchesQuery =
          emp.firstName.toLowerCase().includes(query) ||
          emp.lastName.toLowerCase().includes(query) ||
          emp.email.toLowerCase().includes(query) ||
          emp.role.toLowerCase().includes(query);

        // Department filter
        const matchesDept =
          criteria.department === 'ALL' || emp.department === criteria.department;

        return matchesQuery && matchesDept;
      })
      .sort((a, b) => {
        const valA = a[criteria.sortField];
        const valB = b[criteria.sortField];

        let result: number //= 0;
        if (typeof valA === 'number' && typeof valB === 'number') {
          result = valA - valB;
        } else {
          result = String(valA).localeCompare(String(valB));
        }

        return criteria.sortOrder === 'asc' ? result : -result;
      });
  }, [employees, criteria]);

  return { criteria, setCriteria, processedEmployees };
}
