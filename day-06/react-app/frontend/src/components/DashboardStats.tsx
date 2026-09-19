import React from 'react';

interface DashboardStatsProps {
  totalEmployees: number;
  averageSalary: number;
  totalDepartments: number;
}

export const DashboardStats: React.FC<DashboardStatsProps> = ({
  totalEmployees,
  averageSalary,
  totalDepartments,
}) => {
  // Format salary to INR (Indian numbering system: lakhs/crores)
  const formattedAvgSalary = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(averageSalary);

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <span className="stat-label">Total Employees</span>
        <span className="stat-value">{totalEmployees}</span>
        <span className="stat-subtext">Active records</span>
      </div>

      <div className="stat-card">
        <span className="stat-label">Average Salary</span>
        <span className="stat-value">{formattedAvgSalary}</span>
        <span className="stat-subtext">Per annum</span>
      </div>

      <div className="stat-card">
        <span className="stat-label">Departments</span>
        <span className="stat-value">{totalDepartments}</span>
        <span className="stat-subtext">Operating divisions</span>
      </div>
    </div>
  );
};
