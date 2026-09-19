import React from 'react';
import type { FilterCriteria, SortField, /*SortOrder*/ } from '../types/employee';

interface ControlsBarProps {
  criteria: FilterCriteria;
  departments: string[];
  onCriteriaChange: (updater: (prev: FilterCriteria) => FilterCriteria) => void;
  onOpenAddModal: () => void;
}

export const ControlsBar: React.FC<ControlsBarProps> = ({
  criteria,
  departments,
  onCriteriaChange,
  onOpenAddModal,
}) => {
  return (
    <div className="controls-bar">
      <div className="search-box">
        <input
          type="text"
          placeholder="Search by name, role, email..."
          value={criteria.searchQuery}
          onChange={(e) =>
            onCriteriaChange((prev) => ({ ...prev, searchQuery: e.target.value }))
          }
        />
      </div>

      <div className="filter-group">
        <label>Dept:</label>
        <select
          value={criteria.department}
          onChange={(e) =>
            onCriteriaChange((prev) => ({ ...prev, department: e.target.value }))
          }
        >
          <option value="ALL">All Departments</option>
          {departments.map((dept) => (
            <option key={dept} value={dept}>
              {dept}
            </option>
          ))}
        </select>
      </div>

      <div className="sort-group">
        <label>Sort:</label>
        <select
          value={criteria.sortField}
          onChange={(e) =>
            onCriteriaChange((prev) => ({
              ...prev,
              sortField: e.target.value as SortField,
            }))
          }
        >
          <option value="firstName">First Name</option>
          <option value="department">Department</option>
          <option value="salary">Salary</option>
          <option value="joinDate">Join Date</option>
        </select>

        <button
          type="button"
          className="btn-secondary"
          onClick={() =>
            onCriteriaChange((prev) => ({
              ...prev,
              sortOrder: prev.sortOrder === 'asc' ? 'desc' : 'asc',
            }))
          }
        >
          {criteria.sortOrder === 'asc' ? '↑ Asc' : '↓ Desc'}
        </button>
      </div>

      <button className="btn-primary" onClick={onOpenAddModal}>
        + Add Employee
      </button>
    </div>
  );
};
