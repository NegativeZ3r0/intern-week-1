const API_URL = 'http://127.0.0.1:5069/api/employees';

// --- State Management ---
const state = {
  employees: [],
  search: '',
  department: '',
  sort: 'name-asc'
};

// --- API Service Functions ---
async function apiRequest(url, options = {}) {
  try {
    const res = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options
    });
    if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('API Request failed:', err);
    alert('Action failed. Check console for details.');
  }
}

const fetchEmployees = () => apiRequest(API_URL);
const fetchEmployee = (id) => apiRequest(`${API_URL}/${id}`);
const createEmployee = (data) => apiRequest(API_URL, { method: 'POST', body: JSON.stringify(data) });
const updateEmployee = (id, data) => apiRequest(`${API_URL}/${id}`, { method: 'PUT', body: JSON.stringify(data) });
const removeEmployee = (id) => apiRequest(`${API_URL}/${id}`, { method: 'DELETE' });

// --- Pure Data Pipeline: Filter -> Search -> Sort ---
function getProcessedEmployees() {
  return state.employees
    .filter(emp => {
      const matchDept = !state.department || emp.department === state.department;
      const term = state.search.toLowerCase();
      const matchSearch = emp.name.toLowerCase().includes(term) || emp.role.toLowerCase().includes(term);
      return matchDept && matchSearch;
    })
    .sort((a, b) => {
      switch (state.sort) {
        case 'name-asc': return a.name.localeCompare(b.name);
        case 'name-desc': return b.name.localeCompare(a.name);
        case 'salary-asc': return a.salary - b.salary;
        case 'salary-desc': return b.salary - a.salary;
        default: return 0;
      }
    });
}

// --- DOM References ---
const tableBody = document.getElementById('employee-table-body');
const searchInput = document.getElementById('search-input');
const filterDept = document.getElementById('filter-dept');
const sortBy = document.getElementById('sort-by');
const dialog = document.getElementById('employee-dialog');
const form = document.getElementById('employee-form');
const detailsDialog = document.getElementById('details-dialog');

// --- Render Functions ---
function updateDepartmentDropdown() {
  const departments = [...new Set(state.employees.map(e => e.department))];
  const currentValue = filterDept.value;
  filterDept.innerHTML = '<option value="">All Departments</option>' +
    departments.map(d => `<option value="${d}">${d}</option>`).join('');
  filterDept.value = departments.includes(currentValue) ? currentValue : '';
}

function render() {
  const list = getProcessedEmployees();

  if (list.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 2rem;">No matching employees found.</td></tr>`;
    return;
  }

  tableBody.innerHTML = list.map(emp => `
    <tr>
      <td><strong>${emp.name}</strong></td>
      <td>${emp.role}</td>
      <td>${emp.department}</td>
      <td>${Number(emp.salary).toLocaleString()} Rs.</td>
      <td class="action-buttons">
        <button class="btn-sm btn-info" data-action="view" data-id="${emp.id}">View</button>
        <button class="btn-sm btn-warning" data-action="edit" data-id="${emp.id}">Edit</button>
        <button class="btn-sm btn-danger" data-action="delete" data-id="${emp.id}">Delete</button>
      </td>
    </tr>
  `).join('');
}

// --- Action Handlers ---
async function handleView(id) {
  const emp = await fetchEmployee(id);
  if (!emp) return;
  document.getElementById('details-body').innerHTML = `
    <p><strong>ID:</strong> ${emp.id}</p>
    <p><strong>Name:</strong> ${emp.name}</p>
    <p><strong>Email:</strong> ${emp.email}</p>
    <p><strong>Department:</strong> ${emp.department}</p>
    <p><strong>Role:</strong> ${emp.role}</p>
    <p><strong>Salary:</strong> Rs${Number(emp.salary).toLocaleString()}</p>
  `;
  detailsDialog.showModal();
}

function openEditModal(emp) {
  document.getElementById('modal-title').textContent = emp ? 'Edit Employee' : 'Add Employee';
  document.getElementById('emp-id').value = emp ? emp.id : '';
  document.getElementById('emp-name').value = emp ? emp.name : '';
  document.getElementById('emp-email').value = emp ? emp.email : '';
  document.getElementById('emp-department').value = emp ? emp.department : '';
  document.getElementById('emp-role').value = emp ? emp.role : '';
  document.getElementById('emp-salary').value = emp ? emp.salary : '';
  dialog.showModal();
}

async function handleDelete(id) {
  if (!confirm('Are you sure you want to delete this employee?')) return;
  await removeEmployee(id);
  state.employees = state.employees.filter(e => e.id !== id);
  updateDepartmentDropdown();
  render();
}

// --- Event Listeners ---

// 1. Delegated Table Actions (View, Edit, Delete)
tableBody.addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;
  const id = parseInt(btn.dataset.id, 10);
  const action = btn.dataset.action;

  if (action === 'view') handleView(id);
  if (action === 'edit') {
    const emp = state.employees.find(item => item.id === id);
    if (emp) openEditModal(emp);
  }
  if (action === 'delete') handleDelete(id);
});

// 2. Add Button & Dialog Buttons
document.getElementById('add-btn').addEventListener('click', () => openEditModal(null));
document.getElementById('dialog-cancel-btn').addEventListener('click', () => dialog.close());
document.getElementById('details-close-btn').addEventListener('click', () => detailsDialog.close());

// 3. Form Submit (Add or Edit)
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('emp-id').value;
  const payload = {
    name: document.getElementById('emp-name').value.trim(),
    email: document.getElementById('emp-email').value.trim(),
    department: document.getElementById('emp-department').value.trim(),
    role: document.getElementById('emp-role').value.trim(),
    salary: Number(document.getElementById('emp-salary').value)
  };

  if (id) {
    const updated = await updateEmployee(id, payload);
    if (updated) {
      state.employees = state.employees.map(e => e.id === Number(id) ? updated : e);
    }
  } else {
    const added = await createEmployee(payload);
    if (added) state.employees.push(added);
  }

  dialog.close();
  updateDepartmentDropdown();
  render();
});

// 4. Filtering and Sorting Controls
searchInput.addEventListener('input', (e) => {
  state.search = e.target.value;
  render();
});

filterDept.addEventListener('change', (e) => {
  state.department = e.target.value;
  render();
});

sortBy.addEventListener('change', (e) => {
  state.sort = e.target.value;
  render();
});

// --- Initialization ---
async function init() {
  const data = await fetchEmployees();
  if (data) {
    state.employees = data;
    updateDepartmentDropdown();
    render();
  }
}

init();
