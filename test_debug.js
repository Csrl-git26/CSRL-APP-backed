import mongoose from 'mongoose';
mongoose.connect(process.env.MONGODB_URI || "mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority");

import StudentWeakTopics from './models/StudentWeakTopics.js';

async function test() {
  const rollKey = '2601001';
  const weakTopics = await StudentWeakTopics.find({ studentId: rollKey }).lean();
  
  const weakMap = {};
  for (const wt of weakTopics) {
    const normKey = (wt.testId || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    if (!weakMap[normKey]) {
      weakMap[normKey] = {
        attempted: 0,
        correct: 0,
        wrong: 0,
        totalQuestions: 0,
        subjectMetrics: {
          Physics: { attempted: 0, correct: 0, wrong: 0 },
          Chemistry: { attempted: 0, correct: 0, wrong: 0 },
          Mathematics: { attempted: 0, correct: 0, wrong: 0 },
          Biology: { attempted: 0, correct: 0, wrong: 0 },
        }
      };
    }
    
    const target = weakMap[normKey];
    target.attempted += (wt.attempted || 0);
    target.correct += (wt.correct || 0);
    target.wrong += (wt.wrong || 0);
    
    if (wt.subjectMetrics) {
      ['Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach(sub => {
        if (wt.subjectMetrics[sub]) {
          target.subjectMetrics[sub].attempted += (wt.subjectMetrics[sub].attempted || 0);
          target.subjectMetrics[sub].correct += (wt.subjectMetrics[sub].correct || 0);
          target.subjectMetrics[sub].wrong += (wt.subjectMetrics[sub].wrong || 0);
        }
      });
    }
  }
  console.log(JSON.stringify(weakMap, null, 2));
  process.exit(0);
}
test().catch(e => { console.error(e); process.exit(1); });
