import mongoose from 'mongoose';

const SubjectWiseSchema = new mongoose.Schema({
  strong:   { type: [String], default: [] },
  moderate: { type: [String], default: [] },
  weak:     { type: [String], default: [] },
}, { _id: false });

const CenterOverallWeakTopicsSchema = new mongoose.Schema({
  centerId:      { type: String, required: true },
  testsIncluded: { type: [String], default: [] },
  totalTests:    { type: Number, default: 0 },

  studentCount:  { type: Number, default: 0 }, // Average student count across tests or max student count
  averageScore:  { type: Number, default: 0 }, // Average score across tests

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

// Unique index per center
CenterOverallWeakTopicsSchema.index({ centerId: 1 }, { unique: true });

export default mongoose.models.CenterOverallWeakTopics || mongoose.model('CenterOverallWeakTopics', CenterOverallWeakTopicsSchema);
