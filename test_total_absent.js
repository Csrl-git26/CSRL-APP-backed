const { nestedToFlat, parseTestColumn } = require('./utils/testColumns.js');
const fs = require('fs');
const { MongoClient } = require('mongodb');

async function run() {
  const client = new MongoClient('mongodb+srv://surya:qIqg2X2a537fK63s@csrl.6dhyi.mongodb.net/csrl_db?retryWrites=true&w=majority');
  await client.connect();
  const db = client.db('csrl_db');
  
  // Find Akash Chauhan (roll 2722001)
  const p = await db.collection('profiles').findOne({ ROLL_KEY: '2722001' });
  const t = await db.collection('testscores').findOne({ ROLL_KEY: '2722001' });
  
  console.log("Raw nested tests:", JSON.stringify(t.tests, null, 2));
  
  const flat = nestedToFlat(t);
  console.log("Flat test doc:", JSON.stringify(flat, null, 2));
  
  await client.close();
}
run().catch(console.error);
