import mongoose from 'mongoose';
const schema = new mongoose.Schema({
  facultyId: String, serialNumber: String, contact: String, projectManager: String, mentor: String, degree: String, college: String, passingYear: String, joiningDate: String,
  year: String, email: String, name: String, test: String, subject: String, centres: [String],
  attempted: Number, correct: Number, marks: Number, maxMarks: Number, totalQuestions: Number,
  accuracy: Number, qualification: String, status: String, date: String,
}, { timestamps: true });
schema.index({ year: 1, email: 1, test: 1, subject: 1 }, { unique: true });
export default mongoose.model('FacultyTestResult', schema);
