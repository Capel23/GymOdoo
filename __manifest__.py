{
    'name': 'Gym Management',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Sistema de Gestión de Socios de un Gimnasio',
    'description': """
        Módulo para gestionar:
        - Socios del gimnasio
        - Suscripciones y planes
        - Clases y horarios
        - Instructores
        - Pagos y recibos
        - Reportes e informes
        - Análisis de ingresos y ocupación
    """,
    'author': 'Development Team',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_class_views.xml',
        'views/gym_instructor_views.xml',
        'views/gym_subscription_views.xml',
        'views/gym_partner_views.xml',
        'views/gym_analysis_views.xml',
        'report/gym_partner_reports.xml',
        'report/gym_partner_templates.xml',
        'data/gym_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,
}
