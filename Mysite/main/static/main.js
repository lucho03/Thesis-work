function enable(input_id, button_id) {
    if($('#'+input_id).val().length > 0) {
        $(button_id).attr('disabled', false);
    }
    else {
        $(button_id).attr('disabled', true);
    }
}
/*
function enable2() {
    if('{{ticket.priority}}' == '1') {
        $('#card-{{ticket.id}}').addClass('border-danger');
    }
    if('{{ticket.ticket_comments}}' == 0) {
        $('#comments-view-{{ticket.id}}').attr('disabled', 'disabled');
    }
    if('{{ticket.num_answers}}' == 0) {
        $('#answers-view-{{ticket.id}}').attr('disabled', 'disabled');
    }
}
*/
if('{{ticket.priority}}' == '1') {
    $('#card-{{ticket.id}}').addClass('border-danger');
}
if('{{ticket.ticket_comments}}' == 0) {
    $('#comments-view-{{ticket.id}}').attr('disabled', 'disabled');
}
if('{{ticket.num_answers}}' == 0) {
    $('#answers-view-{{ticket.id}}').attr('disabled', 'disabled');
}