import copy


class EventoPrototype:
    """
    Prototype pattern.
    Load an existing Evento from the DB, clone it, tweak it, save it back.
    """

    def __init__(self, evento_db=None):
        if evento_db:
            self._load_from_db(evento_db)
        else:
            self.nombre        = ""
            self.tipo_id       = None
            self.ubicacion_id  = None
            self.fecha_inicio  = None
            self.fecha_fin     = None
            self.descripcion   = ""
            self.max_asistentes = 100
            self.servicios_ids = []
            self.config        = {}

    def _load_from_db(self, evento):
        self.nombre         = evento.nombre
        self.tipo_id        = evento.tipo_id
        self.ubicacion_id   = evento.ubicacion_id
        self.fecha_inicio   = evento.fecha_inicio
        self.fecha_fin      = evento.fecha_fin
        self.descripcion    = evento.descripcion
        self.max_asistentes = evento.max_asistentes
        self.servicios_ids  = list(evento.servicios.values_list('id', flat=True))
        if hasattr(evento, 'configuracion'):
            cfg = evento.configuracion
            self.config = {
                'tiene_catering':    cfg.tiene_catering,
                'tiene_escenario':   cfg.tiene_escenario,
                'tiene_iluminacion': cfg.tiene_iluminacion,
                'tiene_seguridad':   cfg.tiene_seguridad,
                'tiene_streaming':   cfg.tiene_streaming,
                'tiene_decoracion':  cfg.tiene_decoracion,
                'notas_adicionales': cfg.notas_adicionales,
            }
        else:
            self.config = {}

    def clonar(self) -> 'EventoPrototype':
        """Return a deep copy of this prototype."""
        return copy.deepcopy(self)

    def set_nombre(self, nombre: str) -> 'EventoPrototype':
        self.nombre = nombre
        return self

    def set_fechas(self, inicio, fin) -> 'EventoPrototype':
        self.fecha_inicio = inicio
        self.fecha_fin    = fin
        return self

    def set_max_asistentes(self, cantidad: int) -> 'EventoPrototype':
        self.max_asistentes = cantidad
        return self

    def set_descripcion(self, descripcion: str) -> 'EventoPrototype':
        self.descripcion = descripcion
        return self

    def save_to_db(self, organizador):
        """Persist the clone as a new Evento row and return it."""
        from web.models import Evento, ConfiguracionEvento   # ← import from web

        evento = Evento.objects.create(
            nombre          = self.nombre,
            tipo_id         = self.tipo_id,
            ubicacion_id    = self.ubicacion_id,
            fecha_inicio    = self.fecha_inicio,
            fecha_fin       = self.fecha_fin,
            descripcion     = self.descripcion,
            max_asistentes  = self.max_asistentes,
            organizador     = organizador,
            es_clon         = True,
        )
        evento.servicios.set(self.servicios_ids)

        if self.config:
            ConfiguracionEvento.objects.create(evento=evento, **self.config)

        return evento

    def __str__(self):
        return (
            f"EventoPrototype(nombre={self.nombre}, "
            f"inicio={self.fecha_inicio}, fin={self.fecha_fin})"
        )