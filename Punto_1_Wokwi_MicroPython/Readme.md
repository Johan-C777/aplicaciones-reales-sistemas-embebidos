# Punto 1 - Desarrollo en MicroPython utilizando Wokwi

## Objetivo

Desarrollar en Wokwi una aplicación utilizando un ESP32 programado con MicroPython a partir del esquema suministrado en clase.

## Componentes

- 1 ESP32
- 2 pulsadores
- 2 LEDs
- 2 resistencias limitadoras para los LEDs

## Conexiones

| Elemento | GPIO |
|---|---|
| Pulsador 1 | GPIO 13 |
| Pulsador 2 | GPIO 14 |
| LED rojo | GPIO 25 |
| LED verde | GPIO 26 |

Los pulsadores utilizan las resistencias `PULL_UP` internas del ESP32.

## Funcionamiento

El programa utiliza programación asíncrona para ejecutar varias tareas.

Se implementan:

- Una tarea productora.
- Una tarea consumidora.
- Una cola para intercambio de información.
- Detección de eventos de los pulsadores.
- Control independiente de los dos LEDs.

Al presionar el pulsador 1 se controla el LED rojo.

Al presionar el pulsador 2 se controla el LED verde.

Adicionalmente, una tarea productora genera datos periódicamente y una tarea consumidora recibe dichos datos.

## Archivos

- `main.py`: programa desarrollado en MicroPython.
- `diagram.json`: configuración del circuito utilizado en Wokwi.

## Simulación

El proyecto fue desarrollado y probado utilizando Wokwi con un ESP32 y MicroPython.

## Enlace de Wokwi

[Ver simulación en Wokwi]https://wokwi.com/projects/471976762101862401
