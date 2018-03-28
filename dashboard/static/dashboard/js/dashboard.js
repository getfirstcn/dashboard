//获取csrf令牌
get_all_events();
setInterval(function(){get_all_events()}, 60000);
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// 显示部署表单
$(function(){
    $("#add-deployment").click(function(){
        $("#form-deployment").show();
        $.get('/project/', function(projects){
            for (i in projects)
            {
                console.log(projects[i].name);
                $("#selectProject1").append(" <option> "+projects[i].name+" </option>");
            };
            $.post('/image/',{
                "project": "base"
            },function(data){
               for (i in data)
               {
                   $("#imagenames").append("<option value="+data[i]+">");
               }
            })          
        })
    })
})
//选择镜像
$(function(){
    $("#selectProject1").change(function(){
      var project=  $("#selectProject1").val();
      console.log(project);
      $("#images-1").val("");
      $("#imagenames").empty();
      $("#tag-1").val("");
      $("#tag-list").empty();
      $("#app-1").val("");
      console.log(csrftoken);
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
      $.post('/image/',{
        "project": project
    },function(data){
       for (i in data)
       {
           $("#imagenames").append("<option value="+data[i]+">");
       }
    })
})
})
//选择版本
$(function(){
    $("#images-1").change(function(){
        var image = $("#images-1").val();
        console.log(image);
        $("#tag-1").val("");
        $("#tag-list").empty();
        $("#app-1").val("");
        $.post('/tag/',{"image":image},function(data){
            for (i in data)
            {
                $("#tag-list").append("<option value="+data[i]+">")
            }

        })

    }) 
})
//设置应用名
$(function(){
    $("#images-1").change(function(){
        var image = $("#images-1").val();
        $.post('/app/name/',{'image':image},function(data){
            $("#app-1").val(data)
        })


    })
})
// 隐藏部署表单
$(function(){
    $("#deploymentFormCancel").click(function(){
        $("#form-deployment").hide();

    })
})

//删除部署
$(function(){
    $("#deleteDeploy").click(function(){
        var cks = $(".checkbox-single");
        var result = new Array();
        for (var i=0;i<cks.length;i++)
        {
            if (cks.eq(i).prop("checked"))
            {
                console.log(cks.eq(i).val(),cks.eq(i).attr('name'));
                var dp=cks.eq(i).val();
                var nm=cks.eq(i).attr('name');
                $.post('/deployment/delete/',{"deploy":dp,'namespace':nm},function(data){
                    console.log(data);
                    result.push(dp+'删除：'+data)
                })
            }
        }
        console.log(result);
        parent.location.reload()
    })
})
//修改部署
$(function(){
    $("#changeDeploy").click(function(){
        var cks = $(".checkbox-single");
        var result = new Array();
        for (var i=0;i<cks.length;i++)
        {
            if (cks.eq(i).prop("checked"))
            {
                console.log(cks.eq(i).val(),cks.eq(i).attr('name'));
                var dp=cks.eq(i).val();
                var nm=cks.eq(i).attr('name');
                var port=cks.eq(i).attr('data-port');
                var namespace=cks.eq(i).attr('name');
                $("#form-change-deployment").show();
                var project = dp.split('-')[1];
                console.log(project);
                $("#selectChangeProject1").val(project);
                $("#change-app-1").val(dp);
                $("#changeServicePort1").val(port);
                $("#change-namespace-1").val(namespace);
                $.post('/image/',{'project':project},function(data){
                    for (i in data)
                    {
                        $("#change-imagenames").append("<option value="+data[i]+">");
                    }
                })

            }
        }
    })
})

//改变镜像版本
$(function(){
    $("#change-images-1").change(function(){
        var image = $("#change-images-1").val();
        console.log(image);
        $("#change-tag-1").val("");
        $("#change-tag-list").empty();
        $.post('/tag/',{"image":image},function(data){
            for (i in data)
            {
                $("#change-tag-list").append("<option value="+data[i]+">")
            }

        })

    }) 
})

// 隐藏修改部署表单
$(function(){
    $("#changeDeploymentFormCancel").click(function(){
        $("#form-change-deployment").hide();

    })
})

//显示上传文件
function writeFileName(){
    var uploadFile = document.getElementById('uploadFile1');
    var fileLable = document.getElementById('fileLable1');
    var fileName = uploadFile.files[0].name;
    fileLable.innerHTML=fileName
}

//显示删除pod确定
$(function () {
    var poddelete = $(".pod-delete-dropdown1");
    // var name = poddelete.attr("data-name");
    poddelete.click(function() {
        var name = $(this).attr("data-name");
        var namespace = $(this).attr("data-namespace");
        console.log(name,namespace);
        $("#pod-delete-form1").show();
        $("#pod-delete-confirm1").click(function () {
            $.post('/pod/delete/',{"name":name,"namespace":namespace},function (data) {
                if (data){
                    alert("删除成功");
                    window.location.reload();
                }
                else {
                    alert("删除不一定成功");
                }
            })
        })
    })
})

//隐藏删除pods表单
$(function () {
    $("#pod-delete-cancel1").click(function () {
        $("#pod-delete-form1").hide();
    })
})

//显示应用表单
$(function(){
    $("#app-create-btn1").click(function(){
        $("#form-create-app1").show();
        // $.get('/project/', function(projects){
        //     for (i in projects)
        //     {
        //         console.log(projects[i].name);
        //         $("#selectProject1").append(" <option> "+projects[i].name+" </option>");
        //     };
        //     $.post('/image/',{
        //         "project": "base"
        //     },function(data){
        //        for (i in data)
        //        {
        //            $("#imagenames").append("<option value="+data[i]+">");
        //        }
        //     })
        // })
    })
})

$(function () {
    $(".form-control-text").focus(function () {
        $(this).prev().animate({top:"0px"})
    })
})

//服务协议lable动画
$(function () {
    $("#service-protocol-1").focus(function () {
        $("#service-protocal-label-1").animate({top:"0px"})
    })
})

//标签文字动画
$(function () {
    $("#lable-value-input-0").focus(function () {
        $("#lable-value-text-1").animate({top:"0px"})
    })
})

//图标鼠标悬浮动画
$(function () {
    $(".ion-ios-plus-empty").focus("color","orange")
})

var addENVnum = 0;
function addInputENV() {
    addENVnum++;
    var inputKey=document.createElement("input");
    var inputGroup = document.createElement("div");
    var input = document.createElement("input");
    var span = document.createElement("span");
    var text=document.createTextNode("增加子节点");
    var inputGroupPrepend=document.createElement("div");
    inputKey.className="form-control form-control-text";
    inputKey.setAttribute("placeholder","名称");
    inputKey.setAttribute("type","text");
    inputKey.setAttribute("name","envKey");
    inputKey.setAttribute("id","envKey"+addENVnum);
    inputGroup.setAttribute("class", "input-group");
    inputGroup.setAttribute("id", "envValue"+addENVnum);
	input.setAttribute("name", "envValue");
	input.setAttribute("placeholder", "值");
	input.setAttribute("type","text");
	input.className="form-control form-control-text";
    span.className="ion-ios-close-empty ion-plus-btn";
    span.setAttribute("data-num",addENVnum);
    span.setAttribute("onclick","delInputENV(this)");
    inputGroupPrepend.className="input-group-prepend";
    inputGroupPrepend.appendChild(span);
    inputGroup.appendChild(input);
    inputGroup.appendChild(inputGroupPrepend);
    document.getElementById('env-group-key').appendChild(inputKey);
    document.getElementById('env-group-value').appendChild(inputGroup)
}
// document.getElementById("plus-env-intput").onclick=function () { addInputENV(document.getElementById("env-group-key")) }
// document.getElementById("plus-env-intput").addEventListener("click",function () {
//     addInputENV("env-group-value","env-group-key")
// }
// )

function delInputENV(node) {
    console.log(node)
    num=node.getAttribute("data-num")
    console.log(num)
    var keyGroup = document.getElementById("envKey"+num);
    var valueGroup = document.getElementById("envValue"+num);
    keyGroup.parentNode.removeChild(keyGroup);
    valueGroup.parentNode.removeChild(valueGroup)

}

var addServiceNum=1
function addServiceInput() {
    var inputPort=document.createElement("input")
    var inputPortTarget=document.createElement("input")
    var inputProtocolGroup=document.createElement("div");
    var inputProtocol=document.createElement("select");
    var inputProtocolOption1=document.createElement("option");
    var inputProtocolOption2=document.createElement("option");
    var inputProtocolGroupAppend=document.createElement("div");
    var inputProtocolspan=document.createElement("span");
    inputPort.className="form-control form-control-text"
    inputPort.setAttribute("type","int")
    inputPort.setAttribute("id","input-service-port-"+addServiceNum)
    inputPort.setAttribute("name","servicePort")
    inputPortTarget.className="form-control form-control-text"
    inputPortTarget.setAttribute("type","int")
    inputPortTarget.setAttribute("id","input-service-port-target-"+addServiceNum)
    inputPortTarget.setAttribute("name","targetPort")
    inputProtocolGroup.className="input-group"
    inputProtocolGroup.setAttribute("id","input-protocol-group-"+addServiceNum)
    inputProtocol.className="form-control form-control-text"
    inputProtocol.setAttribute("name","serviceProtocol")
    inputProtocolOption1.setAttribute('value','TCP')
    inputProtocolOption1.innerText='TCP'
    inputProtocolOption2.setAttribute('value','UDP')
    inputProtocolOption2.innerText='UDP'
    inputProtocolGroupAppend.className="input-group-append"
    inputProtocolspan.className="ion-ios-close-empty ion-plus-btn"
    inputProtocolspan.setAttribute("onclick","delServiceInput(this)")
    inputProtocolspan.setAttribute("data-num",addServiceNum)
    inputProtocol.appendChild(inputProtocolOption1)
    inputProtocol.appendChild(inputProtocolOption2)
    inputProtocolGroup.appendChild(inputProtocol)
    inputProtocolGroupAppend.appendChild(inputProtocolspan)
    inputProtocolGroup.appendChild(inputProtocolGroupAppend)
    document.getElementById('service-group-port').appendChild(inputPort)
    document.getElementById('service-group-target-port').appendChild(inputPortTarget)
    document.getElementById('service-group-protocol').appendChild(inputProtocolGroup)
    addServiceNum++
}

// document.getElementById("plus-service-input").addEventListener("click",function () {
//     addServiceInput("service-group-port","service-group-target-port","service-group-protocol")
// }
// )

//减少服务删除
function delServiceInput(node) {
    addServiceNum--
   var num = node.getAttribute("data-num")
    console.log(num)
   var portNode=document.getElementById("input-service-port-"+addServiceNum)
    console.log("服务端口id：input-service-port-"+addServiceNum)
   var portProtocol=document.getElementById("input-protocol-group-"+addServiceNum)
    console.log("服务协议：input-portocol-group-"+addServiceNum)
   var portTarget=document.getElementById("input-service-port-target-"+addServiceNum)
    console.log("服务协议：input-service-port-target-"+addServiceNum)
    portNode.parentNode.removeChild(portNode)
    portProtocol.parentNode.removeChild(portProtocol)
    portTarget.parentNode.removeChild(portTarget)
}

//增加标签输入
var addLableNum = 1
function addLableInput() {
    var key=document.createElement('input');
    var value=document.createElement('input')
    var inputGroup=document.createElement("div")
    var inputGroupAppend=document.createElement("div")
    var span=document.createElement("span")
    key.className="form-control form-control-text"
    key.setAttribute("name","lableKey")
    key.setAttribute("type","text")
    key.setAttribute("id","lable-key-input-"+addLableNum)
    value.className="form-control form-control-text"
    value.setAttribute("name","lableValue")
    value.setAttribute("type","text")
    inputGroup.className="input-group"
    inputGroup.setAttribute("id","lable-value-input-"+addLableNum)
    inputGroupAppend.className="input-group-append"
    span.className="material-input ion-ios-close-empty ion-plus-btn"
    span.setAttribute("onclick","delLableInput(this)")
    span.setAttribute("data-num",addLableNum)
    inputGroupAppend.appendChild(span)
    inputGroup.appendChild(value)
    inputGroup.appendChild(inputGroupAppend)
    document.getElementById('lable-key').appendChild(key)
    document.getElementById('lable-value').appendChild(inputGroup)
    addLableNum++
}
// document.getElementById("plus-lable-input").addEventListener("click",function () {
//     addLableInput("lable-key","lable-value")
// })

//删除输入标签
function delLableInput(node) {
    addLableNum--
    var num=node.getAttribute("data-num")
    console.log(num)
    var nodeKey=document.getElementById("lable-key-input-"+addLableNum)
    var nodeValue=document.getElementById("lable-value-input-"+addLableNum)
    nodeKey.parentNode.removeChild(nodeKey)
    nodeValue.parentNode.removeChild(nodeValue)
}

function deployment_delete(node) {
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    console.log(node)
    var con=confirm("确定删除部署"+name+"吗？")
    if(con == true){
        $.post("/deployment/delete/",{'name':name,'namespace':namespace},function (data,status) {
            if(status=="success"){
                console.log(data.message)
                location.reload()
            }else {
                console.log('删除失败')
            }
            console.log('状态：'+status)
        })
    }
}

function service_delete(node) {
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    console.log(node)
    var con=confirm("确认删出服务"+name+"吗？")
    if (con == true){
        $.post("/service/delete/",{
            "name":name,
            "namespace":namespace
        },function (data,status) {
            if (status == "success"){
                console.log("删除成功");
                console.log(data)
                location.reload()
            }
            else {
                console.log("删除失败")
            }
        })
    }
}

function application_delete(node) {
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    console.log(node)
    var con=confirm("确认删除应用"+name+"吗？")
    if (con == true){
        $.post("/application/delete/",{
            "name":name,
            "namespace":namespace
        },function (data,status) {
            if (status == "success"){
                console.log("删除成功")
                console.log(data)
                location.reload()
            }else {
                console.log("删除失败")
                console.log(data)
            }
        })
    }
}

//加载pod日志
function get_pod_log(node) {
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    $.post('/pod/log/',{
        name:name,
        namespace:namespace
    },function (data) {
        var log_box=document.getElementById('pod-log-box')
        log_box.innerText=data
    })
}

//加载pod事件
function get_pod_event(node) {
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    console.log(name,namespace)
    $.post('/pod/event/',{
        name:name,
        namespace:namespace
    },function (data,status) {
        console.log(data)
        var event_box=document.getElementById('pod-event-content')
        console.log(event_box)
        event_box.innerHTML=data
        $("#eventModal").modal("show")
    })
}

//所有命名空间事件
function get_all_events() {
    $.post('/namespace/event/',function (data) {
        var content=document.getElementById('namespace-all-events')
        content.innerHTML=data
        var number=document.getElementById('events-number').getAttribute('data-events')
        // console.log(number,'个事件')
        var counts=document.getElementById('events-count')
        counts.innerHTML=number
    })
}

//修改服务
function modify_service(node) {
    console.log(node)
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    var titleNode=document.getElementById('modify-service-title')
    titleNode.innerHTML='修改服务:'+name
    $.post('/service/detail/',{'name':name,'namespace':namespace},function (data) {
        console.log(data)
        if(typeof (editor) == "object"){
            editor.setValue(data)
        }else {
            require.config({ paths: { 'vs': '/static/dashboard/vendor/monaco-editor-0.11.1/package/min/vs' }});
        require(['vs/editor/editor.main'], function() {
                editor = monaco.editor.create(document.getElementById('service-editor'), {
                value: [
                    data
			].join('\n'),
                language: 'python'
		});
	});
        }
    })
}
//关闭服务模态会话框一出文本
$(function () {
    $('#update-service-btn').click(function () {
        var value=editor.getValue()
        console.log(value)
        $.post("/service/update/",{"value":value},function (data,status) {
          console.log(data)
            console.log(status)
        })
    })
        // $('#service-editor').children().remove();
})

//修改部署
function modify_deployment(node) {
    console.log(node)
    var name=node.getAttribute('data-name')
    var namespace=node.getAttribute('data-namespace')
    var titleNode=document.getElementById('modify-deployment-title')
    titleNode.innerHTML='修改部署:'+name
    $.post('/deployment/read/',{'name':name,'namespace':namespace},function (data) {
        console.log(data);
        if(typeof (deploymentEditor) == "object"){
            deploymentEditor.setValue(data)
        }else {
            require.config({ paths: { 'vs': '/static/dashboard/vendor/monaco-editor-0.11.1/package/min/vs' }});
        require(['vs/editor/editor.main'], function() {
                deploymentEditor = monaco.editor.create(document.getElementById('deployment-editor'), {
                value: [
                    data
			].join('\n'),
                language: 'python'
		});
	});
        }
    })
}

//关闭部署模态会话框一出文本
$(function () {
    $('#update-deployment-btn').click(function () {
        var value=deploymentEditor.getValue()
        console.log(value)
        $.post("/deployment/modify/",{"value":value},function (data,status) {
          console.log(data)
            console.log(status)
        })
    })
        // $('#service-editor').children().remove();
})






