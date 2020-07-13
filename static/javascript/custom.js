
String.format = function (src) {
    if (arguments.length === 0) return null;
    let args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function (m, i) {
        return args[i];
    });
};

function range(size, startAt = 0) {
    if(startAt>0){
        let tmp = startAt;
        startAt = size;
        size = tmp-startAt;
    }
    return [...Array(size).keys()].map(i => i + startAt);
}

function databaseRecordAjaxPut(model_changed_txt, operation_txt, others_txt) {
    let url_record = '/api/USER/DatabaseRecord/';
    let data_record = $.param({
        "userinfo": "{{ user.id }}",
        "model_changed": model_changed_txt,
        "operation": operation_txt,
        "memo": others_txt
    });
    //console.info("data_record",data_record);
    $.ajax({
        url: url_record,
        method: 'POST',
        data: data_record//, headers: {'X-HTTP-Method-Override': 'PATCH'}
    });
}

function input_autocomplete(values, item_flag) {
    console.info("in function input_autocomplete; values:", values, "; item_flag:", item_flag);
    if (values.length === 0) {
        console.log("do if");
        console.log("empty list. do nothing");
    } else if (values.length > 10) {
        console.log("do else if");
        values.push('...');
        $(item_flag).autocomplete({
            autoFocus: false,
            minLength: 3,
            delay: 10,
            source: function (request, response) {
                let matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
                let max_match = 15;
                let n_match = 0;
                response($.grep(values, function (item) {
                    let flag_match = matcher.test(item);
                    if (item === "..." && n_match === max_match) {
                        return true;
                    } else if (flag_match && n_match < max_match) {
                        n_match += 1;
                        return flag_match;
                    } else {
                        return false;
                    }
                }));
            },
            focus: function (event, ui) {
                if (ui.item.label === "...") {
                    $(item_flag).val("");
                } else {
                    $(item_flag).val(ui.item.label);
                }
                return false;
            },
            select: function (event, ui) {
                if (ui.item.label === "...") {
                    $(item_flag).val("");
                } else {
                    $(item_flag).val(ui.item.label);
                }
                return false;
            }
        });
        console.log("if work");
    } else {
        console.log("do else");
        $(item_flag).autocomplete({
            autoFocus: true,
            minLength: 0,
            delay: 0,
            source: values
        }).autocomplete("search", "");
        console.log("else work");
    }
}

function delete_by_id_simple(url_func, id_func){
    let res = [];
    $.ajax({
      url: url_func + id_func + '/',
      method: 'DELETE',
      success: function () {
          res.push("success");
          res.push(id_func);
          window.location.reload(true);
          },
      error: function (jqXHR, textStatus, errorThrown) {
          res.push("error")
          res.push(jqXHR + ';' + textStatus + ';' + errorThrown)
      }
  });
  return res;
}

