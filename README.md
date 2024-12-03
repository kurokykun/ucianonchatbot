
# Bot de Chat Anónimo - Universidad de Ciencias Informáticas (UCI)

Este bot de chat anónimo está diseñado para facilitar la comunicación entre estudiantes de la Universidad de Ciencias Informáticas (UCI). Los estudiantes pueden conectar con otros compañeros de manera anónima para charlar sin revelar su identidad.

## Funcionalidades

- **Comando /start**: Inicia el proceso de emparejamiento.
- **Preferencias de género**: Los usuarios pueden elegir con quién desean chatear (Chicos, Chicas).
- **Emparejamiento automático**: El bot empareja a los estudiantes según sus preferencias.
- **Mensajes anónimos**: Los mensajes entre usuarios son reenviados sin revelar las identidades.

## Instalación

Sigue los siguientes pasos para instalar y ejecutar el bot en tu máquina local:

### Requisitos

- Python 3.7+
- Librerías: `aiogram`, `dotenv`

### Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/nombre-del-repositorio.git
   cd nombre-del-repositorio
   ```

2. Crea un bot en Telegram usando **BotFather** y obtén el **token** del bot.

3. Configura el token en el archivo de configuración del bot:
   - Crea un archivo `.env` en la raíz del proyecto:
     ```env
     BOT_TOKEN=tu_token_aqui
     ```

4. Ejecuta el bot:
   ```bash
   python main.py
   ```

## Estructura del Proyecto

```
📁 nombre-del-repositorio/
├── main.py                # Archivo principal para iniciar el bot.
├── handlers.py            # Lógica de los comandos y eventos del bot.
├── matchmaker.py          # Módulo para la lógica de emparejamiento.
├── requirements.txt       # Dependencias del proyecto.
├── README.md              # Documentación del proyecto.
└── .env                   # Archivo para variables de entorno (no incluido por defecto).
```

## Cómo Contribuir

Si eres estudiante de la UCI y deseas contribuir al desarrollo de este bot, sigue estos pasos:

1. Haz un **fork** del repositorio.
2. Crea una **rama** para tu funcionalidad o corrección:
   ```bash
   git checkout -b nombre-de-tu-rama
   ```
3. Realiza tus cambios y haz un **commit**:
   ```bash
   git commit -m "Descripción de los cambios realizados"
   ```
4. Sube tus cambios a tu **fork**:
   ```bash
   git push origin nombre-de-tu-rama
   ```
5. Abre un **Pull Request** en el repositorio original.

## Licencia

Este proyecto está bajo una licencia GNU, lo que permite su uso, modificación y distribución. Consulta el archivo LICENSE para más detalles.

Desarrollado por:  
Kuroky 
Universidad de Ciencias Informáticas (UCI)

¡Colabora, mejora y conecta a los estudiantes de nuestra universidad! 🌟
