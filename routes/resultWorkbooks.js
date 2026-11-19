import express from 'express';
import mongoose from 'mongoose';
import multer from 'multer';
import ExcelJS from 'exceljs';
const Model=mongoose.models.ResultWorkbook || mongoose.model('ResultWorkbook',new mongoose.Schema({_id:String,filename:String,data:Buffer,updatedAt:Date}));
const upload=multer({storage:multer.memoryStorage(),limits:{fileSize:10*1024*1024}});
export const resultWorkbooksRouter=express.Router();
const router=resultWorkbooksRouter;
router.use((req,res,next)=>{res.set('Cache-Control','no-store');if(!['admin','centre','bog'].includes(req.user?.role))return res.sendStatus(403);next();});
function key(q){if(!['JEE','NEET'].includes(q.stream)|| (q.stream==='JEE'&&!['MAIN','ADVANCED'].includes(q.branch))||typeof q.testKey!=='string'||!q.testKey.trim()||q.testKey.length>100||q.testKey.includes(',')||q.testKey==='ALL_FMT')throw Error('Select one test, stream and branch.');return JSON.stringify([q.stream,q.stream==='NEET'?null:q.branch,q.testKey.trim().toUpperCase()]);}
router.post('/',(req,res,next)=>{if(req.user.role!=='admin')return res.sendStatus(403);upload.single('file')(req,res,e=>e?res.status(400).json({message:e.message}):next());},async(req,res)=>{try{const id=key(req.query);if(!req.file||! /\.xlsx$/i.test(req.file.originalname))throw Error('Choose an Excel workbook (.xlsx).');const book=new ExcelJS.Workbook();await book.xlsx.load(req.file.buffer);if(!book.worksheets.length)throw Error('The workbook has no sheets.');await Model.findOneAndUpdate({_id:id},{$set:{filename:req.file.originalname,data:req.file.buffer,updatedAt:new Date()}},{upsert:true});res.json({filename:req.file.originalname});}catch(e){res.status(400).json({message:e.message});}});
router.get('/',async(req,res)=>{try{const doc=await Model.findById(key(req.query));if(!doc)return res.status(404).json({message:'No result Excel has been uploaded for this test.'});res.type(/\.xlsx$/i.test(doc.filename)?'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':'application/vnd.ms-excel').attachment(doc.filename).send(doc.data);}catch(e){res.status(400).json({message:e.message});}});
