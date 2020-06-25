(function($) {
  'use strict';

  /*======== 1. PREELOADER ========*/
	$(window).on('load', function () {
		$('#preloader').fadeOut(1000);
	});

  /*======== 2. NAVBAR ========*/

  $(window).on('load', function(){

    var header_area = $('.header');
    var main_area = header_area.find('.navbar');
    var zero = 0;
    var navbarSticky = $('.navbar-sticky');

    $(window).scroll(function(){
      var st = $(this).scrollTop();
      if (st > zero){
        navbarSticky.addClass('navbar-scrollUp');
      } else {
         navbarSticky.removeClass('navbar-scrollUp');
      }
      zero = st;

      if(main_area.hasClass('navbar-sticky') && ( $(this).scrollTop() <= 600 || $(this).width() <= 300)){
        main_area.removeClass('navbar-scrollUp');
        main_area.removeClass('navbar-sticky').appendTo(header_area);
        header_area.css('height', 'auto');
      }else if( !main_area.hasClass('navbar-sticky') && $(this).width() > 300 && $(this).scrollTop() > 600 ){
        header_area.css('height', header_area.height());
        main_area.addClass('navbar-scrollUp');
        main_area.css({'opacity': '0'}).addClass('navbar-sticky');
        main_area.appendTo($('body')).animate({'opacity': 1});
      }
    });

    $(window).trigger('resize');
    $(window).trigger('scroll');
  });

  /* ======== ALL DROPDOWN ON HOVER======== */
  if ($(window).width() > 991) {
    $('.navbar-expand-lg .navbar-nav .dropdown').hover(function () {
      $(this).addClass('').find('.dropdown-menu').addClass('show');
    }, function () {
      $(this).find('.dropdown-menu').removeClass('show');
    });
  }

  if ($(window).width() > 767) {
    $('.navbar-expand-md .navbar-nav .dropdown').hover(function () {
      $(this).addClass('').find('.dropdown-menu').addClass('show');
    }, function () {
      $(this).find('.dropdown-menu').removeClass('show');
    });
  }

  /*======== RS-SLIDER ========*/
  jQuery('#rev_slider_1').show().revolution({
    delay: 5000,
    sliderLayout: 'fullwidth',
    sliderType:'standard',
    responsiveLevels: [1171, 1025, 769, 480],
    gridwidth: [1171, 1025, 769, 480],
    gridheight: [560, 500, 450, 350],

    /* basic navigation arrows and bullets */
    navigation: {
      arrows: {
      enable: true,
      style: 'hesperiden',
      hide_onleave: false
      },

      bullets: {
      enable: false,
      style: 'hesperiden',
      hide_onleave: false,
      h_align: 'center',
      v_align: 'bottom',
      h_offset: 0,
      v_offset: 20,
      space: 5
      }
    },
    disableProgressBar:'on'
  });

  jQuery('#rev_slider_custom_2').show().revolution({
    delay: 5000,
    sliderLayout: 'fullwidth',
    sliderType:'standard',
    responsiveLevels: [1171, 1025, 769, 480],
    gridwidth:[1171, 1025, 769, 480],
    gridheight: [655, 605, 555, 450],
    navigation: {
      arrows: {
        enable: true,
        style: 'hesperiden',
        hide_onleave: false
      },
      bullets: {
        enable: false,
        style: 'hesperiden',
        hide_onleave: false,
        h_align: 'center',
        v_align: 'bottom',
        h_offset: 0,
        v_offset: 20,
        space: 15
      }
    },
    disableProgressBar:'on'
  });

  jQuery('#rev_slider_custom_3').show().revolution({
    delay: 5000,
    sliderLayout: 'fullscreen',
    sliderType:'standard',
    responsiveLevels: [1171, 1025, 769, 480],
    gridwidth:[1171, 1025, 769, 480],
    gridheight: [655, 605, 555, 450],
    navigation: {
      arrows: {
        enable: true,
        style: 'hesperiden',
        hide_onleave: false
      },
      bullets: {
        enable: false,
        style: 'hesperiden',
        hide_onleave: false,
        h_align: 'center',
        v_align: 'bottom',
        h_offset: 0,
        v_offset: 20,
        space: 15
      }
    },
    disableProgressBar:'on'
  });

  jQuery('#rev_slider_custom_4').show().revolution({
    delay: 5000,
    sliderLayout: 'fullwidth',
    sliderType:'standard',
    responsiveLevels: [1171, 1025, 769, 480],
    gridwidth:[1171, 1025, 769, 480],
    gridheight: [655, 605, 555, 450],
    navigation: {
      arrows: {
        enable: true,
        style: 'hesperiden',
        hide_onleave: false
      },
      bullets: {
        enable: false,
        style: 'hesperiden',
        hide_onleave: false,
        h_align: 'center',
        v_align: 'bottom',
        h_offset: 0,
        v_offset: 20,
        space: 15
      }
    },
    disableProgressBar:'on'
  });

  //============================== Topbar Cart Icon =========================

  $('.cart-dropdown a').on('click', function() {
    $('.cart-dropdown a .icon-small').toggleClass('d-none');
  });

  $('body').on("click", function () {
    var cartDropdown = $('.cart-dropdown');
    if(cartDropdown.hasClass('show')){
      $('.shopping-icon').removeClass('d-none');
      $('.close-icon').addClass('d-none');      
    }
  });
  
  //============================== BRAND SLIDER =========================
  $('#brands').owlCarousel({
    loop:true,
    margin:30,
    autoplay: true,
    autoplayTimeout: 3000,
    nav:false,
    dots: false,
    responsiveClass: true,
    responsive:{
      0:{
        items:1
      },
      768:{
        items:3
      },
      992:{
        items:5
      }
    }
  });
  //============================== testimonial =========================
  $('#testimonial').owlCarousel({
    loop:true,
    margin:30,
    dots: false,
    nav:true,
    navText : ['<i class="fa fa-arrow-left"></i>','<i class="fa fa fa-arrow-right"></i>'],
    items:1
  });
  //============================== categories =========================
  $('.categories-slider').owlCarousel({
    margin: 20,
    loop: true,
    autoplay: false,
    nav: true,
    navText : ['<i class="fa fa-arrow-left"></i>','<i class="fa fa fa-arrow-right"></i>'],
    dots: false,
    autoplayTimeout: 1000,
    items: 1,
    center: true
  });
//============================== TEAM SLIDER =========================
  $('.team-slider').owlCarousel({
    loop:true,
    margin:30,
    dots: false,
    nav:true,
    navText : ['<i class="fa fa-arrow-left"></i>','<i class="fa fa fa-arrow-right"></i>'],
    responsive:{
      0:{
        items:1
      },
      600:{
        items:3
      },
      1000:{
        items:4
      }
    }
  });

  /*======== 9. BACK TO TOP ========*/
  $(document).ready(function () {
    $(window).scroll(function () {
      if ($(this).scrollTop() > 100) {
        $('#back-to-top').css('opacity', 1);
      } else {
        $('#back-to-top').css('opacity', 0);
      }
    });
  });

  //============================== ISOTOPE =========================
    // init Isotope
    var $grid = $('.grid').imagesLoaded(function () {
      // init Isotope after all images have loaded
      $grid.isotope({
        itemSelector: '.element-item',
        layoutMode: 'fitRows'
      });
    });

    // filter functions
    var filterFns = {
      // show if number is greater than 50
      numberGreaterThan50: function() {
        var number = $(this).find('.number').text();
        return parseInt( number, 10 ) > 50;
      },
      // show if name ends with -ium
      ium: function() {
        var name = $(this).find('.name').text();
        return name.match( /ium$/ );
      }
    };

    // bind filter button click
    $('#filters').on( 'click', 'button', function() {
      var filterValue = $( this ).attr('data-filter');
      // use filterFn if matches value
      filterValue = filterFns[ filterValue ] || filterValue;
      $grid.isotope({ filter: filterValue });
    });

    // bind sort button click
    $('#sorts').on( 'click', 'button', function() {
      var sortByValue = $(this).attr('data-sort-by');
      $grid.isotope({ sortBy: sortByValue });
    });

    // change is-checked class on buttons
    $('.button-group').each( function( i, buttonGroup ) {
      var $buttonGroup = $( buttonGroup );
      $buttonGroup.on( 'click', 'button', function() {
        $buttonGroup.find('.is-checked').removeClass('is-checked');
        $( this ).addClass('is-checked');
      });
    });


  //============================== VIDEOBOX =========================
  var videoBox = $('.video-box i');
  videoBox.on('click', function(){
    var video = '<iframe class="embed-responsive-item"  allowfullscreen src="'+ $(this).attr('data-video') +'"></iframe>';
    $(this).replaceWith(video);
  });

  //============================== SELECT 2 =========================
  $('.select2-select').select2({
    minimumResultsForSearch: -1
  });

  //============================== VIDEO BOX =========================
  $('.box-video').click(function(){
    $('iframe',this)[0].src += '&amp;autoplay=1';
    $(this).addClass('open');
  });

  //============================== COUNDOWN =========================
  $('#courseTimer').syotimer({
    year: 2019,
    month: 11,
    day: 9,
    hour: 20,
    minute: 30
  });



  /*======== 18. COUNTER-UP ========*/
  var counter = $('#counter');
  if (counter.length) {
    var a = 0;
    $(window).scroll(function() {
      var oTop = counter.offset().top - window.innerHeight;
      if (a === 0 && $(window).scrollTop() > oTop) {
        $('.counter-value').each(function() {
          var $this = $(this),
            countTo = $this.attr('data-count');
          $({
            countNum: $this.text()
          }).animate({
              countNum: countTo
            },
            {
              duration: 5000,
              easing: 'swing',
              step: function() {
                $this.text(Math.floor(this.countNum));
              },
              complete: function() {
                $this.text(this.countNum);
                //alert('finished');
              }

            });
        });
        a = 1;
      }
    });
  }

// scrollup
  $(window).scroll(function(){
  if ($(this).scrollTop() > 100) {
    $('.scrollup').fadeIn();
  } else {
    $('.scrollup').fadeOut();
  }
});

$('.scrollup').click(function(){
  $('html, body').animate({ scrollTop: 0 }, 500);
  return false;
});


  // element-right-sidebar
  $(window).scroll(function () {
    if ($(this).scrollTop() > 400) {
      $('.element-right-sidebar').addClass('sidebar-fixed');
    } else {
      $('.element-right-sidebar').removeClass('sidebar-fixed');
    }

    if ($(window).scrollTop() + $(window).height() > $(document).height() - 590) {
      $('.element-right-sidebar').addClass('right-sidebar-absolute').removeClass('sidebar-fixed');
    } else {
      $('.element-right-sidebar').removeClass('right-sidebar-absolute');
    }
  });

  /*======== 12. MAP ========*/
  function initialize() {
    var myLatLng = { lat: 53.385873, lng: -1.471471 };

    //Custom Style
    var styles = [
      {
        featureType: 'landscape',
        stylers: [
          { color: '#eeddee' }
        ]
      }, {
        featureType: 'natural',
        stylers: [
          { hue: '#ff0000' }
        ]
      }, {
        featureType: 'road',
        stylers: [
          { hue: '#5500aa' },
          { saturation: -70 }
        ]
      }, {
        featureType: 'building',
        elementType: 'labels',
        stylers: [
          { hue: '#000066' }
        ]
      }, {
        featureType: 'poi', //points of interest
        stylers: [
          { hue: '#0044ff' }
        ]
      }
    ];
    var mapOptions = {
      zoom: 14,
      scrollwheel: false,
      center: new google.maps.LatLng(53.385873, -1.471471),
      styles: styles

    };
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    var image = 'assets/img/marker.png';
    var marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      icon: image
    });
  }
  var mapId = $('#map');
  if (mapId.length) {
    google.maps.event.addDomListener(window, 'load', initialize);
  }

  //============================== ANIMATION =========================
  var $animation_elements = $('.animated');
  var $window = $(window);

  function check_if_in_view() {
    var window_height = $window.height();
    var window_top_position = $window.scrollTop();
    var window_bottom_position = (window_top_position + window_height);

    $.each($animation_elements, function() {
      var $element = $(this);
      var element_height = $element.outerHeight();
      var element_top_position = $element.offset().top;
      var element_bottom_position = (element_top_position + element_height);
      var animationType = $(this).attr('data-animation');

      //check to see if this current container is within viewport
      if ((element_bottom_position >= window_top_position) && (element_top_position <= window_bottom_position)) {
        $element.addClass(animationType);
      } else {
        $element.removeClass(animationType);
      }
    });
  }

  $window.on('scroll resize', check_if_in_view);
  $window.trigger('scroll');

  /*======== COUNT INPUT (Quantity) ========*/
  $('.incr-btn').on('click', function(e) {
    var newVal;
    var $button = $(this);
    var oldValue = $button.parent().find('.quantity').val();
    $button.parent().find('.incr-btn[data-action="decrease"]').removeClass('inactive');
    if ($button.data('action') === 'increase') {
        newVal = parseFloat(oldValue) + 1;
    } else {
     // Don't allow decrementing below 1
      if (oldValue > 1) {
          newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 1;
        $button.addClass('inactive');
      }
    }
    $button.parent().find('.quantity').val(newVal);
    e.preventDefault();
  });

  /*======== 11.PRICE SLIDER RANGER  ========*/
  $('[data-toggle="tooltip"]').tooltip();

  /*======== 10. SMOOTH SCROLLING TO SECTION ========*/
  $('.scrolling  a[href*="#"]').on('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    var target = $(this).attr('href');

    function customVeocity(set_offset){
      $(target).velocity('scroll', {
        duration: 800,
        offset: set_offset,
        easing: 'easeOutExpo',
        mobileHA: false
      });
    }

    if ($('#body').hasClass('up-scroll') || $('#body').hasClass('static')) {
      customVeocity(2);
    } else {
      customVeocity(-90);
    }

  });

  /*======== 11.PRICE SLIDER RANGER  ========*/
  var nonLinearStepSlider = document.getElementById('slider-non-linear-step');
  if(nonLinearStepSlider){
    noUiSlider.create(nonLinearStepSlider, {
      connect: true,
      start: [125, 750],
      range: {
          'min': [0],
          'max': [1000]
      }
    });
  }

  var sliderValue = [
    document.getElementById('lower-value'), // 0
    document.getElementById('upper-value')  // 1
  ];

  // Display the slider value and how far the handle moved
  // from the left edge of the slider.
  var priceRange = document.getElementById('price-range');
  if (priceRange) {
    nonLinearStepSlider.noUiSlider.on('update', function(values, handle) {
      sliderValue[handle].innerHTML = '$' + Math.floor(values[handle]);
    });
  }

  /*======== 11.Wow Js  ========*/
  new WOW().init();

  /*======== Google Analytics  ========*/

})(jQuery);
