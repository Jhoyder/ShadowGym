# ShadowGym — Sistema de Gestión de Gimnasio

Sistema web completo para la administración de un gimnasio. Desarrollado con **Django** y diseño oscuro personalizado. Permite gestionar miembros, membresías, pagos y control de asistencia diaria con código QR.

🇬🇧 [View in English](README.en.md)

---

## Características principales

### 🏋️ Gestión de miembros
- Registro, edición y eliminación de miembros
- Búsqueda en tiempo real por nombre, cédula o teléfono
- Filtros de asistencia: Todos / Marcaron hoy / Pendientes hoy
- Estado de membresía activo/inactivo con vencimiento automático

### 📋 Planes de membresía
- Creación de planes con duración flexible (días, semanas, meses)
- Precio por plan con estadísticas de uso
- Vinculación automática con pagos

### 💳 Pagos
- Registro de pagos con múltiples métodos
- Cálculo automático de fechas de membresía al registrar un pago
- Dashboard con ingresos del mes y totales históricos

### ✅ Control de asistencia diaria
- Registro de ingreso por **código único** de cliente o cédula
- Escáner de **código QR** con cámara en tiempo real (html5-qrcode)
- Validación automática: bloquea ingreso si membresía vencida o inactiva
- Limpieza automática de asistencias al iniciar un nuevo día
- Panel de "Asistencia de hoy" con historial en tiempo real

### 📧 Código QR por correo
- Generación de QR único por miembro (`qrcode`)
- Envío del código y QR adjunto por correo electrónico (SMTP Gmail)
- Vista del QR en modal sin salir de la página

### 🔐 Autenticación
- Login/logout con Django Auth
- Todas las vistas protegidas con `@login_required`
- Redirección automática al login al abrir la app

### ⚡ UX sin recarga de página
- Marcar asistencia sin recargar (fetch + actualización de fila)
- Editar registros en modal flotante
- Enviar QR con respuesta visual en modal
- Toast de notificaciones para feedback inmediato

### 🎨 Interfaz
- Tema oscuro personalizado con acento amarillo (#ffde59)
- Sidebar fijo con `position: fixed`
- Layout completamente estático (solo la tabla hace scroll)
- Diseño adaptable para móviles (≤600px)
- Pantalla de login con video de fondo y panel visual

---

## Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Backend | Python 3.14 + Django 6 |
| Base de datos | SQLite (desarrollo) |
| Frontend | HTML, CSS Grid/Flexbox, JavaScript (Fetch API) |
| QR | `qrcode[pil]` |
| Correo | SMTP Gmail via Django Email |
| Lector QR | `html5-qrcode` (CDN) |
| Control de versiones | Git + GitHub |

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/Jhoyder/ShadowGym.git
cd ShadowGym

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Instalar dependencias
pip install django qrcode[pil]

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000/`

---

## Configuración de correo (Gmail)

En `shadowfit/settings.py`:

```python
EMAIL_HOST_USER = 'tucorreo@gmail.com'
EMAIL_HOST_PASSWORD = 'contraseña_de_aplicacion'  # Google App Password
```

Para obtener la contraseña de aplicación:
1. Activa la verificación en dos pasos en tu cuenta Google
2. Ve a **Seguridad → Contraseñas de aplicaciones**
3. Genera una para "Correo" y pégala en `EMAIL_HOST_PASSWORD`

---

## Estructura del proyecto

```
ShadowGym/
├── members/          # Miembros, asistencia, QR
├── memberships/      # Planes de membresía
├── payments/         # Pagos
├── shadowfit/        # Configuración Django
├── templates/
│   ├── dashboard/    # Base, sidebar, modal
│   ├── members/      # Vista miembros + registro QR
│   ├── memberships/  # Vista planes
│   ├── payments/     # Vista pagos
│   └── registration/ # Login
└── static/
    ├── css/          # dashboard.css, login.css
    ├── img/          # Logo
    └── video/        # Video de fondo del login
```

---

## Módulos y vistas principales

### members
| URL | Vista | Descripción |
|---|---|---|
| `/members/` | `dashboard` | Panel principal con KPIs y lista |
| `/members/registro/` | `attendance_register` | Página de registro por código/QR |
| `/members/attendance/by-code/` | `mark_attendance_by_code` | Registro por código |
| `/members/<pk>/attendance/` | `mark_attendance` | Marcar asistencia (AJAX/JSON) |
| `/members/<pk>/qr/` | `member_qr` | Imagen QR del miembro |
| `/members/<pk>/send-code/` | `send_member_code_email` | Enviar QR por correo |

### memberships
| URL | Vista | Descripción |
|---|---|---|
| `/memberships/` | `dashboard` | Panel de planes |
| `/memberships/new/` | `create_plan` | Crear plan |

### payments
| URL | Vista | Descripción |
|---|---|---|
| `/payments/` | `dashboard` | Panel de pagos con revenue |
| `/payments/new/` | `create_payment` | Registrar pago |

---

## Capturas de pantalla

> Agregar capturas del dashboard, login, registro QR y modal del QR.

---

## Autor

**Jhoyder** — Desarrollado como proyecto de portafolio personal.

- GitHub: [@Jhoyder](https://github.com/Jhoyder)

---

## Licencia

Proyecto de uso personal y educativo.
