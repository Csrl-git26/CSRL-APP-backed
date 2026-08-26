const { MongoClient } = require('mongodb');
require('dotenv').config();
async function run() {
  const client = new MongoClient(process.env.MONGO_URI);
  await client.connect();
  const db = client.db('csrl');
  const categories = await db.collection('studentprofiles').distinct('CATEGORY');
  console.log(categories);
  await client.close();
}
run();
