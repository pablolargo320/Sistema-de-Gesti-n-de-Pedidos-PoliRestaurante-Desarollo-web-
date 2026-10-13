from datetime import datetime
from backend.database.database import SessionLocal
from backend.entities.pedido import Pedido


class PedidoDAO:

    def crear(self, datos):
        with SessionLocal() as db:
            pedido = Pedido(
                fecha_creacion=datos.get("fecha_creacion") or datetime.now(),
                estado=datos.get("estado"),
                total=datos.get("total"),
                tipo_pedido=datos.get("tipo_pedido"),
                id_mesa=datos.get("id_mesa"),
                id_cliente=datos.get("id_cliente"),
                Administrador_id_administrador=datos.get(
                    "Administrador_id_administrador"
                ),
                metodo_pago_id_metodo_pago=datos.get(
                    "metodo_pago_id_metodo_pago"
                ),
                domiciliario_id_domiciliario=datos.get(
                    "domiciliario_id_domiciliario"
                ),
            )

            db.add(pedido)
            db.commit()
            db.refresh(pedido)

            return self._convertir_a_dict(pedido)

    def obtener_todos(self):
        with SessionLocal() as db:
            pedidos = (
                db.query(Pedido)
                .order_by(Pedido.id_pedido)
                .all()
            )

            return [
                self._convertir_a_dict(pedido)
                for pedido in pedidos
            ]

    def obtener_por_id(self, id_pedido):
        with SessionLocal() as db:
            pedido = db.get(Pedido, id_pedido)

            if pedido is None:
                return None

            return self._convertir_a_dict(pedido)

    def actualizar(self, id_pedido, datos):
        campos_permitidos = {
            "fecha_creacion",
            "estado",
            "total",
            "tipo_pedido",
            "id_mesa",
            "id_cliente",
            "Administrador_id_administrador",
            "metodo_pago_id_metodo_pago",
            "domiciliario_id_domiciliario",
        }

        with SessionLocal() as db:
            pedido = db.get(Pedido, id_pedido)

            if pedido is None:
                return None

            for campo, valor in datos.items():
                if campo in campos_permitidos:
                    setattr(pedido, campo, valor)

            db.commit()
            db.refresh(pedido)

            return self._convertir_a_dict(pedido)

    def eliminar(self, id_pedido):
        with SessionLocal() as db:
            pedido = db.get(Pedido, id_pedido)

            if pedido is None:
                return False

            db.delete(pedido)
            db.commit()

            return True

    @staticmethod
    def _convertir_a_dict(pedido):
        return {
            "id_pedido": pedido.id_pedido,
            "fecha_creacion": (
                pedido.fecha_creacion.isoformat()
                if pedido.fecha_creacion else None
            ),
            "estado": pedido.estado,
            "total": (
                float(pedido.total)
                if pedido.total is not None else None
            ),
            "tipo_pedido": pedido.tipo_pedido,
            "id_mesa": pedido.id_mesa,
            "id_cliente": pedido.id_cliente,
            "Administrador_id_administrador":
                pedido.Administrador_id_administrador,
            "metodo_pago_id_metodo_pago":
                pedido.metodo_pago_id_metodo_pago,
            "domiciliario_id_domiciliario":
                pedido.domiciliario_id_domiciliario,
        }