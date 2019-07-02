var num = new Object();
function send_request(method, url='/api/', async=false, type='GET', datatype='json') {
        data = {};
        var msg;
        $.each(arguments, function (i, obj) {
           data[obj] = $('input[name="'+ obj +'"]').val();
        });
        $.ajax({
            'url': '/api/?method='+method,
            'type': 'POST',
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
function get_data(id){
    get_msg(id);
    $('#show_msg').scroll(function () {
        if ($('#show_msg').scrollTop() == 0){
            var index = 0;
            var n = num[$("input[name='friend']").val()];
            var is_data = parseInt($('input[name="num"]').val());
            if (is_data - 20 > 20){index = 20 * 60}
            else {index = is_data * 60; is_data = is_data-20}
            if (is_data>0){
            get_msg('chat.action_chat&friend=' + $("input[name='friend']").val()+'&num='+n, index);
            }
        }
    });
}

function get_msg(id, index){
    index = typeof(index) == 'undefined' ? 0 : index;
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
        result = JSON.parse(result);
    if (result.data.name){$('#show_name').html("<h2>"+result.data.name+"</h2>")}
    msg = '';
    if (result.status==0 && result.data.data.msg){
        num[result.data.account]=result.data.data.msg.length;
        $.each(result.data.data.msg, function (i, obj) {
            msg += "<p class='"+obj[1]+"'>"+obj[0]+"<br>"+obj[2]+"</p>"
        });
        msg += "<input type='hidden' name='method' value='chat.send_msg'>";
        msg += "<input type='hidden' name='friend' value='"+result.data.account+"'>";
        msg += "<input type='hidden' name='num' value='"+result.data.not_data+"'>";
        $('#show_msg').html(msg);
        if (index>0){
        $("#show_msg").scrollTop($("#show_msg")[0].scrollHeight - ($("#show_msg")[0].scrollHeight-index));
        }else{$("#show_msg").scrollTop($("#show_msg")[0].scrollHeight)}
    }
       }
    });
    }

function init(username){
    var username = username;
    var host = "ws://wsl.free.idcfengye.com";
  try{
    socket = new WebSocket(host);
    console.log(socket);
    socket.onopen = function(msg){
        socket.send(username);
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
      console.log(ex);
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
        console.log(ex);
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