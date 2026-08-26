import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_usememo = """const chartData = useMemo(() => {
    const actualChart = prefetchedChart || chart;
  const actualWeakTopics = prefetchedWeakTopics || overallWeakTopicsData;
    const rawRows = actualChart?.chartData ?? buildStudentChartData(studentTests, testColumns);"""

good_usememo = """const actualChart = prefetchedChart || chart;
  const actualWeakTopics = prefetchedWeakTopics || overallWeakTopicsData;
  
  const chartData = useMemo(() => {
    const rawRows = actualChart?.chartData ?? buildStudentChartData(studentTests, testColumns);"""

if bad_usememo in content:
    content = content.replace(bad_usememo, good_usememo)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed variable scope successfully!")
else:
    print("Could not find the bad useMemo block")
