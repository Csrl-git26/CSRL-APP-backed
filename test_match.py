import re

TOPIC_SUBJECT_MAP = {
  'ORGANIC COMPOUNDS CONTAINING OXYGEN-ALCOHOLS, PHENOLS & ETHERS, ALDEHYDES & KETONES, CARBOXYLIC ACIDS': 'Chemistry',
  'BASIC MATHS, SETS & RELATION(BASIC TRIGONOMETRY, INEQUALITIES, MODULUS, LOGARITHM, FUNCTIONS & GRAPHS, GREATEST INTEGER FUNCTION, SURDS & INDICES.)': 'Mathematics',
  'TRIGONOMETRIC IDENTITIES, EQUATIONS & INEQUALITIES, PROPERTIES & SOLUTIONS OF TRIANGLES': 'Mathematics',
}

def test(rawTopic):
    trimmed = (rawTopic or '').strip()
    normalized = re.sub(r'\s+', ' ', rawTopic or '').strip().upper()
    normNoEllipsis = re.sub(r'\.+$', '', normalized).strip()
    
    print("Raw:", rawTopic)
    print("normNoEllipsis:", normNoEllipsis)
    
    for knownTopic, knownSubject in TOPIC_SUBJECT_MAP.items():
        if knownTopic.startswith(normNoEllipsis) or normNoEllipsis.startswith(knownTopic):
            print("MATCHED:", knownTopic, "->", knownSubject)
            return
            
    print("NO MATCH")

test("Organic compounds containing oxygen-Alcohols, Phenols & Ethers, Aldehydes & Ketones...")
test("Basic Maths, Sets & Relation")
test("Trigonometric Identities, Equations & Inequalities...")
