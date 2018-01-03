function createJSTree4Offerings() {			
	$('#offerings_tree_div').jstree({
		'plugins' : [ 'themes', 'contextmenu', 'types', 'search', 'sort' ],
		'themes' : {
			//"variant" : "large",
			"stripes" : true,
            "theme" : "classic",
            "dots" : true,
            "icons" : true 
        },
        'ui' : {
            "select_limit" : 1,
            "initially_select" : [ $("#sel_node").val() ]
		},
		'search': {
			"case_insensitive": true,
			"show_only_matches" : true
		},
		'contextmenu' : {
			'items' : customMenu
		},
		'types' : {				
			'offering' : {
				'icon' : {
					'image' : 'file.png'
                }
            },
			'folder' : {
				'icon' : {
					'image' : 'root.png'
                }
            },
			'root' : {
				'icon' : {
					'image' : 'root.png'
                }
            }
        },
		'sort' : function(a, b) {
			a1 = this.get_node(a);
			b1 = this.get_node(b);
			if (a1.icon == b1.icon){
				return (a1.text > b1.text) ? 1 : -1;
			}
		}		
	});
	function customMenu(node)
	{
		var items = {
			'add_item' : {
				'label' : 'Add New Offering',
				'action' : function () { /* action */ }
			},
			'edit_item' : {
				'label' : 'Edit',
				'action' : function () { /* action */ }
			},
			'remove_item' : {
				'label' : 'Remove',
				'action' : function () { /* action */ }
			}
		}		
		if (node.parent === 'offerings_root') {			
			delete items.add_item;			
		} else if (node.parent === '#') {
			delete items.edit_item
			delete items.remove_item;
		}
		return items;
	}	
	$(document).ready(function(){
		populate_tree();
		$('#topics_tree_div')
			.on("select_node.jstree", function (e, data) { 						
			if (data.instance.is_leaf(data.node)){				
				if(data.node.original.isclass == 'true'){				
					var offerings_found = false;
					var sparql = 'select * {?offering rdf:type hw:offeringClassification\\/' + decode_text_2_id(data.node.id) +' }';
					sparqlQuery(sparql, function(json_query_results){
						var offerings_json = JSON.parse(json_query_results);
						var bindings = offerings_json['results']['bindings'];	
						var existing_json = document.getElementById("topics_jstree_compatible_json").value
						existing_json = existing_json.substr(0, existing_json.lastIndexOf(']'));						
						for (key in bindings) {							
							var offering = bindings[key]['offering']['value'];
							offering = offering.substr(offering.lastIndexOf('/') + 1);
							offering = decode_id_2_text(offering); 
							var offering_text = offering.substr(0, offering.lastIndexOf('-'));
							var offering_entry = ', {"id": "'+ offering +'", "parent": "'+ decode_id_2_text(data.node.id) +'", "text": "'
												+offering_text +'", "isclass":"false","icon": "/"}';											
							existing_json = existing_json + offering_entry;
							offerings_found = true;
						}						
						existing_json = existing_json + ']';							
						document.getElementById("offering_jstree_compatible_json").value = 	existing_json;										
						if (offerings_found)
							populate_tree();
					});																		
				} else {
					var selected_offering_id = data.node.id											
					document.getElementById("selected_product_or_offering_id").value = decode_text_2_id(data.node.id);									
					document.getElementById("selected_product_or_offering_name").value = data.node.id.substr(0, data.node.id.lastIndexOf('-'));
					document.getElementById("btnCreateLabel").style.display = 'inline-block';
					document.getElementById("selected_node_type").value = 'OFFERING';
					createTable4SelectedOffering(decode_text_2_id(data.node.id));	// offerings_attrib_val_table.js						
					offeringContentsCollapsibleTree();	
				}
			}			
		});
		$("#search_offering_field").keyup(function () { 
			var value=document.getElementById("search_offering_field").value; 			
			$("#topics_tree_div").jstree("search", value) 
		}); 		 
	}); 			
}

populate_tree = function(){
	$("#topics_tree_div").jstree(true).settings.core.data = JSON.parse(document.getElementById("offering_jstree_compatible_json").value);
	$("#topics_tree_div").jstree(true).refresh();	
	$("#topics_tree_div").bind("loaded.jstree", function (event, data) {data.instance.open_all();}); 
}
