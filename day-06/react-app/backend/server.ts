import express, { Request, Response } from 'express';
import cors from 'cors';

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

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

// In-memory persistence store
let employees: Employee[] = [
  {
    id: 'emp-1',
    firstName: 'Alice',
    lastName: 'Johnson',
    email: 'alice.j@example.com',
    department: 'Engineering',
    role: 'Frontend Architect',
    salary: 115000,
    joinDate: '2022-03-15',
  },
  {
    id: 'emp-2',
    firstName: 'Marcus',
    lastName: 'Vance',
    email: 'marcus.v@example.com',
    department: 'Product',
    role: 'Product Lead',
    salary: 125000,
    joinDate: '2021-08-01',
  },
  {
    id: 'emp-3',
    firstName: 'Elena',
    lastName: 'Rostova',
    email: 'elena.r@example.com',
    department: 'Design',
    role: 'UI/UX Designer',
    salary: 95000,
    joinDate: '2023-01-10',
  },
  {
    id: 'emp-4',
    firstName: 'David',
    lastName: 'Kim',
    email: 'david.k@example.com',
    department: 'Engineering',
    role: 'Backend Engineer',
    salary: 105000,
    joinDate: '2022-11-20',
  },
];

// GET /api/employees - Fetch all
app.get('/api/employees', (_req: Request, res: Response) => {
  res.status(200).json(employees);
});

// GET /api/employees/:id - Fetch single employee
app.get('/api/employees/:id', (req: Request, res: Response) => {
  const employee = employees.find((e) => e.id === req.params.id);
  if (!employee) {
    res.status(404).json({ message: 'Employee not found' });
    return;
  }
  res.status(200).json(employee);
});

// POST /api/employees - Create
app.post('/api/employees', (req: Request, res: Response) => {
  const { firstName, lastName, email, department, role, salary, joinDate } = req.body;

  if (!firstName || !lastName || !email || !department || !role || !salary || !joinDate) {
    res.status(400).json({ message: 'All fields are required' });
    return;
  }

  const newEmployee: Employee = {
    id: `emp-${Date.now()}`,
    firstName,
    lastName,
    email,
    department,
    role,
    salary: Number(salary),
    joinDate,
  };

  employees.push(newEmployee);
  res.status(201).json(newEmployee);
});

// PUT /api/employees/:id - Update
app.put('/api/employees/:id', (req: Request, res: Response) => {
  const index = employees.findIndex((e) => e.id === req.params.id);
  if (index === -1) {
    res.status(404).json({ message: 'Employee not found' });
    return;
  }

  const updated: Employee = {
    ...employees[index],
    ...req.body,
    id: employees[index].id, // Prevent ID overwrite
    salary: Number(req.body.salary ?? employees[index].salary),
  };

  employees[index] = updated;
  res.status(200).json(updated);
});

// DELETE /api/employees/:id - Remove
app.delete('/api/employees/:id', (req: Request, res: Response) => {
  const exists = employees.some((e) => e.id === req.params.id);
  if (!exists) {
    res.status(404).json({ message: 'Employee not found' });
    return;
  }

  employees = employees.filter((e) => e.id !== req.params.id);
  res.status(204).send();
});

app.listen(PORT, () => {
  console.log(`Backend running at http://localhost:${PORT}`);
});
