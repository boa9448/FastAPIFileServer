(function(license_edit_modal, $, undefined){
    $(document).ready(init);


    function init(){
        LicenseEditModal.add_modal_tag();
    }


    class LicenseEditModal{
        static is_handler_init = false;

        constructor(){
            this.user = null;
            this.edit_callback = null;

            this.init_handler();
        }

        init_handler(){
            if(LicenseEditModal.is_handler_init){
                return;
            }

            $("#license-edit-modal").on("click", ".add-day-btn", this.add_day_btn_click_handler.bind(this));
            $("#license-edit-modal").on("click", "#license-edit-modal-save-btn", this.save_btn_click_handler.bind(this));

            LicenseEditModal.is_handler_init = true;
        }

        remove_handler(){
            $("#license-edit-modal").off("click", ".add-day-btn", this.add_day_btn_click_handler.bind(this));
            $("#license-edit-modal").off("click", "#license-edit-modal-save-btn", this.save_btn_click_handler.bind(this));
        }

        add_day_btn_click_handler(e){
            //const add_day = $(this).data("day");
            const add_day = $(e.target).data("day");

            const day = parseInt($("#day-select").val());
            const month = parseInt($("#month-select").val());
            const year = parseInt($("#year-select").val());
            const date = new Date(year, month, day);
            const new_date = new Date(date);

            new_date.setDate(date.getDate() + add_day);
            this.set_date_select(new_date);
        }

        save_btn_click_handler(e){
            if(this.edit_callback){
                const year = parseInt($("#year-select").val());
                const month = parseInt($("#month-select").val()) - 1;
                const day = parseInt($("#day-select").val());
                const date = new Date(year, month, day);

                this.edit_callback(date);
            }
        }

        static add_modal_tag(){
            const modal_tag = `
            <div class="modal fade" id="license-edit-modal" tabindex="-1" aria-labelledby="license-edit-modal-label" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="license-edit-modal-label">
                                파일 이름 - 라이선스 이름
                            </h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="d-flex flex-row mb-3">
                                <select class="form-select me-2" aria-label="year select" id="year-select">
                                </select>
                                <select class="form-select me-2" aria-label="month select" id="month-select">
                                </select>
                                <select class="form-select me-2" aria-label="day select" id="day-select">
                                </select>
                            </div>
                            <div class="d-flex flex-row justify-content-end">
                                <!-- 날짜 추가 버튼 1, 7, 15, 30일-->
                                <button type="button" class="btn btn-primary me-2 add-day-btn" data-day="1">+1일</button>
                                <button type="button" class="btn btn-primary me-2 add-day-btn" data-day="7">+7일</button>
                                <button type="button" class="btn btn-primary me-2 add-day-btn" data-day="15">+15일</button>
                                <button type="button" class="btn btn-primary me-2 add-day-btn" data-day="30">+30일</button>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" id="license-edit-modal-save-btn">
                                적용
                            </button>
                        </div>
                    </div>
                </div>
            </div>`;

            $("body").append(modal_tag);
        }

        show(){
            $("#license-edit-modal").modal("show");
        }


        hide(){
            $("#license-edit-modal").modal("hide");
        }


        edit(license, edit_callback){
            this.license = license;
            this.edit_callback = edit_callback;

            this.set_modal_data();
            this.show();
        }

        set_modal_data(){
            this.set_modal_title();
            this.set_modal_body();
        }

        set_modal_title(){
            const license = this.license;
            const file_name = license.file.name;
            const license_name = license.name;

            const title = `${file_name} - ${license_name}`;
            $("#license-edit-modal-label").text(title);
        }

        set_modal_body(){
            const valid_date = new Date(this.license.valid_date);
            const full_year = valid_date.getFullYear();
            const month = valid_date.getMonth() + 1;
            const day = valid_date.getDate();
            const new_valid_date = new Date(full_year, month, day);

            this.set_date_select_option(new_valid_date);
            this.set_date_select(new_valid_date);
        }

        set_date_select(valid_date){
            const year = valid_date.getFullYear();
            const month = valid_date.getMonth();
            const day = valid_date.getDate();

            $("#year-select").val(year);
            $("#month-select").val(month);
            $("#day-select").val(day);
        }

        set_date_select_option(base_date){
            // 기준 날짜로부터 1년 전부터 1년 후까지의 날짜를 select option으로 추가
            const year = base_date.getFullYear();

            const year_select = $("#year-select");
            const month_select = $("#month-select");
            const day_select = $("#day-select");

            year_select.empty();
            month_select.empty();
            day_select.empty();

            for(let i = year - 1; i <= year + 1; i++){
                year_select.append(`<option value="${i}">${i}</option>`);
            }

            for(let i = 1; i <= 12; i++){
                month_select.append(`<option value="${i}">${i}</option>`);
            }

            for(let i = 1; i <= 31; i++){
                day_select.append(`<option value="${i}">${i}</option>`);
            }
        }

    }
    license_edit_modal.LicenseEditModal = LicenseEditModal;

}(window.license_edit_modal = window.license_edit_modal || {}, jQuery));