function menuToggle() {
    const toggleMenu = document.querySelector('.menu');
    toggleMenu.classList.toggle('active')
}

setTimeout(() => {
    $(".alert").alert("close")
}, 3000);


$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method:$(this).attr("method"),

        url:$(this).attr("action"),

        dataType:"json",

        success:function(res){
            console.log("comment saved to DB");

            if(res.bool== true){
                $('#review-res').html("Review added successfully")
                $(".hide-comment-form").hide()
                $(".hide-review-form").hide()
            }
            
        }



    })
})