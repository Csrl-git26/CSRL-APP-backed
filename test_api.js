import jwt from 'jsonwebtoken';
import fetch from 'node-fetch';

const secret = process.env.JWT_SECRET || 'csrl_super_secret_key_2026';
const token = jwt.sign({ id: '2601001', role: 'student', centerCode: 'KNP' }, secret);

async function test() {
  const url = 'https://csrl-app-backed.onrender.com/api/analytics/student-chart?rollKey=2601001';
  const res = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  console.log(res.status);
  const data = await res.json();
  console.log(JSON.stringify(data, null, 2));
}

test().catch(console.error);
