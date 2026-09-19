import React from 'react';
import type { Employee } from '../types/employee';

interface EmployeeListProps {
  employees: Employee[];
  onView: (employee: Employee) => void;
  onEdit: (employee: Employee) => void;
  onDelete: (id: string) => void;
}

export const EmployeeList: React.FC<EmployeeListProps> = ({
  employees,
  onView,
  onEdit,
  onDelete,
}) => {
  if (employees.length === 0) {
    return <div className="empty-state">No matching employees found.</div>;
  }

  return (
    <div className="table-responsive">
      <table className="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Role</th>
            <th>Salary</th>
            <th>Join Date</th>
            <th style={{ textAlign: 'center' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id}>
              <td>
                <strong>{emp.firstName} {emp.lastName}</strong>
              </td>
              <td>{emp.email}</td>
              <td>
                <span className="badge">{emp.department}</span>
              </td>
              <td>{emp.role}</td>
              <td>Rs. {emp.salary.toLocaleString('en-IN')}</td>
              <td>{emp.joinDate}</td>
              <td>
                <div className="action-buttons">
                  <button className="btn-action view" onClick={() => onView(emp)}>
                    Details
                  </button>
                  <button className="btn-action edit" onClick={() => onEdit(emp)}>
                    Edit
                  </button>
                  <button className="btn-action delete" onClick={() => onDelete(emp.id)}>
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
