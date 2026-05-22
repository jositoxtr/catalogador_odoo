from odoo import api, fields, models
from datetime import timedelta

class TrenCatalog(models.Model):
    _name = 'tren.catalog'
    _description = 'Catálogo de Trenes'
    _order = 'name asc'

    # --- CAMPOS GENERALES ---
    miniatura = fields.Char(string="Ruta Miniatura")
    name = fields.Char(string="Nombre", required=True)
    compania = fields.Char(string="Compañía")
    
    pais = fields.Selection([
        ('Belgium', 'Belgium'), ('Euro', 'Euro'), ('France', 'France'),
        ('Germany', 'Germany'), ('Italy', 'Italy'), ('Japan', 'Japan'),
        ('Nederland', 'Nederland'), ('Spain', 'Spain'), ('Swiss', 'Swiss'),
        ('USA', 'USA')
    ], string="País")

    categoria = fields.Selection([
        ('Locomotora', 'Locomotora'), ('Emu', 'Emu'),
        ('Coche', 'Coche'), ('Furgón', 'Furgón'), ('Vagón', 'Vagón')
    ], string="Categoría")

    marca = fields.Selection([
        ('Arnold', 'Arnold'), ('Athearn', 'Athearn'), ('Bachmann', 'Bachmann'),
        ('Brawa', 'Brawa'), ('Electrotren', 'Electrotren'), ('Evemodel', 'Evemodel'),
        ('Ferromodel', 'Ferromodel'), ('Fleischmann', 'Fleischmann'), ('GreenMax', 'GreenMax'),
        ('Hispatrén', 'Hispatrén'), ('Hobbytrain', 'Hobbytrain'), ('Ibertren', 'Ibertren'),
        ('Imperio del Hobby', 'Imperio del Hobby'), ('Kato', 'Kato'), ('Liliput', 'Liliput'),
        ('Lima', 'Lima'), ('Mabar', 'Mabar'), ('MfTrain', 'MfTrain'), ('MicroACE', 'MicroACE'),
        ('Minitrix', 'Minitrix'), ('Piko', 'Piko'), ('Roco', 'Roco'), ('Startrain', 'Startrain'),
        ('Sudexpress', 'Sudexpress'), ('Tomix', 'Tomix'), ('TopTrain', 'TopTrain'), ('Trix', 'Trix')
    ], string="Marca")

    referencia = fields.Char(string="Referencia", required=True)
    librea = fields.Char(string="Librea")
    epoca = fields.Char(string="Época")
    cantidad = fields.Integer(string="Cantidad", default=1)
    precio = fields.Float(string="Precio Unitario", group_operator="sum")
    moneda = fields.Char(string="Moneda", default="EUR")
    intro = fields.Text(string="Introducción")
    comentarios = fields.Text(string="Comentarios")
    imagen_url = fields.Char(string="URL Imagen")
    imagen_html = fields.Html(string="Previsualización", compute="_compute_imagen_html")
    es_magnetico = fields.Boolean(string="Es Magnético")

    # --- CAMPOS TÉCNICOS ---
    decoder_main = fields.Char(string="Decoder Principal")
    decoder_brand_logo = fields.Char(compute="_compute_decoder_brand_logo", store=True)
    decoder_h1 = fields.Char(string="Decoder H1")
    decoder_h2 = fields.Char(string="Decoder H2")
    cv_address = fields.Integer(string="Dirección CV", default=3, group_operator=False)
    config = fields.Text(string="Configuración")
    tienda = fields.Char(string="Tienda")
    
    propulsion = fields.Selection([
        ('Vapor', 'Vapor'), ('Electricidad', 'Electricidad'),
        ('Diésel', 'Diésel'), ('Híbrido', 'Híbrido')
    ], string="Propulsión")

    # --- MANTENIMIENTO (Lógica computada) ---
    fecha_ultimo_mantenimiento = fields.Date(string="Último Mantenimiento")
    siguiente_mto = fields.Date(string="Siguiente Mantenimiento", compute="_compute_mantenimiento", store=True, compute_sudo=True)
    mantenimiento_intervalo_dias = fields.Integer(string="Días Restantes", compute="_compute_mantenimiento", compute_sudo=True)
    
    semaforo = fields.Selection([
        ('green', 'Bien'), ('amber', 'Próximo'), 
        ('red', 'Urgente'), ('stop', 'Crítico')
    ], string="Estado Mto", compute="_compute_mantenimiento", compute_sudo=True)

    # Campo calculado para sumar el precio total de cada referencia (precio unitario * cantidad)
    inversion_total = fields.Float(
    string="Inversión Real", 
    compute="_compute_inversion_total", 
    store=True
)
    _sql_constraints = [
    ('unique_nom_ref', 'unique(name, referencia)', 'La combinación de Nombre y Referencia debe ser única.')
    ]

    # Cálculo del próximo mantenimiento basado en la fecha del último mantenimiento y asignación de semáforo según la proximidad de esa fecha. Se asume un intervalo
    @api.depends('fecha_ultimo_mantenimiento')
    def _compute_mantenimiento(self):
        hoy = fields.Date.today()
        for reg in self:
            if reg.fecha_ultimo_mantenimiento:
                reg.siguiente_mto = reg.fecha_ultimo_mantenimiento + timedelta(days=120)
                delta = reg.siguiente_mto - hoy
                dias = int(delta.days) # Aseguramos casteo a entero puro
                reg.mantenimiento_intervalo_dias = delta.days
                
                if dias > 60: reg.semaforo = 'green'
                elif dias > 30: reg.semaforo = 'amber'
                elif dias >= 0: reg.semaforo = 'red'
                else: reg.semaforo = 'stop'
            else:
                reg.siguiente_mto = False
                reg.mantenimiento_intervalo_dias = 0
                reg.semaforo = 'stop'

    #  "Previsualización" de miniaturas
    @api.depends('imagen_url')
    def _compute_imagen_html(self):
        for reg in self:
            if reg.imagen_url:
                # Corregido: box-shadow en lugar de shadow
                reg.imagen_html = f'<img src="{reg.imagen_url}" style="max-height: 300px; border-radius: 8px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);"/>'
            else:
                reg.imagen_html = '<p style="color: #999;">Sin fotografía disponible</p>'
   
    # Identificación de marca del decoder principal (para mostrar su logo en la ficha)
    @api.depends('decoder_main')
    def _compute_decoder_brand_logo(self):
        for reg in self:
            # Ponemos el nombre en minúsculas para que la búsqueda no falle
            val = (reg.decoder_main or "").lower()
            
            # Lógica de reconocimiento (igual que en React)
            brand = "desconocido"
            if "esu" in val: brand = "esu"
            elif "zimo" in val: brand = "zimo"
            elif "kato" in val: brand = "kato"
            elif "d&h" in val or "doehler" in val: brand = "d-h"
            elif "viessmann" in val: brand = "viessmann"
            elif "train-" in val or "tom" in val: brand = "tom"
            elif "piko" in val: brand = "piko"
            elif "lenz" in val: brand = "lenz"
            elif "lais" in val: brand = "lais"
            elif "gfb" in val: brand = "gfb"
            elif "digitrax" in val: brand = "digitrax"
            
            # Guardamos solo el nombre de la marca (el nombre del archivo .png)
            reg.decoder_brand_logo = brand if brand != "desconocido" else "desconocido"

    # Cálculo de la inversión total por referencia (precio unitario * cantidad)
    @api.depends('precio', 'cantidad')
    def _compute_inversion_total(self):
        for reg in self:       
            reg.inversion_total = reg.precio * reg.cantidad

    # Método para actualizar los semáforos de mantenimiento (se puede llamar desde un cron)
    def _cron_actualizar_semaforos(self):
        # Buscamos solo los trenes que tienen fecha de mantenimiento 
        # (para no perder tiempo con los que están vacíos)
        trenes = self.search([('fecha_ultimo_mantenimiento', '!=', False)])
        
        for tren in trenes:
            # Ejecutamos el cálculo registro por registro
            tren._compute_mantenimiento()

