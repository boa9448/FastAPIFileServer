(function(list, $, undefined){
    var g_page = 1;
    var g_size = 15;
    var g_user_list = [];

    $(document).ready(init);


    function init(){
        $("#user-list").on("click", ".active-btn", active_btn_handler);
        $("#user-list").on("click", ".admin-btn", admin_btn_handler);
        $("#user-list").on("click", ".show-license-btn", show_license_btn_handler);
        $("#user-list").on("click", ".edit-license-btn", edit_license_btn_handler);
        $("#user-list").on("click", ".download-license-btn", download_license_btn_handler);

        load_data();
    }


    function load_data(){
        show_wait_alert(true);
        const jqXHR = get_user_list(g_page, g_size);
        jqXHR.then(function(data, textStatus, jqXHR){
            const items = data.items;
            const total = data.total;
            const page = data.page;
            const size = data.size;
            const pages = data.pages;
            console.log(data);

            g_user_list.push(...items);
            $("#total-count").text(`Total ${total}`);

            for(const item of items){
                add_user_to_list(item);
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
        }).always(function(){
            show_wait_alert(false);
        });
    }

    function get_user_list(page, size){
        const jqXHR = $.ajax({
            url: `/api/v1/auth/list/?page=${page}&size=${size}`,
            type: "get",
        });

        return jqXHR;
    }


    function add_user_to_list(user){
        const user_id = user.id;
        const user_user_id = user.user_id;
        const name = user.name;
        const email = user.email;
        const is_active = user.is_active;
        const is_admin = user.is_admin;
        const create_date = user.create_date;

        const splited_valid_date = create_date.split("T")[0];
        const active_btn_tag = create_active_btn_tag(user_id, is_active);
        const admin_btn_tag = create_admin_btn_tag(user_id, is_admin);
        const license_list_tag = create_license_list_tag(user.licenses);

        const list_tag = `
        <li class="list-group-item">
            <div class="d-flex justify-content-between">
                <div class="d-flex justify-content-start flex-grow-1 me-2">
                    <div class="user-list-item pt-1 container" data-user-id=${user_id}>
                        <div class="row">
                            ${user_user_id} (${name})
                        </div>
                        <small class="row text-muted">
                            가입 : ${splited_valid_date}
                        </small>
                    </div>
                </div>
                <div class="d-flex justify-content-end align-items-center">
                    ${active_btn_tag}
                    ${admin_btn_tag}
                </div>
            </div>
            <div>
                ${license_list_tag}
            </div>
        </li>`;


        $("#user-list").append(list_tag);
    }

    
    function create_active_btn_tag(id, is_active) {
        const btn_color = !is_active ? "btn-outline-primary" : "btn-outline-danger";
        const btn_tag = ` 
        <button class="btn btn-sm ${ btn_color } active-btn me-2" data-user-id=${ id } data-is-active=${ is_active }>
            <i class="fa-solid fa-user-check"></i>
        </button>`;

        return btn_tag;
    }


    function create_admin_btn_tag(id, is_admin) {
        const btn_color = !is_admin ? "btn-outline-primary" : "btn-outline-danger";
        const btn_tag = `
        <button class="btn btn-sm ${ btn_color } admin-btn me-2" data-user-id=${ id } data-is-admin=${ is_admin }>
            <i class="fa-solid fa-hammer"></i>
        </button>`;

        return btn_tag;
    }


    function create_license_tag(license){
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
        const edit_btn_tag = create_license_edit_btn_tag(license_id);

        const list_tag = `
        <li class="list-group-item d-flex justify-content-between license-item ${disabled}" data-license-id=${license.id}>
            <div class="d-flex justify-content-start flex-grow-1 me-2">
                <div class="license-list-item pt-1 container" data-license-id=${license.id} data-file-id=${file_id}>
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
                ${edit_btn_tag}
                <button type="button" class="btn btn-sm btn-outline-primary download-license-btn" data-license-id=${license_id}>
                    <i class="fa-solid fa-file-arrow-down"></i>
                </button>
            </div>
        </li>`;

        return list_tag;
    }


    function create_license_edit_btn_tag(license_id) {
        const btn_tag = `
        <button class="btn btn-sm btn-outline-success edit-license-btn me-2" data-license-id=${ license_id }
            data-bs-toggle="modal" data-bs-target="#license-edit-modal">
            <i class="fa-solid fa-pen"></i>
        </button>`;

        return btn_tag;
    }


    function create_license_list_tag(licenses){
        if(licenses.length == 0){
            return "";
        }

        let license_child_tags = "";
        for(const license of licenses){
            const license_tag = create_license_tag(license);
            license_child_tags += license_tag;
        }

        const license_parent_tag = `
        <div class="d-flex flex-column border border-1">
            <!-- show btn -->
            <button type="button" class="btn btn-outline-primary btn-sm show-license-btn">라이선스 보기</button>
            <ul class="list-group license-list-group d-none">
                ${ license_child_tags }
            </ul>
        </div>
        `;

        return license_parent_tag;
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


    function active_btn_handler(){
        const user_id = $(this).data("user-id");
        const is_active = $(this).data("is-active");

        const confirm_message = is_active ? "정말로 비활성화 하시겠습니까?" : "정말로 활성화 하시겠습니까?";
        const is_confirm = confirm(confirm_message);
        if(!is_confirm){
            return;
        }

        const jqXHR = $.ajax({
            url: `/api/v1/auth/active/${user_id}/?is_active=${!is_active}`,
            type: "patch",
            contentType: "application/json",
        });

        jqXHR.then(function(data, textStatus, jqXHR){
            const is_active = data.is_active;
            const btn_tag = create_active_btn_tag(user_id, is_active);
            $(`button.active-btn[data-user-id=${user_id}]`).replaceWith(btn_tag);
        }).fail(function(jqXHR, textStatus, errorThrown){
            const message = jqXHR.responseJSON.detail;
            console.log(message);
            alert(message);
        });
    }


    function admin_btn_handler(){
        const user_id = $(this).data("user-id");
        const is_admin = $(this).data("is-admin");

        const confirm_message = is_admin ? "정말로 비활성화 하시겠습니까?" : "정말로 활성화 하시겠습니까?";
        const is_confirm = confirm(confirm_message);
        if(!is_confirm){
            return;
        }

        const jqXHR = $.ajax({
            url: `/api/v1/auth/admin/${user_id}/?is_admin=${!is_admin}`,
            type: "patch",
            contentType: "application/json",
        });

        jqXHR.then(function(data, textStatus, jqXHR){
            const is_admin = data.is_admin;
            const btn_tag = create_admin_btn_tag(user_id, is_admin);
            $(`button.admin-btn[data-user-id=${user_id}]`).replaceWith(btn_tag);
        }).fail(function(jqXHR, textStatus, errorThrown){
            const message = jqXHR.responseJSON.detail;
            console.log(message);
            alert(message);
        });
    }


    function show_license_btn_handler(){
        const license_list = $(this).parent().find(".license-list-group");
        license_list.toggleClass("d-none");
    }


    function edit_license_btn_handler(){
        const license_id = $(this).data("license-id");
        const license = find_license_by_id(license_id);
        const modal = new license_edit_modal.LicenseEditModal();
        modal.edit(license, function(date){
            const tzoffset = (new Date()).getTimezoneOffset() * 60000; //offset in milliseconds
            const localISOTime = (new Date(date - tzoffset)).toISOString().slice(0, -1);
            license.valid_date = localISOTime;
            edit_license(license);
            modal.hide();
        });
    }


    function download_license_btn_handler(){
        if(!confirm("해당 유저의 라이선스를 이용하여 다운로드 하시겠습니까?")){
            return;
        }

        const license_id = $(this).data("license-id");
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


    function find_license_by_id(license_id){
        for(const user of g_user_list){
            for(const license of user.licenses){
                if(license.id == license_id){
                    return license;
                }
            }
        }

        return null;
    }


    function edit_license(license){
        const json_date = JSON.stringify(license);
        const jqXHR = $.ajax({
            url: `/api/v1/license/update/${license.id}/`,
            type: "patch",
            data: json_date,
            contentType: "application/json",
        });

        jqXHR.then(function(data, textStatus, jqXHR){
            const license = data;
            const license_tag = create_license_tag(license);
            $(`li.license-item[data-license-id=${license.id}]`).replaceWith(license_tag);
        }).fail(function(jqXHR, textStatus, errorThrown){
            const message = jqXHR.responseJSON.detail;
            console.log(message);
            alert(message);
        });
    }

}(window.list = window.list || {}, jQuery));