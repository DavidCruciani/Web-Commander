import {display_toast} from '/static/js/toaster.js'
const { ref } = Vue
export default {
    delimiters: ['[[', ']]'],
    props: {
		doc_id: Number
	},
	setup(props) {
        const files_list = ref([])

        async function fetch_files() {
            // const res_files = await fetch('/documentation/' +window.location.pathname.split("/").slice(-1)+ '/get_files')
            const res_files = await fetch('/documentation/' +props.doc_id+ '/get_files')
            if(await res_files.status == 200){
                let loc = await res_files.json()
                files_list.value = loc["files"]
            }else{
                await display_toast(res_files)
            }
        }
        fetch_files()

        async function add_file(){
			// Add file to the task
			let files = document.getElementById('formFileMultiple').files

			// Create a form with all files upload
			let formData = new FormData();
			for(let i=0;i<files.length;i++){
				formData.append("files"+i, files[i]);
			}

			const res = await fetch(
				'/documentation/' + props.doc_id + '/add_files',{
					headers: { "X-CSRFToken": $("#csrf_token").val() },
					method: "POST",
					files: files,
					body: formData
				}
			)
			if(await res.status == 200){
				// Get the new list of files of the task
				await fetch_files()
			}

			await display_toast(res)
		}

        async function delete_file(file){
			// Delete a file in the task
			const res = await fetch('/documentation/' + props.doc_id + '/delete_file/'+file.id)
			if(await res.status == 200){

				// Remove the file from list
				let index = files_list.value.indexOf(file)
				if(index > -1)
					files_list.value.splice(index, 1)
			}
			await display_toast(res)
		}

		return {
            files_list,
            
            add_file,
            delete_file
		}
    },
	template: `
    <div style="display: flex;">
        <input class="form-control" type="file" id="formFileMultiple" multiple/>
        <button class="btn btn-primary btn-sm" @click="add_file()" style="margin-left: 2px;">Submit</button>
    </div>
    <br/>
    <template v-if="files_list.length">
        <template v-for="file in files_list">
            <div>
                <a class="btn btn-link" :href="'/documentation/'+doc_id+'/download_file/'+file.id">
                    [[ file.name ]]
                </a>
                <button class="btn btn-danger btn-sm" @click="delete_file(file)"><i class="fa-solid fa-trash"></i></button>
            </div>
        </template>
    </template>
    `
}