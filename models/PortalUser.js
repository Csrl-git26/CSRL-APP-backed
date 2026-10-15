import mongoose from 'mongoose';
// Overrides keep deleted built-in directory entries disabled across deployments.
const schema = new mongoose.Schema({
  _id: String,
  role: { type: String, enum: ['centre', 'admin'], required: true },
  userId: { type: String, required: true },
  name: { type: String, required: true },
  centres: [String],
  disabled: { type: Boolean, default: false },
  version: { type: String, required: true },
  changedBy: String,
}, { timestamps: true, bufferCommands: false });
export default mongoose.model('PortalUser', schema);
