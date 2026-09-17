import mongoose from 'mongoose';

// Topic-level weak classification (arrays of topic name strings)
const SubjectWiseSchema = new mongoose.Schema({
  strong:   { type: [String], default: [] },
  moderate: { type: [String], default: [] },
  weak:     { type: [String], default: [] },
}, { _id: false });

const StudentWeakTopicsSchema = new mongoose.Schema({
  studentId:   { type: String, required: true }, // The prompt specifies roll number as unique id, which maps to studentId
  studentName: { type: String, default: '' },
  testId:      { type: String, required: true },
  centerId:    { type: String, required: true },
  
  totalScore:  { type: Number, default: 0 },

  strongTopics:   { type: [String], default: [] },
  moderateTopics: { type: [String], default: [] },
  weakTopics:     { type: [String], default: [] },

  subjectWise: {
    PHYSICS:     { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    CHEMISTRY:   { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    MATHEMATICS: { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
  },

  computedAt: { type: Date, default: Date.now },
}, { timestamps: true });

// Unique compound index per student+test
StudentWeakTopicsSchema.index({ studentId: 1, testId: 1 }, { unique: true });
StudentWeakTopicsSchema.index({ centerId: 1, testId: 1 });

export default mongoose.models.StudentWeakTopics || mongoose.model('StudentWeakTopics', StudentWeakTopicsSchema);
