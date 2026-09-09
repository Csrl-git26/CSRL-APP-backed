import fs from 'fs';
const file = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(
  /const categories  = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.CATEGORY\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const categories  = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.CATEGORY).filter(Boolean))].sort((a, b) => a.localeCompare(b))], [data]);"
);

content = content.replace(
  /const centersList = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.centerCode\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const centersList = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.centerCode).filter(Boolean))].sort((a, b) => a.localeCompare(b))], [data]);"
);

content = content.replace(
  /const sponsorsList = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.SPONSOR \|\| displaySponsor\(p\.centerCode\)\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const sponsorsList = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.SPONSOR || displaySponsor(p.centerCode)).filter(Boolean))].sort((a, b) => a.localeCompare(b))], [data]);"
);

content = content.replace(
  /const gendersList = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.GENDER\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const gendersList = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.GENDER).filter(Boolean))].sort((a, b) => a.localeCompare(b))], [data]);"
);

content = content.replace(
  /const statesList  = useMemo\(\(\) => \['ALL', \.\.\.\[\.\.\.new Set\(\(data\?\.profiles \|\| \[\]\)\.map\(\(p\) => p\.STATE\)\.filter\(Boolean\)\)\]\], \[data\]\);/,
  "const statesList  = useMemo(() => ['ALL', ...[...new Set((data?.profiles || []).map((p) => p.STATE).filter(Boolean))].sort((a, b) => a.localeCompare(b))], [data]);"
);

fs.writeFileSync(file, content);
console.log("Fixed sorting in AdminDashboard");
