import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { rankStudentsByTest, computeTestInsights } from '../services/analyticsService.js';

// Exercise the production filter without starting Express or opening MongoDB.
const source = fs.readFileSync(new URL('../server.js', import.meta.url), 'utf8');
const start = source.indexOf('const NEET_CENTRE_CODES =');
const end = source.indexOf('\n/**', start);
const filter = vm.runInNewContext(source.slice(start, end) + '\nfilterByStream');

test('stream filtering preserves actual profiles for explorer and top/bottom rankings', () => {
  for (const [stream, centerCode, testKey] of [['JEE', 'DDN', 'MT02'], ['NEET', 'GLT', 'NCT01']]) {
    const profiles = Array.from({ length: 24 }, (_, i) => ({ ROLL_KEY: String(i + 1), "STUDENT'S NAME": `Student ${i + 1}`, centerCode, stream, CATEGORY: 'GEN' }));
    const tests = profiles.map((p, i) => ({ ROLL_KEY: p.ROLL_KEY, centerCode, stream, [testKey]: i }));
    const result = filter(profiles, tests, stream);
    assert.equal(result.profiles[0], profiles[0]);
    const ranked = rankStudentsByTest(result.profiles, result.tests, testKey);
    for (const row of [...ranked.slice(0, 10), ...ranked.slice(-10)]) {
      assert.equal(row.name, `Student ${row.roll}`);
      assert.equal(row.category, 'GEN');
    }
    assert.equal(computeTestInsights(result.profiles, result.tests, testKey, [testKey], { stream }).overallTopper.name, 'Student 24');
  }
});
