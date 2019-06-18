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
     span = id.split('=');
     num_msg = document.getElementById(span.pop());
     if (num_msg != null)
          num_msg.parentNode.removeChild(num_msg);
     f = document.getElementById(id);
     $(f).css({'color':'black'});
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

function init(username){
  var host = "ws://10.0.10.69:8000/websocket/";
  try{
    socket = new WebSocket(host);
    socket.onopen = function(msg){
        console.log('你已经来到聊天室')
    };
    socket.onmessage = function(msg){
        arr = msg.data.split(':');
        if (arr[0]==$('[name="friend"]').val()){
            get_msg('chat.action_chat&friend=' + $("input[name='friend']").val())
        }else{
            fid = 'chat.action_chat&friend='+arr[0];
            f = document.getElementById(fid);
            $(f).css({'color':'red'})
        }
    };
    socket.onclose   = function(msg){
        console.log("与服务器连接断开");
    };
  }catch(ex){
      log(ex);
  }
  $(".sendInfo").focus();
}

function send(){
  var txt,msg;
  txt = $('input[name="data"]');
  msg = txt.val()+":"+$('[name="friend"]').val();
  if(!msg){
      alert("Message can not be empty");
      return;
  }
  txt.val('');
  txt.focus();
  try{
      console.log(socket);
      socket.send(msg);
  } catch(ex){
      alert(ex);
  }
}

window.onbeforeunload=function(){
    try{
        socket.send('close');
        socket.close();
        socket=null;
    }
    catch(ex){
        log(ex);
    }
};

function show(obj){
    obj.fadeIn()
}

function getCookie(cookieName) {
    var strCookie = document.cookie;
    var arrCookie = strCookie.split("; ");
    for(var i = 0; i < arrCookie.length; i++){
        var arr = arrCookie[i].split("=");
        if(cookieName == arr[0]){
            return arr[1];
        }
    }
    return "";
}