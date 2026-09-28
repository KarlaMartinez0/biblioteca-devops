# 📚 Sistema de Gestión de Biblioteca - DevOps

Aplicación web desarrollada en **Flask** con base de datos **PostgreSQL 15**, orquestada mediante **Docker Compose**.

---

## 👥 Autores / Integrantes

* **Valentina Suarez**
* **Karla Martinez**
* **Isabella Caicedo**
* **Ronny Gutierrez**

---

## 🏗️ Arquitectura del Sistema

* **web**: Aplicación Flask expuesta en el puerto `8080`.
* **db**: Base de datos PostgreSQL 15 con volumen persistente (`pgdata`).

---

## 🚀 Requisitos Previos

* **Docker Desktop** instalado y en ejecución.
* **Git** instalado.

---

## 🛠️ Instrucciones de Uso

### 1. Clonar el repositorio
git clone https://github.com/KarlaMartinez0/biblioteca-devops.git
cd biblioteca-devops

### 2. Iniciar la aplicación
Ejecuta el siguiente comando para construir e iniciar los contenedores:

docker compose up --build

### 3. Acceder al sistema
Abre tu navegador e ingresa a: http://localhost:8080

---

## 📂 Estructura del Proyecto

biblioteca-devops/
├── app/                  # Código fuente de la aplicación Flask
├── db/
│   └── init.sql          # Script de datos e inicialización de BD
├── .dockerignore         # Exclusiones de construcción
├── docker-compose.yml    # Orquestación de servicios
├── Dockerfile            # Construcción de la imagen Flask
└── README.md             # Documentación del proyecto

---

## 🧹 Detener el Entorno

Para detener los servicios, presiona Ctrl + C en la terminal y ejecuta:

docker compose down
