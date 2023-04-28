// Script modify from https://mdbootstrap.com/snippets/jquery/tomekmakowski/631899#css-tab-view
$(function () {
    var $password = $(".check-password[type='password']");
    var $passwordView = $(".toggle-password");
    var $passwordConfirm = $(".check-password-confirm[type='password']");
    var $passwordConfirmView = $(".toggle-password-confirm");
    var passwordVal = "";
    var passwordConfirmVal = "";
    var $submit = $(".check-password-submit[type='submit']");
    var $requirements = $(".requirements");
    var leng, bigLetter, num, specialChar;
    var $leng = $(".leng");
    var $bigLetter = $(".big-letter");
    var $num = $(".num");
    var $specialChar = $(".special-char");
    var specialChars = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~";
    var numbers = "0123456789";

    $requirements.addClass("wrong");

    $password.on("input blur", function (e) {
        var el = $(this);
        var val = el.val();
        $password.addClass("is-invalid");

        if (val != passwordConfirmVal)
            $passwordConfirm.addClass("is-invalid");
        $submit.addClass("disabled");

        if (val.length < 8) {
            leng = false;
        } else if (val.length > 7) {
            leng = true;
        }


        if (val.toLowerCase() == val) {
            bigLetter = false;
        } else {
            bigLetter = true;
        }

        num = false;
        for (var i = 0; i < val.length; i++) {
            for (var j = 0; j < numbers.length; j++) {
                if (val[i] == numbers[j]) {
                    num = true;
                }
            }
        }

        specialChar = false;
        for (var i = 0; i < val.length; i++) {
            for (var j = 0; j < specialChars.length; j++) {
                if (val[i] == specialChars[j]) {
                    specialChar = true;
                }
            }
        }

        //console.log('leng : ', leng, 'big : ', bigLetter, 'num : ', num, 'special : ', specialChar);

        if (leng == true && bigLetter == true && num == true && specialChar == true) {
            $(this).addClass("is-valid").removeClass("is-invalid");
            $requirements.removeClass("wrong").addClass("good");
            passwordVal = val;

            if (val == passwordConfirmVal) {
                $passwordConfirm.addClass("is-valid").removeClass("is-invalid");
                $submit.removeClass("disabled");
            }
        } else {
            $(this).addClass("is-invalid").removeClass("is-valid");

            if (leng == false) {
                $leng.addClass("wrong").removeClass("good");
            } else {
                $leng.addClass("good").removeClass("wrong");
            }

            if (bigLetter == false) {
                $bigLetter.addClass("wrong").removeClass("good");
            } else {
                $bigLetter.addClass("good").removeClass("wrong");
            }

            if (num == false) {
                $num.addClass("wrong").removeClass("good");
            } else {
                $num.addClass("good").removeClass("wrong");
            }

            if (specialChar == false) {
                $specialChar.addClass("wrong").removeClass("good");
            } else {
                $specialChar.addClass("good").removeClass("wrong");
            }
        }
    });

    $passwordConfirm.on("input blur", function (e) {
        if (passwordVal == "") {
            return;
        }
        var el = $(this);
        passwordConfirmVal = el.val();

        if (passwordConfirmVal != passwordVal) {
            el.addClass("is-invalid").removeClass("is-valid");
            $submit.addClass("disabled");
        }
        else if (passwordConfirmVal != "") {
            el.addClass("is-valid").removeClass("is-invalid");
            if ((leng == true && bigLetter == true && num == true && specialChar == true)) {
                $submit.removeClass("disabled");
            }
        }
    });

    $submit.on("click", function (e) {
        passwordVal = "";
        passwordConfirmVal = ""
    })

    $passwordView.on("click", function (e) {
        $(this).toggleClass("bi-eye-slash bi-eye");
        var type = $(this).hasClass("bi-eye") ? "text" : "password";
        $password.attr("type", type);
    })

    $passwordConfirmView.on("click", function (e) {
        $(this).toggleClass("bi-eye-slash bi-eye");
        var type = $(this).hasClass("bi-eye") ? "text" : "password";
        $passwordConfirm.attr("type", type);
    })
});
