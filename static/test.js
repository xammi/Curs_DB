    $(document).ready(function() {
        var url = $("#url"),
            method = $("#method"),
            json = $("#json");

        $("#sender").click(function() {
            $.ajax({
                type: method.val(),
                contentType: "application/json; charset=utf-8",
                url: url.val(),
                data: json.val(),

                beforeSend: function () {
                    $("#response").html("");
                },
                success: function (response) {
                    $("#response").html(JSON.stringify(response));
                },
                error: function () {
                    $("#response").html("error");
                },

                dataType: "json",
            });
        });
    });