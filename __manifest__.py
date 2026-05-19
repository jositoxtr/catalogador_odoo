{
    'name': 'Catalogador',
    'version': '1.0',
    'summary': 'Gestión de material ferroviario a escala',
    'category': 'Tools',
    'author': 'José Luis',
    'license': 'LGPL-3',
    'depends': ['base'], # Librerías de las que dependes
    'data': [
        'security/ir.model.access.csv', # Seguridad
        'views/views.xml', # Vistas
        'data/ir_cron.xml', # Tareas programadas (cron)
    ],
    # Estilo visual Moonlight
    'assets': {
        'web.assets_backend': [
            'catalogador/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'color': '#1B4D3E',
}

