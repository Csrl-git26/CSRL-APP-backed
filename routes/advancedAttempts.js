import express from 'express';
import { randomUUID } from 'node:crypto';
import AdvancedAttemptSheet from '../models/AdvancedAttemptSheet.js';
import { TestBranch } from '../services/testBranchService.js';
import { loadApplicationData } from '../services/dbService.js';
import { parseAdvancedAttemptRows, aggregateAttemptRecords } from '../services/advancedAttemptService.js';
export function createAdvancedAttemptsRouter({Model=AdvancedAttemptSheet,Catalog=TestBranch,loadData=loadApplicationData}={}) {
  const router=express.Router();
  const fail=(status,message)=>Object.assign(new Error(message),{status});
  router.use((req,res,next)=>{res.set('Cache-Control','no-store');if(req.user?.role!=='admin')return res.status(403).json({message:'Admin access required.'});next();});
  const wrap=fn=>async(req,res)=>{try{await fn(req,res);}catch(e){res.status(e.status||503).json({message:e.status?e.message:'Unable to access Advanced attempt data. Please retry.'});}};
  async function validateScope(input) {
    const {stream,branch,testId}=input;
    if(stream!=='JEE'||branch!=='ADVANCED')throw fail(400,'This upload is only for JEE Advanced. Main and NEET are not supported.');
    if(typeof testId!=='string'||!testId.trim()||testId.length>100)throw fail(400,'Select an existing JEE Advanced test.');
    const test=await Catalog.findOne({testId}).lean();
    if(!test || test.stream!=='JEE'||test.branch!=='ADVANCED')throw fail(400,'The selected test is not registered as JEE Advanced. Upload its Advanced results first.');
    return testId;
  }
  router.get('/',wrap(async(req,res)=>{
    const testId=await validateScope(req.query);const saved=await Model.findById(testId).lean();
    res.json({saved:saved?{version:saved.version,count:saved.records.length,filename:saved.filename,uploadedAt:saved.updatedAt}:null});
  }));
  async function prepare(body) {
    const testId=await validateScope(body);const data=await loadData();
    const records=parseAdvancedAttemptRows(body.rows,data.profiles);
    return {testId,records};
  }
  router.post('/preview',wrap(async(req,res)=>{
    const {testId,records}=await prepare(req.body);const saved=await Model.findById(testId).lean();
    res.json({testId,count:records.length,hasSubjects:!!records[0].subjects,questionCounts:[...new Set(records.map(r=>r.totalQuestions))].sort((a,b)=>a-b),centres:[...new Set(records.map(r=>r.centre))].sort(),metrics:aggregateAttemptRecords(records),version:saved?.version||null,previousCount:saved?.records.length||0,preview:records.slice(0,10)});
  }));
  router.post('/',wrap(async(req,res)=>{
    if(req.body.confirm!=='UPLOAD')throw fail(400,'Preview and confirm this upload first.');
    const {testId,records}=await prepare(req.body);
    const values={records,version:randomUUID(),filename:String(req.body.filename||'').slice(0,200),uploadedBy:req.user.loginUserId||req.user.id};
    if(req.body.version) {
      const saved=await Model.findOneAndUpdate({_id:testId,version:req.body.version},{$set:values},{new:true}).lean();
      if(!saved)throw fail(409,'This test was updated by another upload. Preview again before replacing it.');
    }else{
      try{await Model.create({_id:testId,...values});}catch(e){if(e.code===11000)throw fail(409,'This test already has an upload. Preview again before replacing it.');throw e;}
    }
    res.json({success:true,testId,count:records.length,message:`Saved attempt and accuracy counts for ${records.length} JEE Advanced students.`});
  }));
  return router;
}
export default createAdvancedAttemptsRouter();
