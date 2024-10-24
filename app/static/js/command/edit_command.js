import {display_toast} from '../toaster.js'
const { ref, onMounted} = Vue
export default {
    delimiters: ['[[', ']]'],
    emits: ['command_edited'],
	props: {
		command: Object
	},
	setup(props, {emit}) {

        const command_text = ref("")
        let editor
        const prism_lang = ref([])

        async function submit_command(){
            $("#error-code-editor-edit-"+props.command.id).text("")            
            
            if(command_text.value.trim().length == 0){
                $("#error-code-editor-edit-"+props.command.id).text("Give me more")
            }else{
                let url = "/command/"+props.command.id+"/edit_command"
                const res = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": $("#csrf_token").val(), "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "title": $("#input-edit-title-"+props.command.id).val(),
                        "description": $("#textarea-edit-description-"+props.command.id).val(),
                        "command": command_text.value,
                        "text": command_text.value,
                        "lang": $("#select-prism-lang-edit-"+props.command.id).val()
                    })
                });
                if(await res.status==200){
                    $("#modal-edit-command-"+props.command.id).modal("hide")
                    let loc_dict = {
                        "id": props.command.id,
                        "category_id": props.command.category_id,
                        "title": $("#input-edit-title-"+props.command.id).val(),
                        "description": $("#textarea-edit-description-"+props.command.id).val(),
                        "text": command_text.value,
                        "lang": $("#select-prism-lang-edit-"+props.command.id).val()
                    }
                    emit('command_edited', loc_dict)
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

        function check_prism(lang){
            return lang==props.command.lang
        }

        onMounted(() => {                

            editor = new Editor.EditorView({
                doc: props.command.text,
                extensions: [Editor.basicSetup,Editor.EditorView.updateListener.of((v) => {
                    if (v.docChanged) {
                        command_text.value = editor.state.doc.toString()
                    }
                })],
                parent: document.getElementById('id-code-editor-edit-'+props.command.id)
            })

            $('.select2-prism-lang-editor-'+ props.command.id).select2({
                theme: 'bootstrap-5',
                dropdownParent: $("#modal-edit-command-"+ props.command.id)
            })
        })

        return {
            prism_lang,

            submit_command,
            check_prism
        }
    },
	template: `
	<!-- Modal -->
    <div class="modal fade" :id="'modal-edit-command-'+command.id" tabindex="-1" aria-labelledby="edit-command-ModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="edit-command-ModalLabel">Edit a command</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="form-floating">
                        <input class="form-control" :id="'input-edit-title-'+command.id" type="text" :value="command.title"/>
                        <label>Give a title to your command</label>
                    </div>
                    <div class="form-floating">
                        <textarea class="form-control" :id="'textarea-edit-description-'+command.id" :value="command.description"></textarea>
                        <label>Describe your command</label>
                    </div>

                    <div class="create-code-edition" :id="'id-code-editor-edit-'+command.id"></div>
                    <div id="error-code-editor" style="color: brown;"></div>

                    <select :class="'select2-prism-lang-editor-'+command.id" :id="'select-prism-lang-edit-'+command.id">
                        <option v-for="lang in prism_lang" :selected="check_prism(lang.code)" :value="lang.code">[[lang.title]]</option>
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