$(document).ready(function(){function getCookie(name){let cookieValue=null;if(document.cookie&&document.cookie!==''){let cookies=document.cookie.split(';');for(let i=0;i<cookies.length;i++){let cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)===(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
function csrfSafeMethod(method){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
let csrftoken=getCookie('csrftoken');$.ajaxSetup({beforeSend:function(xhr,settings){if(!csrfSafeMethod(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken);}}});$('#uploadSubmit').on('click',function(e){e.preventDefault();if($("#uploadUrl").val()==='0'){$('#uploadError').text("操作失败！！！上传文件类型不能为空");}else if($("#uploadFile").val()===""||$('#uploadFile').val()===undefined||$('#uploadFile').val()===null){$('#uploadError').text("操作失败！！！上传文件不能为空");}else{let form_data=new FormData();form_data.append('uploadFile',$('#uploadFile')[0].files[0]);form_data.append('uploadUrl',$('#uploadUrl').val());form_data.append('uploadOperator',"");let urlUpload="/ADVANCE/Upload/";$.ajax({async:true,url:urlUpload,processData:false,method:'POST',data:form_data,dataType:'json',contentType:false,success:function(data){if(data.error_msg_fatal){$('#uploadInfo').text("");$('#uploadError').text(data.error_msg_fatal);}else{let update_records=parseInt(data.all_records)-parseInt(data.add_records);$('#uploadInfo').text('文件上传和批量添加成功，输入记录共有'+data.all_records+'行，有效的共有'+data.valid_records+"行。\n其中往数据库中增加"+
data.add_records+'行记录，更新了'+update_records+'行记录。'+data.warning);$('#uploadError').text(data.error_msg_tolerant);setTimeout(function(){window.location.reload(true);},30000);}}});}});$('#uploadReset').on('click',function(e){e.preventDefault();$("#uploadFile").val("");$('#uploadInfo').text("");$('#uploadError').text("");});});;