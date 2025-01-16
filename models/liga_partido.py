from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LigaPartido(models.Model):
    _name = 'liga.partido'
    _description = 'Un partido de la liga'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local')
    goles_casa = fields.Integer()

    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante')
    goles_fuera = fields.Integer()

    @api.constrains('equipo_casa')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_casa:
                raise ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos del partido deben ser diferentes.')

    @api.constrains('equipo_fuera')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_fuera:
                raise ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos del partido deben ser diferentes.')

    def actualizoRegistrosEquipo(self):
        for recordEquipo in self.env['liga.equipo'].search([]):
            recordEquipo.victorias = 0
            recordEquipo.empates = 0
            recordEquipo.derrotas = 0
            recordEquipo.goles_a_favor = 0
            recordEquipo.goles_en_contra = 0
            recordEquipo.puntos = 0

            for recordPartido in self.env['liga.partido'].search([]):
                if recordPartido.equipo_casa == recordEquipo:
                    diferencia = recordPartido.goles_casa - recordPartido.goles_fuera
                    if diferencia > 0:
                        recordEquipo.victorias += 1
                        recordEquipo.puntos += 4 if diferencia >= 4 else 3
                    elif diferencia == 0:
                        recordEquipo.empates += 1
                        recordEquipo.puntos += 1
                    else:
                        recordEquipo.derrotas += 1
                        if abs(diferencia) >= 4:
                            recordEquipo.puntos -= 1

                    recordEquipo.goles_a_favor += recordPartido.goles_casa
                    recordEquipo.goles_en_contra += recordPartido.goles_fuera

                if recordPartido.equipo_fuera == recordEquipo:
                    diferencia = recordPartido.goles_fuera - recordPartido.goles_casa
                    if diferencia > 0:
                        recordEquipo.victorias += 1
                        recordEquipo.puntos += 4 if diferencia >= 4 else 3
                    elif diferencia == 0:
                        recordEquipo.empates += 1
                        recordEquipo.puntos += 1
                    else:
                        recordEquipo.derrotas += 1
                        if abs(diferencia) >= 4:
                            recordEquipo.puntos -= 1

                    recordEquipo.goles_a_favor += recordPartido.goles_fuera
                    recordEquipo.goles_en_contra += recordPartido.goles_casa

    def sumar_goles_casa(self):
        for record in self:
            record.goles_casa += 2
        self.actualizoRegistrosEquipo()

    def sumar_goles_fuera(self):
        for record in self:
            record.goles_fuera += 2
        self.actualizoRegistrosEquipo()

class CrearPartidoWizard(models.TransientModel):
    _name = 'crear.partido.wizard'

    equipo_casa = fields.Many2one('liga.equipo', string="Equipo Local", required=True)
    equipo_fuera = fields.Many2one('liga.equipo', string="Equipo Visitante", required=True)

    def crear_partido(self):
        self.env['liga.partido'].create({
            'equipo_casa': self.equipo_casa.id,
            'equipo_fuera': self.equipo_fuera.id,
        })

