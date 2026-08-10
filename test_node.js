const TOPIC_SUBJECT_MAP = {
  'ORGANIC COMPOUNDS CONTAINING OXYGEN-ALCOHOLS, PHENOLS & ETHERS, ALDEHYDES & KETONES, CARBOXYLIC ACIDS': 'Chemistry',
  'BASIC MATHS, SETS & RELATION(BASIC TRIGONOMETRY, INEQUALITIES, MODULUS, LOGARITHM, FUNCTIONS & GRAPHS, GREATEST INTEGER FUNCTION, SURDS & INDICES.)': 'Mathematics',
  'TRIGONOMETRIC IDENTITIES, EQUATIONS & INEQUALITIES, PROPERTIES & SOLUTIONS OF TRIANGLES': 'Mathematics',
};

function test(rawTopic) {
  const trimmed = (rawTopic || '').trim();
  const normalized = (rawTopic || '').replace(/\s+/g, ' ').trim().toUpperCase();
  const normNoEllipsis = normalized.replace(/\.+$/, '').trim();
  
  console.log("Raw:", rawTopic);
  console.log("normNoEllipsis:", normNoEllipsis);
  
  for (const [knownTopic, knownSubject] of Object.entries(TOPIC_SUBJECT_MAP)) {
    if (knownTopic.startsWith(normNoEllipsis) || normNoEllipsis.startsWith(knownTopic)) {
      console.log("MATCHED:", knownTopic, "->", knownSubject);
      return;
    }
  }
  console.log("NO MATCH");
}

test("Organic compounds containing oxygen-Alcohols, Phenols & Ethers, Aldehydes & Ketones...");
test("Basic Maths, Sets & Relation");
test("Trigonometric Identities, Equations & Inequalities...");
