import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../server.js', import.meta.url), 'utf8');
const start = source.indexOf('const NEET_CENTRE_CODES =');
const filter = vm.runInNewContext(source.slice(start, source.indexOf('\n/**', start)) + '\nfilterByStream');

test('MUM belongs to JEE even with historical NEET labels; JMM remains NEET', () => {
  const profiles = [
    { ROLL_KEY: '1', centerCode: ' mum ', stream: 'NEET' },
    { ROLL_KEY: '2', centerCode: 'JMM', stream: 'JEE' },
  ];
  const tests = [
    { ROLL_KEY: '1', centerCode: 'MUM', stream: 'NEET', MT02: 100 },
    { ROLL_KEY: '2', centerCode: 'JMM', stream: 'JEE', MT02: 100 },
    { ROLL_KEY: '3', centerCode: 'MUM', stream: 'NEET', CAT01: 120 },
  ];
  const jee = filter(profiles, tests, 'JEE');
  assert.deepEqual(Array.from(jee.tests, row => row.ROLL_KEY), ['1', '3']);
  const neet = filter(profiles, tests, 'NEET');
  assert.deepEqual(Array.from(neet.tests, row => row.ROLL_KEY), ['2']);
});
