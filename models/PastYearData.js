import mongoose from 'mongoose';

const PastYearDataSchema = new mongoose.Schema({}, { strict: false, timestamps: true });

PastYearDataSchema.index({ 'Sponsor': 1, 'Centre Code': 1, 'Year': 1 });

export default mongoose.models.PastYearData || mongoose.model('PastYearData', PastYearDataSchema);
