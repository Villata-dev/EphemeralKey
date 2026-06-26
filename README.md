# EphemeralKey: Suite de Gestión de Identidad y Credenciales

**EphemeralKey** es una aplicación híbrida de ciberseguridad diseñada para la generación de credenciales criptográficamente seguras y la administración de direcciones de correo electrónico desechables. El sistema implementa características avanzadas de seguridad operativa (OpSec) para mitigar el rastreo y la exposición de datos durante el registro en plataformas de terceros.

El proyecto presenta una arquitectura de despliegue dual, ofreciendo un cliente de escritorio nativo para entornos locales aislados y una interfaz web basada en API REST para despliegues en red.

---

## Características Arquitectónicas y de Seguridad

- **Motor Criptográfico**
  - Generación de contraseñas de alta entropía utilizando el módulo `secrets` de Python, garantizando un nivel de aleatoriedad resistente a ataques de fuerza bruta.

- **Análisis Heurístico en Tiempo Real**
  - Evaluación dinámica de la fuerza de la contraseña mediante cálculos de entropía de Shannon vinculados a eventos de teclado, proporcionando métricas de seguridad precisas.

- **Monitorización Asíncrona de Bandeja de Entrada**
  - Integración con la API REST de **1secmail** para el aprovisionamiento de buzones efímeros.
  - Utiliza hilos de ejecución (`threading`) para el sondeo y recuperación de mensajes entrantes sin bloquear el proceso principal.

- **Protocolos OpSec (Seguridad Operativa)**
  - **Anti-Hijacking:** purgado automático del portapapeles tras **15 segundos** para prevenir la lectura no autorizada por malware residente.
  - **Exportación Local:** almacenamiento temporal de identidades efímeras en archivos locales.

- **Arquitectura de Interfaz Dual**
  - **Desktop Client:** desarrollado con `customtkinter`, ofreciendo una interfaz moderna y optimizada para operaciones locales.
  - **Web Suite:** servidor **Flask** que expone una API REST consumida por un frontend asíncrono con diseño **Glassmorphism**.

---

# Stack Tecnológico

| Categoría | Tecnología |
|-----------|------------|
| Lenguaje Core | Python 3.x |
| Concurrencia | `threading` |
| Backend | Flask (API REST) |
| Frontend Desktop | CustomTkinter |
| Frontend Web | HTML5, CSS3, JavaScript (Fetch API) |
| Integración de Red | requests |

---

# Estructura del Repositorio

```text
EphemeralKey/
│
├── app.py                  # Servidor Flask y endpoints REST
├── gui.py                  # Cliente de escritorio
├── templates/
│   └── index.html          # Interfaz web
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

> **Nota:** Los módulos de generación y conexión fueron encapsulados directamente en las interfaces para optimizar los flujos de ejecución de la versión actual.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/Villata-dev/EphemeralKey.git
cd EphemeralKey
```

---

## 2. Crear un entorno virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecución

## Cliente de Escritorio

Ejecuta la interfaz gráfica con las funciones de seguridad a nivel de sistema.

```bash
python gui.py
```

---

## Servidor Web

Inicia el servidor Flask.

```bash
python app.py
```

La aplicación estará disponible en:

```
http://127.0.0.1:5000
```

---

# Autor

**Francisco Villa** *(Villata-dev)*

Desarrollo de Software e Ingeniería de Seguridad.