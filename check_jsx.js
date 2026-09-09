const fs = require('fs');
const acorn = require('acorn');
const jsx = require('acorn-jsx');
const Parser = acorn.Parser.extend(jsx());

const code = fs.readFileSync('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx', 'utf8');

try {
  Parser.parse(code, {
    sourceType: 'module',
    ecmaVersion: 2020
  });
  console.log("No syntax errors found!");
} catch (e) {
  console.error("Syntax Error at line", e.loc.line, "column", e.loc.column);
  console.error(e.message);
}
