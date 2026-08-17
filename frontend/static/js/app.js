// app.js - Vanilla JS frontend mejorado
const API_BASE = ''; // same origin

// State
let token = sessionStorage.getItem('token') || null;
let currentUser = null;
let currentPage = 1;
let perPage = 10;
let totalItems = 0;
let searchQuery = '';

// Helpers
function showToast(message, type='primary', delay=3000){
  const tc = document.getElementById('toast-container');
  const toastId = 't' + Date.now();
  const toastHtml = `
    <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>`;
  tc.insertAdjacentHTML('beforeend', toastHtml);
  const el = document.getElementById(toastId);
  const bToast = new bootstrap.Toast(el, { delay });
  bToast.show();
  el.addEventListener('hidden.bs.toast', ()=> el.remove());
}

async function apiRequest(path, opts = {}){
  opts.headers = opts.headers || {};
  if (token) opts.headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API_BASE + path, opts);
  if (res.status === 401) {
    // token invalid -> logout
    logout();
    throw new Error('No autorizado. Por favor vuelve a iniciar sesión.');
  }
  return res;
}

// Auth + UI wiring
document.addEventListener('DOMContentLoaded', () => {
  // elements
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const authCards = document.getElementById('auth-cards');
  const dashboard = document.getElementById('dashboard');
  const btnLogout = document.getElementById('btn-logout');
  const displayUser = document.getElementById('display-username');
  const displayId = document.getElementById('display-id');

  const addBtn = document.getElementById('add-leng-btn');
  const addInput = document.getElementById('add-leng-input');
  const perPageSel = document.getElementById('per-page');
  const searchInput = document.getElementById('search-input');

  const btnShowLogin = document.getElementById('btn-show-login');
  const btnShowRegister = document.getElementById('btn-show-register');

  // toggle show auth
  btnShowLogin.onclick = () => {
    authCards.scrollIntoView({behavior:'smooth'});
  };
  btnShowRegister.onclick = () => authCards.scrollIntoView({behavior:'smooth'});

  // login
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const dni = loginForm.dni.value.trim();
    const password = loginForm.password.value;
    try {
      const body = new URLSearchParams();
      body.append('username', dni);
      body.append('password', password);
      const res = await apiRequest('/login', { method: 'POST', body, headers: {'Content-Type':'application/x-www-form-urlencoded'} });
      if (!res.ok) {
        const t = await res.text();
        showToast('Login fallido: ' + t, 'danger');
        return;
      }
      const data = await res.json();
      token = data.access_token;
      sessionStorage.setItem('token', token);
      // fetch user info (we have to find user id from token payload, but backend encodes sub)
      // we simply load dashboard and let user choose ID or we decode JWT client-side if needed
      showToast('Login correcto', 'success');
      authCards.style.display = 'none';
      dashboard.style.display = '';
      // try to get default user id: ask user to pick or use 1
      currentUser = null;
      displayId.textContent = '';
      displayUser.textContent = 'Autenticado';
      loadLanguages();
    } catch (err) {
      showToast(err.message, 'danger');
    }
  });

  // register
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = registerForm.nombre.value.trim();
    const dni = parseInt(registerForm.dni.value);
    const password = registerForm.password.value;
    try {
      const res = await apiRequest('/usuarios', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ nombre, dni, password })
      });
      if (res.status === 201) {
        showToast('Usuario creado. Ahora inicia sesión.', 'success');
        registerForm.reset();
      } else {
        const txt = await res.text();
        showToast('Error: ' + txt, 'danger');
      }
    } catch (err) {
      showToast(err.message, 'danger');
    }
  });

  // logout
  btnLogout.onclick = () => logout();

  // add language
  addBtn.onclick = async (e) => {
    e.preventDefault();
    const lenguaje = addInput.value.trim();
    if (!lenguaje) return;
    // need user id: use display-id (user selects it by editing field)
    const userId = prompt('Introduce tu usuario ID (ej: 1) para agregar'); // quick UX fallback
    if (!userId) { showToast('Usuario ID requerido', 'warning'); return; }
    try {
      const res = await apiRequest(`/usuarios/${userId}/lenguajes`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ lenguaje })
      });
      if (res.status === 201) {
        addInput.value = '';
        showToast('Lenguaje agregado', 'success');
        loadLanguages();
      } else {
        const txt = await res.text();
        showToast('Error: ' + txt, 'danger');
      }
    } catch (err) {
      showToast(err.message, 'danger');
    }
  };

  // search / pagination events
  perPageSel.addEventListener('change', () => { perPage = parseInt(perPageSel.value); currentPage = 1; loadLanguages(); });
  searchInput.addEventListener('input', () => { searchQuery = searchInput.value.trim(); currentPage = 1; loadLanguages(); });

  // show dashboard if already token
  if (token) {
    authCards.style.display = 'none';
    dashboard.style.display = '';
    loadLanguages();
  }
});

// Load + render languages with pagination (uses skip/limit)
async function loadLanguages(){
  const listEl = document.getElementById('langs-list');
  const pagEl = document.getElementById('pagination');
  listEl.innerHTML = '<li class="list-group-item">Cargando...</li>';
  const skip = (currentPage - 1) * perPage;
  // For search we fetch all and filter client-side (API doesn't support search)
  try {
    // pick a user id — ask user or default 1
    const userId = prompt('Introduce Usuario ID para listar (ej: 1)') || '1';
    const res = await apiRequest(`/usuarios/${userId}/lenguajes?skip=${skip}&limit=${perPage}`);
    if (!res.ok) {
      const txt = await res.text();
      listEl.innerHTML = `<li class="list-group-item text-danger">Error: ${txt}</li>`;
      return;
    }
    const items = await res.json();
    // if searchQuery not empty, simple filter
    const filtered = searchQuery ? items.filter(it => it.lenguajes.toLowerCase().includes(searchQuery.toLowerCase())) : items;
    totalItems = filtered.length < perPage ? skip + filtered.length : skip + filtered.length + 1; // approximate
    renderLanguages(filtered, userId);
    renderPagination();
    document.getElementById('display-id').textContent = `ID ${userId}`;
  } catch (err) {
    listEl.innerHTML = `<li class="list-group-item text-danger">Error: ${err.message}</li>`;
  }
}

function renderLanguages(items, userId){
  const listEl = document.getElementById('langs-list');
  listEl.innerHTML = '';
  if (!items.length) {
    listEl.innerHTML = '<li class="list-group-item">No hay lenguajes.</li>';
    return;
  }
  items.forEach(it => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.innerHTML = `
      <div>
        <strong>${escapeHtml(it.leng_id)}</strong>
        <span class="mx-2 text-muted">|</span>
        <span>${escapeHtml(it.lenguajes)}</span>
      </div>
      <div>
        <button class="btn btn-sm btn-outline-secondary me-1" data-action="edit" data-id="${it.leng_id}" data-name="${escapeHtml(it.lenguajes)}">Editar</button>
        <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${it.leng_id}">Eliminar</button>
      </div>
    `;
    listEl.appendChild(li);
  });

  // attach event listeners
  listEl.querySelectorAll('button[data-action="edit"]').forEach(btn => btn.onclick = (e) => {
    const id = btn.dataset.id;
    const name = btn.dataset.name;
    openEditModal(id, name);
  });
  listEl.querySelectorAll('button[data-action="delete"]').forEach(btn => btn.onclick = async () => {
    const id = btn.dataset.id;
    if (!confirm('¿Eliminar lenguaje?')) return;
    try {
      const res = await apiRequest(`/lenguajes/${id}`, { method: 'DELETE' });
      if (res.status === 204) {
        showToast('Eliminado', 'success');
        loadLanguages();
      } else {
        const txt = await res.text();
        showToast('Error: ' + txt, 'danger');
      }
    } catch (err) {
      showToast(err.message, 'danger');
    }
  });
}

function renderPagination(){
  const pagEl = document.getElementById('pagination');
  pagEl.innerHTML = '';
  // Simple previous / next
  const prev = document.createElement('li'); prev.className = 'page-item' + (currentPage === 1 ? ' disabled' : '');
  prev.innerHTML = `<a class="page-link" href="#">Anterior</a>`;
  prev.onclick = (e) => { e.preventDefault(); if (currentPage>1) { currentPage--; loadLanguages(); } };
  const next = document.createElement('li'); next.className = 'page-item';
  next.innerHTML = `<a class="page-link" href="#">Siguiente</a>`;
  next.onclick = (e) => { e.preventDefault(); currentPage++; loadLanguages(); };
  pagEl.appendChild(prev);
  pagEl.appendChild(next);
}

function openEditModal(id, name){
  const editId = document.getElementById('edit-leng-id');
  const editInput = document.getElementById('edit-leng-input');
  editId.value = id;
  editInput.value = name;
  const modalEl = document.getElementById('editModal');
  const modal = new bootstrap.Modal(modalEl);
  modal.show();
  // attach submit once
  const form = document.getElementById('edit-form');
  form.onsubmit = async (e) => {
    e.preventDefault();
    const newName = editInput.value.trim();
    try {
      const res = await apiRequest(`/lenguajes/${id}`, {
        method: 'PUT',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ lenguajes: newName })
      });
      if (res.ok) {
        showToast('Actualizado', 'success');
        modal.hide();
        loadLanguages();
      } else {
        const txt = await res.text();
        showToast('Error: ' + txt, 'danger');
      }
    } catch (err) {
      showToast(err.message, 'danger');
    }
  };
}

function logout(){
  token = null;
  sessionStorage.removeItem('token');
  document.getElementById('auth-cards').style.display = '';
  document.getElementById('dashboard').style.display = 'none';
  showToast('Sesión cerrada', 'info');
}

// simple escape
function escapeHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
