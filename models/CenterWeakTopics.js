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

const CenterWeakTopicsSchema = new mongoose.Schema({
  centerId:            { type: String, required: true },
  testId:              { type: String, required: true },
  
  studentCount:        { type: Number, required: true },
  averageScore:        { type: Number, required: true },

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

// Unique compound index per center+test
CenterWeakTopicsSchema.index({ centerId: 1, testId: 1 }, { unique: true });

export default mongoose.models.CenterWeakTopics || mongoose.model('CenterWeakTopics', CenterWeakTopicsSchema);
