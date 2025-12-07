import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import DashboardLayout from './layout/DashboardLayout';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import InvoicesList from './pages/InvoicesList';
import InvoiceEditor from './pages/InvoiceEditor';

import AuthCallback from './pages/AuthCallback';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/auth/callback" element={<AuthCallback />} />
              
              <Route path="/" element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }>
                <Route index element={<Dashboard />} />
                <Route path="invoices" element={<InvoicesList />} />
                <Route path="invoices/new" element={<InvoiceEditor />} />
                <Route path="invoices/:id/edit" element={<InvoiceEditor />} />
              </Route>
            </Routes>
          </div>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  )
}

export default App
