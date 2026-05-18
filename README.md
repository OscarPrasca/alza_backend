# Manual de requerimientos — Backend Fase 1

## Proyecto

Backend para aplicación de gestión financiera personal basada en:

* Flutter (frontend)
* FastAPI (backend)
* Supabase Auth
* PostgreSQL (Supabase)

---

# 1. Objetivo de Fase 1

La fase 1 contempla únicamente:

## Funcionalidades

* CRUD de billeteras
* CRUD de categorías
* CRUD de etiquetas
* CRUD de transacciones
* Validación JWT Supabase
* API REST estandarizada
* Arquitectura limpia y escalable

---

# 2. Lo que NO entra en Fase 1

NO implementar todavía:

* IA
* OCR
* Voz
* Reportes avanzados
* Predicciones
* Notificaciones
* Background jobs
* WebSockets
* Roles complejos
* Compartir billeteras
* Presupuestos
* Metas financieras

---

# 3. Arquitectura general

```plaintext id="jlwm5p"
Flutter
   |
HTTP + JSON
   |
FastAPI
   |
PostgreSQL (Supabase)
```

---

# 4. Estándar de comunicación

## Formato de datos

Toda la API debe trabajar EXCLUSIVAMENTE con:

```http id="jlwm7w"
Content-Type: application/json
```

---

# 5. Autenticación

## Sistema de auth

Se utilizará:

* [Supabase Auth](https://supabase.com/auth?utm_source=chatgpt.com)

---

# 6. Responsabilidad de autenticación

## Flutter

Responsable de:

* login
* register
* Google login
* recovery password
* persistencia sesión

---

## FastAPI

Responsable de:

* validar JWT
* extraer user_id
* proteger endpoints

---

# 7. Estándar JWT

Todos los endpoints privados deben exigir:

```http id="jlwm9k"
Authorization: Bearer TOKEN
```

---

# 8. Validación JWT

FastAPI debe:

* validar firma JWT Supabase
* verificar expiración
* obtener:

  * user_id
  * email
  * metadata

---

# 9. Requerimientos de conexión Supabase

## La base de datos será administrada desde código

NO usar:

* Supabase auto-generated APIs
* acceso DB directo desde Flutter

---

# 10. Backend es el único acceso permitido a DB

Arquitectura obligatoria:

```plaintext id="jlwmbn"
Flutter -> FastAPI -> PostgreSQL
```

---

# 11. Variables de entorno requeridas

Archivo `.env`

```env id="jlwmdx"
APP_NAME=FinanzasAPI
APP_ENV=development

DATABASE_URL=postgresql://...

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_JWT_SECRET=xxxxx

API_V1_PREFIX=/api/v1
```

---

# 12. Estructura oficial de carpetas

## Estructura definitiva Fase 1

```plaintext id="jlwmgn"
backend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── base.py
│   │   └── migrations/
│   │
│   ├── models/
│   │   ├── wallet_model.py
│   │   ├── category_model.py
│   │   ├── tag_model.py
│   │   └── transaction_model.py
│   │
│   ├── serializers/
│   │   ├── wallet_serializer.py
│   │   ├── category_serializer.py
│   │   ├── tag_serializer.py
│   │   └── transaction_serializer.py
│   │
│   ├── services/
│   │   ├── wallet_service.py
│   │   ├── category_service.py
│   │   ├── tag_service.py
│   │   └── transaction_service.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── wallets.py
│   │       ├── categories.py
│   │       ├── tags.py
│   │       └── transactions.py
│   │
│   ├── middleware/
│   │   └── auth_middleware.py
│   │
│   ├── permissions/
│   │   └── ownership.py
│   │
│   ├── utils/
│   │   ├── responses.py
│   │   └── exceptions.py
│   │
│   └── tests/
│       ├── test_wallets.py
│       ├── test_categories.py
│       ├── test_tags.py
│       └── test_transactions.py
│
├── requirements.txt
├── .env
├── alembic.ini
└── README.md
```

---

# 13. Convención de nombres

## Reglas oficiales

### Archivos

Usar:

```plaintext id="jlwmjc"
snake_case
```

---

## Tablas

Usar plural:

```plaintext id="jlwmls"
wallets
categories
tags
transactions
```

---

## Endpoints

Usar plural REST.

Correcto:

```plaintext id="jlwmo3"
/transactions
/wallets
```

Incorrecto:

```plaintext id="jlwmq8"
/getTransactions
/createWallet
```

---

# 14. Convención UUID

TODAS las entidades deben usar:

```plaintext id="jlwmsw"
UUID
```

Nunca integers.

---

# 15. Entidades oficiales Fase 1

## wallets

Representa:

* efectivo
* banco
* nequi
* paypal
* etc

---

## categories

Representa:

* alimentación
* transporte
* ocio
* salario
* etc

---

## tags

Representa etiquetas libres:

* universidad
* novia
* mercado
* trabajo

---

## transactions

Representa:

* gastos
* ingresos

---

# 16. Relaciones obligatorias

## transaction

Debe pertenecer a:

* 1 wallet
* 1 category
* N tags
* 1 owner (user_id)

---

# 17. Propiedad de datos

TODAS las tablas deben tener:

```plaintext id="jlwmvc"
user_id
```

proveniente del JWT.

---

# 18. Seguridad obligatoria

Un usuario:

## SOLO puede:

* leer sus datos
* modificar sus datos
* eliminar sus datos

---

# 19. Sistema de permisos

## Permiso único Fase 1

### Ownership Permission

Validar:

```plaintext id="jlwmxv"
resource.user_id == jwt.user_id
```

---

# 20. Estándar request JSON

## POST/PATCH/PUT

Siempre:

```json id="jlwmzg"
{
  "data": {
    ...
  }
}
```

---

# 21. Ejemplo request

## Crear transacción

```json id="jlwn1s"
{
  "data": {
    "title": "Hamburguesa",
    "description": "Combo",
    "amount": 25000,
    "type": "expense",
    "wallet_id": "uuid",
    "category_id": "uuid",
    "tag_ids": [
      "uuid1",
      "uuid2"
    ]
  }
}
```

---

# 22. Estándar response JSON

TODAS las respuestas deben tener:

```json id="jlwn4i"
{
  "success": true,
  "message": "Texto",
  "data": {}
}
```

---

# 23. Error estándar

```json id="jlwn72"
{
  "success": false,
  "message": "Error",
  "errors": {}
}
```

---

# 24. Códigos HTTP obligatorios

| Código | Uso            |
| ------ | -------------- |
| 200    | OK             |
| 201    | Created        |
| 400    | Bad request    |
| 401    | Unauthorized   |
| 403    | Forbidden      |
| 404    | Not found      |
| 422    | Validation     |
| 500    | Internal error |

---

# 25. Endpoints oficiales

# Wallets

| Método | Endpoint      |
| ------ | ------------- |
| GET    | /wallets      |
| GET    | /wallets/{id} |
| POST   | /wallets      |
| PATCH  | /wallets/{id} |
| DELETE | /wallets/{id} |

---

# Categories

| Método | Endpoint         |
| ------ | ---------------- |
| GET    | /categories      |
| GET    | /categories/{id} |
| POST   | /categories      |
| PATCH  | /categories/{id} |
| DELETE | /categories/{id} |

---

# Tags

| Método | Endpoint   |
| ------ | ---------- |
| GET    | /tags      |
| GET    | /tags/{id} |
| POST   | /tags      |
| PATCH  | /tags/{id} |
| DELETE | /tags/{id} |

---

# Transactions

| Método | Endpoint           |
| ------ | ------------------ |
| GET    | /transactions      |
| GET    | /transactions/{id} |
| POST   | /transactions      |
| PATCH  | /transactions/{id} |
| DELETE | /transactions/{id} |

---

# 26. Filtros requeridos

## transactions

Debe soportar:

```plaintext id="jlwn9t"
?wallet_id=
?category_id=
?type=
?start_date=
?end_date=
```

---

# 27. Paginación

Formato:

```plaintext id="jlwnc9"
?page=1&limit=20
```

---

# 28. ORM oficial

Usar:

* SQLAlchemy

---

# 29. Migraciones oficiales

Usar:

* Alembic

---

# 30. Validación oficial

Usar:

* Pydantic

Aunque carpeta se llame:

```plaintext id="jlwnf3"
serializers/
```

---

# 31. ¿Qué lleva serializers/?

## Input validation

Ejemplo:

```python id="jlwnhn"
TransactionCreateSerializer
TransactionUpdateSerializer
TransactionResponseSerializer
```

---

# 32. ¿Qué lleva services/?

Toda la lógica de negocio.

Ejemplo:

* crear transacción
* validar wallet ownership
* calcular balances

---

# 33. ¿Qué lleva api/v1/?

Solo:

* endpoints
* request handling
* responses

Sin lógica compleja.

---

# 34. ¿Qué lleva models/?

Solo:

* tablas SQLAlchemy
* relaciones
* columnas

---

# 35. ¿Qué lleva middleware/?

* validación JWT
* extracción user_id

---

# 36. ¿Qué lleva permissions/?

* ownership validation

---

# 37. Balance de wallet

## Requerimiento obligatorio

Al crear/modificar/eliminar transacción:

debe actualizarse balance de wallet.

---

# 38. Tipo transacción

Valores válidos:

```plaintext id="jlwnju"
expense
income
```

---

# 39. Manejo de fechas

Formato oficial:

```plaintext id="jlwnm4"
ISO 8601
```

Ejemplo:

```plaintext id="jlwnon"
2026-04-01T10:30:00Z
```

---

# 40. Testing obligatorio

Usar:

* pytest

---

# 41. Tipos de pruebas mínimas

## CRUD tests

* create
* update
* delete
* permissions

---

# 42. Casos críticos obligatorios

## Debe probarse:

* token inválido
* acceso recurso ajeno
* category inexistente
* wallet inexistente
* amount negativo
* transaction sin wallet

---

# 43. Testing manual API

Usar:

* [Postman](https://www.postman.com?utm_source=chatgpt.com)

o Swagger automático:

```plaintext id="jlwnqf"
http://localhost:8000/docs
```

---

# 44. Flujo oficial frontend/backend

## Flutter

1. Login Supabase
2. Obtener JWT
3. Guardar sesión
4. Consumir FastAPI

---

## FastAPI

1. Validar JWT
2. Obtener user_id
3. Ejecutar lógica
4. Responder JSON estándar

---

# 45. Dependencias mínimas requeridas

```txt id="jlwnsm"
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
python-jose
alembic
pytest
httpx
```

---

# 46. Objetivo final de Fase 1

Al finalizar Fase 1 debe existir:

## Backend profesional funcional con:

* arquitectura limpia
* auth integrada Supabase
* CRUD completo financiero
* ownership seguro
* API REST consistente
* documentación Swagger
* testing básico
* base sólida para IA futura
