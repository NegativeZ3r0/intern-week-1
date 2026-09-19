import React from 'react';
import type { Employee } from '../types/employee';

interface EmployeeDetailsModalProps {
  employee: Employee | null;
  onClose: () => void;
}

export const EmployeeDetailsModal: React.FC<EmployeeDetailsModalProps> = ({
  employee,
  onClose,
}) => {
  if (!employee) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>Employee Record: {employee.id}</h3>
        <div className="details-grid">
          <div>
            <strong>Full Name:</strong> {employee.firstName} {employee.lastName}
          </div>
          <div>
            <strong>Email:</strong> {employee.email}
          </div>
          <div>
            <strong>Department:</strong> {employee.department}
          </div>
          <div>
            <strong>Role:</strong> {employee.role}
          </div>
          <div>
            <strong>Salary:</strong> Rs. {employee.salary.toLocaleString('en-IN')} / year
          </div>
          <div>
            <strong>Joined:</strong> {employee.joinDate}
          </div>
        </div>
        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
