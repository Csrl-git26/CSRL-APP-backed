import fs from 'fs';
const file = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(
  /const categories  = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.CATEGORY\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const categories  = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.CATEGORY).filter(Boolean))].sort((a,b) => String(a).localeCompare(String(b)))], [data]);"
);

content = content.replace(
  /const sponsorsList = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.SPONSOR \|\| \(p\.centerCode === 'KNP' \|\| p\.centerCode === 'GAIL' \? 'GAIL' : \(p\.centerCode === 'JDH' \|\| p\.centerCode === 'OIL_INDIA' \? 'OIL_INDIA' : '—'\)\)\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const sponsorsList = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.SPONSOR || (p.centerCode === 'KNP' || p.centerCode === 'GAIL' ? 'GAIL' : (p.centerCode === 'JDH' || p.centerCode === 'OIL_INDIA' ? 'OIL_INDIA' : '—'))).filter(Boolean))].sort((a,b) => String(a).localeCompare(String(b)))], [data]);"
);

content = content.replace(
  /const gendersList = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.GENDER\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const gendersList = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.GENDER).filter(Boolean))].sort((a,b) => String(a).localeCompare(String(b)))], [data]);"
);

content = content.replace(
  /const statesList  = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.STATE\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const statesList  = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.STATE).filter(Boolean))].sort((a,b) => String(a).localeCompare(String(b)))], [data]);"
);

fs.writeFileSync(file, content);
console.log("Fixed sorting in CentreDashboard");
