import { useState, useEffect, useMemo } from 'react';
import { DashboardStats } from './components/DashboardStats';
import type { Employee, EmployeePayload, FilterCriteria } from './types/employee';
import { employeeApi } from './services/api';
import { ControlsBar } from './components/ControlsBar';
import { EmployeeList } from './components/EmployeeList';
import { EmployeeFormModal } from './components/EmployeeFormModal';
import { EmployeeDetailsModal } from './components/EmployeeDetailsModal';
import './index.css';

export default function App() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [apiError, setApiError] = useState<string | null>(null);

  // Criteria state
  const [criteria, setCriteria] = useState<FilterCriteria>({
    searchQuery: '',
    department: 'ALL',
    sortField: 'firstName',
    sortOrder: 'asc',
  });

  // Derived dashboard statistics
    const stats = useMemo(() => {
      const totalEmployees = employees.length;

      const totalSalary = employees.reduce((sum, emp) => sum + emp.salary, 0);
      const averageSalary = totalEmployees > 0 ? Math.round(totalSalary / totalEmployees) : 0;

      const uniqueDepartments = new Set(employees.map((emp) => emp.department));
      const totalDepartments = uniqueDepartments.size;

      return {
        totalEmployees,
        averageSalary,
        totalDepartments,
      };
    }, [employees]);

  // Modal tracking
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [viewingEmployee, setViewingEmployee] = useState<Employee | null>(null);

  // Initial fetch
  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      setApiError(null);
      const data = await employeeApi.getAll();
      setEmployees(data);
    } catch (err) {
      setApiError(err instanceof Error ? err.message : 'Connection failed');
    } finally {
      setLoading(false);
    }
  };

  // Extract distinct departments for filter dropdown
  const departments = useMemo(() => {
    const depts = new Set(employees.map((e) => e.department));
    return Array.from(depts).sort();
  }, [employees]);

  // Derived filter + sort pipeline
  const filteredEmployees = useMemo(() => {
    const query = criteria.searchQuery.trim().toLowerCase();

    return employees
      .filter((emp) => {
        const matchesQuery =
          !query ||
          emp.firstName.toLowerCase().includes(query) ||
          emp.lastName.toLowerCase().includes(query) ||
          emp.email.toLowerCase().includes(query) ||
          emp.role.toLowerCase().includes(query);

        const matchesDept =
          criteria.department === 'ALL' || emp.department === criteria.department;

        return matchesQuery && matchesDept;
      })
      .sort((a, b) => {
        const valA = a[criteria.sortField];
        const valB = b[criteria.sortField];

        let result = 0;
        if (typeof valA === 'number' && typeof valB === 'number') {
          result = valA - valB;
        } else {
          result = String(valA).localeCompare(String(valB));
        }

        return criteria.sortOrder === 'asc' ? result : -result;
      });
  }, [employees, criteria]);

  // CRUD handlers
  const handleFormSubmit = async (payload: EmployeePayload) => {
    if (editingEmployee) {
      const updated = await employeeApi.update(editingEmployee.id, payload);
      setEmployees((prev) => prev.map((e) => (e.id === updated.id ? updated : e)));
    } else {
      const created = await employeeApi.create(payload);
      setEmployees((prev) => [...prev, created]);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this employee?')) return;
    try {
      await employeeApi.remove(id);
      setEmployees((prev) => prev.filter((e) => e.id !== id));
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Delete failed');
    }
  };

  const openAddModal = () => {
    setEditingEmployee(null);
    setIsFormOpen(true);
  };

  const openEditModal = (employee: Employee) => {
    setEditingEmployee(employee);
    setIsFormOpen(true);
  };

  return (
    <div className="container">
      <header className="dashboard-header">
        <div>
          <h1>Employee Management System</h1>
          <p className="subtitle">
            Showing {filteredEmployees.length} of {employees.length} records
          </p>
        </div>
      </header>

      <DashboardStats
        totalEmployees={stats.totalEmployees}
        averageSalary={stats.averageSalary}
        totalDepartments={stats.totalDepartments}
      />

      {apiError && (
        <div className="error-banner">
          {apiError} — Make sure the backend is running at http://localhost:5000.
        </div>
      )}

      <ControlsBar
        criteria={criteria}
        departments={departments}
        onCriteriaChange={setCriteria}
        onOpenAddModal={openAddModal}
      />

      {loading ? (
        <div className="loading-state">Loading records...</div>
      ) : (
        <EmployeeList
          employees={filteredEmployees}
          onView={(emp) => setViewingEmployee(emp)}
          onEdit={openEditModal}
          onDelete={handleDelete}
        />
      )}

      <EmployeeFormModal
        isOpen={isFormOpen}
        initialData={editingEmployee}
        onClose={() => setIsFormOpen(false)}
        onSubmit={handleFormSubmit}
      />

      <EmployeeDetailsModal
        employee={viewingEmployee}
        onClose={() => setViewingEmployee(null)}
      />
    </div>
  );
}
