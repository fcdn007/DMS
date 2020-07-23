
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

function changeThreeDecimal_f(x) {
    let f_x = parseFloat(x);
    if (isNaN(f_x)) {
        alert('function:changeTwoDecimal->parameter error');
        return false;
    }
    f_x = Math.round(x * 1000) / 1000;
    let s_x = f_x.toString();
    let pos_decimal = s_x.indexOf('.');
    if (pos_decimal < 0) {
        pos_decimal = s_x.length;
        s_x += '.';
    }
    while (s_x.length <= pos_decimal + 3) {
        s_x += '0';
    }
    return s_x;
}

function Median(data_) {
    return Quartile_50(data_);
}

function Quartile_25(data_) {
    return Quartile(data_, 0.25);
}

function Quartile_50(data_) {
    return Quartile(data_, 0.5);
}

function Quartile_75(data_) {
    return Quartile(data_, 0.75);
}

function Quartile(data_, q) {
    data_ = Array_Sort_Numbers(data_);
    let pos = ((data_.length) - 1) * q;
    let base = Math.floor(pos);
    let rest = pos - base;
    if ((data_[base + 1] !== undefined)) {
        return data_[base] + rest * (data_[base + 1] - data_[base]);
    } else {
        return data_[base];
    }
}

function Array_Sort_Numbers(data_) {
    return data_.sort(function (a, b) {
        return a - b;
    });
}

function Array_Sum(data_) {
    return data_.reduce(function (a, b) {
        return a + b;
    }, 0);
}

function Array_Average(data_) {
    return Array_Sum(data_) / data_.length;
}

function Array_Stdev(data_) {
    let i, j, total = 0, mean = 0, diff_sqred_arr = [];
    for (i = 0; i < data_.length; i += 1) {
        total += data_[i];
    }
    mean = total / data_.length;
    for (j = 0; j < data_.length; j += 1) {
        diff_sqred_arr.push(Math.pow((data_[j] - mean), 2));
    }
    return (Math.sqrt(diff_sqred_arr.reduce(function (firstEl, nextEl) {
        return firstEl + nextEl;
    }) / data_.length));
}

function unique(array) {
    return $.grep(array, function (el, index) {
        return index === $.inArray(el, array);
    });
}