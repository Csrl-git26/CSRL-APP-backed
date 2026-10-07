import assert from 'node:assert/strict';
import { test } from 'node:test';
import { validateFacultyResults } from './facultyResults.js';
const row = { name:'Example Faculty',email:'faculty@example.com',year:'2026-27',test:'CMT-01',subject:'PHYSICS',centres:'A & B',attempted:4,correct:0,marks:-4 };
test('preserves negative and zero marks, normalizes centres and accuracy', () => {
  const [r] = validateFacultyResults([row]);
  assert.equal(r.marks,-4); assert.equal(r.accuracy,0); assert.deepEqual(r.centres,['A','B']);
  assert.equal(validateFacultyResults([{...row,attempted:0,correct:0,marks:0}])[0].accuracy,null);
});
test('rejects duplicates and invalid or conflicting attendance', () => {
  assert.throws(()=>validateFacultyResults([row,row]),/duplicate/);
  assert.throws(()=>validateFacultyResults([{...row,correct:5}]),/invalid/);
  assert.throws(()=>validateFacultyResults([{...row,status:'ABSENT'}]),/cannot/);
  assert.throws(()=>validateFacultyResults([{...row,email:''}]),/required/);
});
test('preserves leave separately from missing and scored results', () => {
  const [r] = validateFacultyResults([{...row,attempted:null,correct:null,marks:null,status:'MEDICAL LEAVE'}]);
  assert.equal(r.status,'MEDICAL LEAVE'); assert.equal(r.marks,null);
});
