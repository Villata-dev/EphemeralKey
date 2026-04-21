# 🛡️ EphemeralKey

**EphemeralKey** es una herramienta integral de ciberseguridad diseñada para proteger la privacidad digital de los usuarios. Permite la generación de contraseñas de alta robustez y la creación de bandejas de correo electrónico temporales para evitar el spam y el rastreo en registros de sitios web.

Este proyecto destaca por ser una solución **híbrida**, ofreciendo tanto una interfaz web moderna como una aplicación de escritorio ligera.

---

## 🚀 Características Principales

* **Generador de Contraseñas Pro:** Algoritmos basados en la librería `secrets` de Python para asegurar aleatoriedad criptográficamente fuerte.
* **Correos Temporales Reales:** Integración con la API de 1secmail para generar direcciones de correo funcionales y revisar la bandeja de entrada en tiempo real.
* **Doble Interfaz:**
    * **Web:** Desarrollada con Flask, ideal para despliegues en la nube (como Render o Heroku).
    * **Escritorio:** Desarrollada con Tkinter, para uso local rápido y privado.
* **Seguridad:** Implementación de variables de entorno y manejo de dependencias profesional.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Framework Web:** Flask
* **Interfaz de Escritorio:** Tkinter
* **Peticiones API:** Requests
* **Estilos:** CSS3 (Glassmorphism UI) y HTML5

---

## 📂 Estructura del Proyecto

* `app.py`: Servidor Flask para la versión web.
* `gui.py`: Interfaz gráfica para la versión de escritorio.
* `core.py`: Lógica central del sistema (generación de claves y conexión con APIs).
* `static/`: Archivos CSS y JavaScript para la web.
* `templates/`: Plantillas HTML.
* `requirements.txt`: Dependencias necesarias para el funcionamiento.

---

## 💻 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Villata-dev/EphemeralKey.git](https://github.com/Villata-dev/EphemeralKey.git)
cd EphemeralKey
2. Instalar Dependencias
Se recomienda utilizar un entorno virtual para mantener la limpieza del sistema:

Bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar librerías
pip install -r requirements.txt
3. Ejecutar la Versión Web (Opción B)
Bash
python app.py
La aplicación estará disponible por defecto en http://127.0.0.1:5000

4. Ejecutar la Versión Escritorio (Opción A)
Bash
python gui.py
⚙️ ¿Cómo funciona?
Generación de Llaves
El sistema utiliza el módulo secrets de Python, que genera caracteres aleatorios seguros para aplicaciones de seguridad, proporcionando una resistencia superior frente a ataques de fuerza bruta en comparación con el módulo random estándar.

Gestión de Correos
Mediante peticiones GET a la API de 1secmail, el script solicita una dirección aleatoria. El usuario puede visualizar los mensajes recibidos directamente desde la interfaz, facilitando registros rápidos sin exponer su correo personal.

👤 Autor
Francisco Villa - Villata-dev
Desarrollador de Software enfocado en Ciberseguridad y Soluciones Eficientes.