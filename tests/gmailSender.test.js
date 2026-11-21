import test from 'node:test';
import assert from 'node:assert/strict';
import mongoose from 'mongoose';
import express from 'express';
import {encrypt,decrypt,mime,begin,launch,complete,sendGmail,enabled} from '../services/gmailSender.js';
import {gmailAdminRouter} from '../routes/gmail.js';
test('Gmail encryption, OAuth binding and sender verification',async t=>{
 process.env.GOOGLE_CLIENT_ID='test-client';process.env.GOOGLE_CLIENT_SECRET='test-secret';process.env.GMAIL_SENDER_EMAIL='sender@gmail.com';
 const stateModel=mongoose.models.GmailOAuthState,connection=mongoose.models.GmailConnection;
 const originals={create:stateModel.create,updateOne:stateModel.updateOne,findOneAndUpdate:stateModel.findOneAndUpdate,findOneAndDelete:stateModel.findOneAndDelete,connUpdate:connection.updateOne,fetch:global.fetch};
 t.after(()=>{stateModel.create=originals.create;stateModel.updateOne=originals.updateOne;stateModel.findOneAndUpdate=originals.findOneAndUpdate;stateModel.findOneAndDelete=originals.findOneAndDelete;connection.updateOne=originals.connUpdate;global.fetch=originals.fetch;});
 const ciphertext=encrypt('refresh-secret');assert.equal(decrypt(ciphertext),'refresh-secret');assert.ok(!ciphertext.includes('refresh-secret'));const corrupt=Buffer.from(ciphertext,'base64');corrupt[13]^=1;assert.throws(()=>decrypt(corrupt.toString('base64')));
 let record,saved=0;stateModel.create=async r=>{record={...r,launched:false};};stateModel.updateOne=async(f,u)=>{Object.assign(record,u.$set);};stateModel.findOneAndUpdate=(f,u)=>({lean:async()=>{if(record.launched||f.cookieHash!==record.cookieHash)return null;Object.assign(record,u.$set);return record;}});stateModel.findOneAndDelete=f=>({lean:async()=>f.cookieHash===record.cookieHash&&record.launched?record:null});connection.updateOne=async()=>{saved++;};
 const start=await begin(),url=new URL(start.url);assert.equal(url.pathname,'/api/gmail/launch');const google=new URL(await launch(url.searchParams.get('state'),url.searchParams.get('ticket')));assert.equal(google.searchParams.get('code_challenge_method'),'S256');assert.equal(google.searchParams.get('access_type'),'offline');assert.match(google.searchParams.get('scope'),/gmail.send/);await assert.rejects(launch(url.searchParams.get('state'),url.searchParams.get('ticket')));await assert.rejects(complete('code',url.searchParams.get('state'),'wrong-cookie'));
 global.fetch=async target=>({ok:true,json:async()=>target.includes('/token')?{access_token:'token',refresh_token:'refresh',scope:'https://www.googleapis.com/auth/gmail.send'}:{email_verified:true,email:'wrong@gmail.com'}});await assert.rejects(complete('code',url.searchParams.get('state'),url.searchParams.get('ticket')));assert.equal(saved,0);
 global.fetch=async target=>({ok:true,json:async()=>target.includes('/token')?{access_token:'token',refresh_token:'refresh',scope:'https://www.googleapis.com/auth/gmail.send'}:{email_verified:true,email:'sender@gmail.com'}});await complete('code',url.searchParams.get('state'),url.searchParams.get('ticket'));assert.equal(saved,1);
});
test('Gmail MIME preserves HTML and attachment; rejects header injection',()=>{const raw=mime({subject:'प्रगति result',html:'<h1>Result</h1>',filename:'result.xlsx',attachment:Buffer.from('workbook').toString('base64')},'user@example.com');assert.match(raw,/To: user@example.com/);assert.match(raw,/From:.*sender@gmail.com/);assert.ok(raw.includes(Buffer.from('<h1>Result</h1>').toString('base64')));assert.ok(raw.includes(Buffer.from('workbook').toString('base64')));assert.throws(()=>mime({},'x@example.com\r\nBcc: other@example.com'));});
test('Gmail setup endpoints deny non-admin users',async t=>{const app=express();app.use((req,res,next)=>{req.user={role:'centre'};next();});app.use(gmailAdminRouter);const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));t.after(()=>server.close());for(const [path,method] of [['/status','GET'],['/connect','POST']])assert.equal((await fetch(`http://127.0.0.1:${server.address().port}${path}`,{method})).status,403);});
test('Gmail network failures require review rather than blind retry',async t=>{const model=mongoose.models.GmailConnection,original=model.findById,fetcher=global.fetch;model.findById=()=>({lean:async()=>({email:'sender@gmail.com',token:encrypt('refresh')})});t.after(()=>{model.findById=original;global.fetch=fetcher;});global.fetch=async url=>{if(url.includes('/token'))return {ok:true,json:async()=>({access_token:'a'})};throw Error('network');};await assert.rejects(sendGmail({subject:'result',html:'ok',filename:'r.xlsx',attachment:'eA=='},'user@example.com'),e=>e.uncertain===true);process.env.RESULT_EMAIL_ENABLED='false';assert.equal(await enabled(),false);});
test('Callback explains missing cookies and denied consent without exposing secrets',async t=>{
 const {gmailPublicRouter}=await import('../routes/gmail.js');
 const {connectionFailure}=await import('../services/gmailSender.js');
 assert.ok(!JSON.stringify(connectionFailure(Error('secret-token'))).includes('secret-token'));
 const app=express();app.use(gmailPublicRouter);const server=app.listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));t.after(()=>server.close());
 const base='http://127.0.0.1:'+server.address().port;
 const missing=await fetch(base+'/callback?code=private-code&state=private-state');
 const body=await missing.text();assert.equal(missing.status,400);assert.match(body,/CONNECTION_COOKIE_MISSING/);assert.ok(!body.includes('private-code'));
 assert.match(await (await fetch(base+'/callback?error=access_denied')).text(),/PERMISSION_DENIED/);
});
test('Google credential rejection gives actionable error without returning Google payload',async t=>{
 const model=mongoose.models.GmailOAuthState,original=model.findOneAndDelete,fetcher=global.fetch;
 model.findOneAndDelete=()=>({lean:async()=>({verifier:encrypt('verifier')})});
 global.fetch=async()=>({ok:false,json:async()=>({error:'invalid_client',error_description:'private-details'})});
 t.after(()=>{model.findOneAndDelete=original;global.fetch=fetcher;});
 await assert.rejects(complete('code','state','cookie'),e=>e.connectionCode==='GOOGLE_CLIENT_INVALID'&&!e.message.includes('private-details'));
});
