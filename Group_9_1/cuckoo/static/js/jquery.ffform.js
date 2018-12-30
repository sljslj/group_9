/***************************************************************************************************************/

/* Plugin: jQuery Contact Form FFForm
/* Author: Muhammad Shahbaz Saleem
/* URL: http://www.egrappler.com/ffform-free-jquery-contact-form-plugin-with-validations-amazing-css3-animation
/* License: http://www.egrappler.com/license

/****************************************************************************************************************/
(function ($) {
    $.fn.extend({ ffform: function (options) {

        /**********************************************
        field definition:
        {
            id: 'id of form element', 
            required: true/false,
            requiredMsg:'message for required field',
            type: 'email/text/alpha/custom',
            validate: true/false,
            msg: 'invalid input message',
            regExp: regular express for custom field validation
        }

        /**********************************************/
        let settings = $.extend(
            {'fields': [],
            onSuccess: null,
            onFail: null,
            onValidate: null,
            submitButton: '',
            sendButton: '',
            loadingText: 'Logging in...',
            animation: 'flip',
            validationIndicator: '',
            successIndicator: '',
            errorIndicator: '' }, options);

        return this.each(function () {
            let form = $(this);
            let isValid = true;
            let isUserNameValid = true;
            let isEmailValid = true;
            let validationResult;
            let successIndicator;
            let errorIndicator;
            let validationIndicator;
            init();


            function init() {
                if (!form.is('form')) {
                    alert('No suitable element selected, formify can only be invoked with form element');
                    return; }
                if (settings.submitButton === '') {
                    alert('No submit button specified');
                    return; }
                let serverFields = $('<input type="hidden" name="hid_dynamic"/>');
                let strFields = '';

                $(settings.fields).each(function () {
                    if (strFields === '')
                        strFields = $('#' + this.id).attr('name');
                    else
                        strFields += ',' + $('#' + this.id).attr('name');
                });

                serverFields.val(strFields);
                form.prepend(serverFields);
                successIndicator = $(settings.successIndicator).css({ display: 'none' });
                errorIndicator = $(settings.errorIndicator).css({ display: 'none' });
                validationIndicator = $(settings.validationIndicator).css({ display: 'none' });

                if (settings.animation === 'flip') {
                    let flipper = $('<div class="flip-container"><div class="flipper"><div class="front"></div><div class="back"></div></div></div>');
                    form.after(flipper);
                    form.appendTo(flipper.find('.front'));
                    flipper.find('.back')
                        .append('<span id="msg-close">Close</span>')
                        .append(validationIndicator)
                        .append(successIndicator)
                        .append(errorIndicator);
                }
                else {
                    form.after($('<div class="form-front"></div><div class="form-back"></div>'));
                    form.appendTo($('.form-front'));
                    $('.form-back')
                        .append(validationIndicator)
                        .append(successIndicator)
                        .append(errorIndicator)
                        .append('<span id="msg-close">Close</span>');

                    let front = $('.form-front');
                    let back = $('.form-back');

                    front.css({ position: 'relative', top: '0px', left: '0px', zIndex: 1 });
                    back.css({ position: 'relative', top: '0px', left: '0px', zIndex: 0, display: 'none' });
                }
                //shake effect for invalid fields 
                $('#msg-close').bind('click', function () {
                    setTimeout(function () {
                        $('.invalid').effect('shake');
                    }, 300);
                });

                $(settings.sendButton).click(function (e) {
                    successIndicator.css({ display: 'none' });
                    errorIndicator.css({ display: 'none' });
                    validationIndicator.css({ display: 'none' });

                    e.preventDefault();
                    e.stopImmediatePropagation();
                    validationResult = '<ul id="validation-list">';
                    isEmailValid = true;

                    let the_email = $("#email");
                    let regExp = /^[\w\.\+-]{1,}\@([\da-zA-Z-]{1,}\.){1,}[\da-zA-Z-]{2,6}$/;
                    if(the_email.val() === '')
                    {
                        validationResult += '<li id="v-' + this.id + '">' + this.requiredMsg + '</li>';
                        isEmailValid = false;
                    }
                    else if(!regExp.test(the_email.val()))
                    {
                        validationResult += '<li id="v-' + this.id + '">' + this.msg + '</li>';
                        isEmailValid = false;
                    }

                    if(!isEmailValid)
                    {
                        validationResult += '</ul>';
                        if (settings.onValidate != null) {
                            settings.onValidate(validationResult);
                        }
                        if (settings.animation === 'flip') {
                            $('.flip-container').addClass('flip');
                            $('#msg-close').click(function () {
                                $('.flip-container').removeClass('flip');
                            });
                        }
                        else if (settings.animation === 'fade') {
                            $('.form-front').css({ zIndex: 0 }).fadeOut('slow');
                            $('.form-back').css({ zIndex: 1 }).fadeIn('slow');
                            $('#msg-close').click(function () {
                                $('.form-front').css({ zIndex: 1 }).fadeIn('slow');
                                $('.form-back').css({ zIndex: 0 }).fadeOut('slow');
                            });
                        }
                        if (validationIndicator != null)
                            validationIndicator.html(validationResult).css({ display: 'block' });
                        else {
                            alert(validationResult);
                        }
                        setTimeout(function () {
                            $('#validation-list li').each(function () {
                                let controlId = $(this).attr('id').replace('v-', '');
                                $('#' + controlId).addClass('invalid');
                                //$('#' + controlId).val($(this).html());
                            })
                        }, 500);
                        $('#validation-list li').bind('click', function () {
                            $('#msg-close').click();
                        });
                        return false;
                    }
                    else {
                        send_email();
                    }
                });

                $(settings.submitButton).click(function (e) {

                    successIndicator.css({ display: 'none' });
                    errorIndicator.css({ display: 'none' });
                    validationIndicator.css({ display: 'none' });

                    e.preventDefault();
                    e.stopImmediatePropagation();
                    validationResult = '<ul id="validation-list">';
                    isValid = true;
                    isEmailValid = true;
                    isUserNameValid = true;
                    validate();
                    if (!isValid || !isUserNameValid || !isEmailValid) {
                        validationResult += '</ul>';
                        if (settings.onValidate != null) {
                            settings.onValidate(validationResult);
                        }
                        if (settings.animation === 'flip') {
                            $('.flip-container').addClass('flip');
                            $('#msg-close').click(function () {
                                $('.flip-container').removeClass('flip');
                            });
                        }
                        else if (settings.animation === 'fade') {
                            $('.form-front').css({ zIndex: 0 }).fadeOut('slow');
                            $('.form-back').css({ zIndex: 1 }).fadeIn('slow');
                            $('#msg-close').click(function () {
                                $('.form-front').css({ zIndex: 1 }).fadeIn('slow');
                                $('.form-back').css({ zIndex: 0 }).fadeOut('slow');
                            });
                        }
                        if (validationIndicator != null)
                            validationIndicator.html(validationResult).css({ display: 'block' });
                        else {
                            alert(validationResult);
                        }
                        setTimeout(function () {
                            $('#validation-list li').each(function () {
                                let controlId = $(this).attr('id').replace('v-', '');
                                $('#' + controlId).addClass('invalid');
                                //$('#' + controlId).val($(this).html());
                            })
                        }, 500);
                        $('#validation-list li').bind('click', function () {
                            $('#msg-close').click();
                        });
                        return false;
                    }
                    else {
                        //add animate classe
                        let w = parseFloat($(this).outerWidth());
                        $(this).addClass('animate');
                        $(this).data('text', $(this).val());
                        $(this).val(settings.loadingText);
                        try_login();
                        return false;
                    }
                });
            }
            function send_email() {
                $.ajax({
                    type: 'GET',
                    url: 'deal-email/',
                    data:{
                        email: $("#email").val(),
                    },
                    success: function (result) {
                        alert(result.message)
                    },
                    error: function () {
                        if (settings.onError != null)
                            settings.onError(error);
                        if (settings.animation === 'flip') {
                            $('.flip-container').addClass('flip');
                            $('#msg-close').click(function () {
                                $('.flip-container').removeClass('flip');
                            });
                        }
                        else if (settings.animation === 'fade') {
                            $('.form-front').css({ zIndex: 0 }).fadeOut('slow');
                            $('.form-back').css({ zIndex: 1 }).fadeIn('slow');
                            $('#msg-close').click(function () {
                                $('.form-front').css({ zIndex: 1 }).fadeIn('slow');
                                $('.form-back').css({ zIndex: 0 }).fadeOut('slow');
                            });
                        }
                        if (errorIndicator != null)
                            errorIndicator.css({ display: 'block' });
                        else {
                            alert('Unable to send email at the moment. Please try again later!');
                        }
                        $(settings.submitButton).removeClass('animate').val($(settings.submitButton).data('text'));
                    }
                })
            }

            // 这里为用ajax向后台提交用户输入并进行验证
            function try_login() {
                $.ajax({
                    type: 'POST',
                    url:'deal-login/',
                    data: {
                    username: $("#username").val(),
                    password: $("#password").val(),
                    email: $("#email").val(),
                    idf: $("#idf_code").val(),
                    },
                    success: function (result) {
                        if (settings.onSuccess != null)
                            settings.onSuccess(result);
                        if (settings.animation === 'flip') {
                            $('.flip-container').addClass('flip');
                            $('#msg-close').click(function () {
                                $('.flip-container').removeClass('flip');
                            });
                        }
                        else if (settings.animation === 'fade') {
                            $('.form-front').css({ zIndex: 0 }).fadeOut('slow');
                            $('.form-back').css({ zIndex: 1 }).fadeIn('slow');
                            $('#msg-close').click(function () {
                                $('.form-front').css({ zIndex: 1 }).fadeIn('slow');
                                $('.form-back').css({ zIndex: 0 }).fadeOut('slow');
                            });
                        }
                        if (successIndicator != null) {
                            $('#success').text(result.message);
                            successIndicator.css({ display: 'block' });}
                        else
                            alert('Your message has been sent successfully');

                        setTimeout(function () {
                            if (result.s) {
                                var selfurl = String(document.location);
                                if (selfurl.indexOf('login/0')  || selfurl.indexOf('index') || selfurl.indexOf('forget/0')){
                                    console.log(document.location);
                                    window.location.href='../index';}

                                if (selfurl.indexOf('login/1')  || selfurl.indexOf('index-dark')  || selfurl.indexOf('forget/0')){
                                    console.log(document.location);
                                    window.location.href='../index-dark';}

                                console.log('tiaozhuan');
                                window.history.go(-1);

                                // window.history.go(0);
                                // window.location.replace(location.href);
                                }
                        }, 1500);

                        $(settings.submitButton).removeClass('animate').val($(settings.submitButton).data('text'));
                    },
                    error: function (xhr, status, error) {
                        if (settings.onError != null)
                            settings.onError(error);
                        if (settings.animation === 'flip') {
                            $('.flip-container').addClass('flip');
                            $('#msg-close').click(function () {
                                $('.flip-container').removeClass('flip');
                            });
                        }
                        else if (settings.animation === 'fade') {
                            $('.form-front').css({ zIndex: 0 }).fadeOut('slow');
                            $('.form-back').css({ zIndex: 1 }).fadeIn('slow');
                            $('#msg-close').click(function () {
                                $('.form-front').css({ zIndex: 1 }).fadeIn('slow');
                                $('.form-back').css({ zIndex: 0 }).fadeOut('slow');
                            });
                        }
                        if (errorIndicator != null)
                            errorIndicator.css({ display: 'block' });
                        else {
                            alert('Unable to send your message at the moment. Please try again later!');
                        }
                        $(settings.submitButton).removeClass('animate').val($(settings.submitButton).data('text'));
                    }
                });
                return false;
            }
            // 判断输入是否合法，若合法isVaild=True，否则False
            function validate() {
                $(settings.fields).each(function () {
                    let control = $('#' + this.id);
                    control.removeClass('invalid');
                    // 判读是否必需，若是则不输入时报错requiredMsg
                    if (this.required !== undefined && this.required) {
                        if (control.val() === '' || control.val() === control.attr('placeholder')) {
                            isValid = false;
                            // this.validate = false;
                            if (this.requiredMsg !== undefined)
                                validationResult += '<li id="v-' + this.id + '">' + this.requiredMsg + '</li>';
                        }
                    }
                    // 判断合法性,若不合法则报错msg
                    if (this.validate !== undefined && this.validate) {
                        isValid = validateField(this, control);
                        if (!isValid && this.msg !== undefined && control.val() !== '')
                            validationResult += '<li id="v-' + this.id + '">' + this.msg + '</li>';
                    }
                });
            }
            function validateField(field, control) {
                if (field.regExp !== undefined && field.regExp !== '') {
                    if (!field.regExp.test(control.val())) {
                        return false; } }
                else {
                    if (field.type !== undefined)
                        if (field.type === 'alpha') {
                            let regExp = /^[\w]{1,30}$/;
                            if (!regExp.test(control.val())) {
                                isUserNameValid = false;
                                return false; }
                        }
                        else if (field.type === 'email') {
                            return validateEmail(control.val()); }
                }
                return true;
            }
            function validateEmail(email) {
                let regExp = /^[\w\.\+-]{1,}\@([\da-zA-Z-]{1,}\.){1,}[\da-zA-Z-]{2,6}$/;
                if (!regExp.test(email)) {
                    isEmailValid = false;
                    return false; }
                return true;
            }
        });
    }
    });
})(jQuery);