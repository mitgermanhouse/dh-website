// Allow for stacking of modal dialogs
$(document).ready(function() {
    let modal = $('.modal');
    let body = $('body');

    modal.on('hidden.bs.modal', function (event) {
        $(this).removeClass('fv-modal-stack');
        body.data('fv_open_modals', body.data('fv_open_modals') - 1);
    });

    modal.on('show.bs.modal', function (event) {
        // keep track of the number of open modals
        if (typeof (body.data('fv_open_modals')) == 'undefined') {
            $('body').data('fv_open_modals', 0);
        }

        // if the z-index of this modal has been set, ignore.
        if ($(this).hasClass('fv-modal-stack')) {
            return;
        }

        let open_modals = body.data('fv_open_modals') + 1
        body.data('fv_open_modals', open_modals);

        $(this).addClass('fv-modal-stack');
        $(this).css('z-index', 1040 + (10 * open_modals));

        setTimeout(function () {
            let backdrop = $('.modal-backdrop').not('.fv-modal-stack')
            backdrop.css('z-index', 1039 + (10 * open_modals))
            backdrop.addClass('fv-modal-stack')
        }, 50)
    })
});