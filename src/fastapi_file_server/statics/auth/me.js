(function(me, $, undefined){
    $(document).ready(init);

    function init(){
        $("#back-btn").click(function(){
            window.location.href = "/";
        });

        $("#password-edit-btn").click(function(){
            window.location.href = "/auth/password/edit/";
        });

        $("#edit-btn").click(edit_btn_handler);

        get_user_info();
    }


    function get_user_info(){
        const jqXHR = $.ajax({
            url: "/api/v1/auth/me/",
            type: "GET",
        });

        jqXHR.then(function(data, textStatus, jqXHR){
            const user_id = data.user_id;
            const name = data.name;
            const email = data.email;
            const is_active = data.is_active;

            $("#user-id").val(user_id);
            $("#user-name").val(name);
            $("#user-email").val(email);

            if(is_active){
                $("#no-active-alert").addClass("d-none");
            }else{
                $("#no-active-alert").removeClass("d-none");
            }
        }).fail(function(jqXHR, textStatus, errorThrown){
            alert("사용자 정보를 가져오는데 실패했습니다. 관리자에게 문의하세요.");
        });
    }


    function edit_btn_handler(){
        const password1 = $("#user-password1").val();
        const password2 = $("#user-password2").val();
        const name = $("#user-name").val();
        const email = $("#user-email").val();

        if(password1 != "" && password2 != ""){
            alert("비밀번호를 입력해주세요.");
            return;
        }

        if(password1 != password2){
            alert("비밀번호가 일치하지 않습니다.");
            return;
        }

        const data = JSON.stringify({
            password1: password1,
            password2: password2,
            name: name,
            email: email,
        });

        const jqXHR = edit_user_info(data);
        jqXHR.then(function(data, textStatus, jqXHR){
            alert("사용자 정보가 수정되었습니다.");
            window.location.reload();
        }).fail(function(jqXHR, textStatus, errorThrown){
            const error = jqXHR.responseJSON;
            alert(`사용자 정보를 수정하는데 실패했습니다. ${error.detail}`);
        });
    }

    function edit_user_info(user_info){
        const jqXHR = $.ajax({
            url: "/api/v1/auth/edit/",
            type: "patch",
            data: user_info,
            contentType: "application/json",
        });

        return jqXHR;
    }

}(window.me = window.me || {}, jQuery));