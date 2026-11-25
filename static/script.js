// (function($) {

//     "use strict";
    
//       // background color when scroll 
//     var initScrollNav = function () {
//     var scroll = $(window).scrollTop();
    
//     if (scroll >= 200) {
//       $('.navbar.second-header').addClass("bg-dark");
//       $('.navbar.second-header').addClass("hidden");
//       $('.header-top.first-header').addClass("hidden");
//     } else {
//       $('.navbar.second-header').removeClass("bg-dark");
//       $('.navbar.second-header').removeClass("hidden");
//       $('.header-top.first-header').removeClass("hidden");
//     }
//     }
    
//     $(window).scroll(function () {
//     initScrollNav();
//     });
    
//     $(document).ready(function() {
    
//       /* Video */
//       var $videoSrc;  
//         $('.play-btn').click(function() {
//           $videoSrc = $(this).data( "src" );
//         });
    
//         $('#myModal').on('shown.bs.modal', function (e) {
    
//         $("#video").attr('src',$videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0" ); 
//       })
    
//       $('#myModal').on('hide.bs.modal', function (e) {
//         $("#video").attr('src',$videoSrc); 
//       })
        
//       var swiper = new Swiper(".slider", {
//         effect: "fade",
//         loop: true,
//         autoplay: {
//           delay: 4000,
//           disableOnInteraction: false,
//         },
//         navigation: {
//           nextEl: ".main-slider-button-next",
//           prevEl: ".main-slider-button-prev",
//         },
//       });
    
//       var swiper = new Swiper(".testimonial-swiper", {
//         slidesPerView: 3,
//         spaceBetween: 20,
//         pagination: {
//           el: ".swiper-pagination",
//           clickable: true,
//         },
//         breakpoints: {
//           0: {
//             slidesPerView: 1,
//           },
//           640: {
//             slidesPerView: 2,
//           },
//           1024: {
//             slidesPerView: 3,
//           },
//         },
//       });
    
//     }); // End of a document
    
//     })(jQuery);
    
  


//     //jQuery time
// var current_fs, next_fs, previous_fs; //fieldsets
// var left, opacity, scale; //fieldset properties which we will animate
// var animating; //flag to prevent quick multi-click glitches

// $(".next").click(function(){
//   if(animating) return false;
//   animating = true;
  
//   current_fs = $(this).parent();
//   next_fs = $(this).parent().next();
  
//   //activate next step on progressbar using the index of next_fs
//   $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
  
//   //show the next fieldset
//   next_fs.show(); 
//   //hide the current fieldset with style
//   current_fs.animate({opacity: 0}, {
//     step: function(now, mx) {
//       //as the opacity of current_fs reduces to 0 - stored in "now"
//       //1. scale current_fs down to 80%
//       scale = 1 - (1 - now) * 0.2;
//       //2. bring next_fs from the right(50%)
//       left = (now * 50)+"%";
//       //3. increase opacity of next_fs to 1 as it moves in
//       opacity = 1 - now;
//       current_fs.css({'transform': 'scale('+scale+')'});
//       next_fs.css({'left': left, 'opacity': opacity});
//     }, 
//     duration: 500, 
//     complete: function(){
//       current_fs.hide();
//       animating = false;
//     }, 
//     //this comes from the custom easing plugin
//     easing: 'easeOutQuint'
//   });
// });

// $(".previous").click(function(){
//   if(animating) return false;
//   animating = true;
  
//   current_fs = $(this).parent();
//   previous_fs = $(this).parent().prev();
  
//   //de-activate current step on progressbar
//   $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
  
//   //show the previous fieldset
//   previous_fs.show(); 
//   //hide the current fieldset with style
//   current_fs.animate({opacity: 0}, {
//     step: function(now, mx) {
//       //as the opacity of current_fs reduces to 0 - stored in "now"
//       //1. scale previous_fs from 80% to 100%
//       scale = 0.8 + (1 - now) * 0.2;
//       //2. take current_fs to the right(50%) - from 0%
//       left = ((1-now) * 50)+"%";
//       //3. increase opacity of previous_fs to 1 as it moves in
//       opacity = 1 - now;
//       current_fs.css({'left': left});
//       previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
//     }, 
//     duration: 500, 
//     complete: function(){
//       current_fs.hide();
//       animating = false;
//     }, 
//     //this comes from the custom easing plugin
//     easing: 'easeOutQuint'
//   });
// });

// $(".submit").click(function(){
//   return false;
// });