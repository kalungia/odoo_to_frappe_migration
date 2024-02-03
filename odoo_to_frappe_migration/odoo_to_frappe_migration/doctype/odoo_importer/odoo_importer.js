// For license information, please see license.txt

frappe.ui.form.on("Odoo Importer", {
	refresh(frm) {
		if(frm.doc.connection_status != "Connected Successfully" || frm.doc.status != "Connection Error"){
			frm.add_custom_button(__('Test Connection'), function () {
				frappe.call({
					method: 'odoo_to_frappe_migration.odoo_to_frappe_migration.doctype.odoo_importer.odoo_importer.oodo_connector',
					args:{
						host: frm.doc.host,
						database: frm.doc.database,
						username: frm.doc.username,
						password: frm.doc.password
					},
					callback: function(r) {
						if(r.message == 2){
							frm.set_value({
								connection_status: 'Connected Successfully',
								status: 'Connected'
							});
		    				odoo_data_sample(frm);
						}else{
							frm.set_value({
								connection_status: 'Connection Unsuccessfully',
								status: 'Connection Error'
							});
		    				frm.save();
						}
					}
				})
			});
		}
		if(frm.doc.status == "Connected"){
			frm.add_custom_button(__('Start Importer'), function () {
				if(frm.doc.status == 'Connected'){
					frm.set_value({
						status: 'Ready'
					});
					frm.refresh_field('status');
				}
			});
		}
	},
});


let odoo_data_sample = function (frm) {
	frappe.call({
		method: 'odoo_to_frappe_migration.odoo_to_frappe_migration.doctype.odoo_importer.odoo_importer.odoo_data_sample',
		args:{
			docname: frm.doc.name
		},
		callback: function(r) {
			frm.refresh_field('total_data');
			frm.refresh_field('status');
		}
	})
}

