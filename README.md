# 🚀 API REST con Flask

Un proyecto de API REST desarrollado con Flask y Flask-RESTful para el curso de Programación Avanzada. Esta API proporciona endpoints para gestión de recursos y autenticación de usuarios.

## 📋 Descripción del Proyecto

Este proyecto implementa una API REST moderna utilizando Flask como framework principal, con una arquitectura modular que separa claramente las responsabilidades entre rutas, recursos y vistas. Incluye un sistema de autenticación con interfaz web y está diseñado para ser escalable y fácil de mantener.

## 🛠️ Tecnologías Utilizadas

- **Backend:**
  - ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) Python 3.x
  - ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) Flask
  - Flask-RESTful (para la creación de APIs REST)

- **Frontend:**
  - ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) HTML5
  - ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) Tailwind CSS

## 📁 Estructura del Proyecto

```
Contruccion-de-API/
│
├── app.py              # Aplicación principal Flask
├── routes.py           # Definición de rutas y recursos de la API
├── recursos.py         # Lógica de recursos (en desarrollo)
├── templates/          # Plantillas HTML
│   └── login.html      # Página de inicio de sesión
├── .gitignore          # Archivos y carpetas ignorados por Git
└── README.md           # Documentación del proyecto
```

## 🎯 Funcionalidades

### ✅ Implementadas
- **API REST básica** con endpoints de demostración
- **Sistema de rutas modular** usando Flask-RESTful
- **Interfaz de login** responsiva con Tailwind CSS
- **Endpoint HelloWorld** (`/`) para pruebas básicas
- **Endpoint de items** (`/item/<id>`) para gestión de recursos

### 🔄 En desarrollo
- Sistema completo de autenticación
- CRUD completo para recursos
- Validación de datos
- Manejo de errores personalizado
- Base de datos integration

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso a paso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/AlbertHyb/Contruccion-de-API.git
   cd Contruccion-de-API
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install flask flask-restful
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

5. **Acceder a la API:**
   - Servidor local: `http://localhost:5000`
   - Login: `http://localhost:5000/login` (si está configurado)

## 📡 Endpoints Disponibles

| Método | Endpoint | Descripción | Estado |
|--------|----------|-------------|--------|
| `GET` | `/` | Mensaje de bienvenida | ✅ Activo |
| `GET` | `/item/<int:id>` | Obtener información de un item | ✅ Activo |
| `POST` | `/login` | Autenticación de usuario | 🔄 En desarrollo |

### Ejemplos de uso

**Obtener mensaje de bienvenida:**
```bash
curl -X GET http://localhost:5000/
```

**Obtener información de un item:**
```bash
curl -X GET http://localhost:5000/item/123
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
python -m pytest

# Verificar funcionamiento básico
curl -X GET http://localhost:5000/
```

## 📝 Desarrollo

### Contribuir al proyecto

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

### Estructura de commits
- `feat:` para nuevas funcionalidades
- `fix:` para correcciones de bugs
- `docs:` para cambios en documentación
- `style:` para cambios de formato
- `refactor:` para refactorización de código

## 🔧 Configuración

### Variables de entorno
Crear un archivo `.env` con las siguientes variables:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///app.db
```

## 🐛 Solución de Problemas

### Problemas comunes

1. **Error de importación de Flask:**
   ```bash
   pip install --upgrade flask flask-restful
   ```

2. **Puerto ocupado:**
   ```bash
   # Cambiar puerto en app.py o usar:
   python app.py --port 8000
   ```

3. **Problemas con entorno virtual:**
   ```bash
   deactivate
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   ```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

- **Alberto** - [AlbertHyb](https://github.com/AlbertHyb)

## 🤝 Agradecimientos

- Curso de Programación Avanzada
- Comunidad de Flask
- Documentación oficial de Python

---

⭐ **¡No olvides dar una estrella al proyecto si te resulta útil!**

📞 **¿Preguntas?** Abre un [issue](https://github.com/AlbertHyb/Contruccion-de-API/issues) en el repositorio.