# EphemeralKey

**EphemeralKey** es una plataforma híbrida de ciberseguridad diseñada para la provisión de identidades digitales efímeras. Su arquitectura modular permite la mitigación de huellas de rastreo, la generación de entropía criptográfica de grado militar y la verificación de credenciales comprometidas en bases de datos de dominio público (*Data Breaches*).

El proyecto está diseñado bajo los estándares de **Seguridad Operativa (OpSec)** e incluye múltiples interfaces de interacción:

- Cliente de consola (**Headless CLI**)
- Aplicación de escritorio nativa
- Suite web aislada en contenedores

---

# Especificaciones Técnicas y Arquitectura Core

## Módulos de Seguridad y Criptografía

### Motor Criptográfico (CSPRNG)
Generación de credenciales basada en la librería `secrets` del estándar de Python, excluyendo caracteres ambiguos para evitar errores de transcripción.

### Diceware Passphrases
Generación de frases de contraseña de alta entropía semántica, resistentes a ataques de diccionario asimétricos.

### k-Anonymity Verification
Integración con la API de **Have I Been Pwned (HIBP)**.

El sistema:

1. Calcula localmente el hash **SHA-1**.
2. Envía únicamente los primeros **5 caracteres** del hash.
3. Verifica filtraciones sin exponer la contraseña completa, garantizando privacidad criptográfica.

### File Shredder
Algoritmo de destrucción de datos multipasada.

- Sobrescribe la ubicación física de la memoria con bytes aleatorios.
- Invoca posteriormente la eliminación mediante:

```python
os.remove()
```

---

## Protocolos de Protección (OpSec)

### Clipboard Anti-Hijacking
Rutina de purgado temporizado.

Las credenciales copiadas al portapapeles del sistema operativo se destruyen automáticamente después de **15 segundos**.

### Rate Limiting & Security Headers
El backend Web (**Flask**) implementa:

- Rate Limiting en memoria.
- Cabeceras HTTP de seguridad:
  - `Strict-Transport-Security`
  - `X-Frame-Options`

Estas medidas ayudan a mitigar:

- Denegación de Servicio (DoS)
- Clickjacking
- Diversos vectores de inyección

---

# Ecosistema y Despliegue

La plataforma permite implementaciones en distintos entornos según las necesidades operacionales.

## 1. Interfaz de Línea de Comandos (CLI)

Instalación global mediante el paquete Wheel.

Optimizado para scripting en Bash y tuberías (*pipes*).

```bash
python setup.py install

ephemeralkey --password --length 32
ephemeralkey --email
```

---

## 2. Cliente Desktop (Standalone)

Desarrollado sobre **CustomTkinter**, proporciona monitoreo asíncrono en tiempo real de la bandeja de entrada mediante **Threading**, evitando el bloqueo de la interfaz principal.

```bash
python gui.py
```

---

## 3. Suite Web (Docker)

Despliegue orientado a producción mediante **Gunicorn** y **Docker Compose**.

```bash
docker-compose up --build -d
```

---

# Desarrollo y Control de Calidad

El repositorio sigue prácticas de ingeniería de software orientadas a **CI/CD**.

## Integración Continua

Flujos de trabajo configurados en:

```text
.github/workflows/ci.yml
```

Ejecución automática de pruebas mediante **pytest**.

## Pruebas Unitarias

Cobertura de módulos de red y criptografía ubicada en:

```text
tests/
```

Implementación de **Mocking** para evitar llamadas reales a APIs durante los pipelines.

## Estandarización del Código

Configuración respaldada por:

- `.editorconfig`
- `setup.cfg`
- Hooks de **pre-commit**

---

# Información del Proyecto

**Arquitecto de Software:** Francisco Villa

**Licencia:** MIT

Consulte el archivo `LICENSE` para más información.
