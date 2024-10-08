import {display_toast} from '../toaster.js'
const { ref, nextTick, onMounted} = Vue
export default {
    delimiters: ['[[', ']]'],
	props: {
		category: Object
	},
	setup(props) {

        const command_text = ref("")
        let editor
        const prism_lang = ref([])

        async function submit_command(){
            $("#error-code-editor").text("")            
            
            if(command_text.value.trim().length == 0){
                $("#error-code-editor").text("Give me more")
            }else{
                let url = "/command/create_command"
                const res = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": $("#csrf_token").val(), "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "title": $("#input-title").val(),
                        "description": $("#textarea-description").val(),
                        "command": command_text.value,
                        "category_id": props.category.id,
                        "lang": $("#select-prism-lang").val()
                    })
                });
                if(await res.status==200){
                    // window.location.replace("/command/")
                }
                display_toast(res)
            }
        }

        async function fetch_prism_lang() {
            const res = await fetch("/command/prism-lang")
            if(await res.status==404 ){
                display_toast(res)
            }else{
                let loc = await res.json()
                prism_lang.value = loc
            }
        }
        fetch_prism_lang()

        onMounted(() => {                

            editor = new Editor.EditorView({
                doc: "\n\n",
                extensions: [Editor.basicSetup,Editor.EditorView.updateListener.of((v) => {
                    if (v.docChanged) {
                        command_text.value = editor.state.doc.toString()
                    }
                })],
                parent: document.getElementById('id-code-editor')
            })

            $('.select2-prism-lang').select2({
                theme: 'bootstrap-5',
                dropdownParent: $("#modal-create-command")
            })
        })

        return {
            prism_lang,

            submit_command
        }
    },
	template: `
	<!-- Modal -->
    <div class="modal fade" id="modal-create-command" tabindex="-1" aria-labelledby="create-command-ModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="create-command-ModalLabel">Create a new command</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="form-floating">
                        <input class="form-control" id="input-title" type="text"/>
                        <label>Give a title to your command</label>
                    </div>
                    <div class="form-floating">
                        <textarea class="form-control" id="textarea-description"></textarea>
                        <label>Describe your command</label>
                    </div>

                    <div class="create-code-edition" id="id-code-editor"></div>
                    <div id="error-code-editor" style="color: brown;"></div>

                    <select class="select2-prism-lang" id="select-prism-lang">
                        <option v-for="lang in prism_lang" :value="lang.code">[[lang.title]]</option>
                    </select>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="submit_command">Save changes</button>
                </div>
            </div>
        </div>
    </div>

    `
}