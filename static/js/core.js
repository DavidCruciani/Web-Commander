
$(document).ready(function() {
    get_command()

    $("#searchbar").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#data tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
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
            get_command()
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
    // console.log(element.parentElement.parentElement.firstElementChild.firstElementChild)
    $.post({
        url: '/delete_command',
        data: JSON.stringify({"command": element.parentElement.parentElement.firstElementChild.firstElementChild.outerText}),
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

function get_command(flag = -1){
    // console.log(window.location.search)
    $.getJSON('/get_command'+window.location.search, function(data) {
        $('#data').empty()
        $('<tr>').append(
            $('<th>'),
            $('<th>').text("COMMAND"),
            $('<th>').text("LAST RUN"),
            $('<th>').text("")
        ).appendTo('#data')
        cp = 0
        $.each(data, function(i, item) {
            for(j in item.sort()){
                if( flag == cp){
                    spe_div = $('<div>').attr({"class": "collapse show", "id": "collapse_"+cp})
                }
                else{
                    spe_div = $('<div>').attr({"class": "collapse", "id": "collapse_"+cp})
                }
                $('<tr>').append(
                    $('<td>').append(
                        $("<a>").attr({"class": "btn btn-primary", "data-toggle": "collapse", "href": "#collapse_"+cp, "role": "button", "aria-expanded": "false", "aria-controls": "collapse"+cp}).text("🔽"),
                    ),
                    $('<td>').append(
                        $('<button>').attr("onclick", "run_command(this, false)").text(item[j][0]).css({
                            "padding": "7px",
                            "box-sizing": "border-box",
                            "margin": "0",
                        }),
                        $('<button>').attr("onclick", "run_command(this, true)").text("Copy to Terminal").css({
                            "padding": "7px",
                            "box-sizing": "border-box",
                            "margin": "0",
                        })
                    ).css({
                        "padding": "7px",
                        "box-sizing": "border-box",
                        "margin": "0",
                    }),
                    $('<td>').text(item[j][1]),
                    $('<td>').append(
                        $('<button>').attr("onclick", "delete_command(this)").text("Remove").css({
                            "padding": "7px",
                            "box-sizing": "border-box",
                            "margin": "0",
                        })
                    ),
                    
                ).appendTo("#data")
                $('<tr>').append(
                    $('<td>').attr({"colspan": "4"}).append(
                        spe_div.append(
                            $('<div>').attr({"class": "card card-body", "id": "divNote"+item[j][2][0]}).append(
                                $('<span>').append($('<button>').attr({"onclick": "edit_note(this)", "type": "button", "class": "btn btn-primary", "id": "note_"+item[j][2][0]}).text("edit")).css(
                                    {
                                        "right": "1em",
                                        "position": "relative"
                                    }
                                ),
                                item[j][2][1]
                            )
                        )
                    )
                ).appendTo("#data")
                cp += 1
            }
            
        })
    })
}


function edit_note(element){
    id = element.id.split("_")[1]
    
    $.getJSON('/get_note?id='+id, function(data) {
        $("#divNote"+id).empty()
        // console.log(data['note'])

        $("#divNote"+id).append(
            $('<span>').append($('<button>').attr({"onclick": "save_note(this)", "type": "button", "class": "btn btn-primary", "id": "note_"+id}).text("Save")).css(
                {
                    "right": "1em",
                    "position": "relative"
                }
            ),
            $('<textarea>').attr({"id": "note_area", "rows": "5", "cols": "50", "maxlength": "5000"}).append(
                data['note']
            )
        )
        
    })
}

function save_note(element){
    console.log(element.parentElement.parentElement.parentElement.id.split("_")[1])
    $.post({
        url: '/save_note',
        data: JSON.stringify({"id_note": element.id.split("_")[1], "note": $('#note_area').val()}),
        contentType: 'application/json',
        success: function(data) {
            $('#status').empty()
            $('#status').css("color", "green")
            $('#status').text(data['message'])
            get_command(element.parentElement.parentElement.parentElement.id.split("_")[1])
        },
        error: function(xhr, status, error) {
            $('#status').empty()
            $('#status').css("color", "brown")
            $('#status').text(xhr.responseJSON['message'])
        },
    });
}



function action_add(){
    $.post({
        url: '/add_command',
        data: JSON.stringify({"command": $('#Cname').val(), "category": $('#cat-select').val()}),
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

function display_cat(){
    $.getJSON('/get_category_list', function(data) {
        $.each(data, function(i, item) {
            for(j in item.sort()){
                $('<a>').text(item[j][1]).attr({
                    "class": "dropdown-item",
                    "href": "/categ_list?cat=" + item[j][0]
                }).appendTo("#dropdown_cat")
            }
        })
    })
}
