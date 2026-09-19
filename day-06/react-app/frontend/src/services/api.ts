import type { Employee, EmployeePayload } from '../types/employee';

const BASE_URL = 'http://localhost:5000/api/employees';

export const employeeApi = {
  async getAll(): Promise<Employee[]> {
    const res = await fetch(BASE_URL);
    if (!res.ok) throw new Error('Failed to load employee list');
    return res.json();
  },

  async getById(id: string): Promise<Employee> {
    const res = await fetch(`${BASE_URL}/${id}`);
    if (!res.ok) throw new Error('Failed to load employee details');
    return res.json();
  },

  async create(payload: EmployeePayload): Promise<Employee> {
    const res = await fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to create employee');
    return res.json();
  },

  async update(id: string, payload: Partial<EmployeePayload>): Promise<Employee> {
    const res = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to update employee');
    return res.json();
  },

  async remove(id: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete employee');
  },
};
