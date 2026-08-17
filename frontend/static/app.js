const loginForm = document.getElementById('login-form');
const loginSection = document.getElementById('login-section');
const userSection = document.getElementById('user-section');
const userIdInput = document.getElementById('user-id-input');
const userIdDisplay = document.getElementById('user-id-display');
const loadLangsBtn = document.getElementById('load-langs');
const langsList = document.getElementById('langs-list');
const addLangForm = document.getElementById('add-lang-form');

let token = null;

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const dni = loginForm.dni.value.trim();
  const password = loginForm.password.value;

  const body = new URLSearchParams();
  body.append('username', dni);
  body.append('password', password);

  const res = await fetch('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: body.toString()
  });

  if (!res.ok) {
    alert('Login fallido');
    return;
  }
  const data = await res.json();
  token = data.access_token;
  loginSection.style.display = 'none';
  userSection.style.display = '';
  userIdDisplay.textContent = userIdInput.value;
});

loadLangsBtn.addEventListener('click', () => loadLanguages());

async function loadLanguages() {
  const userId = userIdInput.value;
  userIdDisplay.textContent = userId;
  const res = await fetch(`/usuarios/${userId}/lenguajes?skip=0&limit=20`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) {
    alert('Error cargando lenguajes');
    return;
  }
  const langs = await res.json();
  langsList.innerHTML = '';
  langs.forEach(l => {
    const li = document.createElement('li');
    li.textContent = `${l.leng_id}: ${l.lenguajes}`;
    // Edit button
    const btnEdit = document.createElement('button');
    btnEdit.textContent = 'Editar';
    btnEdit.onclick = () => {
      const nuevo = prompt('Nuevo nombre', l.lenguajes);
      if (!nuevo) return;
      fetch(`/lenguajes/${l.leng_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ lenguajes: nuevo })
      }).then(r => {
        if (r.ok) loadLanguages(); else alert('No se pudo editar');
      });
    };
    // Delete button
    const btnDel = document.createElement('button');
    btnDel.textContent = 'Eliminar';
    btnDel.onclick = () => {
      if (!confirm('¿Eliminar?')) return;
      fetch(`/lenguajes/${l.leng_id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      }).then(r => {
        if (r.status === 204) loadLanguages(); else alert('No se pudo eliminar');
      });
    };

    li.appendChild(btnEdit);
    li.appendChild(btnDel);
    langsList.appendChild(li);
  });
}

addLangForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const lenguaje = addLangForm.lenguaje.value.trim();
  const userId = userIdInput.value;
  const res = await fetch(`/usuarios/${userId}/lenguajes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ lenguaje })
  });
  if (res.status === 201) {
    addLangForm.reset();
    loadLanguages();
  } else {
    const txt = await res.text();
    alert('Error: ' + txt);
  }
});
