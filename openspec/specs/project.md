# Project: Train Inventory Manager (Modelismo Ferroviario)

## Overview

Este proyecto es un sistema de gestión de inventario especializado para coleccionistas de modelismo ferroviario, desarrollado como un módulo personalizado en Odoo. Centraliza datos técnicos, seguimiento automático de mantenimiento y análisis visual de la colección, sustituyendo el manejo manual de archivos por una base de datos relacional.

## Main Features

### 1. Data Architecture (Models)

- Backend Relacional: Sustitución de inventario_trenes.csv por modelos de Odoo (tren.catalog).
- Campos Técnicos: Definición de los 26 campos originales usando tipos nativos (Char, Float, Boolean, Selection, Date).
- Sanitización Automática: Implementación de lógica en el modelo (create/write) para trim, capitalización y eliminación de caracteres no deseados.
- Integridad de Datos: Restricción SQL única para la combinación Nombre + Referencia.

### 2. Smart Maintenance System

- Lógica de Mantenimiento: Cálculo automático en Python.
  fecha_ultimo_mto + 120 días = fecha_siguiente_mto.
- Semáforo Dinámico (Compute Fields):
  Verde: > 60 días restantes.
  Ámbar: 30-60 días.
  Rojo: 0-30 días.
  Stop (Gris): Fecha vencida o sin datos.

### 3. Visual Inventory Gallery (Kanban)

- Vista Kanban Personalizada: Diseño de tarjetas que replican el estilo "TrainCard" (300x200px aprox).
- Indicadores Visuales Dinámicos:Logos e iconos cargados mediante URLs de Amazon S3 (para mantener la DB ligera).Widgets de prioridad para el semáforo de mantenimiento.
- Búsqueda Avanzada Nativa: Uso del Search View de Odoo para filtrar por País, Categoría, Marca y estado de mantenimiento.

### 4. Dynamic Forms & UI

- Visibilidad Condicional: Uso de attrs (o invisible en Odoo 17) para mostrar campos técnicos (Decoders, Mantenimiento, Propulsión) solo si la categoría es "Locomotora" o "EMU".
- Documentación Dinámica: Campo computado que genera el link al PDF en S3 basado en la referencia.

### 5. Analytics & Reports

- Dashboard Nativo: Aprovechamiento de las vistas Graph y Pivot de Odoo.
- Reportes Predefinidos: Inversión total, unidades por marca, porcentaje de acoplamiento magnético, etc.

### Tech Stack (Odoo Framework)

- Python: Lógica de negocio y modelos.
- XML: Definición de vistas (Kanban, Form, List, Graph).
- PostgreSQL: Motor de base de datos.
- QWeb: Motor de plantillas para las tarjetas visuales.
- Bootstrap: Maquetación de la interfaz.

### Design Goals

- "Odoo Native" Feel: Mantener la estética limpia del backend de Odoo.
- Ligereza: No almacenar imágenes en base de datos; usar links externos.
- Automatización: Minimizar la entrada manual de datos mediante campos computados.

### Scope & Constraints

- Sin Archivos CSV en Vivo: El CSV se usa solo para la importación inicial de las 498 unidades.
- Seguridad: Uso de ir.model.access.csv para definir permisos de usuario.
- Multi-compañía: Preparado para entornos multi-compañía de Odoo si fuera necesario.

### Data Dictionary (Selection Values)

- Países: Belgium, Euro, France, Germany, Italy, Japan, Nederland, Spain, Swiss, USA.
- Categoría: Locomotora, Emu, Coche, Furgón, Vagón.
- Marca: Arnold, Athearn, Bachmann, Brawa, Electrotren, Evemodel, Ferromodel, Fleischmann, GreenMax, Hispatrén, Hobbytrain, Ibertren, Imperio del Hobby, Kato, Liliput, Lima, Mabar, MfTrain, MicroACE, Minitrix, Piko, Roco, Startrain, Sudexpress, Tomix, TopTrain, Trix.
- Propulsión: Vapor, Electricidad, Diésel, Híbrido.
