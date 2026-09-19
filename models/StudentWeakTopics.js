import mongoose from 'mongoose';

// Topic-level weak classification
// Items stored as { topic: string, ar: number, acc: number } objects (or plain strings for legacy data)
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

const StudentWeakTopicsSchema = new mongoose.Schema({
  studentId:   { type: String, required: true }, // The prompt specifies roll number as unique id, which maps to studentId
  studentName: { type: String, default: '' },
  testId:      { type: String, required: true },
  centerId:    { type: String, required: true },
  
  totalScore:  { type: Number, default: 0 },

  strongTopics:   { type: mongoose.Schema.Types.Mixed, default: [] },
  moderateTopics: { type: mongoose.Schema.Types.Mixed, default: [] },
  weakTopics:     { type: mongoose.Schema.Types.Mixed, default: [] },

  subjectWise: {
    PHYSICS:     { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    CHEMISTRY:   { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    MATHEMATICS: { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    BOTANY:      { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    ZOOLOGY:     { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
  },

  computedAt: { type: Date, default: Date.now },
}, { timestamps: true });

// Unique compound index per student+test
StudentWeakTopicsSchema.index({ studentId: 1, testId: 1 }, { unique: true });
StudentWeakTopicsSchema.index({ centerId: 1, testId: 1 });

export default mongoose.models.StudentWeakTopics || mongoose.model('StudentWeakTopics', StudentWeakTopicsSchema);
