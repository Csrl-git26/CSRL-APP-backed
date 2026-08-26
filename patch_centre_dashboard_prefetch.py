import sys
import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Add imports
imports_to_add = """import { getStudentOverallWeakTopics } from '../services/weakTopicApi';
import { fetchStudentChart } from '../services/dataService';"""

if "getStudentOverallWeakTopics" not in content:
    content = content.replace("import { useAuth }", imports_to_add + "\nimport { useAuth }")

# Add state
if "const [prefetchedData, setPrefetchedData] = useState({});" not in content:
    content = content.replace("const [searchTerm,       setSearchTerm]       = useState('');", "const [searchTerm,       setSearchTerm]       = useState('');\n  const [prefetchedData, setPrefetchedData] = useState({});")


old_handle_bulk = """  const handleBulkExportPDF = async () => {
    if (!filteredStudents.length) return;
    setIsExportingBulk(true);
    setBulkExportProgress(`Starting export...`);
    
    setTimeout(async () => {
      try {
        // Using static imports to avoid dynamic import interop issues
        
        let pdf = null;
        let count = 0;
        
        for (const student of filteredStudents) {"""


new_handle_bulk = """  const handleBulkExportPDF = async () => {
    if (!filteredStudents.length) return;
    setIsExportingBulk(true);
    setBulkExportProgress(`Preparing...`);
    
    setTimeout(async () => {
      try {
        const dataMap = {};
        let fetched = 0;
        for (let i = 0; i < filteredStudents.length; i += 5) {
          const chunk = filteredStudents.slice(i, i + 5);
          await Promise.all(chunk.map(async (student) => {
            const roll = student.ROLL_KEY;
            const [chartRes, topicsRes] = await Promise.all([
               fetchStudentChart(null, roll, null).catch(() => null),
               getStudentOverallWeakTopics(roll).catch(() => null)
            ]);
            dataMap[roll] = {
               chart: chartRes || null,
               topics: topicsRes?.data || null
            };
            fetched++;
          }));
          setBulkExportProgress(`Fetched ${fetched} / ${filteredStudents.length}`);
        }
        
        setPrefetchedData(dataMap);
        setBulkExportProgress(`Generating layout...`);
        
        // Wait for React to render the newly fetched data
        await new Promise(r => setTimeout(r, 1000));
        
        // Using static imports to avoid dynamic import interop issues
        let pdf = null;
        let count = 0;
        
        for (const student of filteredStudents) {"""

content = content.replace(old_handle_bulk, new_handle_bulk)

# Patch the rendering of StudentProfileView inside isExportingBulk
old_render = """      {isExportingBulk && (
        <div style={{ position: 'absolute', opacity: 0, pointerEvents: 'none', zIndex: -10000 }}>
          {filteredStudents.map(student => (
            <StudentProfileView 
              key={student.ROLL_KEY}
              profile={student} 
              studentTests={data.tests.find(t => t.ROLL_KEY === student.ROLL_KEY) || {}} 
              testColumns={data.testColumns} 
              isHiddenForBulk={true} 
            />
          ))}
        </div>
      )}"""

new_render = """      {isExportingBulk && (
        <div style={{ position: 'absolute', opacity: 0, pointerEvents: 'none', zIndex: -10000 }}>
          {filteredStudents.map(student => (
            <StudentProfileView 
              key={student.ROLL_KEY}
              profile={student} 
              studentTests={data.tests.find(t => t.ROLL_KEY === student.ROLL_KEY) || {}} 
              testColumns={data.testColumns} 
              isHiddenForBulk={true}
              prefetchedChart={prefetchedData[student.ROLL_KEY]?.chart || null}
              prefetchedWeakTopics={prefetchedData[student.ROLL_KEY]?.topics || null}
            />
          ))}
        </div>
      )}"""

content = content.replace(old_render, new_render)

with open(filepath, 'w') as f:
    f.write(content)
print("Successfully patched handleBulkExportPDF for prefetching data")
