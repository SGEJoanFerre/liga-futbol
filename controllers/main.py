# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web
class Main(http.Controller):
    # Decorador que indica que la URL "/ligafutbol/equipo/json" atenderá por HTTP, sin autenticación
    # Devolverá texto que estará en formato JSON
    # Se puede probar accediendo a http://localhost:8069/ligafutbol/equipo/json
    @http.route('/ligafutbol/equipo/json', type='http', auth='none')
    def obtenerDatosEquiposJSON(self):
        # Obtenemos la referencia al modelo de Equipo
        equipos = request.env['liga.equipo'].sudo().search([])

        # Generamos una lista con información que queremos sacar en JSON
        listaDatosEquipos = []
        for equipo in equipos:
            listaDatosEquipos.append([
                equipo.nombre,
                str(equipo.fecha_fundacion),
                equipo.jugados,
                equipo.puntos,
                equipo.victorias,
                equipo.empates,
                equipo.derrotas
            ])
        # Convertimos la lista generada a JSON
        json_result = json.dumps(listaDatosEquipos)

        return json_result

    # Nueva funcionalidad para eliminar partidos empatados
    @http.route('/eliminarempates', type='http', auth='user', methods=['GET'], csrf=False)
    def eliminar_empates(self):
        # Obtenemos todos los partidos empatados
        partidos = request.env['liga.partido'].sudo().search([('goles_casa', '=', 'goles_fuera')])
        cantidad = len(partidos)

        # Eliminamos los partidos
        partidos.unlink()

        # Retornamos el número de partidos eliminados
        return f"Se eliminaron {cantidad} partidos empatados."

