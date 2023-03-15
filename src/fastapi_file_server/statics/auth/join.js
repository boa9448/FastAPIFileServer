(function(join, $, undefined){
    $(document).ready(init);

    function init(){
        $("#join-btn").click(join_btn_handler);
        $("#back-btn").click(back_btn_handler);
    }


    function join_btn_handler(){
        const user_id = $("#user-id").val();
        const password1 = $("#password1").val();
        const password2 = $("#password2").val();
        const name = $("#name").val();
        const email = $("#email").val();

        if (password1 != password2){
            alert("비밀번호가 일치하지 않습니다.");
            return;
        }

        const user_info = {
            "user_id": user_id,
            "password1": password1,
            "password2": password2,
            "name": name,
            "email": email
        };

        show_spinnner(true);
        const jqXHR = user_join(user_info);
        jqXHR.then(function(data, textStatus, jqXHR){
            alert("회원가입이 완료되었습니다.");
            location.href = "/auth/login/";
        }).fail(function(jqXHR, textStatus, errorThrown){
            const error_msg = jqXHR.responseJSON.detail;
            alert(error_msg);
        }).always(function(){
            show_spinnner(false);
        });
    }


    function back_btn_handler(){
        location.href = "/auth/login/";
    }


    function user_join(user_info){
        const data = JSON.stringify(user_info);
        const jqXHR = $.ajax({
            url: "/api/v1/auth/user/create/",
            type: "post",
            data: data,
            contentType: "application/json",
        });

        return jqXHR;
    }


    function show_spinnner(is_show){
        if (is_show){
            $("#spinner").removeClass("d-none");
        } else {
            $("#spinner").addClass("d-none");
        }
    }
}(window.join = window.join || {}, jQuery));