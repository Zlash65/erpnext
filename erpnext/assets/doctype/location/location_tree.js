frappe.treeview_settings["Location"] = {
	ignore_fields: ["parent_location"],
	get_tree_nodes: 'erpnext.assets.doctype.location.location.get_children',
	add_tree_node: 'erpnext.assets.doctype.location.location.add_node',
	filters: [
		{
			fieldname: "location",
			fieldtype: "Link",
			options: "Location",
			label: __("Location"),
			get_query: function () {
				return {
					filters: [["Location", "is_group", "=", 1]]
				};
			}
		},
		{
			fieldname: "show_area",
			fieldtype: "Check",
			default: 0,
			label: __("Show Area"),
		}
	],
	breadcrumb: "Assets",
	root_label: "All Locations",
	get_tree_root: false,
	menu_items: [
		{
			label: __("New Location"),
			action: function () {
				frappe.new_doc("Location", true);
			},
			condition: 'frappe.boot.user.can_create.indexOf("Location") !== -1'
		}
	],
	onrender: function (node) {
		let page = frappe.treeview_settings['Location'].page;
		if(!page.fields_dict.show_area.get_value()) return;
		if (!node.is_root) {
			if (node.data.area) {
				$('<span class="total-area pull-right text-muted small">'
					+ flt(node.data.area, 3).toLocaleString('en')
					+ '</span>').insertBefore(node.$ul);
			}
		} else {
			// Get the total of all locations in square meters
			frappe.call({
				method: "erpnext.assets.doctype.location.location.get_total_location",
				args: {
					location: frappe.treeview_settings['Location'].page.fields_dict.location.get_value()
				},
				callback: function (r) {
					$('<span class="total-area pull-right text-muted small">'
						+ flt(r.message).toLocaleString('en')
						+ '</span>').insertBefore(node.$ul);
				}
			});
		}
	},
	onload: function(treeview) {
		// set on_change for area checkbox
		treeview.page.fields_dict.show_area.df.change = () => {
			treeview.make_tree();
		};

		frappe.treeview_settings['Location'].page = {};
		$.extend(frappe.treeview_settings['Location'].page, treeview.page);
		treeview.make_tree();
	},
};