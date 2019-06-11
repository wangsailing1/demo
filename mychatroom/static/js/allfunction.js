function send_request(method, url='/api/', async=false, type='GET', datatype='json') {
        data = {};
        var msg;
        $.each(arguments, function (i, obj) {
           data[obj] = $('input[name="'+ obj +'"]').val();
        });
        $.ajax({
            'url': '/api/?method='+method,
            'type': 'GET',
            'datatype': datatype,
            'async': false,
            'data': data,
            'success':function (data) {
                data = JSON.parse(data);
                msg = data
            }
        });
        return msg
}
function get_msg(id){
    // result = send_request(id);
    $.ajax({
       'url':'/api/?method='+id,
       'type':'get',
       'datatype':'json',
       'success': function (result) {
                var result = JSON.parse(result);
    if (result.data.name){$('#show_name').html("<h2>"+result.data.name+"</h2>")}
    msg = '';
    if (result.status==0 && result.data.data.msg){
        $.each(result.data.data.msg, function (i, obj) {
            msg += "<p class='"+obj[1]+"'>"+obj[0]+"<br>"+obj[2]+"</p>"
        });
        msg += "<input type='hidden' name='method' value='chat.send_msg'>";
        msg += "<input type='hidden' name='friend' value='"+result.data.account+"'>";
        $('#show_msg').html(msg);
        $("#show_msg").scrollTop($("#show_msg")[0].scrollHeight);
    }
       }
    });
    }