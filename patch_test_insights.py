import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Imports
old_imports = "import { Loader2, Trophy, BarChart3, TrendingDown, Users, AlertCircle } from 'lucide-react';"
new_imports = "import { Loader2, Trophy, BarChart3, TrendingDown, Users, AlertCircle, Search, Eye } from 'lucide-react';"
content = content.replace(old_imports, new_imports)

# 2. Props
old_props = """  showStudentCard,
  hideSubjectAverages = false,
}) {"""
new_props = """  showStudentCard,
  hideSubjectAverages = false,
  onViewStudent,
}) {"""
content = content.replace(old_props, new_props)

# 3. States and Memo lists
old_states = """  const [rankMode, setRankMode] = useState('all');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedCenter, setSelectedCenter] = useState('ALL');

  const centerOptions = useMemo("""
new_states = """  const [rankMode, setRankMode] = useState('all');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedCenter, setSelectedCenter] = useState('ALL');

  const [searchTerm, setSearchTerm] = useState('');
  const [filterSponsor, setFilterSponsor] = useState('ALL');
  const [filterCategory, setFilterCategory] = useState('ALL');
  const [filterGender, setFilterGender] = useState('ALL');

  const sponsorsList = useMemo(() => ['ALL', ...[...new Set((rankedStudents || []).map((p) => p.sponsor).filter(Boolean))]], [rankedStudents]);
  const categories = useMemo(() => ['ALL', ...[...new Set((rankedStudents || []).map((p) => p.category).filter(Boolean))]], [rankedStudents]);
  const gendersList = useMemo(() => ['ALL', ...[...new Set((rankedStudents || []).map((p) => p.gender).filter(Boolean))]], [rankedStudents]);

  const centerOptions = useMemo("""
content = content.replace(old_states, new_states)

# 4. filteredRanked logic
old_filtered = """  const filteredRanked = useMemo(() => {
    const centerFiltered = selectedCenter === 'ALL'
      ? rankedStudents
      : rankedStudents.filter((r) => r.center === selectedCenter);

    const highToLow = [...centerFiltered].sort((a, b) => (b.marks - a.marks) || a.rank - b.rank);
    const lowToHigh = [...centerFiltered].sort((a, b) => (a.marks - b.marks) || a.rank - b.rank);

    let selected = highToLow;
    if (rankMode === 'top10') selected = highToLow.slice(0, 10);
    if (rankMode === 'bottom10') selected = lowToHigh.slice(0, 10);

    return sortOrder === 'asc'
      ? [...selected].sort((a, b) => (a.marks - b.marks) || a.rank - b.rank)
      : [...selected].sort((a, b) => (b.marks - a.marks) || a.rank - b.rank);
  }, [rankedStudents, selectedCenter, sortOrder, rankMode]);"""
new_filtered = """  const filteredRanked = useMemo(() => {
    let list = [...rankedStudents];

    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      list = list.filter(s => (s.name || '').toLowerCase().includes(q) || (s.roll || '').toLowerCase().includes(q));
    }

    list = list.filter(s => {
      const matchCat     = filterCategory === 'ALL' || s.category === filterCategory;
      const matchSponsor = filterSponsor  === 'ALL' || s.sponsor  === filterSponsor;
      const matchGender  = filterGender   === 'ALL' || s.gender   === filterGender;
      const matchCenter  = selectedCenter === 'ALL' || s.center   === selectedCenter;
      return matchCat && matchSponsor && matchGender && matchCenter;
    });

    const highToLow = [...list].sort((a, b) => (b.marks - a.marks) || a.rank - b.rank);
    const lowToHigh = [...list].sort((a, b) => (a.marks - b.marks) || a.rank - b.rank);

    let selected = highToLow;
    if (rankMode === 'top10') selected = highToLow.slice(0, 10);
    if (rankMode === 'bottom10') selected = lowToHigh.slice(0, 10);

    return sortOrder === 'asc'
      ? [...selected].sort((a, b) => (a.marks - b.marks) || a.rank - b.rank)
      : [...selected].sort((a, b) => (b.marks - a.marks) || a.rank - b.rank);
  }, [rankedStudents, selectedCenter, sortOrder, rankMode, searchTerm, filterCategory, filterSponsor, filterGender]);"""
content = content.replace(old_filtered, new_filtered)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched TestInsightsPanel states and logic")
