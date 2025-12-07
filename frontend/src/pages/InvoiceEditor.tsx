import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2, Save, ArrowLeft } from 'lucide-react';
import { invoices } from '../lib/api';

export default function InvoiceEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isNew = !id;

  const [formData, setFormData] = useState({
    invoice_number: 'INV-' + Date.now().toString().slice(-4),
    client_name: '',
    client_email: '',
    date: new Date().toISOString().split('T')[0],
    due_date: '',
    status: 'draft',
    line_items: [{ description: 'Item 1', quantity: 1, unit_price: 0 }]
  });

  // Fetch existing invoice if editing
  const { data: invoiceData } = useQuery({
    queryKey: ['invoice', id],
    queryFn: () => invoices.get(id!),
    enabled: !isNew,
  });

  useEffect(() => {
    if (invoiceData) {
      setFormData({
        invoice_number: invoiceData.invoice_number,
        client_name: invoiceData.client_name,
        client_email: invoiceData.client_email || '',
        date: invoiceData.date.split('T')[0],
        due_date: invoiceData.due_date ? invoiceData.due_date.split('T')[0] : '',
        status: invoiceData.status,
        line_items: invoiceData.content.items || []
      });
    }
  }, [invoiceData]);

  const mutation = useMutation({
    mutationFn: (data: any) => {
      const payload = {
        ...data,
        total_amount: calculateTotal(data.line_items),
        content: { items: data.line_items }
      };
      // remove transient line_items from root if you want, but API ignores extra fields usually
      // payload.line_items = undefined; 
      
      if (isNew) return invoices.create(payload);
      return invoices.update(id!, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      navigate('/invoices');
    }
  });

  const calculateTotal = (items: any[]) => {
    return items.reduce((acc, item) => acc + (item.quantity * item.unit_price), 0);
  };

  const handleLineItemChange = (index: number, field: string, value: any) => {
    const newItems = [...formData.line_items];
    newItems[index] = { ...newItems[index], [field]: value };
    setFormData({ ...formData, line_items: newItems });
  };

  const addLineItem = () => {
    setFormData({
      ...formData,
      line_items: [...formData.line_items, { description: '', quantity: 1, unit_price: 0 }]
    });
  };

  const removeLineItem = (index: number) => {
    const newItems = formData.line_items.filter((_, i) => i !== index);
    setFormData({ ...formData, line_items: newItems });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const totalAmount = calculateTotal(formData.line_items);

  return (
    <div className="h-[calc(100vh-4rem)] flex gap-6">
      {/* Editor Column */}
      <div className="flex-1 overflow-y-auto pr-2">
        <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
                <button onClick={() => navigate('/invoices')} className="text-gray-500 hover:text-gray-700">
                    <ArrowLeft className="h-5 w-5" />
                </button>
                <h1 className="text-2xl font-bold text-gray-900">{isNew ? 'New Invoice' : 'Edit Invoice'}</h1>
            </div>
            <button
                onClick={handleSubmit}
                disabled={mutation.isPending}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none"
            >
                <Save className="h-4 w-4 mr-2" />
                Save Invoice
            </button>
        </div>

        <div className="space-y-6 bg-white p-6 rounded-lg shadow">
            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Invoice Number</label>
                    <input
                        type="text"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                        value={formData.invoice_number}
                        onChange={e => setFormData({...formData, invoice_number: e.target.value})}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Date</label>
                    <input
                        type="date"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                        value={formData.date}
                        onChange={e => setFormData({...formData, date: e.target.value})}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Client Name</label>
                    <input
                        type="text"
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                        value={formData.client_name}
                        onChange={e => setFormData({...formData, client_name: e.target.value})}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Client Email</label>
                    <input
                        type="email"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                        value={formData.client_email}
                        onChange={e => setFormData({...formData, client_email: e.target.value})}
                    />
                </div>
            </div>

            <div className="mt-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Line Items</h3>
                <div className="space-y-4">
                    {formData.line_items.map((item, index) => (
                        <div key={index} className="flex gap-4 items-start">
                            <div className="flex-1">
                                <input
                                    type="text"
                                    placeholder="Description"
                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                                    value={item.description}
                                    onChange={e => handleLineItemChange(index, 'description', e.target.value)}
                                />
                            </div>
                            <div className="w-24">
                                <input
                                    type="number"
                                    placeholder="Qty"
                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                                    value={item.quantity}
                                    onChange={e => handleLineItemChange(index, 'quantity', parseInt(e.target.value) || 0)}
                                />
                            </div>
                            <div className="w-32">
                                <input
                                    type="number"
                                    placeholder="Price"
                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                                    value={item.unit_price}
                                    onChange={e => handleLineItemChange(index, 'unit_price', parseFloat(e.target.value) || 0)}
                                />
                            </div>
                            <div className="w-24 py-2 text-right font-medium text-gray-700">
                                ${(item.quantity * item.unit_price).toFixed(2)}
                            </div>
                            <button
                                type="button"
                                onClick={() => removeLineItem(index)}
                                className="p-2 text-red-600 hover:text-red-900"
                            >
                                <Trash2 className="h-5 w-5" />
                            </button>
                        </div>
                    ))}
                </div>
                <button
                    type="button"
                    onClick={addLineItem}
                    className="mt-4 inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-500"
                >
                    <Plus className="h-4 w-4 mr-1" />
                    Add Item
                </button>
            </div>

            <div className="border-t border-gray-200 pt-4 flex justify-end">
                <div className="text-xl font-bold text-gray-900">
                    Total: ${totalAmount.toFixed(2)}
                </div>
            </div>
        </div>
      </div>

      {/* Preview Column */}
      <div className="flex-1 bg-gray-100 rounded-lg p-4 hidden lg:block">
        {!isNew ? (
             <iframe 
                src={invoices.getPdfUrl(id!)} 
                className="w-full h-full rounded shadow-lg border border-gray-200 bg-white"
                title="PDF Preview"
            />
        ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
                <p>Save invoice to verify PDF preview</p>
            </div>
        )}
      </div>
    </div>
  );
}
