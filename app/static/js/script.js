 $(document).ready(function () {
     $('.parallax').parallax();
     $(".button-collapse").sideNav();

     $('.single-item').slick({
         dots: true,
         adaptiveHeight: true,
         //  variableWidth: true,
         autoplay: true,
         autoplaySpeed: 2000,
         centerMode: true,
         centerPadding: '0px',
         arrows:false
        //  slidesToShow: 2
     });
 });