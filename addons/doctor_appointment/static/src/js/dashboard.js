odoo.define('doctor_appointment_booking_odoo_stg.MyCustomAction', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var MyCustomAction = AbstractAction.extend({
        template: 'CustomDashBoard',
        start: function () {
            this._super.apply(this, arguments);
            console.log("Custom Action Loaded");
        }
    });

    core.action_registry.add("dashboard_tags", MyCustomAction);

    return MyCustomAction;
});
