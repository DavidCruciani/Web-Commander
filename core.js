cp_box = 3

$(document).ready(function() {
    const item = document.querySelector('.item');
    item.addEventListener('dragstart', dragStart);

    /* drop targets */
    const boxes = document.querySelectorAll('.box');

    boxes.forEach(box => {
        box.addEventListener('dragenter', dragEnter)
        box.addEventListener('dragover', dragOver);
        box.addEventListener('dragleave', dragLeave);
        box.addEventListener('drop', drop);
    });
})

$('#scan').click(function() {
    actionScan();
});
$('#add').click(function() {
    actionAdd();
});


function actionScan() {
    tab_index_box = []
    for (let i=1; i< cp_box; i++){
        if ($("#box" + i).children().text()){
            tab_index_box.push(i)
        }
    }
    if(!tab_index_box)
        console.log("empty")
    else{
        text = ""
        for( i in tab_index_box){
            text += $("#box" + tab_index_box[i]).children().text() + " && "
        }
        $('<tr>').append(
            $('<td>').text(text)
        ).appendTo("#data")
    }

    
}

function actionAdd() {
    $('.drop-targets').append(
        $("<div>").attr({"class": "box", "id": "box" + cp_box})
    )

    const item = document.querySelector("#box" + cp_box);

    item.addEventListener('dragenter', dragEnter);
    item.addEventListener('dragover', dragOver);
    item.addEventListener('dragleave', dragLeave);
    item.addEventListener('drop', drop);

    cp_box += 1
}









// Drag Function
function dragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.id);
    setTimeout(() => {
        e.target.classList.add('hide');
    }, 0);
}

function dragEnter(e) {
    e.preventDefault();
    e.target.classList.add('drag-over');
}
function dragOver(e) {
    e.preventDefault();
    e.target.classList.add('drag-over');
}

function dragLeave(e) {
    e.target.classList.remove('drag-over');
}

function drop(e) {
    e.target.classList.remove('drag-over');

    // get the draggable element
    const id = e.dataTransfer.getData('text/plain');
    const draggable = document.getElementById(id);

    // add it to the drop target
    e.target.appendChild(draggable);

    // display the draggable element
    draggable.classList.remove('hide');
}