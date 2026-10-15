import mongoose from 'mongoose';
const schema = new mongoose.Schema({
  _id: String,
  userId: { type: String, required: true, index: true },
  name: String,
  centres: [String],
  loginAt: { type: Date, required: true, index: true },
  lastSeenAt: { type: Date, required: true },
  endedAt: Date,
  activeUntil: Date,
  sessionMs: { type: Number, default: 0 },
  activeMs: { type: Number, default: 0 },
  revision: { type: Number, default: 0 },
}, { bufferCommands: false });
export default mongoose.model('PortalLoginSession', schema);
