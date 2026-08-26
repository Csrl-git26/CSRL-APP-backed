import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad1 = "const rawRows = chart?.chartData ?? buildStudentChartData(studentTests, testColumns);"
good1 = "const actualChart = prefetchedChart || chart;\n    const rawRows = actualChart?.chartData ?? buildStudentChartData(studentTests, testColumns);"

bad2 = "}, [chart, studentTests, testColumns, stream]);"
good2 = "}, [chart, prefetchedChart, studentTests, testColumns, stream]);"

bad3 = "() => chart?.weakSubject ?? computeWeakSubject(studentTests, testColumns),"
good3 = "() => (prefetchedChart || chart)?.weakSubject ?? computeWeakSubject(studentTests, testColumns),"

bad4 = "[chart, studentTests, testColumns]"
good4 = "[chart, prefetchedChart, studentTests, testColumns]"

bad5 = "const weakSubjectsArr = overallWeakTopicsData?.overallWeakSubjects || [];"
good5 = "const actualWeakTopics = prefetchedWeakTopics || overallWeakTopicsData;\n  const weakSubjectsArr = actualWeakTopics?.overallWeakSubjects || [];"

bad6 = "const weakTopicsBySubject = overallWeakTopicsData?.overallWeakTopics || {};"
good6 = "const weakTopicsBySubject = actualWeakTopics?.overallWeakTopics || {};"

bad7 = "const overallRecommendations = overallWeakTopicsData?.overallRecommendations || [];"
good7 = "const overallRecommendations = actualWeakTopics?.overallRecommendations || [];"

content = content.replace(bad1, good1)
content = content.replace(bad2, good2)
content = content.replace(bad3, good3)
content = content.replace(bad4, good4)
content = content.replace(bad5, good5)
content = content.replace(bad6, good6)
content = content.replace(bad7, good7)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched StudentProfileView to dynamically use prefetched props")
