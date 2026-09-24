import re

# Fix 1: Add ErrorBoundary to App.jsx
app_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/App.jsx'
with open(app_path, 'r') as f:
    content = f.read()

old_imports = """import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import Layout from './components/Layout';
import Login from './components/Login';
import DataAdminLogin from './components/DataAdminLogin';
import StudentDashboard from './components/StudentDashboard';
import CentreDashboard from './components/CentreDashboard';
import AdminDashboard from './components/AdminDashboard';"""

new_imports = """import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import Layout from './components/Layout';
import Login from './components/Login';
import DataAdminLogin from './components/DataAdminLogin';
import StudentDashboard from './components/StudentDashboard';
import CentreDashboard from './components/CentreDashboard';
import AdminDashboard from './components/AdminDashboard';
import ErrorBoundary from './components/ErrorBoundary';"""

old_routes = """          user?.role === 'STUDENT' ? <StudentDashboard /> :
          user?.role === 'CENTRE' ? <CentreDashboard /> :
          <AdminDashboard />"""

new_routes = """          user?.role === 'STUDENT' ? <ErrorBoundary><StudentDashboard /></ErrorBoundary> :
          user?.role === 'CENTRE' ? <ErrorBoundary><CentreDashboard /></ErrorBoundary> :
          <ErrorBoundary><AdminDashboard /></ErrorBoundary>"""

if old_imports in content:
    content = content.replace(old_imports, new_imports)
    print("Added ErrorBoundary import")
else:
    print("Could not find import block!")

if old_routes in content:
    content = content.replace(old_routes, new_routes)
    print("Wrapped dashboards with ErrorBoundary")
else:
    print("Could not find routes block!")

with open(app_path, 'w') as f:
    f.write(content)

print("App.jsx updated!")
