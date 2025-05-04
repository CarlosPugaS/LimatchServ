# 🚀 Proyecto Full Stack - LimatchServ

> **LimatchServ**  
> Plataforma web pensada para conectar a personas que buscan servicios con prestadores locales en la comuna de Limache.  
> Su misión es mejorar la visibilidad de trabajadores independientes y facilitar la contratación de servicios relacionados con el hogar y el bienestar.

---

## 🛠️ Tecnologías utilizadas

### Frontend

<div>
  <code><img width="70" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/vite.png" alt="Vite" title="Vite"/></code>
  <code><img width="70" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/react.png" alt="React" title="React"/></code>
  <code><img width="70" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/tailwind_css.png" alt="Tailwind CSS" title="Tailwind CSS"/></code>
</div>

### Backend

<div>
  <code><img width="70" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" title="Python"/></code>
  <code><img width="70" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/flask.png" alt="Flask" title="Flask"/></code>
  <code><img width="70" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/postgresql.png" alt="PostgreSQL" title="PostgreSQL"/></code>
</div>

**Otras tecnologías implementadas:**
- Python-dotenv
- SQLAlchemy
- Flask-Migrate
- JWT (Autenticación)
- Bcrypt (Hash de contraseñas)
- CORS (Frontend ↔ Backend)

---

## 📁 Estructura del proyecto

```
LimatchServ/
├── Front/      → Aplicación web (Vite + React)
├── Back/       → API REST (Flask + PostgreSQL)
```

---

## ✅ Estado del proyecto

- [x] Estructura base de frontend y backend
- [x] Modelo entidad-relación (ER)
- [x] Registro y login con JWT
- [x] Hashing de contraseñas con bcrypt
- [x] Creación y respuesta de presupuestos
- [x] Flujo de match entre cliente y prestador
- [x] Sistema de reseñas y calificaciones cruzadas
- [ ] Filtro por categoría y especialidad
- [ ] Panel de usuario (`/mi-perfil`)
- [ ] Seguridad por rol (`@role_required`)
- [ ] Tests y documentación API (pendiente)

---

## 🧪 Cómo correr el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/CarlosPugaS/limatchserv.git
cd limatchserv
```

### 2. Iniciar el frontend

```bash
cd front
npm install
npm run dev
```

### 3. Iniciar el backend

```bash
cd ../back
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## 📆 Última actualización

03/05/2025

---

## 👨‍💻 Autor

Desarrollado por **Carlos Puga Salinas**  
[🔗 LinkedIn](https://www.linkedin.com/in/carlospugasalinas) | [🐙 GitHub](https://github.com/CarlosPugaS)
