import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const { user } = useAuth();
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      <div className="mt-4">
        <p>Welcome back, {user?.full_name}!</p>
        <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                    <div className="flex items-center">
                        <div className="flex-1 w-0">
                           <dt className="text-sm font-medium text-gray-500 truncate">Quick Action</dt>
                           <dd>
                               <Link to="/invoices/new" className="text-lg font-medium text-primary-600 hover:text-primary-500">
                                   Create New Invoice
                               </Link>
                           </dd>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}
