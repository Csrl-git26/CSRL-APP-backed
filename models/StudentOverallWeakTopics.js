import mongoose from 'mongoose';

const SubjectWiseSchema = new mongoose.Schema({
  strong:   { type: [String], default: [] },
  moderate: { type: [String], default: [] },
  weak:     { type: [String], default: [] },
}, { _id: false });

const StudentOverallWeakTopicsSchema = new mongoose.Schema({
  studentId:     { type: String, required: true },
  studentName:   { type: String, default: '' },
  centerId:      { type: String, required: true },
  testsIncluded: { type: [String], default: [] }, // tests student attempted
  totalTests:    { type: Number, default: 0 },

  totalScore:    { type: Number, default: 0 },

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

// Unique index per student
StudentOverallWeakTopicsSchema.index({ studentId: 1 }, { unique: true });
StudentOverallWeakTopicsSchema.index({ centerId: 1 });

export default mongoose.models.StudentOverallWeakTopics || mongoose.model('StudentOverallWeakTopics', StudentOverallWeakTopicsSchema);
