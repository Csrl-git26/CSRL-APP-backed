import mongoose from 'mongoose';
const recipient = new mongoose.Schema({
  email: String, name: String, roles: [String],
  status: { type: String, enum: ['pending', 'sending', 'sent', 'failed', 'review', 'skipped'], default: 'pending' },
  firstAttempt: Date, lockUntil: Date, providerId: String, error: String,
}, { _id: false });
const schema = new mongoose.Schema({
  _id: String, selection: mongoose.Schema.Types.Mixed, report: mongoose.Schema.Types.Mixed,
  subject: String, html: String, text: String, attachment: String, filename: String,
  recipients: [recipient], skippedUsers: [String],
  state: { type: String, enum: ['draft', 'queued', 'complete'], default: 'draft' },
  createdBy: String, createdAt: { type: Date, default: Date.now }, startedAt: Date,
});
schema.index({ state: 1, createdAt: -1 });
export default mongoose.models.ResultNotification || mongoose.model('ResultNotification', schema);
