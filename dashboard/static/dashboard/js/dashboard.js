//获取csrf令牌
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
