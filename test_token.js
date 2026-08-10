import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
dotenv.config();

const token = jwt.sign(
  { id: '2601001', centerCode: 'KNP', role: 'student' },
  process.env.JWT_SECRET || 'secret' // I need the actual secret if it's hitting production!
);
console.log(token);
