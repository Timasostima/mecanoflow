# MecanoFlow

MecanoFlow es una aplicación de mecanografía que ayuda a mejorar la velocidad y precisión de escritura. La aplicación ofrece diferentes modos de práctica y muestra estadísticas detalladas sobre el rendimiento del usuario.


## Instalación

1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Instala las dependencias usando pip:

> [!TIP]
> Se recomienda usar un entorno virtual para instalar las dependencias.
> Se puede crear un entorno virtual con el siguiente comando:
> ```bash
> python -m venv venv
> ```

```bash
pip install -r requirements.txt
```

## Uso

Para iniciar la aplicación, ejecuta el archivo `main.py`:

```bash
python main.py
```

## Manual de Usuario

### Interfaz Principal

- **Barra de Aplicación**: Contiene el logo que cambia del color acorde al tema.
- **Barra de Ajustes**: Contiene el menú de idiomas y personalización de los modos de práctica.
- **Área de Mecanografía**: Aquí es donde se muestra el texto para practicar y donde el usuario escribe.
- **Estadísticas**: Muestra la velocidad de escritura (WPM), precisión y errores.
- **Gráfico de Velocidad y precisión**: Es el gráfico que aparece tras finalizar una práctica. 

### Modos de Práctica

- **Modo Temporizador**: Practica durante un tiempo determinado (30, 60, 90 o 120 segundos).
- **Modo Palabras**: Practica escribiendo la candidad de palabras fija (10, 20, 30, 40).

> [!IMPORTANT]
> Hay muchos atajos de teclado que puedes usar para mejorar tu experiencia de usuario. En todos los elementos puedes ver este atajo poniento el cursor sobre el elemento.