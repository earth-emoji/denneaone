$( document ).ready(function() {
    var slug = $("span[id^=slug_]").attr('id').split('_')[1];
    const MEDIA_URL = "/media/";

    $('#product-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")
        var url = "/products/"+ slug +"/update/";
        $.ajax({ data: $(this).serialize(), 
            type: $(this).attr('method'), 
            url: $(this).attr('action'), 
            success: function(response) {
                 console.log(response);
                 if(response['success']) {
                    $("#results").html("<div class='alert alert-success'>\
                                Succesfully updated job details. View 'Preview' tab for changes.</div>");
                    $("#product_name").html(response.name);
                    $("#description").html(response.description);
                    $("#price").html(response.price);
                    $("#stock").html(response.stock);
                    
                 } 
                 if(response['error']) {
                     $("#nameerr").html(response['error']['name']);
                     $("#descerr").html(response['error']['description']);
                     $("#priceerr").html(response['error']['price']);
                     $("#sqerr").html(response['error']['stock_quantity']);
                 } 
            },
            error: function (request, status, error) {
                 console.log(request.responseText);
            }
        });
    });

    $('#album-create').on('submit', function(event) {
        event.preventDefault();
        var url = "/products/"+ slug +"/album-create/";
        // Get form
        var form = $('#album-form')[0];
        var data = new FormData(form);
        $.ajax({ 
            data: data, 
            type: $(this).attr('method'), 
            url: $(this).attr('action'),
            enctype: 'multipart/form-data',
            processData: false,  // Important!
            contentType: false,
            cache: false,
            timeout: 600000,
            success: function(response) {
                console.log(response);
                $('#albumModal').modal('hide');
                if(response['success']) {
                   $("#results").html("<div class='alert alert-success'>\
                               Succesfully created album.</div>");
                   $("#album_name").html(response.name);
                   // $("#cover").attr('src', MEDIA_URL + response.cover);
                   $("#images").prepend("<img class='img-thumbnail' src='" + MEDIA_URL + response.cover + "' />");
                   
                } 
                if(response['error']) {
                    $("#defaulterr").html(response['error']['default']);
                } 
           },
           error: function (request, status, error) {
                console.log(request.responseText);
            }
        });
    });

})
