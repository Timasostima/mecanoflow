<p align="center">
  <a href="README.md">English</a>
  ｜
  <a>Español</a>
</p>

# MecanoFlow

MecanoFlow es una aplicación de mecanografía que ayuda a mejorar la velocidad y precisión de escritura. La aplicación ofrece diferentes modos de práctica y muestra estadísticas detalladas sobre el rendimiento del usuario.

<p align="center">
  <img width="55%" alt="mecanoflow_logo" src="res/app_logo.png">
</p>

<details>
    <summary><h2>Images</h2></summary>
    <figure>
        <table cellspacing="0" cellpadding="0" border="0">
          <tr>
            <td style="text-align: center;">
              <img src="https://github.com/user-attachments/assets/b95ae6b2-0c32-49a5-9a25-2d3436c92641" alt="yellow theme" />
            </td>
            <td style="text-align: center;">
              <img src="https://github.com/user-attachments/assets/f0056701-eeff-4ab9-9a4e-5eed9a8035e0" alt="sky theme" />
            </td>
          </tr>
          <tr>
            <td style="text-align: center;">
              <img src="https://github.com/user-attachments/assets/8bd7f50f-f5f9-4ba5-9799-bda531923278" alt="coffee theme" />
            </td>
            <td style="text-align: center;">
              <img src="https://github.com/user-attachments/assets/505f2546-abfa-4168-b6f0-bc9f64c200ba" alt="yellow theme chart" />
            </td>
          </tr>
        </table>
    </figure>
</details>

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
