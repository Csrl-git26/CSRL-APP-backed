import os
import re

api_file = '/Users/surya/Desktop/CSRL-APP-frontend/src/services/weakTopicApi.js'
with open(api_file, 'r') as f:
    api_code = f.read()

# Add the two new APIs if they don't exist
if 'uploadTopicMap' not in api_code:
    new_apis = """
/**
 * uploadTopicMap — upload a standalone topic mapping CSV
 */
export async function uploadTopicMap(formData) {
  clearWeakTopicsFrontendCache();
  const res = await fetch(`${BASE}/api/admin/weak-topics/upload-topic-map`, {
    method:  'POST',
    headers: authHeaders(),
    body:    formData,
  });
  return handleResponse(res);
}

/**
 * uploadMarksSheet — upload a marks-only CSV (requires Topic Map to be uploaded first)
 */
export async function uploadMarksSheet(formData) {
  clearWeakTopicsFrontendCache();
  const res = await fetch(`${BASE}/api/admin/weak-topics/upload-marks-sheet`, {
    method:  'POST',
    headers: authHeaders(),
    body:    formData,
  });
  return handleResponse(res);
}
"""
    api_code += new_apis
    with open(api_file, 'w') as f:
        f.write(api_code)
    print("Patched weakTopicApi.js")

modal_file = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/UploadMarksAwardSheetModal.jsx'
with open(modal_file, 'r') as f:
    modal_code = f.read()

if 'uploadType' not in modal_code:
    # 1. Update imports
    modal_code = modal_code.replace(
        "import { uploadTestSheet } from '../services/weakTopicApi';",
        "import { uploadTestSheet, uploadTopicMap, uploadMarksSheet } from '../services/weakTopicApi';"
    )
    
    # 2. Add state for uploadType
    modal_code = modal_code.replace(
        "const [testId, setTestId] = useState('');",
        "const [testId, setTestId] = useState('');\n  const [uploadType, setUploadType] = useState('marks'); // 'topic' or 'marks'"
    )
    
    # 3. Update handleUpload
    old_upload = """    try {
      const res = await uploadTestSheet(formData);"""
    
    new_upload = """    try {
      let res;
      if (uploadType === 'topic') {
        res = await uploadTopicMap(formData);
      } else {
        res = await uploadMarksSheet(formData);
      }"""
    modal_code = modal_code.replace(old_upload, new_upload)
    
    # 4. Update the text descriptions
    old_desc = "Upload a single unified CSV test sheet (combining headers, topics, answer key, and student marks) to compute center and student weak subjects."
    new_desc = "Step 1: Upload the Topic Mapping CSV. Step 2: Upload the Marks Awarded CSV. You must upload the Topic Map before the Marks Sheet."
    modal_code = modal_code.replace(old_desc, new_desc)
    
    # 5. Add Radio buttons to select uploadType before the testId input
    old_test_id = """          <div style={{ marginBottom: 20 }}>
            <label className="label" style={{ fontSize: 12, fontWeight: 700 }}>
              Test Name / ID"""
              
    new_test_id = """          <div style={{ marginBottom: 20, display: 'flex', gap: '20px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 14, cursor: 'pointer' }}>
              <input type="radio" name="uploadType" checked={uploadType === 'topic'} onChange={() => { setUploadType('topic'); setFile(null); setStatus('idle'); }} />
              1. Topic Mapping CSV
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 14, cursor: 'pointer' }}>
              <input type="radio" name="uploadType" checked={uploadType === 'marks'} onChange={() => { setUploadType('marks'); setFile(null); setStatus('idle'); }} />
              2. Marks Awarded CSV
            </label>
          </div>

          <div style={{ marginBottom: 20 }}>
            <label className="label" style={{ fontSize: 12, fontWeight: 700 }}>
              Test Name / ID"""
    modal_code = modal_code.replace(old_test_id, new_test_id)
    
    # 6. Change subtext
    old_subtext = "Row 1=Headers, Row 2=Topics, Row 3=Answers, Row 4+=Marks"
    new_subtext = "{uploadType === 'topic' ? 'Format: Question, Topic, Subject' : 'Format: Location, Roll No, Name, Q1, Q2...'}"
    modal_code = modal_code.replace(old_subtext, new_subtext)
    
    with open(modal_file, 'w') as f:
        f.write(modal_code)
    print("Patched UploadMarksAwardSheetModal.jsx")
