import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom'; 
import { Plus, FileText, Edit, Trash2 } from 'lucide-react';
import { invoices } from '../lib/api';

export default function InvoicesList() {
  const { data: invoiceList, isLoading, isError, refetch } = useQuery({
    queryKey: ['invoices'],
    queryFn: invoices.list,
  });

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this invoice?')) {
      await invoices.delete(id);
      refetch();
    }
  };

  if (isLoading) return <div className="p-4">Loading invoices...</div>;
  if (isError) return <div className="p-4 text-red-500">Error loading invoices</div>;

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Invoices</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all invoices including client, date, and status.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            to="/invoices/new"
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 sm:w-auto"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create Invoice
          </Link>
        </div>
      </div>
      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                      Invoice #
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Client
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Date
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Amount
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Status
                    </th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {invoiceList?.map((invoice: any) => (
                    <tr key={invoice.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                        {invoice.invoice_number}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{invoice.client_name}</td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {new Date(invoice.date).toLocaleDateString()}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        ${invoice.total_amount.toFixed(2)}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold leading-5 text-green-800">
                          {invoice.status}
                        </span>
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <div className="flex justify-end gap-2">
                            <a 
                                href={invoices.getPdfUrl(invoice.id)} 
                                target="_blank"
                                rel="noreferrer"
                                className="text-gray-400 hover:text-gray-900"
                                title="Download PDF"
                            >
                                <FileText className="h-4 w-4" />
                            </a>
                            <Link to={`/invoices/${invoice.id}/edit`} className="text-primary-600 hover:text-primary-900" title="Edit">
                                <Edit className="h-4 w-4" />
                            </Link>
                            <button onClick={() => handleDelete(invoice.id)} className="text-red-600 hover:text-red-900" title="Delete">
                                <Trash2 className="h-4 w-4" />
                            </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {(!invoiceList || invoiceList.length === 0) && (
                      <tr>
                          <td colSpan={6} className="py-10 text-center text-gray-500">No invoices found. Create one to get started.</td>
                      </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
