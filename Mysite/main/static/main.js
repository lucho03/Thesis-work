function enable(input_id, button_id) {
    if($('#'+input_id).val().length > 0) {
        $(button_id).attr('disabled', false);
    }
    else {
        $(button_id).attr('disabled', true);
    }
}

$("#file-id").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings("#file-label-id").addClass("selected").html(fileName);
});

function click_row(id_row, id_ticket, permission) {
    if(permission === 'True') {
        url = window.location.href.replace('dashboard', 'list_tickets#card-'+id_ticket);
    }
    else {
        url = window.location.href.replace('dashboard', 'tickets#card-'+id_ticket);
    }
    $(location).prop('href', url);
};