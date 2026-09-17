const { rankStudentsByTest } = require('./services/analyticsService.js');

const profiles = [{ ROLL_KEY: '123', "STUDENT'S NAME": "Test" }];
const tests = [{
  ROLL_KEY: '123',
  CMT01_Physics: 30,
  CMT01_Chemistry: 40,
  CMT01_Biology: 50,
  CMT01_Math: 20
}];

const ranked = rankStudentsByTest(profiles, tests, "CMT01");
console.log(JSON.stringify(ranked, null, 2));
