
$(document).ready(function() {
    get_category()

    $("#searchbar").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#data tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
})


function delete_category(element){
    // console.log(element)
    // console.log(element.parentElement.parentElement.firstElementChild.firstElementChild)
    $.post({
        url: '/delete_category',
        data: JSON.stringify({"category": element.parentElement.parentElement.firstElementChild.outerText}),
        contentType: 'application/json',
        success: function(data) {
            $('#status').empty()
            $('#status').css("color", "green")
            $('#status').text(data['message'])
            get_category()
        },
        error: function(xhr, status, error) {
            $('#status').empty()
            $('#status').css("color", "brown")
            $('#status').text(xhr.responseJSON['message'])
        },
    });
}

function get_category(){
    // console.log(window.location.search)
    $.getJSON('/get_category', function(data) {
        $('#data').empty()
        $('<tr>').append(
            $('<th>').text("CATEGORY"),
            $('<th>').text("")
        ).appendTo('#data')
        $.each(data, function(i, item) {
            for(j in item.sort()){
                $('<tr>').append(
                    $('<td>').text(item[j][0]).css({
                        "padding": "7px",
                        "box-sizing": "border-box",
                        "margin": "0",
                    }),
                    $('<td>').text(item[j][1]),
                    $('<td>').append(
                        $('<button>').attr("onclick", "delete_category(this)").text("Remove").css({
                            "padding": "7px",
                            "box-sizing": "border-box",
                            "margin": "0",
                        })
                    )
                ).appendTo("#data")
            }
        })
    })
}

function action_add(){
    $.post({
        url: '/add_category',
        data: JSON.stringify({"category": $('#Cname').val()}),
        contentType: 'application/json',
        success: function(data) {
            $('#status').empty()
            $('#status').css("color", "green")
            $('#status').text(data['message'])
            get_category()
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