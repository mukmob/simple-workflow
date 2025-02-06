{
    "name": "Doctor Appointment Booking, Clinic appointment booking in odoo website, doctor scheduling odoo, patient appointment booking, appointment dashboard",
    "license": "OPL-1",
    "category":'Appointment',
    "version": "14.0.1.0.0",
    "sequence":1,
    "summary": "",
    "description": """
    Doctor Appointment Booking, Clinic appointment booking in odoo website, doctor scheduling odoo, appointment dashboard, Hospital Appointment Booking in odoo, 
    doctor appointment booking with online payment, appointment booking with offline payment option, doctor appointments in odoo.
    """,
    "author": "Steigern Tech LLP",
    "website": "https://steigerntech.com/",
    "support" : "steigerntech@gmail.com",
    "live_demo_url": "",
    "depends": ['base', 'hr','web','website','website_sale','payment','sale_management'], 
    "data": [
        'security/ir.model.access.csv',

        "views/customer_view.xml",
        "views/website_view.xml",
        "views/doctor.xml",
        "views/category.xml",
        "views/services.xml",
        "views/time_slots.xml",
        "views/web_menu.xml",
        "data/seq_customer.xml",
  
        "views/dashboard_view.xml",
    ],
  
    'images':["static/description/banner.gif"],

    
   'assets': {
       'web.qweb': [
            'doctor_appointment_booking_odoo_stg/static/src/xml/dashboard.xml',

        ],
    'web.assets_backend': [
        'doctor_appointment_booking_odoo_stg/static/src/js/chart.js',
        'doctor_appointment_booking_odoo_stg/static/src/css/dashboard.css',
        'doctor_appointment_booking_odoo_stg/static/src/js/dashboard.js',
    ],
},
    "installable": True,
    "auto_install": False,
}

