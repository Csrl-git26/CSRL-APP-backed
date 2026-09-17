import mongoose from 'mongoose';

const SubjectWiseSchema = new mongoose.Schema({
  strong:   { type: [String], default: [] },
  moderate: { type: [String], default: [] },
  weak:     { type: [String], default: [] },
}, { _id: false });

const CenterWeakTopicsSchema = new mongoose.Schema({
  centerId:            { type: String, required: true },
  testId:              { type: String, required: true },
  
  studentCount:        { type: Number, required: true },
  averageScore:        { type: Number, required: true },

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

// Unique compound index per center+test
CenterWeakTopicsSchema.index({ centerId: 1, testId: 1 }, { unique: true });

export default mongoose.models.CenterWeakTopics || mongoose.model('CenterWeakTopics', CenterWeakTopicsSchema);
