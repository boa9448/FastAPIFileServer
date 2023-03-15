(function(login, $, undefined) {
    $(document).ready(init);


    function init(){
        $("#join-btn").click(function(){
            window.location.href = "/auth/join/";
        });

        $("#login-btn").click(loging_btn_handler);
    }


    function loging_btn_handler(){
        const user_id = $("#user-id").val();
        const password = $("#password").val();

        const jqXHR = user_login(user_id, password);

        show_spinner(true);
        jqXHR.then(function(data, textStatus, jqXHR){
            const redirect_url = data.redirect_url;
            window.location.href = redirect_url;
        }).fail(function(jqXHR, textStatus, errorThrown){
            const data = jqXHR.responseJSON;
            const error = data["error"];
            console.log(error);

            alert("로그인에 실패했습니다.");
        }).always(function(){
            show_spinner(false);
        });
    }

    
    function user_login(user_id, password){
        const data = JSON.stringify({
            "user_id": user_id,
            "password": password
        });

        const jqXHR = $.ajax({
            url: "/api/v1/auth/user/token/session/",
            type: "post",
            data: data,
            contentType: "application/json",
        });

        return jqXHR;
    }

    function show_spinner(is_show){
        const spinner = $("#login-spinner");
        if(is_show){
            spinner.removeClass("d-none");
        }else{
            spinner.addClass("d-none");
        }
    }
}(window.login = window.login || {}, jQuery));