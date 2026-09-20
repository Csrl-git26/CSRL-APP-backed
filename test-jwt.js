import jwt from 'jsonwebtoken';
import fetch from 'node-fetch';
const token = jwt.sign({ rollKey: 'admin', role: 'admin' }, 'csrl_jwt_secret_2024', { expiresIn: '1h' });
console.log("Token:", token);

fetch('https://csrl-app-backed-1.onrender.com/api/analytics/centre-chart?centerCode=AGR', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
}).then(res => res.json()).then(console.log).catch(console.error);
