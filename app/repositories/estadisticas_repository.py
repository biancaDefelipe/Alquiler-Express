from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, case, and_, literal_column
from sqlalchemy.sql.functions import coalesce
from models import DATABASE
from models.usuario import Usuario
from models.propiedad import Propiedad
from models.reserva import Reserva


def obtener_cantidad_inquilinos_por_fecha_registro(datos_estadistica):
    try:
        nuevos_usuarios = (DATABASE.session.query(Usuario.fecha_registro,
                                                  func.count(Usuario.id_usuario).label("cantidad_inquilinos"))
            .filter(Usuario.rol == "INQUILINO",
                    Usuario.eliminado == "NO",
                    Usuario.fecha_registro >= datos_estadistica["fecha_desde"],
                    Usuario.fecha_registro <= datos_estadistica["fecha_hasta"])
            .group_by(Usuario.fecha_registro)
            .order_by(Usuario.fecha_registro.asc())
            .all()
        )

        return nuevos_usuarios
    
    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise


def obtener_usuarios_inquilinos(datos_estadistica):
    try:
        nuevos_usuarios = (DATABASE.session.query(Usuario.nombre, Usuario.apellido,
                                                  Usuario.dni, Usuario.mail,
                                                  Usuario.telefono, Usuario.fecha_nacimiento,
                                                  Usuario.rol)
            .filter(Usuario.rol == "INQUILINO",
                    Usuario.eliminado == "NO",
                    Usuario.fecha_registro >= datos_estadistica["fecha_desde"],
                    Usuario.fecha_registro <= datos_estadistica["fecha_hasta"])
            .order_by(Usuario.fecha_registro.desc())
            .all()
        )

        return nuevos_usuarios
    
    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise


def obtener_ingresos_por_cada_propiedad(datos_estadistica):
    try:
        ingresos_por_prop = (
            DATABASE.session
            .query(
                Propiedad.id_propiedad,
                Propiedad.titulo,
                coalesce(
                    func.sum(
                        case(
                            # Positional whens en lugar de lista
                            (
                                and_(
                                    Reserva.id_propiedad == Propiedad.id_propiedad,
                                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                                ),
                                Reserva.precio_total
                            ),
                            else_=0
                        )
                    ),
                    literal_column("0")
                ).label("total_ingresos")
            )
            .outerjoin(
                Reserva,
                and_(
                    Reserva.id_propiedad == Propiedad.id_propiedad,
                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                )
            )
            .group_by(Propiedad.id_propiedad)
            .order_by(func.sum(
                case(
                    (
                        and_(
                            Reserva.id_propiedad == Propiedad.id_propiedad,
                            Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                            Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                        ),
                        Reserva.precio_total
                    ),
                    else_=0
                )
            ).desc())
            .all()
        )
        return ingresos_por_prop
    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise


def obtener_ingresos_por_tipo_propiedad(datos_estadistica):
    try:
        ingresos_por_tipo = (
            DATABASE.session
            .query(
                Propiedad.tipo,
                coalesce(
                    func.sum(
                        case(
                            (
                                and_(
                                    Reserva.id_propiedad == Propiedad.id_propiedad,
                                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                                ),
                                Reserva.precio_total
                            ),
                            else_=0
                        )
                    ),
                    literal_column("0")
                ).label("total_ingresos")
            )
            .outerjoin(
                Reserva,
                and_(
                    Reserva.id_propiedad == Propiedad.id_propiedad,
                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                )
            )
            .group_by(Propiedad.tipo)
            .order_by(func.sum(
                case(
                    (
                        and_(
                            Reserva.id_propiedad == Propiedad.id_propiedad,
                            Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                            Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                        ),
                        Reserva.precio_total
                    ),
                    else_=0
                )
            ).desc())
            .all()
        )
        return ingresos_por_tipo
    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise


def obtener_reservas_por_cada_propiedad(datos_estadistica):
    try:
        reservas_por_prop = (
            DATABASE.session
            .query(
                Propiedad.id_propiedad,
                Propiedad.titulo,
                coalesce(
                    func.sum(
                        case(
                            (
                                and_(
                                    Reserva.id_propiedad == Propiedad.id_propiedad,
                                    Reserva.estado      != "CANCELADA",
                                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                                ),
                                1
                            ),
                            else_=0
                        )
                    ),
                    literal_column("0")
                ).label("cant_reservas")
            )
            .outerjoin(
                Reserva,
                and_(
                    Reserva.id_propiedad == Propiedad.id_propiedad,
                    Reserva.estado      != "CANCELADA",
                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                )
            )
            .group_by(Propiedad.id_propiedad)
            .order_by(func.sum(
                case(
                    (
                        and_(
                            Reserva.id_propiedad == Propiedad.id_propiedad,
                            Reserva.estado      != "CANCELADA",
                            Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                            Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                        ),
                        1
                    ),
                    else_=0
                )
            ).desc())
            .all()
        )
        return reservas_por_prop
    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise


def obtener_reservas_por_tipo_propiedad(datos_estadistica):
    try:
        reservas_por_tipo = (
            DATABASE.session
            .query(
                Propiedad.tipo,
                coalesce(
                    func.sum(
                        case(
                            (
                                and_(
                                    Reserva.id_propiedad == Propiedad.id_propiedad,
                                    Reserva.estado      != "CANCELADA",
                                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                                ),
                                1
                            ),
                            else_=0
                        )
                    ),
                    literal_column("0")
                ).label("cant_reservas")
            )
            .outerjoin(
                Reserva,
                and_(
                    Reserva.id_propiedad == Propiedad.id_propiedad,
                    Reserva.estado      != "CANCELADA",
                    Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                    Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                )
            )
            .group_by(Propiedad.tipo)
            .order_by(func.sum(
                case(
                    (
                        and_(
                            Reserva.id_propiedad == Propiedad.id_propiedad,
                            Reserva.estado      != "CANCELADA",
                            Reserva.fecha_inicio <= datos_estadistica["fecha_hasta"],
                            Reserva.fecha_fin    >= datos_estadistica["fecha_desde"]
                        ),
                        1
                    ),
                    else_=0
                )
            ).desc())
            .all()
        )
        return reservas_por_tipo
    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise
