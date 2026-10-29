import mongoose from 'mongoose';
// One atomic snapshot per JEE Advanced test; separate from marks and Main/NEET data.
const schema = new mongoose.Schema({
  _id: String, version: { type: String, required: true },
  records: [{ _id: false, roll: String, name: String, centre: String, totalQuestions: Number, notAttempted: Number, attempted: Number, incorrect: Number, correct: Number }],
  filename: String, uploadedBy: String,
}, { timestamps: true });
export default mongoose.models.AdvancedAttemptSheet || mongoose.model('AdvancedAttemptSheet', schema);
