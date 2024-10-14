import {display_toast} from '/static/js/toaster.js'
export default {
    delimiters: ['[[', ']]'],
    props: {
		doc: Object
	},
	setup(props) {

        async function edit_doc(doc_id){
			// Add file to the task
            $("#error-edit-title-"+doc_id).text()
            let title = $("#input-edit-title-" + doc_id).val()
            let description = $("#textarea-edit-description-" + doc_id).val()

            if (!title){
                $("#error-edit-title-"+doc_id).text("Need a title")
                return
            }

			const res = await fetch(
				'/documentation/' + doc_id + '/edit',{
					headers: { "X-CSRFToken": $("#csrf_token").val(), "Content-Type": "application/json" },
					method: "POST",
					body: JSON.stringify({"title": title, "description": description})
				}
			)
			if(await res.status == 200){
				props.doc.title=title
                props.doc.description=description
                $("#edit-doc-" + doc_id).modal("hide")
			}

			await display_toast(res)
		}

		return {
            edit_doc
		}
    },
	template: `
    <!-- Modal Edit Doc -->
    <div class="modal fade" :id="'edit-doc-'+doc.id" tabindex="-1" aria-labelledby="EditDocLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="EditDocLabel">Edit doc [[doc.title]]</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="row">
                        <div class="form-floating col">
                            <input class="form-control" :id="'input-edit-title-'+doc.id" :value="doc.title" type="text"/>
                            <label>Title</label>
                        </div>
                        <div class="form-floating col">
                            <textarea class="form-control" :id="'textarea-edit-description-'+doc.id" :value="doc.description"></textarea>
                            <label>Description</label>
                        </div>
                        <div :id="'error-edit-title-'+doc.id" style="color: brown;"></div>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="edit_doc(doc.id)">Save changes</button>
                </div>
            </div>
        </div>
    </div>
    `
}