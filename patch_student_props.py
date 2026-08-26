import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad1 = "export default function StudentProfileView({ profile, studentTests, testColumns, isHiddenForBulk = false }) {"
good1 = "export default function StudentProfileView({ profile, studentTests, testColumns, isHiddenForBulk = false, prefetchedChart = null, prefetchedWeakTopics = null }) {"

bad2 = """  const [chart, setChart] = React.useState(null);"""
good2 = """  const [chart, setChart] = React.useState(prefetchedChart);"""

bad3 = """  const [overallWeakTopicsData, setOverallWeakTopicsData] = React.useState(null);"""
good3 = """  const [overallWeakTopicsData, setOverallWeakTopicsData] = React.useState(prefetchedWeakTopics);"""

bad4 = """  React.useEffect(() => {
    if (!profile?.ROLL_KEY) return;
    let cancelled = false;
    getStudentOverallWeakTopics(profile.ROLL_KEY).then((res) => {
      if (!cancelled && res.success && res.data) {
        if (res.data.overallWeakSubjects) setOverallWeakSubjects(res.data.overallWeakSubjects);
        setOverallWeakTopicsData(res.data);
      }
    });
    
    fetchStudentChart(null, profile.ROLL_KEY, null).then((res) => {
      console.log('DEBUG API RESPONSE:', res);
      if (!cancelled && res) setChart(res);
    }).catch(() => {});
    
    return () => { cancelled = true; };
  }, [profile?.ROLL_KEY]);"""

good4 = """  React.useEffect(() => {
    if (!profile?.ROLL_KEY) return;
    if (prefetchedChart && prefetchedWeakTopics) {
      // If data is prefetched (e.g. bulk export), don't fetch again
      if (prefetchedWeakTopics.overallWeakSubjects) setOverallWeakSubjects(prefetchedWeakTopics.overallWeakSubjects);
      return;
    }
    
    let cancelled = false;
    getStudentOverallWeakTopics(profile.ROLL_KEY).then((res) => {
      if (!cancelled && res.success && res.data) {
        if (res.data.overallWeakSubjects) setOverallWeakSubjects(res.data.overallWeakSubjects);
        setOverallWeakTopicsData(res.data);
      }
    });
    
    fetchStudentChart(null, profile.ROLL_KEY, null).then((res) => {
      if (!cancelled && res) setChart(res);
    }).catch(() => {});
    
    return () => { cancelled = true; };
  }, [profile?.ROLL_KEY, prefetchedChart, prefetchedWeakTopics]);"""

content = content.replace(bad1, good1).replace(bad2, good2).replace(bad3, good3).replace(bad4, good4)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched StudentProfileView props successfully")
