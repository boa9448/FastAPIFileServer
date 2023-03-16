(function(list, $, undefined) {
    var g_page = 1;
    var g_size = 15;


    $(document).ready(init);

    function init(){
        $("#license-list").on("click", ".download-btn", function(e){
            const license_id = $(this).data("license-id");
            download_file(license_id);
        });

        load_data();
    }


    function load_data(){
        show_wait_alert(true);
        const jqXHR = get_license_list();
        jqXHR.then(function(data, textStatus, jqXHR){
            const items = data.items;
            const total = data.total;
            const page = data.page;
            const size = data.size;
            const pages = data.pages;
            console.log(data);
            $("#total-count").text(`Total ${total}`);

            if(total == 0){
                alert("보유한 라이선스가 없습니다.");
                return;
            }

            for(const item of items){
                add_license_to_list(item);
            }

            if(items.length < size){
                $("#end-item-alert").removeClass("d-none");
            }
            else{
                g_page++;
                scroll_activate();
            }
        }).fail(function(jqXHR, textStatus, errorThrown){
            const error_code = jqXHR.status;
            const message = jqXHR.responseJSON.detail;
            alert(message);

            if(error_code == 401){
                window.location.href = "/auth/me/";
            }
        }).always(function(){
            show_wait_alert(false);
        });
    }

    function get_license_list(page, size){
        const jqXHR = $.ajax({
            url: "/api/v1/license/list/",
            type: "get",
        });

        return jqXHR;
    }


    function download_file(license_id){
        const jqXHR = $.ajax({
            url: `/api/v1/license/token/${license_id}/`,
            type: "get",
        });

        jqXHR.then(function(data, textStatus, jqXHR){
            const token = data.license_token;
            const download_url = `/api/v1/file/download/?license_token=${token}`;
            window.open(download_url, "_blank");
        }).fail(function(jqXHR, textStatus, errorThrown){
            const error_code = jqXHR.status;
            const message = jqXHR.responseJSON.detail;
            alert(message);
        });
    }


    function add_license_to_list(license){
        const license_id = license.id;
        const valid_date = license.valid_date;
        const is_active = license.is_active;

        const file = license.file;
        const file_id = file.id;
        const file_name = file.name;
        const file_kb_size = (file.size / 1024).toFixed(2);

        const splited_valid_date = valid_date.split("T")[0];
        const disabled = is_active ? "" : "disabled";
        const deactive_tag = is_active ? "" : `<span class="badge bg-danger me-3">만료</span>`;

        const list_tag = `
        <li class="list-group-item d-flex justify-content-between list-group-item-action ${disabled}">
            <div class="d-flex justify-content-start flex-grow-1 me-2">
                <div class="license-list-item pt-1 container" data-license-id=${license.id}>
                    <div class="row">
                        ${file_name} (${file_kb_size} KB)
                    </div>
                    <small class="row text-muted">
                        유효기간 : ${splited_valid_date}
                    </small>
                </div>
            </div>
            <div class="d-flex justify-content-end align-items-center">
                ${deactive_tag}
                <button type="button" class="btn btn-sm btn-primary download-btn" data-license-id=${license_id}>
                    <i class="fa-solid fa-file-arrow-down"></i>
                </button>
            </div>
        </li>`;


        $("#license-list").append(list_tag);
    }


    function show_wait_alert(is_show){
        if(is_show){
            $("#wait-alert").removeClass("d-none");
        }
        else{
            $("#wait-alert").addClass("d-none");
        }
    }


    function scroll_activate() {
        $(window).on("scroll", function () {
            if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
                $(window).off("scroll");
                load_data();
            }
        });
    }

})(window.list = window.list || {}, jQuery);