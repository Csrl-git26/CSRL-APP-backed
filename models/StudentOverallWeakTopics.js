import mongoose from 'mongoose';

// Items stored as { topic: string, ar: number, acc: number } objects
const TopicItemSchema = new mongoose.Schema({
  topic: { type: String },
  ar:    { type: Number },  // Attempt Rate % (0-100)
  acc:   { type: Number },  // Accuracy % (0-100)
}, { _id: false });

const SubjectWiseSchema = new mongoose.Schema({
  strong:   { type: [TopicItemSchema], default: [] },
  moderate: { type: [TopicItemSchema], default: [] },
  weak:     { type: [TopicItemSchema], default: [] },
}, { _id: false });

const StudentOverallWeakTopicsSchema = new mongoose.Schema({
  studentId:     { type: String, required: true },
  studentName:   { type: String, default: '' },
  centerId:      { type: String, required: true },
  testsIncluded: { type: [String], default: [] }, // tests student attempted
  totalTests:    { type: Number, default: 0 },

  totalScore:    { type: Number, default: 0 },

  strongTopics:   { type: mongoose.Schema.Types.Mixed, default: [] },
  moderateTopics: { type: mongoose.Schema.Types.Mixed, default: [] },
  weakTopics:     { type: mongoose.Schema.Types.Mixed, default: [] },

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
