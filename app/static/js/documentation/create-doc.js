import {display_toast} from '/static/js/toaster.js'
export default {
    delimiters: ['[[', ']]'],
    props: {
	},
	setup(props) {

        async function create_doc(){
			// Add file to the task
            $("#error-create-title").text()
            let title = $("#input-create-title").val()
            let description = $("#textarea-create-description").val()

            if (!title){
                $("#error-create-title").text("Need a title")
                return
            }

			const res = await fetch(
				'/documentation/create',{
					headers: { "X-CSRFToken": $("#csrf_token").val(), "Content-Type": "application/json" },
					method: "POST",
					body: JSON.stringify({"title": title, "description": description})
				}
			)
			if(await res.status == 200){
                $("#modal-create-doc").modal("hide")
			}

			await display_toast(res)
		}

		return {
            create_doc
		}
    },
	template: `
    <!-- Modal Create Doc -->
    <div class="modal fade" id="modal-create-doc" tabindex="-1" aria-labelledby="CreateDocLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="CreateDocLabel">Create doc</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="row">
                        <div class="form-floating col">
                            <input class="form-control" id="input-create-title" type="text"/>
                            <label>Title</label>
                        </div>
                        <div class="form-floating col">
                            <textarea class="form-control" id="textarea-create-description"></textarea>
                            <label>Description</label>
                        </div>
                        <div id="error-create-title" style="color: brown;"></div>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="create_doc()">Save changes</button>
                </div>
            </div>
        </div>
    </div>
    `
}