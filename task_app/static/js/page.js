$(document).ready(function () {

  $('#deadline').persianDatepicker({
            format: 'YYYY/MM/DD',
            initialValue: false,
            autoClose: true,
            minDate: new persianDate()  // ⬅️ تنظیم حداقل تاریخ: امروز

        });
});