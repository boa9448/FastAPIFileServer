(function(password_edit, $, undefined){
    $(document).ready(init);


    function init(){
        $("#back-btn").click(function(){
            window.location.href = "/auth/me/";
        });

        $("#edit-btn").click(edit_btn_handler);
    }


    function edit_btn_handler(){
        const cur_password = $("#cur-password").val();
        const password1 = $("#password1").val();
        const password2 = $("#password2").val();

        if(cur_password == "" || cur_password == undefined){
            alert("현재 비밀번호를 입력해주세요.");
            return;
        }

        if(password1 == "" || password2 == ""
            || password1 == undefined || password2 == undefined){
            alert("비밀번호를 입력해주세요.");
            return;
        }

        if(password1 != password2){
            alert("비밀번호가 일치하지 않습니다.");
            return;
        }

        show_spinner(true);
        const jqXHR = edit_password(cur_password, password1, password2);
        jqXHR.then(function(data, textStatus, jqXHR){
            alert("비밀번호가 변경되었습니다.");
            window.location.href = "/auth/me/";
        }).fail(function(jqXHR, textStatus, errorThrown){
            const message = jqXHR.responseJSON.detail;
            alert(message);
        }).always(function(){
            show_spinner(false);
        });
    }


    function edit_password(cur_password, password1, password2){
        const json_data = JSON.stringify({
            cur_password: cur_password,
            password1: password1,
            password2: password2
        });

        const jqXHR = $.ajax({
            url: "/api/v1/auth/password/edit/",
            type: "patch",
            data: json_data,
            contentType: "application/json",
        });

        return jqXHR;
    }


    function show_spinner(is_show){
        if(is_show){
            $("#edit-spinner").show();
        }
        else{
            $("#edit-spinner").hide();
        }
    }

}(window.password_edit = window.password_edit || {}, jQuery));