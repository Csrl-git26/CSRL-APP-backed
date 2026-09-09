import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

boundary_code = """
import React, { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  componentDidCatch(error, errorInfo) {
    this.setState({ error, errorInfo });
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 20, background: '#fee', color: '#c00' }}>
          <h2>Something went wrong in AdminDashboard.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </details>
        </div>
      );
    }
    return this.props.children; 
  }
}
"""

if "class ErrorBoundary" not in content:
    content = boundary_code + content

old_return = "return (\n    <div className=\"dashboard-container\">"
new_return = "return (\n    <ErrorBoundary>\n    <div className=\"dashboard-container\">"
content = content.replace(old_return, new_return)

old_end = "</div>\n  );\n}"
new_end = "</div>\n    </ErrorBoundary>\n  );\n}"
content = content.replace(old_end, new_end)
    
with open(filepath, 'w') as f:
    f.write(content)
print("Added ErrorBoundary")
