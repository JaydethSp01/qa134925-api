from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(title="Sistema de Reservas - Restaurante", version="1.0.0")

# CRUD generico server-side (persistencia multi-dispositivo)
try:
    from app.routers import data as _data_router
    app.include_router(_data_router.router)
except Exception as _e:
    import logging; logging.getLogger('uvicorn').warning('data router: %s', _e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic Models ────────────────────────────────────────────────────────

class Restaurante(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: str
    email: str
    capacidad_total: int
    horario_apertura: str
    horario_cierre: str
    descripcion: Optional[str] = None

class RestauranteCreate(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: str
    capacidad_total: int
    horario_apertura: str
    horario_cierre: str
    descripcion: Optional[str] = None


class Mesa(BaseModel):
    id: int
    restaurante_id: int
    numero: int
    capacidad: int
    ubicacion: str
    estado: str

class MesaCreate(BaseModel):
    restaurante_id: int
    numero: int
    capacidad: int
    ubicacion: str
    estado: str


class Cliente(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str
    fecha_registro: str
    notas: Optional[str] = None

class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    notas: Optional[str] = None


class Reserva(BaseModel):
    id: int
    cliente_id: int
    mesa_id: int
    restaurante_id: int
    fecha: str
    hora_inicio: str
    hora_fin: str
    num_personas: int
    estado: str
    notas: Optional[str] = None
    created_at: str

class ReservaCreate(BaseModel):
    cliente_id: int
    mesa_id: int
    restaurante_id: int
    fecha: str
    hora_inicio: str
    hora_fin: str
    num_personas: int
    estado: str
    notas: Optional[str] = None


# ─── Seed Data ──────────────────────────────────────────────────────────────

restaurantes_db: List[dict] = [
    {
        "id": 1,
        "nombre": "La Terraza Mediterránea",
        "direccion": "Calle Mayor 45, Madrid 28013",
        "telefono": "+34 91 234 5678",
        "email": "info@laterraza.com",
        "capacidad_total": 80,
        "horario_apertura": "12:00",
        "horario_cierre": "23:30",
        "descripcion": "Cocina mediterránea de autor con terraza en el centro de Madrid",
    },
    {
        "id": 2,
        "nombre": "El Rincón del Chef",
        "direccion": "Av. de la Castellana 120, Madrid 28046",
        "telefono": "+34 91 876 5432",
        "email": "reservas@rincondelchef.com",
        "capacidad_total": 50,
        "horario_apertura": "13:00",
        "horario_cierre": "00:00",
        "descripcion": "Alta cocina fusión española y japonesa en un ambiente íntimo",
    },
    {
        "id": 3,
        "nombre": "Brasas del Sur",
        "direccion": "Plaza de la Puerta Nueva 8, Sevilla 41001",
        "telefono": "+34 954 111 222",
        "email": "hola@brasasdelsur.com",
        "capacidad_total": 120,
        "horario_apertura": "13:30",
        "horario_cierre": "01:00",
        "descripcion": "Carnes a la brasa y tapas andaluzas con vistas a la Giralda",
    },
]

mesas_db: List[dict] = [
    {"id": 1,  "restaurante_id": 1, "numero": 1,  "capacidad": 2,  "ubicacion": "interior", "estado": "disponible"},
    {"id": 2,  "restaurante_id": 1, "numero": 2,  "capacidad": 4,  "ubicacion": "interior", "estado": "reservada"},
    {"id": 3,  "restaurante_id": 1, "numero": 3,  "capacidad": 6,  "ubicacion": "exterior", "estado": "disponible"},
    {"id": 4,  "restaurante_id": 1, "numero": 4,  "capacidad": 2,  "ubicacion": "terraza",  "estado": "ocupada"},
    {"id": 5,  "restaurante_id": 1, "numero": 5,  "capacidad": 8,  "ubicacion": "interior", "estado": "disponible"},
    {"id": 6,  "restaurante_id": 1, "numero": 6,  "capacidad": 4,  "ubicacion": "terraza",  "estado": "disponible"},
    {"id": 7,  "restaurante_id": 2, "numero": 1,  "capacidad": 4,  "ubicacion": "interior", "estado": "disponible"},
    {"id": 8,  "restaurante_id": 2, "numero": 2,  "capacidad": 2,  "ubicacion": "barra",    "estado": "disponible"},
    {"id": 9,  "restaurante_id": 2, "numero": 3,  "capacidad": 6,  "ubicacion": "exterior", "estado": "reservada"},
    {"id": 10, "restaurante_id": 2, "numero": 4,  "capacidad": 4,  "ubicacion": "interior", "estado": "mantenimiento"},
    {"id": 11, "restaurante_id": 3, "numero": 1,  "capacidad": 10, "ubicacion": "exterior", "estado": "disponible"},
    {"id": 12, "restaurante_id": 3, "numero": 2,  "capacidad": 6,  "ubicacion": "interior", "estado": "reservada"},
]

clientes_db: List[dict] = [
    {"id": 1, "nombre": "Carlos",    "apellido": "García López",      "email": "carlos.garcia@email.com",   "telefono": "+34 600 111 222", "fecha_registro": "2025-03-10", "notas": "Alergia al marisco"},
    {"id": 2, "nombre": "María",     "apellido": "Fernández Torres",  "email": "maria.fernandez@email.com", "telefono": "+34 611 333 444", "fecha_registro": "2025-04-15", "notas": None},
    {"id": 3, "nombre": "Alejandro", "apellido": "Martínez Ruiz",     "email": "alex.martinez@email.com",   "telefono": "+34 622 555 666", "fecha_registro": "2025-05-20", "notas": "Prefiere mesa exterior"},
    {"id": 4, "nombre": "Sofía",     "apellido": "López Sánchez",     "email": "sofia.lopez@email.com",     "telefono": "+34 633 777 888", "fecha_registro": "2025-06-01", "notas": "VIP — cliente frecuente"},
    {"id": 5, "nombre": "David",     "apellido": "Hernández Pérez",   "email": "david.hernandez@email.com", "telefono": "+34 644 999 000", "fecha_registro": "2025-06-10", "notas": None},
    {"id": 6, "nombre": "Laura",     "apellido": "González Díaz",     "email": "laura.gonzalez@email.com",  "telefono": "+34 655 111 333", "fecha_registro": "2026-01-05", "notas": "Vegetariana estricta"},
    {"id": 7, "nombre": "Iñigo",     "apellido": "Zabala Etxeberria", "email": "inigo.zabala@email.com",    "telefono": "+34 666 222 444", "fecha_registro": "2026-02-18", "notas": "Celiaco confirmado"},
    {"id": 8, "nombre": "Beatriz",   "apellido": "Romero Castillo",   "email": "beatriz.romero@email.com",  "telefono": "+34 677 888 555", "fecha_registro": "2026-04-03", "notas": None},
]

reservas_db: List[dict] = [
    {"id": 1, "cliente_id": 1, "mesa_id": 2,  "restaurante_id": 1, "fecha": "2026-06-28", "hora_inicio": "14:00", "hora_fin": "16:00", "num_personas": 3, "estado": "confirmada", "notas": "Cumpleaños — tarta de postre",     "created_at": "2026-06-20T10:00:00"},
    {"id": 2, "cliente_id": 2, "mesa_id": 3,  "restaurante_id": 1, "fecha": "2026-06-28", "hora_inicio": "21:00", "hora_fin": "23:00", "num_personas": 5, "estado": "confirmada", "notas": None,                                 "created_at": "2026-06-21T11:30:00"},
    {"id": 3, "cliente_id": 3, "mesa_id": 9,  "restaurante_id": 2, "fecha": "2026-06-29", "hora_inicio": "13:30", "hora_fin": "15:30", "num_personas": 4, "estado": "pendiente",  "notas": "Mesa exterior si es posible",       "created_at": "2026-06-22T09:00:00"},
    {"id": 4, "cliente_id": 4, "mesa_id": 5,  "restaurante_id": 1, "fecha": "2026-06-30", "hora_inicio": "20:00", "hora_fin": "22:30", "num_personas": 7, "estado": "confirmada", "notas": "Cliente VIP — decoración especial", "created_at": "2026-06-23T14:00:00"},
    {"id": 5, "cliente_id": 5, "mesa_id": 1,  "restaurante_id": 1, "fecha": "2026-07-01", "hora_inicio": "14:30", "hora_fin": "16:00", "num_personas": 2, "estado": "cancelada",  "notas": None,                                 "created_at": "2026-06-24T16:45:00"},
    {"id": 6, "cliente_id": 6, "mesa_id": 7,  "restaurante_id": 2, "fecha": "2026-07-02", "hora_inicio": "21:30", "hora_fin": "23:30", "num_personas": 3, "estado": "pendiente",  "notas": "Menú vegetariano para todos",       "created_at": "2026-06-25T08:20:00"},
    {"id": 7, "cliente_id": 7, "mesa_id": 12, "restaurante_id": 3, "fecha": "2026-07-03", "hora_inicio": "13:00", "hora_fin": "15:00", "num_personas": 6, "estado": "confirmada", "notas": "Sin gluten obligatorio",            "created_at": "2026-06-26T17:10:00"},
    {"id": 8, "cliente_id": 8, "mesa_id": 4,  "restaurante_id": 1, "fecha": "2026-07-04", "hora_inicio": "20:30", "hora_fin": "22:00", "num_personas": 2, "estado": "completada", "notas": "Aniversario",                       "created_at": "2026-06-27T12:00:00"},
]

restaurante_counter = len(restaurantes_db) + 1
mesa_counter       = len(mesas_db) + 1
cliente_counter    = len(clientes_db) + 1
reserva_counter    = len(reservas_db) + 1


# ─── Restaurantes CRUD ──────────────────────────────────────────────────────

@app.get("/restaurantes", response_model=List[Restaurante])
def get_restaurantes():
    return restaurantes_db


@app.get("/restaurantes/{restaurante_id}", response_model=Restaurante)
def get_restaurante(restaurante_id: int):
    item = next((r for r in restaurantes_db if r["id"] == restaurante_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    return item


@app.post("/restaurantes", response_model=Restaurante, status_code=201)
def create_restaurante(body: RestauranteCreate):
    global restaurante_counter
    nuevo = body.dict()
    nuevo["id"] = restaurante_counter
    restaurante_counter += 1
    restaurantes_db.append(nuevo)
    return nuevo


@app.put("/restaurantes/{restaurante_id}", response_model=Restaurante)
def update_restaurante(restaurante_id: int, body: RestauranteCreate):
    idx = next((i for i, r in enumerate(restaurantes_db) if r["id"] == restaurante_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    updated = body.dict()
    updated["id"] = restaurante_id
    restaurantes_db[idx] = updated
    return updated


@app.delete("/restaurantes/{restaurante_id}")
def delete_restaurante(restaurante_id: int):
    idx = next((i for i, r in enumerate(restaurantes_db) if r["id"] == restaurante_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    restaurantes_db.pop(idx)
    return {"message": "Restaurante eliminado correctamente"}


# ─── Mesas CRUD ─────────────────────────────────────────────────────────────

@app.get("/mesas", response_model=List[Mesa])
def get_mesas(
    restaurante_id: Optional[int] = Query(default=None),
    estado: Optional[str] = Query(default=None),
):
    result = list(mesas_db)
    if restaurante_id is not None:
        result = [m for m in result if m["restaurante_id"] == restaurante_id]
    if estado is not None:
        result = [m for m in result if m["estado"] == estado]
    return result


@app.get("/mesas/{mesa_id}", response_model=Mesa)
def get_mesa(mesa_id: int):
    item = next((m for m in mesas_db if m["id"] == mesa_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return item


@app.post("/mesas", response_model=Mesa, status_code=201)
def create_mesa(body: MesaCreate):
    global mesa_counter
    nueva = body.dict()
    nueva["id"] = mesa_counter
    mesa_counter += 1
    mesas_db.append(nueva)
    return nueva


@app.put("/mesas/{mesa_id}", response_model=Mesa)
def update_mesa(mesa_id: int, body: MesaCreate):
    idx = next((i for i, m in enumerate(mesas_db) if m["id"] == mesa_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    updated = body.dict()
    updated["id"] = mesa_id
    mesas_db[idx] = updated
    return updated


@app.delete("/mesas/{mesa_id}")
def delete_mesa(mesa_id: int):
    idx = next((i for i, m in enumerate(mesas_db) if m["id"] == mesa_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    mesas_db.pop(idx)
    return {"message": "Mesa eliminada correctamente"}


# ─── Clientes CRUD ──────────────────────────────────────────────────────────

@app.get("/clientes", response_model=List[Cliente])
def get_clientes(search: Optional[str] = Query(default=None)):
    if search:
        q = search.lower()
        return [
            c for c in clientes_db
            if q in c["nombre"].lower()
            or q in c["apellido"].lower()
            or q in c["email"].lower()
        ]
    return clientes_db


@app.get("/clientes/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: int):
    item = next((c for c in clientes_db if c["id"] == cliente_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return item


@app.post("/clientes", response_model=Cliente, status_code=201)
def create_cliente(body: ClienteCreate):
    global cliente_counter
    nuevo = body.dict()
    nuevo["id"] = cliente_counter
    nuevo["fecha_registro"] = datetime.now().strftime("%Y-%m-%d")
    cliente_counter += 1
    clientes_db.append(nuevo)
    return nuevo


@app.put("/clientes/{cliente_id}", response_model=Cliente)
def update_cliente(cliente_id: int, body: ClienteCreate):
    idx = next((i for i, c in enumerate(clientes_db) if c["id"] == cliente_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    updated = body.dict()
    updated["id"] = cliente_id
    updated["fecha_registro"] = clientes_db[idx]["fecha_registro"]
    clientes_db[idx] = updated
    return updated


@app.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: int):
    idx = next((i for i, c in enumerate(clientes_db) if c["id"] == cliente_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    clientes_db.pop(idx)
    return {"message": "Cliente eliminado correctamente"}


# ─── Reservas CRUD ──────────────────────────────────────────────────────────

@app.get("/reservas", response_model=List[Reserva])
def get_reservas(
    restaurante_id: Optional[int] = Query(default=None),
    cliente_id: Optional[int] = Query(default=None),
    mesa_id: Optional[int] = Query(default=None),
    fecha: Optional[str] = Query(default=None),
    estado: Optional[str] = Query(default=None),
):
    result = list(reservas_db)
    if restaurante_id is not None:
        result = [r for r in result if r["restaurante_id"] == restaurante_id]
    if cliente_id is not None:
        result = [r for r in result if r["cliente_id"] == cliente_id]
    if mesa_id is not None:
        result = [r for r in result if r["mesa_id"] == mesa_id]
    if fecha is not None:
        result = [r for r in result if r["fecha"] == fecha]
    if estado is not None:
        result = [r for r in result if r["estado"] == estado]
    return result


@app.get("/reservas/{reserva_id}", response_model=Reserva)
def get_reserva(reserva_id: int):
    item = next((r for r in reservas_db if r["id"] == reserva_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return item


@app.post("/reservas", response_model=Reserva, status_code=201)
def create_reserva(body: ReservaCreate):
    global reserva_counter
    nueva = body.dict()
    nueva["id"] = reserva_counter
    nueva["created_at"] = datetime.now().isoformat()
    reserva_counter += 1
    reservas_db.append(nueva)
    return nueva


@app.put("/reservas/{reserva_id}", response_model=Reserva)
def update_reserva(reserva_id: int, body: ReservaCreate):
    idx = next((i for i, r in enumerate(reservas_db) if r["id"] == reserva_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    updated = body.dict()
    updated["id"] = reserva_id
    updated["created_at"] = reservas_db[idx]["created_at"]
    reservas_db[idx] = updated
    return updated


@app.delete("/reservas/{reserva_id}")
def delete_reserva(reserva_id: int):
    idx = next((i for i, r in enumerate(reservas_db) if r["id"] == reserva_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    reservas_db.pop(idx)
    return {"message": "Reserva eliminada correctamente"}


# ─── Stats endpoint (dashboard) ─────────────────────────────────────────────

@app.get("/stats")
def get_stats():
    hoy = datetime.now().strftime("%Y-%m-%d")
    return {
        "total_restaurantes":   len(restaurantes_db),
        "total_mesas":          len(mesas_db),
        "mesas_disponibles":    len([m for m in mesas_db if m["estado"] == "disponible"]),
        "mesas_reservadas":     len([m for m in mesas_db if m["estado"] == "reservada"]),
        "mesas_ocupadas":       len([m for m in mesas_db if m["estado"] == "ocupada"]),
        "total_clientes":       len(clientes_db),
        "total_reservas":       len(reservas_db),
        "reservas_hoy":         len([r for r in reservas_db if r["fecha"] == hoy]),
        "reservas_confirmadas": len([r for r in reservas_db if r["estado"] == "confirmada"]),
        "reservas_pendientes":  len([r for r in reservas_db if r["estado"] == "pendiente"]),
        "reservas_canceladas":  len([r for r in reservas_db if r["estado"] == "cancelada"]),
        "reservas_completadas": len([r for r in reservas_db if r["estado"] == "completada"]),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)