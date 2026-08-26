import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad = """        // Temporarily move to body to avoid overflow clipping from parent modals/tabs
        const originalParent = page1.parentNode;
        const tempContainer = document.createElement('div');
        tempContainer.style.position = 'absolute';
        tempContainer.style.top = '0';
        tempContainer.style.left = '0';
        tempContainer.style.width = '800px';
        tempContainer.style.zIndex = '-9999';
        tempContainer.style.opacity = '0';
        document.body.appendChild(tempContainer);
        tempContainer.appendChild(page1);

        // Wait a frame for layout recalculation
        await new Promise(r => setTimeout(r, 100));

        const canvas1 = await html2canvas(page1, { 
          scale: 2, 
          useCORS: true,
          windowHeight: page1.scrollHeight,
          height: page1.scrollHeight,
          windowWidth: 800,
          width: 800
        });
        
        originalParent.appendChild(page1);
        document.body.removeChild(tempContainer);"""

good = """        // Wait a frame for layout recalculation
        await new Promise(r => setTimeout(r, 100));

        const canvas1 = await html2canvas(page1, { 
          scale: 2, 
          useCORS: true,
          windowHeight: page1.scrollHeight,
          height: page1.scrollHeight,
          windowWidth: 800,
          width: 800
        });"""

if bad in content:
    content = content.replace(bad, good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Successfully patched StudentProfileView.jsx")
else:
    print("Could not find target string in StudentProfileView.jsx")
