from odoo import http
from odoo.http import request
import json as json 
from datetime import datetime
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from odoo import _  

_logger = logging.getLogger(__name__) 


class AppointmentWebsite(http.Controller):

    @http.route('/my/Appointment', type='http', auth='public', website=True)
    def medical_booking_1(self, **kwargs):
        categories = request.env['appointment.category'].search([('active', '=', True)])  
        selected_category_id = int(kwargs.get('category_id', 0)) if kwargs.get('category_id') else None
        selected_treatment_id = int(kwargs.get('treatment_id', 0)) if kwargs.get('treatment_id') else None
        selected_doctor_id = kwargs.get('doctor')
        selected_available_date = kwargs.get('available_date')

        today_date = date.today()
        services = request.env['appointment.service']
        doctors = request.env['appointment.doctors'].search([])

        if selected_category_id:
            services = request.env['appointment.service'].search([('category_id', '=', selected_category_id)])

        if selected_treatment_id:
            doctors = request.env['appointment.doctors'].search([('service_ids', '=', selected_treatment_id)])

        return request.render('doctor_appointment_booking_odoo_stg.medical_booking_1', {
            'categories': categories,
            'today_date': today_date,
            'selected_category': selected_category_id,
            'services': services,
            'selected_treatment': selected_treatment_id,
            'doctors': doctors,
            'selected_doctor': selected_doctor_id,
            'available_date': selected_available_date
        })


    @http.route('/booking/step2', type='http', auth='public', website=True)
    def medical_booking_2(self, **kwargs):
        selected_available_date = kwargs.get('sub_dates')
        selected_doctor_id = kwargs.get('sub_doctor_id')
        selected_treatment_id = kwargs.get('sub_service_id')

        if selected_doctor_id:
            try:
                doctor = request.env['appointment.doctors'].sudo().browse(int(selected_doctor_id))
                doctor_name = doctor.name if doctor else None
                if doctor_name:
                    time_slots = request.env['appointment.time.slot'].sudo().search([
                        ('doctor_id', '=', doctor.id),
                        # ('booked', '=', False)  # Uncomment if you want to filter out booked slots
                    ])
                    
                    time_slots_by_day = {}
                    for slot in time_slots:
                        if slot.day not in time_slots_by_day:
                            time_slots_by_day[slot.day] = []
                        time_slots_by_day[slot.day].append((str(slot.start_time), str(slot.end_time)))

                    print('=============time_slots_by_day============', time_slots_by_day)
                    available_dates = sorted(time_slots_by_day.keys())  # Sort the days alphabetically (Monday to Sunday)
                    print('=============available_dates============', available_dates)

                else:
                    time_slots_by_day = {}
                    available_dates = []
            except Exception as e:
                time_slots_by_day = {}
                available_dates = []
                doctor_name = None
        else:
            time_slots_by_day = {}
            doctor_name = None

        return request.render('doctor_appointment_booking_odoo_stg.medical_booking_2', {
            'doctor_name': doctor_name,
            'time_slots_by_day': time_slots_by_day,
            'available_dates': available_dates,
            'selected_treatment_id': selected_treatment_id,
            'available_date': selected_available_date,
            'selected_doctor': selected_doctor_id,  
            
        })

    @http.route('/booking/step3', type='http', auth='public', website=True)
    def medical_booking_3(self, **kwargs):
    
        selectedTime = kwargs.get('selectedTime')
        selectedDate = kwargs.get('selectedDate')
        selected_doctor = kwargs.get('doctor_name')
        selected_treatment_id = kwargs.get('selected_treatment_id')

        return request.render('doctor_appointment_booking_odoo_stg.medical_booking_3', {
            'selected_doctor': selected_doctor,
            'selected_treatment_id': selected_treatment_id,
            'selectedTime':selectedTime,
            'selectedDate':selectedDate,
        })
        

    @http.route('/booking/step4', type='http', auth='public', website=True)
    def medical_booking_4(self, **kwargs):
        selected_doctor = kwargs.get('doctor_name')
        selected_treatment_id = kwargs.get('selected_treatment_id')
        user_email = kwargs.get('user_email')
        user_name = kwargs.get('user_name')
        user_contact_no = kwargs.get('user_contact_no')
        user_password = kwargs.get('user_password')
        accountCheckbox = kwargs.get('accountCheckbox') 
        selectedTime = kwargs.get('selectedTime')
        selectedDate = kwargs.get('selectedDate')
        selected_payment_option = kwargs.get('selected_payment_option')
        
        street = kwargs.get('street')
        city = kwargs.get('city')
        zipcode = kwargs.get('zipcode')
        country = kwargs.get('country')
        state = kwargs.get('state')
        
        # Format the selected date
        formatted_date = ""
        if selectedDate:
            try:
                date_obj = datetime.strptime(selectedDate, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%B %d, %Y')
            except ValueError:
                formatted_date = selectedDate

        price_with_currency = 0.0
        service_name = ""
        price = 0.0
    
       
        # Service Information
        if selected_treatment_id:
            service = request.env['appointment.service'].sudo().search([('id', '=', int(selected_treatment_id))], limit=1)
            if service:
                service_name = service.name
                price = service.price
                price_with_currency = service.price_with_currency

                
        return request.render('doctor_appointment_booking_odoo_stg.medical_booking_4', {
            'selected_doctor': selected_doctor,
            'service_name': service_name,
            'price_with_currency': price_with_currency,
            'price':price,
            'user_name': user_name,
            'user_contact_no': user_contact_no,
            'user_email': user_email,
            'user_password': user_password,
            'accountCheckbox': accountCheckbox,
            'selectedTime': selectedTime,
            'selectedDate': selectedDate,
            'formatted_date': formatted_date,
            'selected_payment_option': selected_payment_option,
            'street':street,
            'city':city,
            'zipcode':zipcode,
            'country':country,
            'state':state,
        })
        
    @http.route('/booking/step5', type='http', auth="public", website=True)
    def medical_booking_5(self, **kwargs):
        selected_doctor = kwargs.get('doctor_name')
        service_name = kwargs.get('service_name')
        price = kwargs.get('price') 
        price_with_currency = kwargs.get('price_with_currency')
        user_name = kwargs.get('user_name')
        user_email = kwargs.get('user_email')
        user_contact_no = kwargs.get('user_contact_no')
        user_password = kwargs.get('user_password')
        accountCheckbox = kwargs.get('accountCheckbox') 
        selectedTime = kwargs.get('selectedTime')
        selectedDate = kwargs.get('selectedDate')
        selected_payment_option = kwargs.get('selected_payment_option')
        street = kwargs.get('street')
        city = kwargs.get('city')
        zipcode = kwargs.get('zipcode')
        country = kwargs.get('country')
        state = kwargs.get('state')

        db_date_format = ""
        if selectedDate:
            try:
                date_obj = datetime.strptime(selectedDate, '%Y-%m-%d')
                db_date_format = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                db_date_format = selectedDate

        start_time, end_time = None, None
        if selectedTime and '-' in selectedTime:
            start_str, end_str = selectedTime.split('-')
            try:
                start_time = float(start_str.strip())
                end_time = float(end_str.strip())
            except ValueError:
                print("Error: selectedTime could not be converted to float values.")

        partner = request.env['res.partner'].sudo().search([('email', '=', user_email)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': user_name,
                'email': user_email,
                'phone': user_contact_no,
                'street': street,
                'city': city,
                'zip': zipcode,  
                'country_id': request.env['res.country'].search([('name', '=', country)], limit=1).id,
                'state_id': request.env['res.country.state'].search([('name', '=', state)], limit=1).id,
            })

        
        error_message = None
        if accountCheckbox == 'on':
            existing_user = request.env['res.users'].sudo().search([('login', '=', user_email)], limit=1)
            if existing_user:
                error_message = "An account with this email ID already exists. You can proceed with booking."
            else:
                request.env['res.users'].sudo().create({
                    'name': user_name,
                    'login': user_email,
                    'partner_id': partner.id,
                    'password': user_password,
                    'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                })

        product_id = None
        if service_name:
            service = request.env['appointment.service'].sudo().search([('name', '=', service_name)], limit=1)
            product = request.env['product.template'].sudo().search([('name', '=', service_name)], limit=1)

            if not product:
                product_data = {
                    'name': service_name,
                    'list_price': price,
                    'taxes_id': [(6, 0, [])],
                    'detailed_type': 'service',
                }
                # if service:
                #     product_data['image_1920'] = service.service_image

                product = request.env['product.template'].sudo().create(product_data)

            product_variant = product.product_variant_id
            if product_variant:
                product_id = product_variant.id

            if product:
                product.sudo().write({'website_published': True})
                product.website_published = True
                print(f"Product {product.name} has been published.")

        if selected_payment_option == 'paypal' and product_id:
            sale_order = request.website.sale_get_order(force_create=True)
            print("sale_order=====================================================", sale_order)
            
            if sale_order.partner_id != partner:
                print("--------------partner----------------------------",partner)
                sale_order.partner_id = partner.id
                sale_order.order_line.unlink()
                cart_values = sale_order._cart_update(
                    product_id=product_id,
                    add_qty=1, 
                    price_unit=price
                )
                sale_order.write({
                    'partner_invoice_id': partner.id,
                    'partner_shipping_id': partner.id,
                })
                
                if cart_values.get('quantity', 0) > 0:
                    
                    
                    doctor_id = request.env['appointment.doctors'].sudo().search([('name', '=', selected_doctor)], limit=1).id
                    doctor = request.env['appointment.doctors'].sudo().search([('name', '=', selected_doctor)], limit=1)
                    doctor_email = doctor.email if doctor else False
                    print("doctor_email=====================================================", doctor_email)

                    time_slot = request.env['appointment.time.slot'].sudo().search([
                        ('doctor_id', '=', doctor_id),
                        ('start_time', '=', start_time),
                        ('end_time', '=', end_time),
                    ], limit=1)
                    time_slot_id = time_slot.id if time_slot else False

                    if partner and doctor_id:
                        service = request.env['appointment.service'].sudo().search([('name', '=', service_name)], limit=1)
                        appointment = request.env['appointment.customer'].sudo().create({
                            'partner_id': partner.id,
                            'contact': user_contact_no,
                            'email': user_email,
                            'street': street,
                            'city': city,
                            'zip': zipcode,  
                            'country_id': request.env['res.country'].search([('name', '=', country)], limit=1).id,
                            'state_id': request.env['res.country.state'].search([('name', '=', state)], limit=1).id,
                            'doctor_id': doctor_id,
                            'appointment_date': db_date_format,
                            'service_ids': [(6, 0, [service.id])] if service else [],
                            'time_slot_id': time_slot_id,
                        })
                        
                    outgoing_mail_server = request.env['ir.mail_server'].sudo().search([], limit=1)
                    email_from_dynamic = outgoing_mail_server.from_filter if outgoing_mail_server else 'default@example.com'

                    print("email_from_dynamicemail_from_dynamicemail_from_dynamic-------------------------",email_from_dynamic)

                    if user_email:
                        try:
                            email_values_user = {
                                'subject': _('Booking Confirmation'),
                                'body_html': f"""
                                    <p>{_('Dear')} {user_name},</p>
                                    <p>{_('You have selected')} {selected_doctor} {_('for the service:')} {service_name}.</p>
                                    <p>{_('The total price for the service is')} {price_with_currency}.</p>
                                    <p>{_('Your appointment is scheduled for')} {db_date_format} {_('from')} {start_time} {_('to')} {end_time}.</p>
                                    <p>{_('Thank you for booking with us!')}</p>
                                """,
                                'email_to': user_email,
                                'email_from': email_from_dynamic,
                            }
                            mail_user = request.env['mail.mail'].sudo().create(email_values_user)
                            mail_user.send()
                            print("Email sent to user.")
                        except Exception as e:
                            print(f"Failed to send email to user: {e}")
                    if doctor_email:
                        try:
                            email_values_doctor = {
                                'subject': _('New Appointment Scheduled'),
                                'body_html': f"""
                                    <p>{_('Dear Dr.')} {selected_doctor},</p>
                                    <p>{_('A new appointment has been booked with you. Below are the details:')}</p>
                                    <ul>
                                        <li><strong>{_('Patient Name:')}</strong> {user_name}</li>
                                        <li><strong>{_('Service:')}</strong> {service_name}</li>
                                        <li><strong>{_('Date:')}</strong> {db_date_format}</li>
                                        <li><strong>{_('Time:')}</strong> {start_time} {_('to')} {end_time}</li>
                                        <li><strong>{_('Contact:')}</strong> {user_contact_no}</li>
                                        <li><strong>{_('Email:')}</strong> {user_email}</li>
                                    </ul>
                                    <p>{_('Please prepare accordingly. If you have any questions, feel free to reach out to the patient directly.')}</p>
                                    <p>{_('Thank you!')}</p>
                                """,
                                'email_cc': doctor_email,
                                'email_from': email_from_dynamic,
                            }
                            mail_doctor = request.env['mail.mail'].sudo().create(email_values_doctor)
                            mail_doctor.send()
                            print("Email sent to doctor.")
                        except Exception as e:
                            print(f"Failed to send email to doctor: {e}")


                    return request.redirect("/shop/cart")  
        else:
           
            doctor_id = request.env['appointment.doctors'].sudo().search([('name', '=', selected_doctor)], limit=1).id
            doctor = request.env['appointment.doctors'].sudo().search([('name', '=', selected_doctor)], limit=1)
            doctor_email = doctor.email if doctor else False
            print("doctor_email=====================================================", doctor_email)

            time_slot = request.env['appointment.time.slot'].sudo().search([
                ('doctor_id', '=', doctor_id),
                ('start_time', '=', start_time),
                ('end_time', '=', end_time),
            ], limit=1)
            time_slot_id = time_slot.id if time_slot else False

            
            if partner and doctor_id:
                service = request.env['appointment.service'].sudo().search([('name', '=', service_name)], limit=1)
                appointment = request.env['appointment.customer'].sudo().create({
                    'partner_id': partner.id,
                    'contact': user_contact_no,
                    'email': user_email,
                    'street': street,
                    'city': city,
                    'zip': zipcode,  
                    'country_id': request.env['res.country'].search([('name', '=', country)], limit=1).id,
                    'state_id': request.env['res.country.state'].search([('name', '=', state)], limit=1).id,
                    'doctor_id': doctor_id,
                    'appointment_date': db_date_format,
                    'service_ids': [(6, 0, [service.id])] if service else [],
                    'time_slot_id': time_slot_id,
                })
            outgoing_mail_server = request.env['ir.mail_server'].sudo().search([], limit=1)
            email_from_dynamic = outgoing_mail_server.from_filter if outgoing_mail_server else 'default@example.com'

            print("email_from_dynamicemail_from_dynamicemail_from_dynamic-------------------------",email_from_dynamic)
            
            if user_email:
                try:
                    email_values_user = {
                        'subject': _('Booking Confirmation'),
                        'body_html': f"""
                            <p>{_('Dear')} {user_name},</p>
                            <p>{_('You have selected Dr.')} {selected_doctor} {_('for the service:')} {service_name}.</p>
                            <p>{_('The total price for the service is')} {price_with_currency}.</p>
                            <p>{_('Your appointment is scheduled for')} {db_date_format} {_('from')} {start_time} {_('to')} {end_time}.</p>
                            <p>{_('Thank you for booking with us!')}</p>
                        """,
                        'email_to': user_email,
                        'email_from': email_from_dynamic,
                    }
                    mail_user = request.env['mail.mail'].sudo().create(email_values_user)
                    mail_user.send()
                    print("Email sent to user.")
                except Exception as e:
                    print(f"Failed to send email to user: {e}")
            if doctor_email:
                try:
                    email_values_doctor = {
                        'subject': _('New Appointment Scheduled'),
                        'body_html': f"""
                            <p>{_('Dear Dr.')} {selected_doctor},</p>
                            <p>{_('A new appointment has been booked with you. Below are the details:')}</p>
                            <ul>
                                <li><strong>{_('Patient Name:')}</strong> {user_name}</li>
                                <li><strong>{_('Service:')}</strong> {service_name}</li>
                                <li><strong>{_('Date:')}</strong> {db_date_format}</li>
                                <li><strong>{_('Time:')}</strong> {start_time} {_('to')} {end_time}</li>
                                <li><strong>{_('Contact:')}</strong> {user_contact_no}</li>
                                <li><strong>{_('Email:')}</strong> {user_email}</li>
                            </ul>
                            <p>{_('Please prepare accordingly. If you have any questions, feel free to reach out to the patient directly.')}</p>
                            <p>{_('Thank you!')}</p>
                        """,
                        'email_cc': doctor_email,
                        'email_from': email_from_dynamic,
                    }
                    mail_doctor = request.env['mail.mail'].sudo().create(email_values_doctor)
                    mail_doctor.send()
                    print("Email sent to doctor.")
                except Exception as e:
                    print(f"Failed to send email to doctor: {e}")
            
            return request.render('doctor_appointment_booking_odoo_stg.medical_booking_done_5', {
                'selected_doctor': selected_doctor,
                'service_name': service_name,
                'price_with_currency': price_with_currency,
                'user_name': user_name,
                'user_contact_no': user_contact_no,
                'user_email': user_email,
                'street': street,
                'city': city,
                'zipcode': zipcode,
                'country': country,
                'state': state,
                'user_password': user_password,
                'accountCheckbox': accountCheckbox,
                'selectedTime': selectedTime,
                'selectedDate': db_date_format,
                'start_time': start_time,
                'end_time': end_time,
                'error_message': error_message,
            })
    
        
   

    @http.route('/my/appointmentlist', type='http', auth="user", website=True)
    def appointment_list(self, **kwargs):
        user = request.env.user
        if not user:
            return request.redirect('/web/login')

        is_admin = user.has_group('base.group_system')  
        if is_admin:
            appointments = request.env['appointment.customer'].search([])
            invoices = request.env['account.move'].search([])
            sale_orders = request.env['sale.order'].search([])
        else:
            appointments = request.env['appointment.customer'].search([('partner_id', '=', user.partner_id.id)])
            invoices = request.env['account.move'].search([('partner_id', '=', user.partner_id.id)])
            sale_orders = request.env['sale.order'].search([('partner_id', '=', user.partner_id.id)])
        return request.render('doctor_appointment_booking_odoo_stg.portal_appointment_table_layout', {
            'docs': appointments,
            'invoices': invoices,
            'sale_orders': sale_orders,
        })
        
    @http.route('/my/Doctors', type='http', auth="user", website=True)
    def doctor_appointment_list(self, **kwargs):
        user = request.env.user
        is_admin = user.has_group('base.group_system')
        if is_admin:
            appointments = request.env['appointment.customer'].sudo().search([])
        else:
            doctor = request.env['appointment.doctors'].sudo().search([('email', '=', user.login)], limit=1)
            appointments = request.env['appointment.customer'].sudo().search([('doctor_id', '=', doctor.id)])
        return request.render('doctor_appointment_booking_odoo_stg.portal_doctor_appointment_table_layout', {
            'docs': appointments, 
        })
        
    @http.route('/my/Doctors/mark_done', type='http', auth="user", methods=['POST'], website=True)
    def mark_appointment_done(self, appointment_id):
        appointment = request.env['appointment.customer'].sudo().browse(int(appointment_id))
        if appointment.exists() and appointment.state != 'done':
            appointment.state = 'done'
        return request.redirect('/my/Doctors')
    
       
       
        
    @http.route('/booking/get_time_slot', type='http', auth="public", methods=['POST'], csrf=False)
    def appointment_date(self, **kwargs):
        date = kwargs.get('date')
        doctor_id = kwargs.get('doctor_id')
        selected_date_obj = datetime.strptime(date, '%Y-%m-%d')
        selected_day = selected_date_obj.strftime('%A').lower()  
        dr_id = request.env['appointment.time.slot'].sudo().search([('doctor_id.id', '=', doctor_id),('day', '=', selected_day)])
        # ,('booked', '=', False)
        #dr_id = request.env['appointment.time.slot'].sudo().search([])
        avaiable_slot = {}
        slot_val = 0
        for slot in dr_id:
            time = str(slot.start_time) + ' - ' + str(slot.end_time)
            #avaiable_slot.update(time)
            avaiable_slot[slot_val] = time
            slot_val+=1

        return  json.dumps(avaiable_slot)
    
  
    
class AppointmentDashboardController(http.Controller):
    


    @http.route('/dashboard/data', type='json', auth='user')
    def dashboard_data(self):
        today = datetime.today()
        db_date_format = today.strftime('%Y-%m-%d')

        # Fetch appointments for today's date
        appointments = request.env['appointment.customer'].search([('appointment_date', '=', db_date_format)])
        total_appointments = request.env['appointment.customer'].search_count([])
        done_appointments = request.env['appointment.customer'].search_count([('state', '=', 'done')])
        print("<<<<<<<<<<,,done_appointments>>>>>>>>>>>>",done_appointments)
        pending_appointments = request.env['appointment.customer'].search_count([('state', '=', 'confirm')])
        print("<<<<<<<<<<,,pending_appointments>>>>>>>>>>>>",pending_appointments)
        total_earnings = sum(request.env['appointment.customer'].search([]).mapped('price'))
        total_patients = request.env['appointment.customer'].search_count([])

        # Prepare appointment data
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'partner_name': appointment.partner_id.name,
                'doctor_name': appointment.doctor_id.name,
                'state': appointment.state,
                'time_slot_id': appointment.time_slot_id.display_name,
                'price': appointment.price,
            })

        # Monthly data
        current_year = today.year
        monthly_data = []
        for month in range(1, 13):
            start_date = datetime(current_year, month, 1)
            end_date = start_date + relativedelta(months=1, days=-1)

            monthly_appointments = request.env['appointment.customer'].search([
                ('appointment_date', '>=', start_date.date()),
                ('appointment_date', '<=', end_date.date())
            ])
            monthly_total_price = sum(monthly_appointments.mapped('price'))

            monthly_data.append({
                'month': start_date.strftime('%B'),
                'appointments': len(monthly_appointments),
                'totalEarnings': monthly_total_price,
            })

       
        data = {
            'totalAppointments': total_appointments,
            'doneAppointments': done_appointments,
            'pendingAppointments': pending_appointments,
            'totalEarnings': total_earnings,
            'totalPatients': total_patients,
            'result': appointments_data,
            'monthlyData': monthly_data,
        }

        _logger.info("Dashboard data: %s", data)
        return data