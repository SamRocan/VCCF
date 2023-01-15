//<![CDATA[
    function subscription(company){
        $.ajax({
            type: "GET",
            url: '/jsonSubscription',
            data: {
                "company":company
            },
            dataType: "json",
            success: function (data) {
            },
            failure: function () {
            }
        });
    }
    //]]>