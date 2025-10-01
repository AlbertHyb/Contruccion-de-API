# API REST con Flask

Un proyecto de API REST desarrollado con Flask y Flask-RESTful para el curso de Programación Avanzada. Esta API proporciona endpoints para gestión de recursos y autenticación de usuarios.

## Descripción del Proyecto

Este proyecto implementa una API REST moderna utilizando Flask como framework principal, con una arquitectura modular que separa claramente las responsabilidades entre rutas, recursos y vistas. Incluye un sistema de autenticación con interfaz web y está diseñado para ser escalable y fácil de mantener.

## Tecnologías Utilizadas

- **Backend:**
  - ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) Python 3.x
  - ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) Flask
  - Flask-RESTful (para la creación de APIs REST)

- **Frontend:**
  - ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) HTML5
  - ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) Tailwind CSS

## Estructura del Proyecto

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

## Funcionalidades

# Construcción de API con Flask y Supabase

Este proyecto es una API y frontend minimalista para registro e inicio de sesión de usuarios, usando **Flask** y **Supabase** como backend de autenticación.

## Requisitos

- Python 3.8+
- pip
- Cuenta en [Supabase](https://supabase.com/)
- (Opcional) Entorno virtual Python

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/AlbertHyb/Contruccion-de-API.git
   cd Contruccion-de-API
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python3 -m venv .env
   source .env/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura tus claves de Supabase:**
   - Crea un archivo `config.py` (no se sube a GitHub, está en `.gitignore`).
   - Agrega tus claves:
     ```python
     SUPABASE_URL = "https://<TU_SUPABASE_URL>.supabase.co"
     SUPABASE_KEY = "<TU_SUPABASE_KEY>"
     ```

   **O usa variables de entorno** (recomendado para producción):
   - Exporta tus claves antes de correr la app:
     ```bash
     export SUPABASE_URL="https://<TU_SUPABASE_URL>.supabase.co"
     export SUPABASE_KEY="<TU_SUPABASE_KEY>"
     ```

## Uso

1. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

2. **Abre tu navegador en:**
   ```
   http://127.0.0.1:5000/login
   ```
   o
   ```
   http://127.0.0.1:5000/registro
   ```

## Estructura del proyecto

```
Contruccion-de-API/
│
├── app.py
├── config.py           # Tus claves (no se sube a GitHub)
├── recursos.py
├── routes.py
├── requirements.txt
├── templates/
│   ├── login.html
│   └── registro.html
└── ...
```

## Seguridad

- **No subas tus claves de Supabase a GitHub.**
- Usa variables de entorno o archivos ignorados por git para tus datos sensibles.

## Créditos

- [Flask](https://flask.palletsprojects.com/)
- [Supabase](https://supabase.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

¿Tienes dudas o sugerencias? ¡Abre un issue o pull request!
### Ejemplos de uso

**Obtener mensaje de bienvenida:**
```bash
curl -X GET http://localhost:5000/
```

**Obtener información de un item:**
```bash
curl -X GET http://localhost:5000/item/123
```

## Testing

```bash
# Ejecutar tests (cuando estén implementados)
python -m pytest

# Verificar funcionamiento básico
curl -X GET http://localhost:5000/
```

## Desarrollo

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

## Solución de Problemas

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

## Licencia

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
