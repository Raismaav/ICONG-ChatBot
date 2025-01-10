# Consideraciones

Este documento tiene como propósito detallar las acciones necesarias para garantizar el desarrollo continuo y sostenible del proyecto ICONG ChatBot, describiendo mejoras que aumenten su mantenibilidad, escalabilidad y funcionalidad. El proyecto ICONG ChatBot es una herramienta diseñada para facilitar la interacción con un asistente virtual especializado en normatividad contable, utilizando inteligencia artificial para responder consultas y gestionar conversaciones de manera eficiente.

## Escalabilidad

Se deben tomar medidas para garantizar que el proyecto pueda escalar fácilmente a medida que crezca su uso y funcionalidad.

- **Almacenamiento en bases de datos:**
  - Actualmente, las conversaciones se almacenan utilizando el método `__save_to_file()` en la clase `message_manager.py`. Se propone reemplazar este método con uno que utilice una base de datos como `SQLite` o `MongoDB` para una gestión más eficiente y robusta de los datos.

- **Uso de embeddings:**
  - Implementar embeddings para almacenar y gestionar el contexto del asistente. Esto permitirá un manejo más eficiente de los tokens y reducirá la necesidad de consultas directas a los archivos de texto almacenados en la carpeta `context_files`.

## Mantenibilidad

Se deben implementar mejoras que faciliten el mantenimiento y la evolución del proyecto a largo plazo.

- **Documentación:**
  - Mejorar y ampliar la documentación del proyecto para incluir descripciones detalladas de cada componente y ejemplos prácticos de uso, facilitando la comprensión y mantenimiento por parte de futuros desarrolladores.

- **Estructura del proyecto:**
  - Revisar y optimizar la organización de archivos y carpetas para mantener una estructura lógica y bien definida.

- **Desacoplamiento de modelos de datos:**
  - Los módulos cruciales ya cuentan con este desacoplamiento, pero se invita a revisarlos y mejorarlos en caso de ser necesario para garantizar una mantenibilidad y escalabilidad óptimas.

- **Pruebas unitarias:**
  - Implementar pruebas unitarias utilizando un marco como `pytest` para garantizar la calidad del código y detectar errores de manera más rápida y eficiente.

- **Implementación de UIDs estándar:**
  - Establecer un sistema de identificadores únicos (UIDs) estándar para las conversaciones y los mensajes. Esto facilitará el rastreo, la auditoría y la integración de datos entre diferentes sistemas y módulos, mejorando la mantenibilidad y el manejo de los datos a largo plazo.

## Funcionalidad

Se proponen mejoras funcionales que aumenten las capacidades y usabilidad del proyecto.

- **Integración de la rama `extract-conac-data`:**
  - En esta rama existe el código necesario para realizar la actualización recurrente y automática de los archivos de normatividad, asegurando que el asistente cuente siempre con la información más reciente del CONAC.

- **Endpoint para herramientas del cliente:**
  - Implementar un endpoint que permita definir y gestionar las herramientas que el cliente puede ejecutar, asegurando que solo se declaren en el servidor las herramientas disponibles.

- **Sistema de recomendación de herramientas:**
  - Desarrollar un sistema que sugiera herramientas al usuario basado en su historial de uso, mejorando así la experiencia de interacción.

- **Chats grupales:**
  - Incorporar la funcionalidad de chats grupales, permitiendo que varios usuarios interactúen con el asistente virtual simultáneamente.

Estas consideraciones están diseñadas para guiar el desarrollo y asegurar que el proyecto pueda evolucionar de manera eficiente y sostenible.
