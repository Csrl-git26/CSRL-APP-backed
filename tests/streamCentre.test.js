import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

// Exercise the route's actual filter without starting the server or a database.
const source = readFileSync(new URL('../server.js', import.meta.url), 'utf8');
const start = source.indexOf('const NEET_CENTRE_CODES =');
const end = source.indexOf('\n/**', start);
const filter = vm.runInNewContext(source.slice(start, end) + '\nfilterByStream');

test('NEET centres cannot leak into CAT01 JEE rankings through stale labels or scores', () => {
  const profiles = [
    { ROLL_KEY: '1', centerCode: ' jmm ', stream: 'JEE' },
    { ROLL_KEY: '2', centerCode: 'KNP', stream: 'JEE' },
    { ROLL_KEY: '3', centerCode: 'JMM', stream: 'JEE' },
  ];
  const tests = [
    { ROLL_KEY: '1', centerCode: 'JMM', stream: 'JEE', CAT01_Physics: 50, MT01: 100 },
    { ROLL_KEY: '2', centerCode: 'KNP', stream: 'JEE', CAT01_Physics: 60 },
    { ROLL_KEY: '4', centerCode: 'JMM', stream: 'JEE', CAT01_Physics: 70 },
  ];
  const jee = filter(profiles, tests, 'JEE');
  assert.deepEqual(Array.from(jee.profiles, p => p.ROLL_KEY), ['2']);
  assert.deepEqual(Array.from(jee.tests, p => p.ROLL_KEY), ['2']);
  const neet = filter(profiles, tests, 'NEET');
  assert.deepEqual(Array.from(neet.profiles, p => p.ROLL_KEY).sort(), ['1', '3', '4']);
  assert.equal(filter(profiles, tests, 'ALL').profiles, profiles);
});
