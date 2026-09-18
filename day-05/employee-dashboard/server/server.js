import http from 'node:http';

// In-memory data store
let employees = [
  { id: 1, name: 'Alice Smith', email: 'alice@example.com', department: 'Engineering', role: 'Software Engineer', salary: 85000 },
  { id: 2, name: 'Bob Jones', email: 'bob@example.com', department: 'Marketing', role: 'Marketing Specialist', salary: 62000 },
  { id: 3, name: 'Charlie Lee', email: 'charlie@example.com', department: 'Design', role: 'UI/UX Designer', salary: 74000 },
  { id: 4, name: 'Diana Prince', email: 'diana@example.com', department: 'Engineering', role: 'Tech Lead', salary: 110000 }
];

let nextId = 5;

// Helper: parse JSON body from incoming streams
const parseRequestBody = (req) => {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(err);
      }
    });
    req.on('error', reject);
  });
};

const server = http.createServer(async (req, res) => {
  const origin = req.headers.origin || '*';

  const sendResponse = (statusCode, data) => {
    res.writeHead(statusCode, {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end(data !== undefined ? JSON.stringify(data) : '');
  };

  if (req.method === 'OPTIONS') {
    sendResponse(204);
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  // Normalize path: trims '/api/employees/' -> '/api/employees'
  const pathname = url.pathname.replace(/\/+$/, '') || '/';
  const matchId = pathname.match(/^\/api\/employees\/(\d+)$/);
  const id = matchId ? parseInt(matchId[1], 10) : null;
  const isBaseRoute = pathname === '/api/employees';

  try {
    // GET /api/employees -> List all
    if (req.method === 'GET' && isBaseRoute) {
      return sendResponse(200, employees);
    }

    // GET /api/employees/:id -> Details
    if (req.method === 'GET' && id !== null) {
      const emp = employees.find(e => e.id === id);
      return emp ? sendResponse(200, emp) : sendResponse(404, { message: 'Not found' });
    }

    // POST /api/employees or /api/employees/ -> Add new
    if (req.method === 'POST' && isBaseRoute) {
      const payload = await parseRequestBody(req);
      const newEmp = { id: nextId++, ...payload };
      employees.push(newEmp);
      return sendResponse(201, newEmp);
    }

    // PUT /api/employees/:id -> Edit
    if (req.method === 'PUT' && id !== null) {
      const payload = await parseRequestBody(req);
      const index = employees.findIndex(e => e.id === id);
      if (index === -1) return sendResponse(404, { message: 'Not found' });

      employees[index] = { ...employees[index], ...payload, id };
      return sendResponse(200, employees[index]);
    }

    // DELETE /api/employees/:id -> Delete
    if (req.method === 'DELETE' && id !== null) {
      const index = employees.findIndex(e => e.id === id);
      if (index === -1) return sendResponse(404, { message: 'Not found' });

      employees.splice(index, 1);
      return sendResponse(200, { message: 'Deleted successfully' });
    }

    sendResponse(404, { message: 'Route not found' });
  } catch (err) {
    sendResponse(500, { message: 'Internal Server Error', error: err.message });
  }
});

const PORT = 5069;
server.listen(PORT, () => console.log(`API Server running at http://127.0.0.1:${PORT}/`));
