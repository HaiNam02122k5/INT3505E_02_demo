import React, { useState, useEffect } from 'react';
import { Book, Users, ArrowLeftRight, LogIn, LogOut, Plus, Edit, Trash2, BookOpen, Search } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

const LibraryApp = () => {
  const [token, setToken] = useState(null);
  const [activeTab, setActiveTab] = useState('books');
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Form states
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [bookForm, setBookForm] = useState({ title: '', author: '', isbn: '', copies: 1 });
  const [memberForm, setMemberForm] = useState({ name: '', phone_number: '', address: '' });
  const [borrowForm, setBorrowForm] = useState({ member_id: '', book_id: '' });
  const [editMode, setEditMode] = useState({ active: false, type: '', id: null });
  const [searchTerm, setSearchTerm] = useState('');

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };

  // Fetch data
  const fetchBooks = async () => {
    try {
      const res = await fetch(`${API_BASE}/books`, { headers });
      const data = await res.json();
      if (Array.isArray(data)) setBooks(data);
      else if (data[0]) setBooks(data[0]);
    } catch (err) {
      console.error('Lỗi khi tải sách:', err);
    }
  };

  const fetchMembers = async () => {
    try {
      const res = await fetch(`${API_BASE}/members`, { headers });
      const data = await res.json();
      if (Array.isArray(data)) setMembers(data);
      else if (data[0]) setMembers(data[0]);
    } catch (err) {
      console.error('Lỗi khi tải thành viên:', err);
    }
  };

  const fetchTransactions = async (memberId) => {
    try {
      const res = await fetch(`${API_BASE}/members/${memberId}/transactions`, { headers });
      const data = await res.json();
      setTransactions(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Lỗi khi tải giao dịch:', err);
    }
  };

  useEffect(() => {
    if (token) {
      fetchBooks();
      fetchMembers();
    }
  }, [token]);

  // Login
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginForm)
      });
      const data = await res.json();
      if (res.ok) {
        setToken(data.access_token);
        setSuccess('Đăng nhập thành công!');
        setLoginForm({ username: '', password: '' });
      } else {
        setError(data.msg || 'Đăng nhập thất bại');
      }
    } catch (err) {
      setError('Lỗi kết nối server');
    }
    setLoading(false);
  };

  // Add/Update Book
  const handleBookSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const url = editMode.active
        ? `${API_BASE}/books/${editMode.id}`
        : `${API_BASE}/books`;
      const method = editMode.active ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(bookForm)
      });
      const data = await res.json();

      if (res.ok) {
        setSuccess(data.message);
        setBookForm({ title: '', author: '', isbn: '', copies: 1 });
        setEditMode({ active: false, type: '', id: null });
        fetchBooks();
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi khi xử lý sách');
    }
    setLoading(false);
  };

  // Delete Book
  const handleDeleteBook = async (id) => {
    if (!confirm('Bạn có chắc muốn xóa sách này?')) return;
    try {
      const res = await fetch(`${API_BASE}/books/${id}`, { method: 'DELETE', headers });
      const data = await res.json();
      if (res.ok) {
        setSuccess(data.message);
        fetchBooks();
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi khi xóa sách');
    }
  };

  // Add/Update Member
  const handleMemberSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const url = editMode.active
        ? `${API_BASE}/members/${editMode.id}`
        : `${API_BASE}/members`;
      const method = editMode.active ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(memberForm)
      });
      const data = await res.json();

      if (res.ok) {
        setSuccess(data.message);
        setMemberForm({ name: '', phone_number: '', address: '' });
        setEditMode({ active: false, type: '', id: null });
        fetchMembers();
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi khi xử lý thành viên');
    }
    setLoading(false);
  };

  // Delete Member
  const handleDeleteMember = async (id) => {
    if (!confirm('Bạn có chắc muốn xóa thành viên này?')) return;
    try {
      const res = await fetch(`${API_BASE}/members/${id}`, { method: 'DELETE', headers });
      const data = await res.json();
      if (res.ok) {
        setSuccess(data.message);
        fetchMembers();
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi khi xóa thành viên');
    }
  };

  // Borrow Book
  const handleBorrow = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/members/${borrowForm.member_id}/transactions/${borrowForm.book_id}`, {
        method: 'POST',
        headers
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess(data.message);
        setBorrowForm({ member_id: '', book_id: '' });
        fetchBooks();
        if (borrowForm.member_id) fetchTransactions(borrowForm.member_id);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi khi mượn sách');
    }
    setLoading(false);
  };

  // Return Book
  const handleReturn = async (bookId, memberId) => {
    try {
      const res = await fetch(`${API_BASE}/members/${memberId}/transactions/${bookId}`, {
        method: 'DELETE',
        headers
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess(data.message);
        fetchBooks();
        fetchTransactions(memberId);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi khi trả sách');
    }
  };

  const filteredBooks = books.filter(book =>
    book.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.author?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.isbn?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredMembers = members.filter(member =>
    member.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.phone?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (!token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
          <div className="text-center mb-6">
            <BookOpen className="w-16 h-16 text-indigo-600 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-800">Thư Viện SOS</h1>
            <p className="text-gray-600 mt-2">Đăng nhập để tiếp tục</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tên đăng nhập
              </label>
              <input
                type="text"
                value={loginForm.username}
                onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Mật khẩu
              </label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <LogIn className="w-5 h-5" />
              {loading ? 'Đang xử lý...' : 'Đăng nhập'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-indigo-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <BookOpen className="w-8 h-8" />
              <h1 className="text-2xl font-bold">Quản Lý Thư Viện</h1>
            </div>
            <button
              onClick={() => setToken(null)}
              className="flex items-center gap-2 bg-indigo-700 hover:bg-indigo-800 px-4 py-2 rounded-lg transition"
            >
              <LogOut className="w-5 h-5" />
              Đăng xuất
            </button>
          </div>
        </div>
      </div>

      {/* Notifications */}
      {error && (
        <div className="container mx-auto px-4 pt-4">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
            <button onClick={() => setError('')} className="float-right font-bold">×</button>
          </div>
        </div>
      )}
      {success && (
        <div className="container mx-auto px-4 pt-4">
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            {success}
            <button onClick={() => setSuccess('')} className="float-right font-bold">×</button>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4">
          <div className="flex gap-1">
            {[
              { id: 'books', label: 'Sách', icon: Book },
              { id: 'members', label: 'Thành viên', icon: Users },
              { id: 'transactions', label: 'Mượn/Trả', icon: ArrowLeftRight }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setSearchTerm('');
                  setError('');
                  setSuccess('');
                }}
                className={`flex items-center gap-2 px-6 py-3 border-b-2 transition ${
                  activeTab === tab.id
                    ? 'border-indigo-600 text-indigo-600 font-medium'
                    : 'border-transparent text-gray-600 hover:text-gray-800'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-6">
        {/* Books Tab */}
        {activeTab === 'books' && (
          <div className="grid md:grid-cols-3 gap-6">
            {/* Form */}
            <div className="md:col-span-1">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Plus className="w-5 h-5" />
                  {editMode.active ? 'Cập nhật sách' : 'Thêm sách mới'}
                </h2>
                <form onSubmit={handleBookSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Tiêu đề</label>
                    <input
                      type="text"
                      value={bookForm.title}
                      onChange={(e) => setBookForm({...bookForm, title: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Tác giả</label>
                    <input
                      type="text"
                      value={bookForm.author}
                      onChange={(e) => setBookForm({...bookForm, author: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">ISBN</label>
                    <input
                      type="text"
                      value={bookForm.isbn}
                      onChange={(e) => setBookForm({...bookForm, isbn: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      required
                      disabled={editMode.active}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Số lượng</label>
                    <input
                      type="number"
                      value={bookForm.copies}
                      onChange={(e) => setBookForm({...bookForm, copies: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      min="0"
                      required
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      disabled={loading}
                      className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                    >
                      {editMode.active ? 'Cập nhật' : 'Thêm'}
                    </button>
                    {editMode.active && (
                      <button
                        type="button"
                        onClick={() => {
                          setEditMode({ active: false, type: '', id: null });
                          setBookForm({ title: '', author: '', isbn: '', copies: 1 });
                        }}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                      >
                        Hủy
                      </button>
                    )}
                  </div>
                </form>
              </div>
            </div>

            {/* List */}
            <div className="md:col-span-2">
              <div className="bg-white rounded-lg shadow">
                <div className="p-4 border-b">
                  <div className="relative">
                    <Search className="w-5 h-5 absolute left-3 top-2.5 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Tìm kiếm sách..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
                <div className="p-4 space-y-3 max-h-[600px] overflow-y-auto">
                  {filteredBooks.map(book => (
                    <div key={book.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="font-bold text-lg text-gray-800">{book.title}</h3>
                          <p className="text-gray-600">Tác giả: {book.author}</p>
                          <p className="text-sm text-gray-500">ISBN: {book.isbn}</p>
                          <p className={`text-sm font-medium mt-1 ${book.copies > 0 ? 'text-green-600' : 'text-red-600'}`}>
                            Còn lại: {book.copies} cuốn
                          </p>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => {
                              setEditMode({ active: true, type: 'book', id: book.id });
                              setBookForm({
                                title: book.title,
                                author: book.author,
                                isbn: book.isbn,
                                copies: book.copies
                              });
                            }}
                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                          >
                            <Edit className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => handleDeleteBook(book.id)}
                            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                  {filteredBooks.length === 0 && (
                    <p className="text-center text-gray-500 py-8">Không tìm thấy sách nào</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Members Tab */}
        {activeTab === 'members' && (
          <div className="grid md:grid-cols-3 gap-6">
            <div className="md:col-span-1">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Plus className="w-5 h-5" />
                  {editMode.active ? 'Cập nhật thành viên' : 'Thêm thành viên'}
                </h2>
                <form onSubmit={handleMemberSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Họ và tên</label>
                    <input
                      type="text"
                      value={memberForm.name}
                      onChange={(e) => setMemberForm({...memberForm, name: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Số điện thoại</label>
                    <input
                      type="text"
                      value={memberForm.phone_number}
                      onChange={(e) => setMemberForm({...memberForm, phone_number: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      required
                      maxLength="10"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Địa chỉ</label>
                    <textarea
                      value={memberForm.address}
                      onChange={(e) => setMemberForm({...memberForm, address: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      rows="3"
                      required
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      disabled={loading}
                      className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                    >
                      {editMode.active ? 'Cập nhật' : 'Thêm'}
                    </button>
                    {editMode.active && (
                      <button
                        type="button"
                        onClick={() => {
                          setEditMode({ active: false, type: '', id: null });
                          setMemberForm({ name: '', phone_number: '', address: '' });
                        }}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                      >
                        Hủy
                      </button>
                    )}
                  </div>
                </form>
              </div>
            </div>

            <div className="md:col-span-2">
              <div className="bg-white rounded-lg shadow">
                <div className="p-4 border-b">
                  <div className="relative">
                    <Search className="w-5 h-5 absolute left-3 top-2.5 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Tìm kiếm thành viên..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
                <div className="p-4 space-y-3 max-h-[600px] overflow-y-auto">
                  {filteredMembers.map(member => (
                    <div key={member.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="font-bold text-lg text-gray-800">{member.name}</h3>
                          <p className="text-gray-600">📞 {member.phone}</p>
                          <p className="text-sm text-gray-500">📍 {member.address}</p>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => {
                              setEditMode({ active: true, type: 'member', id: member.id });
                              setMemberForm({
                                name: member.name,
                                phone_number: member.phone,
                                address: member.address
                              });
                            }}
                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                          >
                            <Edit className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => handleDeleteMember(member.id)}
                            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                  {filteredMembers.length === 0 && (
                    <p className="text-center text-gray-500 py-8">Không tìm thấy thành viên nào</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Transactions Tab */}
        {activeTab === 'transactions' && (
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <ArrowLeftRight className="w-5 h-5" />
                Mượn sách
              </h2>
              <form onSubmit={handleBorrow} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Thành viên</label>
                  <select
                    value={borrowForm.member_id}
                    onChange={(e) => {
                      setBorrowForm({...borrowForm, member_id: e.target.value});
                      if (e.target.value) fetchTransactions(e.target.value);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    required
                  >
                    <option value="">Chọn thành viên</option>
                    {members.map(m => (
                      <option key={m.id} value={m.id}>{m.name} - {m.phone}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Sách</label>
                  <select
                    value={borrowForm.book_id}
                    onChange={(e) => setBorrowForm({...borrowForm, book_id: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    required
                  >
                    <option value="">Chọn sách</option>
                    {books.filter(b => b.copies > 0).map(b => (
                      <option key={b.id} value={b.id}>{b.title} (Còn: {b.copies})</option>
                    ))}
                  </select>
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                >
                  Mượn sách
                </button>
              </form>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold mb-4">Lịch sử mượn/trả</h2>
              {borrowForm.member_id ? (
                <div className="space-y-3 max-h-[500px] overflow-y-auto">
                  {transactions.length > 0 ? (
                    transactions.map(t => (
                      <div key={t.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex justify-between items-start">
                          <div>
                            <h4 className="font-bold text-gray-800">{t.book_title}</h4>
                            <p className="text-sm text-gray-600">
                              Mượn: {new Date(t.borrow_date).toLocaleDateString('vi-VN')}
                            </p>
                            {t.return_date ? (
                              <p className="text-sm text-green-600">
                                Đã trả: {new Date(t.return_date).toLocaleDateString('vi-VN')}
                              </p>
                            ) : (
                              <p className="text-sm text-orange-600 font-medium">Chưa trả</p>
                            )}
                          </div>
                          {!t.return_date && (
                            <button
                              onClick={() => handleReturn(t.book_id, t.member_id)}
                              className="px-3 py-1 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition"
                            >
                              Trả sách
                            </button>
                          )}
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 text-center py-8">Chưa có giao dịch nào</p>
                  )}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">Vui lòng chọn thành viên để xem lịch sử</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LibraryApp;