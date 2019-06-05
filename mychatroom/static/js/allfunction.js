function send_request(method, url='/api/', async=false, type='GET', datatype='json') {
        data = {};
        var msg;
        $.each(arguments, function (i, obj) {
           data[obj] = $('input[name="'+ obj +'"]').val()
        });
        console.log(data);
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