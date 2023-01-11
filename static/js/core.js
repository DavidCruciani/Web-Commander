
$(document).ready(function() {
    get_command()
})


function run_command(element, flag){
    if(flag)
        data = {"command": element.parentElement.parentElement.firstElementChild.firstElementChild.outerText, "terminal": $('#tnum').val(), "flag": flag}
    else
        data = {"command": element.textContent, "terminal": $('#tnum').val(), "flag": flag}
    $.post({
        url: '/run_command',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(data) {
            $('#status').empty()
            $('#status').css("color", "green")
            $('#status').text(data['message'])
        },
        error: function(xhr, status, error) {
            $('#status').empty()
            $('#status').css("color", "brown")
            $('#status').text(xhr.responseJSON['message'])
        },
    });
}

function delete_command(element){
    // console.log(element)
    // console.log(element.parentElement.parentElement.firstElementChild)
    $.post({
        url: '/delete_command',
        data: JSON.stringify({"command": element.parentElement.parentElement.firstElementChild.outerText}),
        contentType: 'application/json',
        success: function(data) {
            $('#status').empty()
            $('#status').css("color", "green")
            $('#status').text(data['message'])
            get_command()
        },
        error: function(xhr, status, error) {
            $('#status').empty()
            $('#status').css("color", "brown")
            $('#status').text(xhr.responseJSON['message'])
        },
    });
}

function get_command(){
    $.getJSON('/get_command', function(data) {
        $('#data').empty()
        $('<tr>').append(
            $('<th>').text("COMMAND"),
            $('<th>').text("LAST RUN"),
            $('<th>').text("")
        ).appendTo('#data')
        $.each(data, function(i, item) {
            for(j in item.sort()){
                $('<tr>').append(
                    $('<td>').append(
                        $('<button>').attr("onclick", "run_command(this, false)").text(item[j]),
                        $('<button>').attr("onclick", "run_command(this, true)").text("Copy to Terminal")
                    ),
                    $('<td>'),
                    $('<td>').append(
                        $('<button>').attr("onclick", "delete_command(this)").text("Remove")
                    )
                ).appendTo("#data")
            }
        })
    })
}

function action_add(){
    $.post({
        url: '/add_command',
        data: JSON.stringify({"command": $('#Cname').val()}),
        contentType: 'application/json',
        success: function(data) {
            $('#status').empty()
            $('#status').css("color", "green")
            $('#status').text(data['message'])
            get_command()
        },
        error: function(xhr, status, error) {
            $('#status').empty()
            $('#status').css("color", "brown")
            $('#status').text(xhr.responseJSON['message'])
        },
    });
}


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

