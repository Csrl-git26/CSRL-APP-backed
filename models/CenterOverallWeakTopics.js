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

const CenterOverallWeakTopicsSchema = new mongoose.Schema({
  centerId:      { type: String, required: true },
  stream:        { type: String, default: 'JEE' },
  testsIncluded: { type: [String], default: [] },
  totalTests:    { type: Number, default: 0 },

  studentCount:  { type: Number, default: 0 }, // Average student count across tests or max student count
  averageScore:  { type: Number, default: 0 }, // Average score across tests

  strongTopics:   { type: mongoose.Schema.Types.Mixed, default: [] },
  moderateTopics: { type: mongoose.Schema.Types.Mixed, default: [] },
  weakTopics:     { type: mongoose.Schema.Types.Mixed, default: [] },

  // Separate metrics preserve the existing string-based classification API.
  topicRatesVersion: { type: Number },
  topicRates: {
    type: [new mongoose.Schema({
      topic: { type: String, required: true },
      subject: String,
      attempted: Number,
      correct: Number,
      totalPossible: Number,
      attemptPercentage: Number,
      accuracyPercentage: { type: Number, default: null },
    }, { _id: false })],
    default: undefined,
  },

  subjectWise: {
    PHYSICS:     { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    CHEMISTRY:   { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    MATHEMATICS: { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    BOTANY:      { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
    ZOOLOGY:     { type: SubjectWiseSchema, default: () => ({ strong: [], moderate: [], weak: [] }) },
  },

  computedAt: { type: Date, default: Date.now },
}, { timestamps: true });

// Unique index per center
CenterOverallWeakTopicsSchema.index({ centerId: 1, stream: 1 }, { unique: true });

export default mongoose.models.CenterOverallWeakTopics || mongoose.model('CenterOverallWeakTopics', CenterOverallWeakTopicsSchema);
